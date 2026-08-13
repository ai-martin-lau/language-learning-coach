import contextlib
import io
from pathlib import Path
import struct
import tempfile
import unittest
import wave


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

import sys

sys.path.insert(0, str(SCRIPTS))
import validate_audio


def write_wav(path: Path, samples, sample_rate=8000, sample_width=2):
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(sample_width)
        audio.setframerate(sample_rate)
        if sample_width == 1:
            payload = bytes(samples)
        else:
            payload = b"".join(
                sample.to_bytes(sample_width, "little", signed=True) for sample in samples
            )
        audio.writeframes(payload)


class ValidateAudioTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.directory = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_valid_wav_passes(self):
        path = self.directory / "valid.wav"
        write_wav(path, [0, 1200, -1200, 600] * 400)
        result = validate_audio.validate(path)
        self.assertIn("OK format=wav", result)
        self.assertIn("frames=1600", result)

    def test_zero_frame_wav_fails(self):
        path = self.directory / "zero.wav"
        write_wav(path, [])
        with self.assertRaisesRegex(validate_audio.ValidationError, "zero frames"):
            validate_audio.validate(path)

    def test_digitally_silent_wav_fails(self):
        path = self.directory / "silent.wav"
        write_wav(path, [0, 0, 0, 0] * 400)
        with self.assertRaisesRegex(validate_audio.ValidationError, "below threshold"):
            validate_audio.validate(path)

    def test_unsigned_eight_bit_silence_fails(self):
        path = self.directory / "silent-8-bit.wav"
        write_wav(path, [128, 128, 128, 128] * 400, sample_width=1)
        with self.assertRaisesRegex(validate_audio.ValidationError, "below threshold"):
            validate_audio.validate(path)

    def test_unsigned_eight_bit_signal_passes(self):
        path = self.directory / "signal-8-bit.wav"
        write_wav(path, [128, 129, 127, 128] * 400, sample_width=1)
        self.assertIn("OK format=wav", validate_audio.validate(path))

    def test_too_short_wav_fails(self):
        path = self.directory / "too-short.wav"
        write_wav(path, [0, 1200, -1200, 600])
        with self.assertRaisesRegex(validate_audio.ValidationError, "too short"):
            validate_audio.validate(path)

    def test_corrupt_wav_fails(self):
        path = self.directory / "fake.wav"
        path.write_text("not audio", encoding="utf-8")
        with self.assertRaises(validate_audio.ValidationError):
            validate_audio.validate(path)

    def test_truncated_wav_fails(self):
        path = self.directory / "truncated.wav"
        write_wav(path, [100, 200, 300, 400] * 400)
        data = bytearray(path.read_bytes())
        path.write_bytes(data[:-2])
        with self.assertRaisesRegex(validate_audio.ValidationError, "truncated RIFF container"):
            validate_audio.validate(path)

    def test_riff_declared_size_past_end_fails(self):
        path = self.directory / "bad-riff-size.wav"
        write_wav(path, [100, 200, 300, 400] * 400)
        data = bytearray(path.read_bytes())
        declared_size = struct.unpack("<I", data[4:8])[0]
        data[4:8] = struct.pack("<I", declared_size + 1000)
        path.write_bytes(data)
        with self.assertRaisesRegex(validate_audio.ValidationError, "truncated RIFF container"):
            validate_audio.validate(path)

    def test_empty_file_is_input_error(self):
        path = self.directory / "empty.wav"
        path.touch()
        with self.assertRaisesRegex(OSError, "empty"):
            validate_audio.validate(path)

    def test_unsupported_format_fails(self):
        path = self.directory / "audio.mp3"
        path.write_bytes(b"ID3not-really-an-mp3")
        with self.assertRaises(NotImplementedError):
            validate_audio.validate(path)

    def test_cli_reports_distinct_exit_codes(self):
        missing = self.directory / "missing.wav"
        old_argv = sys.argv
        stderr = io.StringIO()
        try:
            sys.argv = ["validate_audio.py", str(missing)]
            with contextlib.redirect_stderr(stderr):
                code = validate_audio.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(validate_audio.EXIT_INPUT, code)
        self.assertIn("INPUT_ERROR", stderr.getvalue())

    def test_cli_success_and_failure_categories(self):
        valid = self.directory / "valid.wav"
        invalid = self.directory / "invalid.wav"
        unsupported = self.directory / "unsupported.mp3"
        write_wav(valid, [0, 1200, -1200, 600] * 400)
        write_wav(invalid, [])
        unsupported.write_bytes(b"ID3not-really-an-mp3")

        cases = [
            (valid, 0, "OK format=wav"),
            (invalid, validate_audio.EXIT_INVALID, "INVALID"),
            (unsupported, validate_audio.EXIT_UNSUPPORTED, "UNSUPPORTED"),
        ]
        for path, expected_code, marker in cases:
            with self.subTest(path=path):
                old_argv = sys.argv
                stdout = io.StringIO()
                stderr = io.StringIO()
                try:
                    sys.argv = ["validate_audio.py", str(path)]
                    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                        code = validate_audio.main()
                finally:
                    sys.argv = old_argv
                self.assertEqual(expected_code, code)
                self.assertIn(marker, stdout.getvalue() + stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
