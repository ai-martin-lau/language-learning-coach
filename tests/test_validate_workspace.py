import contextlib
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TEMPLATES = ROOT / "assets" / "learning-workspace"

sys.path.insert(0, str(SCRIPTS))
import validate_workspace


class ValidateWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name) / "korean"
        shutil.copytree(TEMPLATES, self.workspace)

    def tearDown(self):
        self.tempdir.cleanup()

    def replace(self, filename, old, new, count=1):
        path = self.workspace / filename
        text = path.read_text(encoding="utf-8")
        self.assertGreaterEqual(
            text.count(old), count, f"fixture marker not found enough times: {old!r}"
        )
        path.write_text(text.replace(old, new, count), encoding="utf-8")

    def remove_line(self, filename, line):
        self.replace(filename, line + "\n", "")

    def assert_error_contains(self, report, fragment):
        self.assertFalse(report.ok)
        self.assertTrue(
            any(fragment in error for error in report.errors),
            f"missing {fragment!r} in errors: {report.errors}",
        )

    def call_main(self, path):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validate_workspace.main([str(path)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_current_templates_form_a_valid_workspace(self):
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(1, report.phrase_count)
        self.assertEqual(30, report.function_count)

    def test_missing_required_file_is_reported(self):
        (self.workspace / "function-map.md").unlink()
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "function-map.md: missing required file")

    def test_required_fields_are_checked_in_each_state_file(self):
        cases = [
            ("profile.md", "- 固定触发点：待填写", "missing field '固定触发点'"),
            ("phrase-bank.md", "- 沟通修复表达：待填写", "missing field '沟通修复表达'"),
            ("progress.md", "- 兴趣输入：待填写", "missing field '兴趣输入'"),
        ]
        for filename, line, expected in cases:
            with self.subTest(filename=filename):
                with tempfile.TemporaryDirectory() as directory:
                    workspace = Path(directory) / "workspace"
                    shutil.copytree(TEMPLATES, workspace)
                    path = workspace / filename
                    text = path.read_text(encoding="utf-8")
                    path.write_text(text.replace(line + "\n", "", 1), encoding="utf-8")
                    report = validate_workspace.validate(workspace)
                    self.assert_error_contains(report, expected)

    def test_duplicate_phrase_id_is_reported_with_lines(self):
        path = self.workspace / "phrase-bank.md"
        text = path.read_text(encoding="utf-8")
        block = text[text.index("## P001") :]
        path.write_text(text + "\n" + block, encoding="utf-8")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate phrase ID P001")
        self.assertEqual(2, report.phrase_count)

    def test_malformed_phrase_id_is_rejected(self):
        self.replace("phrase-bank.md", "## P001 — 沟通意图", "## P01 — 沟通意图")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid phrase heading 'P01'")

    def test_phrase_id_zero_is_rejected(self):
        self.replace("phrase-bank.md", "## P001 — 沟通意图", "## P000 — 沟通意图")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid phrase heading 'P000'")

    def test_duplicate_function_id_also_exposes_the_missing_id(self):
        self.replace("function-map.md", "| F02 |", "| F01 |")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate function ID F01")
        self.assert_error_contains(report, "missing function IDs: F02")

    def test_function_map_placeholders_are_not_treated_as_ids(self):
        report = validate_workspace.validate(self.workspace)
        self.assertFalse(any("invalid function ID '—'" in error for error in report.errors))

    def test_invalid_function_priority_and_state_are_reported(self):
        self.replace(
            "function-map.md",
            "| F01 | 询问姓名 | pending | not_selected |",
            "| F01 | 询问姓名 | urgent | mastered |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid priority 'urgent'")
        self.assert_error_contains(report, "invalid function state 'mastered'")

    def test_invalid_starter_function_id_is_reported(self):
        self.replace(
            "phrase-bank.md",
            "- 起步功能编号：待填写（F01–F30；无对应项写 `not_applicable`）",
            "- 起步功能编号：F31",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid starter function ID 'F31'")

    def test_invalid_evidence_dimension_prompt_and_result_are_distinct(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| speaking | 待填写 | `hint` | `mastered` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid dimension 'speaking'")
        self.assert_error_contains(report, "invalid prompt level 'hint'")
        self.assert_error_contains(report, "invalid result state 'mastered'")

    def test_all_six_evidence_dimensions_are_required(self):
        self.remove_line(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "missing evidence dimensions: reading")

    def test_duplicate_evidence_dimension_is_reported(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate dimension listening")
        self.assert_error_contains(report, "missing evidence dimensions: reading")

    def test_recognized_or_higher_requires_substantive_evidence(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 待填写 | `none` | `independent` | `direct_task` | 完成任务 | 待确认 | 尚未安排 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "cannot use unresolved '任务'")
        self.assert_error_contains(report, "cannot use unresolved '证据日期'")
        self.assert_error_contains(report, "cannot use unresolved '下次复测'")

    def test_substantive_recognized_evidence_passes(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace(
            "phrase-bank.md", "- 来源链接或文件：待填写", "- 来源链接或文件：hotel-greeting.wav"
        )
        self.replace("phrase-bank.md", "- 目标变体：待填写", "- 目标变体：韩国标准语")
        self.replace(
            "phrase-bank.md", "- 交付方式：待填写", "- 交付方式：课程内完整 WAV 播放器"
        )
        self.replace(
            "phrase-bank.md", "- 来源支持内容：待填写", "- 来源支持内容：完整表达的合成声音"
        )
        self.replace(
            "phrase-bank.md", "- 技术验证：待填写", "- 技术验证：validate_audio.py 通过"
        )
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `direct_task` | 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_new_can_record_a_failed_direct_attempt(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 酒店问候 | `intent` | `new` | `direct_task` | 未能提取 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_pronunciation_cannot_be_upgraded_from_self_report(self):
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| pronunciation | 跟读 | `none` | `independent` | `self_report` | 用户说已跟读 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "pronunciation evidence cannot be upgraded from self_report")

    def test_listening_evidence_requires_a_delivered_audio_source_class(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `direct_task` | 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "listening evidence requires a delivered audio source class")

    def test_listening_evidence_requires_substantive_audio_source_fields(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `direct_task` | 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unresolved audio source field '来源链接或文件'")
        self.assert_error_contains(report, "unresolved audio source field '目标变体'")
        self.assert_error_contains(report, "unresolved audio source field '交付方式'")
        self.assert_error_contains(report, "unresolved audio source field '来源支持内容'")
        self.assert_error_contains(report, "unresolved audio source field '技术验证'")

    def test_advanced_result_requires_no_prompt(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `intent` | `independent` | `direct_task` | 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "independent result requires prompt level none")

    def test_recognized_result_requires_a_recorded_prompt_level(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `not_applicable` | `recognized` | `direct_task` | 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "recognized result requires a recorded prompt level")

    def test_cued_result_requires_an_actual_prompt(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `cued` | `direct_task` | 完成任务 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "cued result requires an actual prompt")

    def test_evidence_environment_is_required_for_recorded_results(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `not_applicable` | 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "requires a recorded evidence environment")

    def test_interaction_cannot_be_recorded_as_a_direct_non_simulated_task(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 酒店角色扮演 | `none` | `independent` | `direct_task` | 完成问候 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "interaction evidence cannot use environment 'direct_task'")

    def test_pending_task_words_are_unresolved_evidence(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 待测试 | `none` | `recognized` | `direct_task` | 完成 | 2026-08-16 | 待安排 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "cannot use unresolved '任务'")
        self.assert_error_contains(report, "cannot use unresolved '下次复测'")

    def test_tts_cannot_be_presented_as_a_native_recording(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace("phrase-bank.md", "- 来源支持内容：待填写", "- 来源支持内容：母语者发音示范")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "source class tts is presented as a native recording")

    def test_native_source_class_cannot_describe_synthetic_speech(self):
        self.replace(
            "phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`native_traceable`"
        )
        self.replace("phrase-bank.md", "- 交付方式：待填写", "- 交付方式：合成语音（TTS）")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "synthetic speech is labelled as native_traceable")

    def test_tts_limitation_statement_is_not_a_native_claim(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace(
            "phrase-bank.md",
            "- 来源支持内容：待填写",
            "- 来源支持内容：仅供初次听辨，不能证明母语者发音",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_tts_comparison_with_native_audio_is_not_a_native_claim(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace(
            "phrase-bank.md",
            "- 来源支持内容：待填写",
            "- 来源支持内容：TTS 与母语者录音不同，只供排练",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_native_text_used_for_tts_is_not_called_a_native_recording(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace(
            "phrase-bank.md",
            "- 来源支持内容：待填写",
            "- 来源支持内容：母语者提供的文本，经 TTS 合成",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_native_source_can_explicitly_state_it_is_not_tts(self):
        self.replace(
            "phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`native_official`"
        )
        self.replace("phrase-bank.md", "- 技术验证：待填写", "- 技术验证：已确认非 TTS")
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_invalid_source_class_is_reported(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`official`")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid source class 'official'")

    def test_progress_retest_rows_use_shared_dimension_and_prompt_enums(self):
        self.replace(
            "progress.md",
            "|  |  |  |  |  |  |  |",
            "| P001 | speaking | 2026-08-17 | 酒店任务 | hint | 餐厅 | 延迟复测 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "progress.md:")
        self.assert_error_contains(report, "invalid dimension 'speaking'")
        self.assert_error_contains(report, "invalid prompt level 'hint'")

    def test_function_map_phrase_references_must_exist(self):
        self.replace("function-map.md", "| F01 | 询问姓名 | pending | not_selected | — |", "| F01 | 询问姓名 | pending | active | P999 |")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unknown phrase reference P999")

    def test_progress_phrase_references_must_exist(self):
        self.replace(
            "progress.md",
            "|  |  |  |  |  |  |  |",
            "| P999 | listening | 2026-08-17 | 酒店任务 | none | 餐厅 | 延迟复测 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unknown phrase reference P999")

    def test_unknown_phrase_heading_is_not_silently_ignored(self):
        self.replace("phrase-bank.md", "## P001 — 沟通意图", "## Q001 — 沟通意图")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid phrase heading 'Q001'")
        self.assert_error_contains(report, "no valid phrase blocks")

    def test_missing_evidence_table_header_is_reported(self):
        self.replace(
            "phrase-bank.md",
            "| 维度 | 任务 | 提示级别 | 结果 | 证据环境 | 表现记录 | 证据日期 | 下次复测 |",
            "| 维度 | 任务 | 提示级别 | 成果 | 证据环境 | 表现记录 | 证据日期 | 下次复测 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "missing table header 维度 | 任务 | 提示级别")

    def test_cli_success_and_validation_failure_exit_codes(self):
        code, stdout, stderr = self.call_main(self.workspace)
        self.assertEqual(0, code)
        self.assertIn("OK workspace=", stdout)
        self.assertEqual("", stderr)

        (self.workspace / "profile.md").unlink()
        code, stdout, stderr = self.call_main(self.workspace)
        self.assertEqual(validate_workspace.EXIT_INVALID, code)
        self.assertEqual("", stdout)
        self.assertIn("INVALID profile.md: missing required file", stderr)
        self.assertIn("INVALID errors=1", stderr)

    def test_cli_missing_directory_is_an_input_error(self):
        missing = Path(self.tempdir.name) / "missing"
        code, stdout, stderr = self.call_main(missing)
        self.assertEqual(validate_workspace.EXIT_INPUT, code)
        self.assertEqual("", stdout)
        self.assertIn("INPUT_ERROR", stderr)


if __name__ == "__main__":
    unittest.main()
