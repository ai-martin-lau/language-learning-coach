import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import wave


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

import sys

sys.path.insert(0, str(SCRIPTS))
import generate_tts


def write_valid_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        frames = b"".join(
            sample.to_bytes(2, "little", signed=True)
            for sample in ([0, 1200, -1200, 600] * 400)
        )
        audio.writeframes(frames)


class GenerateTtsTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.directory = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_parse_macos_voices_handles_multiword_names_and_locales(self):
        output = """\
Eddy (English (US))    en_US    # Hello!
Yuna                    ko_KR    # \uc548\ub155\ud558\uc138\uc694!
Mei-Jia                 zh_TW    # \u4f60\u597d！
"""

        voices = generate_tts.parse_macos_voices(output)

        self.assertEqual(
            [
                generate_tts.Voice("Eddy (English (US))", "en-US", "macos"),
                generate_tts.Voice("Yuna", "ko-KR", "macos"),
                generate_tts.Voice("Mei-Jia", "zh-TW", "macos"),
            ],
            voices,
        )

    def test_parse_windows_voices_accepts_single_or_multiple_json_objects(self):
        one = '{"name":"Microsoft Heami Desktop","locale":"ko-KR"}'
        many = (
            '[{"name":"Microsoft Heami Desktop","locale":"ko-KR"},'
            '{"name":"Microsoft Zira Desktop","locale":"en-US"}]'
        )

        self.assertEqual(
            [generate_tts.Voice("Microsoft Heami Desktop", "ko-KR", "windows")],
            generate_tts.parse_windows_voices(one),
        )
        self.assertEqual(2, len(generate_tts.parse_windows_voices(many)))

    def test_language_matching_accepts_language_or_exact_locale(self):
        self.assertTrue(generate_tts.locale_matches("ko-KR", "ko"))
        self.assertTrue(generate_tts.locale_matches("ko_KR", "ko-KR"))
        self.assertFalse(generate_tts.locale_matches("ja-JP", "ko"))

    def test_rate_mapping_is_bounded_for_each_engine(self):
        self.assertEqual(140, generate_tts.macos_rate(80))
        self.assertEqual(-2, generate_tts.windows_rate(80))
        self.assertEqual("-20%", generate_tts.edge_rate(80))
        self.assertEqual(10, generate_tts.windows_rate(1000))
        self.assertEqual(-10, generate_tts.windows_rate(0))

    @mock.patch.object(generate_tts.shutil, "which")
    @mock.patch.object(generate_tts.subprocess, "run")
    def test_probe_macos_reports_target_voice_without_mutation(self, run, which):
        which.side_effect = lambda name: f"/usr/bin/{name}" if name in {"say", "afconvert"} else None
        run.return_value = mock.Mock(
            returncode=0,
            stdout="Yuna                    ko_KR    # \uc548\ub155\ud558\uc138\uc694!\n",
            stderr="",
        )

        report = generate_tts.probe("ko-KR", system="Darwin")

        self.assertTrue(report["local_ready"])
        self.assertEqual("Yuna", report["matching_local_voices"][0]["name"])
        run.assert_called_once()

    @mock.patch.object(generate_tts, "run_checked")
    def test_macos_synthesis_uses_say_afconvert_and_validates_wav(self, run_checked):
        output = self.directory / "lesson.wav"

        def fake_run(command, **kwargs):
            if command[0] == "/usr/bin/afconvert":
                write_valid_wav(Path(command[-1]))
            return mock.Mock(returncode=0, stdout="", stderr="")

        run_checked.side_effect = fake_run

        result = generate_tts.synthesize_macos(
            text="\uc548\ub155\ud558\uc138\uc694",
            voice=generate_tts.Voice("Yuna", "ko-KR", "macos"),
            rate_percent=80,
            output=output,
            say_path="/usr/bin/say",
            afconvert_path="/usr/bin/afconvert",
        )

        self.assertTrue(output.exists())
        self.assertIn("OK format=wav", result)
        say_command = run_checked.call_args_list[0].args[0]
        self.assertEqual("/usr/bin/say", say_command[0])
        self.assertIn("Yuna", say_command)
        self.assertNotIn("\uc548\ub155\ud558\uc138\uc694", " ".join(say_command[:-1]))

    @mock.patch.object(generate_tts, "run_checked")
    def test_windows_synthesis_passes_text_through_environment_not_script(self, run_checked):
        output = self.directory / "lesson.wav"

        def fake_run(command, **kwargs):
            write_valid_wav(Path(kwargs["env"]["LLC_TTS_OUTPUT"]))
            self.assertNotIn("\uc548\ub155\ud558\uc138\uc694", command[-1])
            return mock.Mock(returncode=0, stdout="", stderr="")

        run_checked.side_effect = fake_run

        result = generate_tts.synthesize_windows(
            text="\uc548\ub155\ud558\uc138\uc694",
            voice=generate_tts.Voice("Microsoft Heami Desktop", "ko-KR", "windows"),
            rate_percent=80,
            output=output,
            powershell_path="C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
        )

        self.assertTrue(output.exists())
        self.assertIn("OK format=wav", result)
        env = run_checked.call_args.kwargs["env"]
        self.assertEqual("\uc548\ub155\ud558\uc138\uc694", env["LLC_TTS_TEXT"])
        self.assertEqual("Microsoft Heami Desktop", env["LLC_TTS_VOICE"])

    def test_online_runtime_refuses_nonempty_nonvenv_directory(self):
        runtime = self.directory / "runtime"
        runtime.mkdir()
        (runtime / "keep.txt").write_text("user data", encoding="utf-8")

        with self.assertRaisesRegex(generate_tts.SetupError, "not an isolated TTS environment"):
            generate_tts.install_online_runtime(runtime)

        self.assertEqual("user data", (runtime / "keep.txt").read_text(encoding="utf-8"))

    @mock.patch.object(generate_tts, "install_online_runtime")
    @mock.patch.object(generate_tts, "synthesize_edge")
    @mock.patch.object(generate_tts, "system_voices", return_value=(None, []))
    def test_auto_engine_installs_free_online_fallback_when_explicitly_allowed(
        self, system_voices, synthesize_edge, install_online_runtime
    ):
        output = self.directory / "lesson.wav"
        runtime = self.directory / "runtime"
        install_online_runtime.return_value = True
        synthesize_edge.return_value = "OK format=wav duration=1.000s"

        result = generate_tts.synthesize_auto(
            text="\uc548\ub155\ud558\uc138\uc694",
            language="ko-KR",
            voice_name=None,
            rate_percent=80,
            output=output,
            runtime_dir=runtime,
            allow_online=True,
            install_missing=True,
            system="Linux",
        )

        self.assertIn("OK format=wav", result)
        install_online_runtime.assert_called_once_with(runtime)
        synthesize_edge.assert_called_once()

    @mock.patch.object(generate_tts, "system_voices", return_value=(None, []))
    def test_auto_engine_never_installs_or_uses_online_without_permission(self, system_voices):
        with self.assertRaisesRegex(generate_tts.SetupError, "no matching free system voice"):
            generate_tts.synthesize_auto(
                text="\uc548\ub155\ud558\uc138\uc694",
                language="ko-KR",
                voice_name=None,
                rate_percent=80,
                output=self.directory / "lesson.wav",
                runtime_dir=self.directory / "runtime",
                allow_online=False,
                install_missing=True,
                system="Linux",
            )

    @mock.patch.object(generate_tts, "probe")
    def test_probe_cli_emits_json(self, probe):
        probe.return_value = {"system": "Darwin", "local_ready": True}
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = generate_tts.main(["probe", "--language", "ko-KR"])

        self.assertEqual(0, code)
        self.assertEqual(
            {"system": "Darwin", "local_ready": True},
            json.loads(stdout.getvalue()),
        )


if __name__ == "__main__":
    unittest.main()
