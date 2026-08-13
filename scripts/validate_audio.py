#!/usr/bin/env python3
"""Validate that a local PCM WAV contains playable, non-silent audio."""

import argparse
import math
import os
from pathlib import Path
import struct
import sys
import wave


EXIT_INTERNAL = 1
EXIT_INPUT = 3
EXIT_UNSUPPORTED = 4
EXIT_INVALID = 5
MIN_DURATION_SECONDS = 0.1


class ValidationError(Exception):
    """An expected audio validation failure."""


def pcm_peak(chunk: bytes, sample_width: int) -> int:
    if sample_width == 1:
        return max((abs(sample - 128) for sample in chunk), default=0)
    if sample_width == 2:
        return max((abs(sample[0]) for sample in struct.iter_unpack("<h", chunk)), default=0)
    if sample_width == 3:
        return max(
            (
                abs(int.from_bytes(chunk[index : index + 3], "little", signed=True))
                for index in range(0, len(chunk), 3)
            ),
            default=0,
        )
    if sample_width == 4:
        return max((abs(sample[0]) for sample in struct.iter_unpack("<i", chunk)), default=0)
    raise ValidationError(f"unsupported PCM sample width: {sample_width} bytes")


def validate_wav(path: Path) -> str:
    with path.open("rb") as raw_audio:
        header = raw_audio.read(12)
    if len(header) < 12 or header[:4] != b"RIFF" or header[8:12] != b"WAVE":
        raise ValidationError("invalid RIFF/WAVE header")
    declared_file_size = struct.unpack("<I", header[4:8])[0] + 8
    actual_file_size = path.stat().st_size
    if declared_file_size > actual_file_size:
        raise ValidationError(
            f"truncated RIFF container: expected {declared_file_size} bytes, found {actual_file_size}"
        )

    try:
        with wave.open(str(path), "rb") as audio:
            channels = audio.getnchannels()
            sample_width = audio.getsampwidth()
            sample_rate = audio.getframerate()
            declared_frames = audio.getnframes()
            compression = audio.getcomptype()

            if compression != "NONE":
                raise ValidationError("compressed WAV is not supported")
            if channels <= 0 or sample_width <= 0 or sample_rate <= 0:
                raise ValidationError("invalid audio parameters")
            if declared_frames <= 0:
                raise ValidationError("audio has zero frames")

            duration = declared_frames / sample_rate
            if not math.isfinite(duration) or duration < MIN_DURATION_SECONDS:
                raise ValidationError(
                    f"audio is too short: {duration:.3f}s; minimum is {MIN_DURATION_SECONDS:.3f}s"
                )

            frames_read = 0
            peak = 0
            while True:
                chunk = audio.readframes(65536)
                if not chunk:
                    break
                frame_size = channels * sample_width
                if len(chunk) % frame_size:
                    raise ValidationError("audio payload ends inside a frame")
                frames_read += len(chunk) // frame_size
                peak = max(peak, pcm_peak(chunk, sample_width))

            if frames_read != declared_frames:
                raise ValidationError(
                    f"truncated audio payload: expected {declared_frames} frames, read {frames_read}"
                )
            signal_floor = max(1, int((1 << (sample_width * 8 - 1)) * 0.001))
            if peak < signal_floor:
                raise ValidationError(
                    f"audio signal is below threshold: peak {peak}, minimum {signal_floor}"
                )

    except (EOFError, wave.Error) as exc:
        raise ValidationError(str(exc) or "cannot decode WAV") from exc

    return (
        "OK format=wav "
        f"frames={declared_frames} sample_rate={sample_rate} "
        f"duration={duration:.3f}s peak={peak}"
    )


def detect_format(path: Path) -> str:
    with path.open("rb") as handle:
        header = handle.read(12)
    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WAVE":
        return "wav"
    if path.suffix.lower() in {".wav", ".wave"}:
        return "wav"
    return "unsupported"


def validate(path: Path) -> str:
    if not path.exists():
        raise OSError("file does not exist")
    if not path.is_file():
        raise OSError("path is not a regular file")
    if not os.access(path, os.R_OK):
        raise OSError("file is not readable")
    if path.stat().st_size == 0:
        raise OSError("file is empty")

    audio_format = detect_format(path)
    if audio_format == "wav":
        return validate_wav(path)
    raise NotImplementedError(
        f"format {path.suffix.lower() or 'unknown'} has no bundled decoder; convert to PCM WAV"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a local PCM WAV before delivering it to a learner."
    )
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        print(validate(args.path))
        return 0
    except OSError as exc:
        print(f"INPUT_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INPUT
    except NotImplementedError as exc:
        print(f"UNSUPPORTED reason={exc}", file=sys.stderr)
        return EXIT_UNSUPPORTED
    except ValidationError as exc:
        print(f"INVALID format=wav reason={exc}", file=sys.stderr)
        return EXIT_INVALID
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"INTERNAL_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
