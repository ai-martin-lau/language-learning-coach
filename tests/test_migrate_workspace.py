import contextlib
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TEMPLATES = ROOT / "assets" / "learning-workspace"

sys.path.insert(0, str(SCRIPTS))
import migrate_workspace
import validate_workspace


class MigrateWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name) / "legacy-language"
        shutil.copytree(TEMPLATES, self.workspace)
        self.progress = self.workspace / "progress.md"
        self.current_section = migrate_workspace.current_foundation_section()
        current = self.progress.read_bytes()
        start = current.index(migrate_workspace.FOUNDATION_HEADING)
        end = current.index(migrate_workspace.RETEST_HEADING)
        self.progress.write_bytes(
            current[:start] + self.current_section + current[end:]
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def make_legacy(self) -> bytes:
        current = self.progress.read_bytes()
        start = current.index(migrate_workspace.FOUNDATION_HEADING)
        end = current.index(migrate_workspace.RETEST_HEADING)
        legacy = current[:start] + current[end:]
        self.progress.write_bytes(legacy)
        return legacy

    def call_main(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = migrate_workspace.main([str(self.workspace)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_inserts_current_empty_section_and_preserves_other_bytes(self):
        before = self.make_legacy()
        anchor = before.index(migrate_workspace.RETEST_HEADING)

        changed = migrate_workspace.migrate(self.workspace)

        self.assertTrue(changed)
        self.assertEqual(
            before[:anchor] + self.current_section + before[anchor:],
            self.progress.read_bytes(),
        )

        lines = self.current_section.decode().splitlines()
        header_index = lines.index(migrate_workspace.FOUNDATION_TABLE_HEADER.decode())
        self.assertEqual(11, len(lines[header_index].strip("|").split("|")))
        self.assertEqual(11, len(lines[header_index + 2].strip("|").split("|")))

    def test_existing_table_is_unchanged_without_writing(self):
        before = self.progress.read_bytes()
        with mock.patch.object(migrate_workspace, "atomic_write") as atomic_write:
            changed = migrate_workspace.migrate(self.workspace)

        self.assertFalse(changed)
        atomic_write.assert_not_called()
        self.assertEqual(before, self.progress.read_bytes())

    def test_table_header_without_heading_is_invalid_and_does_not_write(self):
        before = self.progress.read_bytes().replace(
            migrate_workspace.FOUNDATION_HEADING + b"\n\n",
            b"",
            1,
        )
        self.progress.write_bytes(before)

        with self.assertRaisesRegex(
            migrate_workspace.MigrationError, "malformed or duplicate"
        ):
            migrate_workspace.migrate(self.workspace)
        self.assertEqual(before, self.progress.read_bytes())

    def test_second_run_is_idempotent(self):
        self.make_legacy()
        self.assertTrue(migrate_workspace.migrate(self.workspace))
        after_first_run = self.progress.read_bytes()

        self.assertFalse(migrate_workspace.migrate(self.workspace))
        self.assertEqual(after_first_run, self.progress.read_bytes())

    def test_renames_legacy_task_map_heading_without_changing_rows(self):
        before = self.progress.read_bytes().replace(
            migrate_workspace.MISSION_HEADING,
            migrate_workspace.LEGACY_MISSION_HEADING,
            1,
        )
        self.progress.write_bytes(before)

        self.assertTrue(migrate_workspace.migrate(self.workspace))

        expected = before.replace(
            migrate_workspace.LEGACY_MISSION_HEADING,
            migrate_workspace.MISSION_HEADING,
            1,
        )
        self.assertEqual(expected, self.progress.read_bytes())

    def test_renames_heading_and_adds_foundation_in_one_run(self):
        before = self.make_legacy().replace(
            migrate_workspace.MISSION_HEADING,
            migrate_workspace.LEGACY_MISSION_HEADING,
            1,
        )
        self.progress.write_bytes(before)

        self.assertTrue(migrate_workspace.migrate(self.workspace))

        after = self.progress.read_bytes()
        self.assertIn(migrate_workspace.MISSION_HEADING, after)
        self.assertNotIn(migrate_workspace.LEGACY_MISSION_HEADING, after)
        self.assertIn(migrate_workspace.FOUNDATION_TABLE_HEADER, after)

    def test_missing_progress_is_an_input_error_without_write(self):
        self.progress.unlink()

        with self.assertRaisesRegex(OSError, "progress.md does not exist"):
            migrate_workspace.migrate(self.workspace)
        self.assertFalse(self.progress.exists())

    def test_missing_anchor_is_invalid_and_does_not_write(self):
        before = self.make_legacy().replace(
            migrate_workspace.RETEST_HEADING,
            "## 复测安排".encode(),
        )
        self.progress.write_bytes(before)

        with self.assertRaisesRegex(migrate_workspace.MigrationError, "missing insertion anchor"):
            migrate_workspace.migrate(self.workspace)
        self.assertEqual(before, self.progress.read_bytes())

    def test_migrated_modern_legacy_fixture_passes_validator(self):
        self.make_legacy()
        before = validate_workspace.validate(self.workspace)
        self.assertFalse(before.ok)
        self.assertTrue(
            any("sound-script foundation" in error for error in before.errors),
            before.errors,
        )

        self.assertTrue(migrate_workspace.migrate(self.workspace))

        after = validate_workspace.validate(self.workspace)
        self.assertTrue(after.ok, after.errors)

    def test_cli_reports_changed_then_unchanged(self):
        self.make_legacy()

        code, stdout, stderr = self.call_main()
        self.assertEqual(0, code)
        self.assertIn("changed workspace=", stdout)
        self.assertEqual("", stderr)

        code, stdout, stderr = self.call_main()
        self.assertEqual(0, code)
        self.assertIn("unchanged workspace=", stdout)
        self.assertEqual("", stderr)

    def test_cli_reports_input_and_invalid_exit_codes(self):
        self.progress.unlink()
        code, stdout, stderr = self.call_main()
        self.assertEqual(migrate_workspace.EXIT_INPUT, code)
        self.assertEqual("", stdout)
        self.assertIn("INPUT_ERROR", stderr)

        shutil.copy(TEMPLATES / "progress.md", self.progress)
        before = self.make_legacy().replace(
            migrate_workspace.RETEST_HEADING,
            "## 复测安排".encode(),
        )
        self.progress.write_bytes(before)
        code, stdout, stderr = self.call_main()
        self.assertEqual(migrate_workspace.EXIT_INVALID, code)
        self.assertEqual("", stdout)
        self.assertIn("INVALID", stderr)
        self.assertEqual(before, self.progress.read_bytes())


if __name__ == "__main__":
    unittest.main()
