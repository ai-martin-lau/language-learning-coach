#!/usr/bin/env python3
"""Generate validated, free-first TTS audio on macOS and Windows."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import venv

import validate_audio


EXIT_INTERNAL = 1
EXIT_SETUP = 2
EXIT_INPUT = 3
EXIT_SYNTHESIS = 4

ONLINE_PACKAGES = ("edge-tts==7.2.8", "imageio-ffmpeg==0.6.0")
MACOS_VOICE_RE = re.compile(
    r"^(?P<name>.+?)\s+(?P<locale>[a-z]{2,3}[_-][A-Z]{2})\s+#"
)
WINDOWS_VOICE_SCRIPT = r"""
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Speech
$synth = [System.Speech.Synthesis.SpeechSynthesizer]::new()
try {
  $voices = @($synth.GetInstalledVoices() | ForEach-Object {
    [PSCustomObject]@{
      name = $_.VoiceInfo.Name
      locale = $_.VoiceInfo.Culture.Name
    }
  })
  ConvertTo-Json -InputObject $voices -Compress
} finally {
  $synth.Dispose()
}
""".strip()
WINDOWS_SYNTHESIS_SCRIPT = r"""
Add-Type -AssemblyName System.Speech
$synth = [System.Speech.Synthesis.SpeechSynthesizer]::new()
try {
  $synth.SelectVoice($env:LLC_TTS_VOICE)
  $synth.Rate = [int]$env:LLC_TTS_RATE
  $format = [System.Speech.AudioFormat.SpeechAudioFormatInfo]::new(
    44100,
    [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen,
    [System.Speech.AudioFormat.AudioChannel]::Mono
  )
  $synth.SetOutputToWaveFile($env:LLC_TTS_OUTPUT, $format)
  $synth.Speak($env:LLC_TTS_TEXT)
  $synth.SetOutputToNull()
} finally {
  $synth.Dispose()
}
""".strip()
WINDOWS_INSTALL_VOICE_SCRIPT = r"""
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$name = "Language.TextToSpeech~~~$($env:LLC_TTS_LOCALE)~0.0.1.0"
$capability = Get-WindowsCapability -Online -Name $name
if ($null -eq $capability) {
  throw "Windows has no Text-to-Speech capability named $name"
}
if ($capability.State -ne "Installed") {
  Add-WindowsCapability -Online -Name $name -ErrorAction Stop | Out-Null
}
Write-Output $name
""".strip()


class SetupError(Exception):
    """The requested free TTS environment is unavailable or incomplete."""


class InputError(Exception):
    """A CLI argument or output target is invalid."""


class SynthesisError(Exception):
    """A synthesis or conversion command failed."""


@dataclass(frozen=True)
class Voice:
    name: str
    locale: str
    engine: str


def normalize_locale(value: str) -> str:
    value = value.strip().replace("_", "-")
    parts = value.split("-")
    if len(parts) == 1:
        return parts[0].lower()
    return "-".join((parts[0].lower(), parts[1].upper(), *parts[2:]))


def locale_matches(locale: str, requested: str) -> bool:
    locale = normalize_locale(locale)
    requested = normalize_locale(requested)
    if "-" in requested:
        return locale == requested
    return locale.split("-", 1)[0] == requested


def parse_macos_voices(output: str) -> list[Voice]:
    voices: list[Voice] = []
    for line in output.splitlines():
        match = MACOS_VOICE_RE.match(line.rstrip())
        if match:
            voices.append(
                Voice(
                    match.group("name").strip(),
                    normalize_locale(match.group("locale")),
                    "macos",
                )
            )
    return voices


def parse_windows_voices(output: str) -> list[Voice]:
    if not output.strip():
        return []
    try:
        payload = json.loads(output)
    except json.JSONDecodeError as exc:
        raise SetupError(f"cannot parse Windows voice list: {exc}") from exc
    if isinstance(payload, dict):
        payload = [payload]
    if not isinstance(payload, list):
        raise SetupError("Windows voice list is not a JSON object or array")
    voices: list[Voice] = []
    for item in payload:
        if not isinstance(item, dict) or not item.get("name") or not item.get("locale"):
            raise SetupError("Windows voice list contains an incomplete entry")
        voices.append(
            Voice(str(item["name"]), normalize_locale(str(item["locale"])), "windows")
        )
    return voices


def macos_rate(rate_percent: int) -> int:
    return max(80, min(400, round(175 * rate_percent / 100)))


def windows_rate(rate_percent: int) -> int:
    return max(-10, min(10, round((rate_percent - 100) / 10)))


def edge_rate(rate_percent: int) -> str:
    delta = max(-100, min(100, rate_percent - 100))
    return f"{delta:+d}%"


def run_checked(
    command: list[str], *, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
    except OSError as exc:
        raise SetupError(f"cannot run {command[0]}: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "unknown command failure").strip()
        raise SynthesisError(f"{command[0]} failed: {detail}")
    return result


def powershell_path() -> str | None:
    return (
        shutil.which("powershell.exe")
        or shutil.which("powershell")
        or shutil.which("pwsh")
    )


def system_voices(
    language: str | None = None, *, system: str | None = None
) -> tuple[dict[str, str] | None, list[Voice]]:
    system = system or platform.system()
    if system == "Darwin":
        say_path = shutil.which("say")
        afconvert_path = shutil.which("afconvert")
        if not say_path or not afconvert_path:
            return None, []
        result = run_checked([say_path, "-v", "?"])
        voices = parse_macos_voices(result.stdout)
        return {"kind": "macos", "say": say_path, "afconvert": afconvert_path}, voices
    if system == "Windows":
        shell = powershell_path()
        if not shell:
            return None, []
        result = run_checked(
            [shell, "-NoProfile", "-NonInteractive", "-Command", WINDOWS_VOICE_SCRIPT]
        )
        return {"kind": "windows", "powershell": shell}, parse_windows_voices(result.stdout)
    return None, []


def runtime_python(runtime_dir: Path) -> Path:
    candidates = (
        runtime_dir / "Scripts" / "python.exe",
        runtime_dir / "bin" / "python3",
        runtime_dir / "bin" / "python",
    )
    return next((candidate for candidate in candidates if candidate.is_file()), candidates[0])


def online_runtime_ready(runtime_dir: Path) -> bool:
    python = runtime_python(runtime_dir)
    if not python.is_file():
        return False
    result = subprocess.run(
        [str(python), "-c", "import edge_tts, imageio_ffmpeg"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def install_online_runtime(runtime_dir: Path) -> bool:
    runtime_dir = runtime_dir.resolve()
    if online_runtime_ready(runtime_dir):
        return False
    if runtime_dir.exists() and any(runtime_dir.iterdir()) and not (runtime_dir / "pyvenv.cfg").is_file():
        raise SetupError(
            f"{runtime_dir} is not an isolated TTS environment; refusing to overwrite it"
        )
    if not (runtime_dir / "pyvenv.cfg").is_file():
        runtime_dir.parent.mkdir(parents=True, exist_ok=True)
        try:
            venv.EnvBuilder(with_pip=True, clear=False).create(runtime_dir)
        except OSError as exc:
            raise SetupError(f"cannot create isolated TTS environment: {exc}") from exc
    python = runtime_python(runtime_dir)
    result = subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            *ONLINE_PACKAGES,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "pip failed").strip()
        raise SetupError(f"cannot install free online TTS environment: {detail}")
    if not online_runtime_ready(runtime_dir):
        raise SetupError("online TTS environment installation completed but imports still fail")
    return True


def online_voices(runtime_dir: Path, language: str | None = None) -> list[Voice]:
    if not online_runtime_ready(runtime_dir):
        raise SetupError("free online TTS environment is not installed")
    code = (
        "import asyncio,json,edge_tts;"
        "print(json.dumps(asyncio.run(edge_tts.list_voices()),ensure_ascii=False))"
    )
    result = run_checked([str(runtime_python(runtime_dir)), "-c", code])
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SetupError(f"cannot parse online voice list: {exc}") from exc
    voices = [
        Voice(str(item["ShortName"]), normalize_locale(str(item["Locale"])), "edge")
        for item in payload
        if isinstance(item, dict) and item.get("ShortName") and item.get("Locale")
    ]
    if language:
        voices = [voice for voice in voices if locale_matches(voice.locale, language)]
    return voices


def choose_voice(
    voices: list[Voice], language: str, voice_name: str | None = None
) -> Voice:
    matching = [voice for voice in voices if locale_matches(voice.locale, language)]
    if voice_name:
        named = [voice for voice in matching if voice.name == voice_name]
        if not named:
            raise SetupError(
                f"voice '{voice_name}' is not installed for requested language {language}"
            )
        return named[0]
    if not matching:
        raise SetupError(f"no voice matches requested language {language}")
    return matching[0]


def prepare_output(output: Path, force: bool) -> Path:
    output = output.expanduser().resolve()
    if output.suffix.lower() != ".wav":
        raise InputError("output path must end in .wav")
    if output.exists() and not force:
        raise InputError(f"output already exists: {output}; pass --force to replace it")
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def finalize_wav(temporary_wav: Path, output: Path) -> str:
    try:
        validation = validate_audio.validate(temporary_wav)
    except Exception:
        temporary_wav.unlink(missing_ok=True)
        raise
    os.replace(temporary_wav, output)
    return validation


def synthesize_macos(
    *,
    text: str,
    voice: Voice,
    rate_percent: int,
    output: Path,
    say_path: str,
    afconvert_path: str,
) -> str:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="llc-tts-", dir=output.parent) as directory:
        temporary = Path(directory)
        aiff = temporary / "speech.aiff"
        wav = temporary / "speech.wav"
        run_checked(
            [say_path, "-v", voice.name, "-r", str(macos_rate(rate_percent)), "-o", str(aiff), text]
        )
        run_checked(
            [afconvert_path, "-f", "WAVE", "-d", "LEI16@44100", str(aiff), str(wav)]
        )
        return finalize_wav(wav, output)


def synthesize_windows(
    *,
    text: str,
    voice: Voice,
    rate_percent: int,
    output: Path,
    powershell_path: str,
) -> str:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="llc-tts-", dir=output.parent) as directory:
        wav = Path(directory) / "speech.wav"
        env = os.environ.copy()
        env.update(
            {
                "LLC_TTS_TEXT": text,
                "LLC_TTS_VOICE": voice.name,
                "LLC_TTS_RATE": str(windows_rate(rate_percent)),
                "LLC_TTS_OUTPUT": str(wav),
            }
        )
        run_checked(
            [
                powershell_path,
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                WINDOWS_SYNTHESIS_SCRIPT,
            ],
            env=env,
        )
        return finalize_wav(wav, output)


def synthesize_edge(
    *,
    text: str,
    language: str,
    voice_name: str | None,
    rate_percent: int,
    output: Path,
    runtime_dir: Path,
) -> str:
    voice = choose_voice(online_voices(runtime_dir, language), language, voice_name)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    python = runtime_python(runtime_dir)
    with tempfile.TemporaryDirectory(prefix="llc-tts-", dir=output.parent) as directory:
        temporary = Path(directory)
        mp3 = temporary / "speech.mp3"
        wav = temporary / "speech.wav"
        run_checked(
            [
                str(python),
                "-m",
                "edge_tts",
                "--voice",
                voice.name,
                f"--rate={edge_rate(rate_percent)}",
                "--text",
                text,
                "--write-media",
                str(mp3),
            ]
        )
        ffmpeg_result = run_checked(
            [str(python), "-c", "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"]
        )
        ffmpeg = ffmpeg_result.stdout.strip()
        if not ffmpeg:
            raise SetupError("free online TTS environment has no converter executable")
        run_checked(
            [
                ffmpeg,
                "-nostdin",
                "-y",
                "-i",
                str(mp3),
                "-ac",
                "1",
                "-ar",
                "44100",
                "-c:a",
                "pcm_s16le",
                str(wav),
            ]
        )
        return finalize_wav(wav, output)


def synthesize_auto(
    *,
    text: str,
    language: str,
    voice_name: str | None,
    rate_percent: int,
    output: Path,
    runtime_dir: Path,
    allow_online: bool,
    install_missing: bool,
    system: str | None = None,
) -> str:
    engine, voices = system_voices(language, system=system)
    matching = [voice for voice in voices if locale_matches(voice.locale, language)]
    if engine and matching:
        voice = choose_voice(voices, language, voice_name)
        if engine["kind"] == "macos":
            return synthesize_macos(
                text=text,
                voice=voice,
                rate_percent=rate_percent,
                output=output,
                say_path=engine["say"],
                afconvert_path=engine["afconvert"],
            )
        if engine["kind"] == "windows":
            return synthesize_windows(
                text=text,
                voice=voice,
                rate_percent=rate_percent,
                output=output,
                powershell_path=engine["powershell"],
            )
    if not allow_online:
        raise SetupError(
            f"no matching free system voice for {language}; install a free system voice "
            "or explicitly allow the free online fallback"
        )
    if install_missing:
        install_online_runtime(runtime_dir)
    elif not online_runtime_ready(runtime_dir):
        raise SetupError(
            "free online TTS environment is missing; rerun with --install-missing after approval"
        )
    return synthesize_edge(
        text=text,
        language=language,
        voice_name=voice_name,
        rate_percent=rate_percent,
        output=output,
        runtime_dir=runtime_dir,
    )


def install_windows_voice(language: str) -> str:
    if platform.system() != "Windows":
        raise SetupError("Windows voice installation can only run on Windows")
    locale = normalize_locale(language)
    if not re.fullmatch(r"[a-z]{2,3}-[A-Z]{2}", locale):
        raise InputError("Windows voice installation requires a language-region locale such as ko-KR")
    shell = powershell_path()
    if not shell:
        raise SetupError("Windows PowerShell is unavailable")
    env = os.environ.copy()
    env["LLC_TTS_LOCALE"] = locale
    result = run_checked(
        [shell, "-NoProfile", "-NonInteractive", "-Command", WINDOWS_INSTALL_VOICE_SCRIPT],
        env=env,
    )
    return result.stdout.strip()


def probe(
    language: str | None = None,
    *,
    runtime_dir: Path | None = None,
    system: str | None = None,
) -> dict[str, object]:
    detected_system = system or platform.system()
    engine, voices = system_voices(language, system=detected_system)
    matching = (
        [voice for voice in voices if locale_matches(voice.locale, language)]
        if language
        else voices
    )
    return {
        "system": detected_system,
        "language": normalize_locale(language) if language else None,
        "local_engine": engine["kind"] if engine else None,
        "local_ready": bool(engine and matching),
        "matching_local_voices": [asdict(voice) for voice in matching],
        "online_runtime": str(runtime_dir.resolve()) if runtime_dir else None,
        "online_ready": bool(runtime_dir and online_runtime_ready(runtime_dir)),
        "paid_api_required": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Probe, install, and use free TTS environments for validated learner WAVs."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    probe_parser = subparsers.add_parser("probe", help="inspect the current TTS environment")
    probe_parser.add_argument("--language")
    probe_parser.add_argument("--runtime-dir", type=Path)

    voices_parser = subparsers.add_parser("voices", help="list matching free voices")
    voices_parser.add_argument("--language")
    voices_parser.add_argument("--runtime-dir", type=Path)
    voices_parser.add_argument("--online", action="store_true")

    install_online_parser = subparsers.add_parser(
        "install-online", help="install the optional free online fallback in an isolated venv"
    )
    install_online_parser.add_argument("--runtime-dir", type=Path, required=True)

    install_windows_parser = subparsers.add_parser(
        "install-windows-voice", help="install a free Windows Text-to-Speech language capability"
    )
    install_windows_parser.add_argument("--language", required=True)

    synthesize_parser = subparsers.add_parser(
        "synthesize", help="generate and validate a labelled synthetic PCM WAV"
    )
    synthesize_parser.add_argument("--text", required=True)
    synthesize_parser.add_argument("--language", required=True)
    synthesize_parser.add_argument("--voice")
    synthesize_parser.add_argument("--rate-percent", type=int, default=85)
    synthesize_parser.add_argument("--output", type=Path, required=True)
    synthesize_parser.add_argument("--runtime-dir", type=Path)
    synthesize_parser.add_argument("--allow-online", action="store_true")
    synthesize_parser.add_argument("--install-missing", action="store_true")
    synthesize_parser.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "probe":
            print(
                json.dumps(
                    probe(args.language, runtime_dir=args.runtime_dir),
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        elif args.command == "voices":
            if args.online:
                if args.runtime_dir is None:
                    raise InputError("--runtime-dir is required with --online")
                voices = online_voices(args.runtime_dir, args.language)
            else:
                _, voices = system_voices(args.language)
                if args.language:
                    voices = [
                        voice for voice in voices if locale_matches(voice.locale, args.language)
                    ]
            print(json.dumps([asdict(voice) for voice in voices], ensure_ascii=False))
        elif args.command == "install-online":
            changed = install_online_runtime(args.runtime_dir)
            print(
                json.dumps(
                    {
                        "status": "installed" if changed else "already_ready",
                        "runtime_dir": str(args.runtime_dir.resolve()),
                        "packages": ONLINE_PACKAGES,
                        "paid_api_required": False,
                    },
                    ensure_ascii=False,
                )
            )
        elif args.command == "install-windows-voice":
            print(
                json.dumps(
                    {
                        "status": "installed_or_already_ready",
                        "capability": install_windows_voice(args.language),
                        "paid_api_required": False,
                    },
                    ensure_ascii=False,
                )
            )
        elif args.command == "synthesize":
            output = prepare_output(args.output, args.force)
            runtime_dir = args.runtime_dir or output.parent / ".tts-runtime"
            validation = synthesize_auto(
                text=args.text,
                language=args.language,
                voice_name=args.voice,
                rate_percent=args.rate_percent,
                output=output,
                runtime_dir=runtime_dir,
                allow_online=args.allow_online,
                install_missing=args.install_missing,
            )
            print(
                json.dumps(
                    {
                        "status": "ok",
                        "output": str(output),
                        "label": "synthetic speech (TTS)",
                        "validation": validation,
                        "paid_api_required": False,
                    },
                    ensure_ascii=False,
                )
            )
        return 0
    except InputError as exc:
        print(f"INPUT_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INPUT
    except SetupError as exc:
        print(f"SETUP_ERROR reason={exc}", file=sys.stderr)
        return EXIT_SETUP
    except (SynthesisError, validate_audio.ValidationError) as exc:
        print(f"SYNTHESIS_ERROR reason={exc}", file=sys.stderr)
        return EXIT_SYNTHESIS
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"INTERNAL_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
