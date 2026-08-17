import contextlib
from datetime import date, timedelta
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import wave


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
        progress = self.workspace / "progress.md"
        progress.write_text(
            progress.read_text(encoding="utf-8").replace(
                "### YYYY-MM-DD", "### 2026-08-16", 1
            ),
            encoding="utf-8",
        )
        defaults = (
            ("profile.md", "- 目标语言：待填写", "- 目标语言：测试语言"),
            (
                "profile.md",
                "- 语言变体／地区：待填写",
                "- 语言变体／地区：测试标准变体",
            ),
            (
                "profile.md",
                "- 可观察的目标：待填写",
                "- 可观察的目标：完成测试旅行任务",
            ),
            ("profile.md", "- 优先情境：待填写", "- 优先情境：旅行"),
            (
                "progress.md",
                "- 本次唯一重点：待填写",
                "- 本次唯一重点：完成一个测试旅行任务",
            ),
            (
                "progress.md",
                "- 最小完成任务：待填写",
                "- 最小完成任务：在无答案条件下完成核心请求",
            ),
            ("phrase-bank.md", "- 情境：待填写", "- 情境：测试旅行场景"),
            ("phrase-bank.md", "- 模态：声音／文字／混合／其他", "- 模态：混合"),
            ("phrase-bank.md", "- 目标表达：待填写", "- 目标表达：test phrase"),
            (
                "phrase-bank.md",
                "- 含义或交际功能：待填写",
                "- 含义或交际功能：完成测试请求",
            ),
            (
                "phrase-bank.md",
                "- 学习者自己的版本：待填写",
                "- 学习者自己的版本：test phrase",
            ),
            (
                "phrase-bank.md",
                "- 变体与语域：待填写",
                "- 变体与语域：测试标准变体；礼貌",
            ),
        )
        for filename, old, new in defaults:
            self.replace(filename, old, new)

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

    def set_complete_tts_source(self):
        replacements = (
            ("- 来源类别：`pending`", "- 来源类别：`tts`"),
            ("- 表达与语域核实：待填写", "- 表达与语域核实：教材例句确认用于酒店问候"),
            ("- 来源链接或文件：待填写", "- 来源链接或文件：hotel-greeting.wav"),
            ("- 目标变体：待填写", "- 目标变体：韩国标准语"),
            ("- 声音引擎或说话人：待填写", "- 声音引擎或说话人：系统韩语 TTS 声音"),
            ("- 交付方式：待填写", "- 交付方式：课程内完整 WAV 播放器"),
            ("- 来源支持内容：待填写", "- 来源支持内容：完整表达的合成声音"),
            ("- 技术验证：待填写", "- 技术验证：validate_audio.py 通过"),
        )
        for old, new in replacements:
            self.replace("phrase-bank.md", old, new)

    def set_complete_native_source(self):
        replacements = (
            ("- 来源类别：`pending`", "- 来源类别：`native_traceable`"),
            ("- 表达与语域核实：待填写", "- 表达与语域核实：可追溯母语教材确认完整表达与语域"),
            ("- 来源链接或文件：待填写", "- 来源链接或文件：https://example.test/native-audio"),
            ("- 目标变体：待填写", "- 目标变体：目标地区标准变体"),
            ("- 声音引擎或说话人：待填写", "- 声音引擎或说话人：可追溯母语说话人 A"),
            ("- 交付方式：待填写", "- 交付方式：课程内原始音频播放器"),
            ("- 来源支持内容：待填写", "- 来源支持内容：完整表达、目标变体与发音参照"),
            ("- 技术验证：待填写", "- 技术验证：来源文件可解码并已人工播放"),
        )
        for old, new in replacements:
            self.replace("phrase-bank.md", old, new)

    def set_target_script(self, script):
        self.replace(
            "profile.md",
            "- 目标文字脚本：待填写（latin／hangul／japanese／arabic／cyrillic／greek／hebrew／devanagari／thai／han／other／not_applicable）",
            f"- 目标文字脚本：{script}",
        )

    def set_lesson_date(self, lesson_date):
        if lesson_date != "2026-08-16":
            self.replace(
                "progress.md",
                "### 2026-08-16",
                f"### {lesson_date}\n\n### 2026-08-16",
            )

    def set_error_pattern(
        self,
        *,
        pattern_id="E01",
        category="form_retrieval",
        observation_dates="2026-08-16",
        phrase_ids="P001",
        problem="无法在酒店场景中无提示提取问候",
        next_task="在新酒店场景中区分并提取问候",
        state="observing",
    ):
        path = self.workspace / "progress.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        header = "| 模式编号 | 类别 | 观察日期 | 关联语块 | 观察到的问题 | 下一辨别任务 | 状态 |"
        header_index = lines.index(header)
        row_index = header_index + 2
        self.assertEqual("|  |  |  |  |  |  |  |", lines[row_index])
        lines[row_index] = (
            f"| {pattern_id} | {category} | {observation_dates} | {phrase_ids} | "
            f"{problem} | {next_task} | `{state}` |"
        )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def duplicate_phrase_block(self, phrase_id):
        path = self.workspace / "phrase-bank.md"
        text = path.read_text(encoding="utf-8")
        start = text.index("## P001")
        end = text.find("\n## ", start + 1)
        block_end = len(text) if end == -1 else end
        block = text[start:block_end].replace("## P001", f"## {phrase_id}", 1)
        path.write_text(text.rstrip() + "\n\n" + block, encoding="utf-8")

    def set_phrase_identity(self, phrase_id, target, meaning, learner_version):
        path = self.workspace / "phrase-bank.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        start = next(
            index for index, line in enumerate(lines) if line.startswith(f"## {phrase_id} ")
        )
        end = next(
            (
                index
                for index in range(start + 1, len(lines))
                if lines[index].startswith("## P")
            ),
            len(lines),
        )
        replacements = {
            "目标表达": target,
            "含义或交际功能": meaning,
            "学习者自己的版本": learner_version,
        }
        for label, value in replacements.items():
            matches = [
                index
                for index in range(start + 1, end)
                if lines[index].startswith(f"- {label}：")
            ]
            self.assertEqual(1, len(matches), f"expected one {label} field in {phrase_id}")
            lines[matches[0]] = f"- {label}：{value}"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_valid_wav(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(path), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(8000)
            samples = [0, 1200, -1200, 600] * 400
            audio.writeframes(
                b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples)
            )

    def set_mission(
        self,
        mission_id,
        evidence_requirements,
        status,
        *,
        victory="能独立完成交通任务并处理追问",
        recent="精确证据要求均已核对",
        next_change="改变地点",
    ):
        domains = {
            "M01": "transport",
            "M02": "lodging",
            "M03": "eating",
            "M04": "shopping",
            "M05": "directions_local_geography",
            "M06": "communication_repair",
            "M07": "basic_help",
        }
        domain = domains[mission_id]
        self.replace(
            "progress.md",
            f"| {mission_id} | {domain} | 待用户选择具体任务 | — | `not_selected` | — | — |",
            f"| {mission_id} | {domain} | {victory} | {evidence_requirements} | `{status}` | {recent} | {next_change} |",
        )

    def set_a2_screen(
        self,
        status,
        domains="transport, lodging, eating, shopping, communication_repair",
        dimensions="listening, spoken_production, reading, writing, interaction, pronunciation",
        field_check="M03",
        conclusion="证据与已测试旅行任务中的 A2 风格表现一致；正式 CEFR 未确认",
    ):
        self.replace(
            "progress.md",
            "| A2S01 | `not_ready` | — | — | — | 只报告单项任务的实际证据阶梯 |",
            f"| A2S01 | `{status}` | {domains} | {dimensions} | {field_check} | {conclusion} |",
        )

    def set_mission_state(self, mission_id, old_state, new_state):
        path = self.workspace / "progress.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        matches = [index for index, line in enumerate(lines) if line.startswith(f"| {mission_id} |")]
        self.assertEqual(1, len(matches), f"expected one mission row for {mission_id}")
        index = matches[0]
        self.assertIn(f"`{old_state}`", lines[index])
        lines[index] = lines[index].replace(f"`{old_state}`", f"`{new_state}`", 1)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def set_full_retained_evidence_and_ready_missions(self):
        today = date.today()
        first_learning = today - timedelta(days=1)
        self.set_target_script("hangul")
        self.set_lesson_date(today.isoformat())
        self.set_complete_native_source()
        self.replace(
            "phrase-bank.md", "- 首学日期：待填写", f"- 首学日期：{first_learning.isoformat()}"
        )
        rows = {
            "listening": (
                "meaning_response",
                "response: 听懂变化后的旅行回应",
                "real_world_task",
            ),
            "spoken_production": ("audio", "attachment:spoken-retained", "direct_task"),
            "reading": ("meaning_response", "response: 读懂新地点标牌", "direct_task"),
            "writing": ("target_text", "response: 서울역 已填写旅行表格", "direct_task"),
            "interaction": (
                "action",
                "action: 与真人完成请求和追问",
                "real_world_task",
            ),
            "pronunciation": (
                "audio",
                "attachment:pronunciation-retained",
                "direct_task",
            ),
        }
        for dimension, (medium, performance, environment) in rows.items():
            self.replace(
                "phrase-bank.md",
                f"| {dimension} | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
                f"| {dimension} | 延迟旅行任务 | `none` | `retained` | `{environment}` | `{medium}` | {performance} | {today.isoformat()} | 下次旅行前 |",
            )

        for phrase_id in ("P002", "P003", "P004", "P005"):
            self.duplicate_phrase_block(phrase_id)
        identities = {
            "P001": ("표현 하나", "完成交通请求", "표현 하나"),
            "P002": ("표현 둘", "完成住宿请求", "표현 둘"),
            "P003": ("표현 셋", "完成点餐请求", "표현 셋"),
            "P004": ("표현 넷", "完成购物请求", "표현 넷"),
            "P005": ("표현 다섯", "完成沟通修复", "표현 다섯"),
        }
        for phrase_id, identity in identities.items():
            self.set_phrase_identity(phrase_id, *identity)

        self.set_mission(
            "M01",
            "P001:listening:core, P001:spoken_production:follow_up",
            "delayed_passed",
        )
        self.set_mission(
            "M02",
            "P002:reading:core; P002:writing:follow_up",
            "delayed_passed",
        )
        self.set_mission(
            "M03",
            "P003:interaction:core, P003:pronunciation:repair",
            "field_checked",
        )
        self.set_mission(
            "M04",
            "P004:writing:core, P004:interaction:follow_up",
            "delayed_passed",
        )
        self.set_mission(
            "M06",
            "P005:spoken_production:core, P005:interaction:repair",
            "delayed_passed",
        )
        self.set_a2_screen("evidence_consistent_in_tested_tasks")

    def test_current_templates_form_a_valid_workspace(self):
        report = validate_workspace.validate(TEMPLATES)
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
            ("phrase-bank.md", "- 表达与语域核实：待填写", "missing field '表达与语域核实'"),
            ("phrase-bank.md", "- 声音引擎或说话人：待填写", "missing field '声音引擎或说话人'"),
            ("progress.md", "- 兴趣输入：待填写", "missing field '兴趣输入'"),
            ("progress.md", "- 微沉浸状态：off", "missing field '微沉浸状态'"),
            (
                "progress.md",
                "- 微沉浸触发与单项动作：—",
                "missing field '微沉浸触发与单项动作'",
            ),
            (
                "profile.md",
                "- 目标文字脚本：待填写（latin／hangul／japanese／arabic／cyrillic／greek／hebrew／devanagari／thai／han／other／not_applicable）",
                "missing field '目标文字脚本'",
            ),
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

    def test_progress_requires_recurring_error_table(self):
        path = self.workspace / "progress.md"
        text = path.read_text(encoding="utf-8")
        start = text.index("## 反复错误队列")
        end = text.index("## 生活嵌入与真实使用", start)
        path.write_text(text[:start] + text[end:], encoding="utf-8")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "missing table header 模式编号")

    def test_valid_observing_error_pattern_passes(self):
        self.set_error_pattern()
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_error_pattern_id_category_and_state_use_declared_enums(self):
        self.set_error_pattern(pattern_id="E00", category="grammar", state="mastered")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid error pattern ID 'E00'")
        self.assert_error_contains(report, "invalid error category 'grammar'")
        self.assert_error_contains(report, "invalid error pattern state 'mastered'")

    def test_error_pattern_phrase_references_must_exist(self):
        self.set_error_pattern(phrase_ids="P001, P999")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unknown phrase reference P999")

    def test_duplicate_error_pattern_id_is_rejected(self):
        self.set_error_pattern()
        path = self.workspace / "progress.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        row_index = next(index for index, line in enumerate(lines) if line.startswith("| E01 |"))
        lines.insert(row_index + 1, lines[row_index])
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate error pattern ID E01")

    def test_error_pattern_requires_substantive_problem_and_discrimination_task(self):
        self.set_error_pattern(problem="待填写", next_task="—")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unresolved '观察到的问题'")
        self.assert_error_contains(report, "unresolved '下一辨别任务'")

    def test_error_pattern_date_must_use_iso_format(self):
        self.set_error_pattern(observation_dates="2026/08/16")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid observation date '2026/08/16'")

    def test_recurring_error_pattern_requires_two_distinct_lesson_dates(self):
        self.set_error_pattern(state="recurring")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "recurring state requires at least 2 distinct lesson dates")

    def test_resolved_error_pattern_requires_two_distinct_lesson_dates(self):
        self.set_error_pattern(state="resolved")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "resolved state requires at least 2 distinct lesson dates")

    def test_error_pattern_requires_at_least_one_phrase_reference(self):
        self.set_error_pattern(phrase_ids="—")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "error pattern requires at least one phrase reference")

    def test_recurring_error_pattern_accepts_two_distinct_lesson_dates(self):
        self.set_lesson_date("2026-08-15")
        self.set_error_pattern(
            observation_dates="2026-08-15, 2026-08-16",
            state="recurring",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_error_pattern_dates_must_be_unique_real_lesson_dates(self):
        self.set_error_pattern(observation_dates="2026-08-15, 2026-08-15")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate observation date 2026-08-15")
        self.assert_error_contains(report, "observation date 2026-08-15 has no matching lesson heading")

    def test_error_pattern_future_date_is_rejected(self):
        future = (date.today() + timedelta(days=1)).isoformat()
        self.set_error_pattern(observation_dates=future)
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, f"observation date {future} cannot be in the future")

    def test_micro_immersion_status_uses_declared_enum(self):
        self.replace("progress.md", "- 微沉浸状态：off", "- 微沉浸状态：automatic")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid micro-immersion status 'automatic'")

    def test_enabled_micro_immersion_requires_one_concrete_action(self):
        self.replace("progress.md", "- 微沉浸状态：off", "- 微沉浸状态：on")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "enabled micro-immersion requires a concrete trigger and action")

    def test_enabled_micro_immersion_with_one_concrete_action_passes(self):
        self.replace("progress.md", "- 微沉浸状态：off", "- 微沉浸状态：on")
        self.replace(
            "progress.md",
            "- 微沉浸触发与单项动作：—",
            "- 微沉浸触发与单项动作：打开地图后无答案回忆一次问路表达",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_started_workspace_requires_one_focus_and_completion_task(self):
        self.replace(
            "progress.md",
            "- 本次唯一重点：完成一个测试旅行任务",
            "- 本次唯一重点：待填写",
        )
        self.replace(
            "progress.md",
            "- 最小完成任务：在无答案条件下完成核心请求",
            "- 最小完成任务：待填写",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "started workspace requires substantive '本次唯一重点'")
        self.assert_error_contains(report, "started workspace requires substantive '最小完成任务'")

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
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| speaking | 待填写 | `hint` | `mastered` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid dimension 'speaking'")
        self.assert_error_contains(report, "invalid prompt level 'hint'")
        self.assert_error_contains(report, "invalid result state 'mastered'")

    def test_invalid_response_medium_is_reported(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `recognized` | `direct_task` | `text` | response: 读对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid response medium 'text'")

    def test_all_six_evidence_dimensions_are_required(self):
        self.remove_line(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "missing evidence dimensions: reading")

    def test_duplicate_evidence_dimension_is_reported(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate dimension listening")
        self.assert_error_contains(report, "missing evidence dimensions: reading")

    def test_recognized_or_higher_requires_substantive_evidence(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 待填写 | `none` | `independent` | `direct_task` | `meaning_response` | response: 完成任务 | 待确认 | 尚未安排 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "cannot use unresolved '任务'")
        self.assert_error_contains(report, "cannot use unresolved '证据日期'")
        self.assert_error_contains(report, "cannot use unresolved '下次复测'")

    def test_substantive_recognized_evidence_passes(self):
        self.set_complete_tts_source()
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `direct_task` | `meaning_response` | response: 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_new_can_record_a_failed_direct_attempt(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 酒店问候 | `intent` | `new` | `direct_task` | `romanization` | response: 未能提取 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_untested_new_requires_not_applicable_response_medium(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `self_report` | 待填写 | 待填写 | 待填写 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "untested new result requires response medium not_applicable")

    def test_observed_failed_attempt_requires_an_actual_response_medium(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `intent` | `new` | `direct_task` | `not_applicable` | response: 未能判断 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "attempted new result requires a recorded response medium")

    def test_pronunciation_cannot_be_upgraded_from_self_report(self):
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| pronunciation | 跟读 | `none` | `independent` | `self_report` | `self_report` | self_report: 用户说已跟读 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "self_report cannot upgrade pronunciation above new")

    def test_self_report_cannot_upgrade_any_ability(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 阅读菜单 | `none` | `recognized` | `self_report` | `self_report` | self_report: 用户说读懂了 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "self_report cannot upgrade reading above new")

    def test_spoken_production_above_new_requires_audio(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `romanization` | response: 罗马字输入正确 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "spoken_production above new requires response medium audio")

    def test_audio_can_support_spoken_production_without_upgrading_pronunciation(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | attachment:audio-001 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_pronunciation_above_new_requires_audio(self):
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| pronunciation | 检查重音 | `none` | `independent` | `direct_task` | `target_text` | response: 拼写正确 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "pronunciation above new requires response medium audio")

    def test_writing_above_new_requires_target_text(self):
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `romanization` | response: 罗马字输入正确 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "writing above new requires response medium target_text")

    def test_target_text_can_support_writing(self):
        self.set_target_script("hangul")
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | response: 안녕하세요 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_target_text_requires_declared_target_script(self):
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | response: 안녕하세요 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "target_text evidence requires a declared target script"
        )

    def test_target_text_must_contain_declared_script_characters(self):
        self.set_target_script("hangul")
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | response: hello | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "target_text performance payload contains no hangul script characters"
        )

    def test_target_text_latin_script_passes_with_latin_answer(self):
        self.set_target_script("latin")
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | response: bonjour | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_target_text_not_applicable_script_cannot_upgrade(self):
        self.set_target_script("not_applicable")
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | response: bonjour | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "target_text evidence cannot use target script not_applicable"
        )

    def test_target_text_other_script_allows_manual_script_review(self):
        self.set_target_script("other")
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | response: 𐐐𐐯𐑊𐐬 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_target_script_character_detection_covers_declared_scripts(self):
        cases = (
            ("latin", "bonjour", "привет"),
            ("hangul", "안녕하세요", "annyeong"),
            ("japanese", "駅", "eki"),
            ("arabic", "مرحبا", "marhaba"),
            ("cyrillic", "привет", "privet"),
            ("greek", "γεια", "geia"),
            ("hebrew", "שלום", "shalom"),
            ("devanagari", "नमस्ते", "namaste"),
            ("thai", "สวัสดี", "sawasdee"),
            ("han", "你好", "nihao"),
        )
        for script, positive, negative in cases:
            with self.subTest(script=script):
                self.assertTrue(validate_workspace.payload_contains_script(positive, script))
                self.assertFalse(validate_workspace.payload_contains_script(negative, script))
        self.assertTrue(validate_workspace.payload_contains_script("ｂｏｎｊｏｕｒ", "latin"))

    def test_target_text_script_check_does_not_scan_task_column(self):
        self.set_target_script("hangul")
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 한글 쓰기 | `none` | `independent` | `direct_task` | `target_text` | response: annyeong | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "target_text performance payload contains no hangul script characters"
        )

    def test_invalid_target_script_enum_is_reported(self):
        self.set_target_script("hangul_or_latin")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid target script 'hangul_or_latin'")

    def test_listening_evidence_requires_a_delivered_audio_source_class(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `direct_task` | `meaning_response` | response: 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "listening evidence requires a delivered audio source class")

    def test_listening_evidence_requires_substantive_audio_source_fields(self):
        self.replace("phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`tts`")
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `direct_task` | `meaning_response` | response: 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unresolved audio source field '来源链接或文件'")
        self.assert_error_contains(report, "unresolved audio source field '表达与语域核实'")
        self.assert_error_contains(report, "unresolved audio source field '目标变体'")
        self.assert_error_contains(report, "unresolved audio source field '声音引擎或说话人'")
        self.assert_error_contains(report, "unresolved audio source field '交付方式'")
        self.assert_error_contains(report, "unresolved audio source field '来源支持内容'")
        self.assert_error_contains(report, "unresolved audio source field '技术验证'")

    def test_advanced_result_requires_no_prompt(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `intent` | `independent` | `direct_task` | `meaning_response` | response: 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "independent result requires prompt level none")

    def test_recognized_result_requires_a_recorded_prompt_level(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `not_applicable` | `recognized` | `direct_task` | `meaning_response` | response: 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "recognized result requires a recorded prompt level")

    def test_cued_result_requires_an_actual_prompt(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `cued` | `direct_task` | `meaning_response` | response: 完成任务 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "cued result requires an actual prompt")

    def test_evidence_environment_is_required_for_recorded_results(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 酒店问候听辨 | `none` | `recognized` | `not_applicable` | `meaning_response` | response: 选对含义 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "requires a recorded evidence environment")

    def test_interaction_cannot_be_recorded_as_a_direct_non_simulated_task(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 酒店角色扮演 | `none` | `independent` | `direct_task` | `target_text` | response: 完成问候 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "interaction evidence cannot use environment 'direct_task'")

    def test_pending_task_words_are_unresolved_evidence(self):
        self.replace(
            "phrase-bank.md",
            "| listening | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| listening | 待测试 | `none` | `recognized` | `direct_task` | `meaning_response` | response: 完成 | 2026-08-16 | 待安排 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "cannot use unresolved '任务'")
        self.assert_error_contains(report, "cannot use unresolved '下次复测'")

    def test_meaning_response_requires_structured_response_reference(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | 音频已准备交付，等待用户作答 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium meaning_response requires performance reference 'response:'"
        )

    def test_structured_response_reference_must_start_performance_record(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | 说明文字 response: 读对标牌 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium meaning_response requires performance reference 'response:'"
        )

    def test_target_text_requires_structured_response_reference(self):
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 写下问候 | `none` | `independent` | `direct_task` | `target_text` | 尚待用户作答 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium target_text requires performance reference 'response:'"
        )

    def test_romanization_requires_structured_response_reference(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读转写 | `none` | `independent` | `direct_task` | `romanization` | 用户输入了转写 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium romanization requires performance reference 'response:'"
        )

    def test_audio_requires_file_or_attachment_reference(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | 学习者完整说出目标句 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium audio requires performance reference 'file:' or 'attachment:'"
        )

    def test_audio_reference_prefix_cannot_be_embedded_in_another_key(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | profile:not-an-audio-reference | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium audio requires performance reference 'file:' or 'attachment:'"
        )

    def test_audio_file_reference_requires_existing_local_file(self):
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:audio/missing.wav | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "audio file does not exist")

    def test_audio_file_reference_rejects_directory(self):
        (self.workspace / "audio").mkdir()
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:audio | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "audio path is not a regular file")

    def test_audio_file_reference_rejects_invalid_audio(self):
        path = self.workspace / "audio" / "invalid.wav"
        path.parent.mkdir()
        path.write_text("not audio", encoding="utf-8")
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:audio/invalid.wav | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "audio file failed validation")

    def test_audio_file_reference_accepts_valid_workspace_relative_wav(self):
        self.write_valid_wav(self.workspace / "audio" / "learner.wav")
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:audio/learner.wav verified learner sample | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_audio_file_reference_accepts_valid_absolute_wav(self):
        path = self.workspace / "learner-absolute.wav"
        self.write_valid_wav(path)
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:{path} | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_audio_file_reference_rejects_relative_path_escape(self):
        outside = self.workspace.parent / "outside.wav"
        self.write_valid_wav(outside)
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:../outside.wav | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "relative audio file must stay inside the workspace"
        )

    def test_audio_file_reference_rejects_symlink_escape(self):
        outside = self.workspace.parent / "outside-symlink.wav"
        self.write_valid_wav(outside)
        link = self.workspace / "learner-link.wav"
        link.symlink_to(outside)
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:learner-link.wav | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "relative audio file must stay inside the workspace"
        )

    def test_audio_file_reference_accepts_quoted_path_with_spaces(self):
        path = self.workspace / "audio" / "learner sample.wav"
        self.write_valid_wav(path)
        self.replace(
            "phrase-bank.md",
            "| spoken_production | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| spoken_production | 说出问候 | `none` | `independent` | `direct_task` | `audio` | file:\"audio/learner sample.wav\" | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_action_requires_structured_action_reference(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 现场购票 | `none` | `independent` | `real_world_task` | `action` | 成功买到车票 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium action requires performance reference 'action:'"
        )

    def test_self_report_requires_structured_self_report_reference(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 自主阅读 | `none` | `new` | `self_report` | `self_report` | 用户说读过 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "response medium self_report requires performance reference 'self_report:'"
        )

    def test_structured_response_reference_rejects_placeholder_payload(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 待用户作答 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "response medium meaning_response cannot use unresolved performance reference payload '待用户作答'",
        )

    def test_structured_payload_rejects_embedded_waiting_for_user_answer(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 任务已发送，仍未收到回答 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "performance reference payload still awaits the learner response"
        )

    def test_structured_payload_rejects_still_waiting_for_user_answer_variant(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 音频已备好，仍在等用户回答 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "performance reference payload still awaits the learner response"
        )

    def test_meaning_response_cannot_disguise_self_report_as_original_answer(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 用户自述已经读懂 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "meaning_response performance payload cannot be self-report"
        )

    def test_independent_action_rejects_explicit_full_prompt_claim(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 现场购票 | `none` | `independent` | `real_world_task` | `action` | action: 在完整提示下完成购票 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "independent action payload contradicts prompt level none"
        )

    def test_independent_action_allows_explicit_no_full_prompt_statement(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 现场购票 | `none` | `independent` | `real_world_task` | `action` | action: 未在完整提示下，独立完成购票 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_structured_action_allows_waiting_for_other_person_after_completed_action(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 现场购票 | `none` | `independent` | `real_world_task` | `action` | action: 等待店员回答后成功拿到车票 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_task_may_legitimately_wait_for_another_persons_reply(self):
        self.set_target_script("hangul")
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 询问后等待店员回答 | `none` | `independent` | `simulation` | `target_text` | response: 안녕하세요，成功完成询问与回应 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_substantive_evidence_date_cannot_be_in_the_future(self):
        future = date.today() + timedelta(days=1)
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 读标牌 | `none` | `recognized` | `direct_task` | `meaning_response` | response: 读对含义 | {future.isoformat()} | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "evidence date cannot be later than today")

    def test_substantive_evidence_date_must_be_iso(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `recognized` | `direct_task` | `meaning_response` | response: 读对含义 | 今天 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "evidence date must use ISO YYYY-MM-DD")

    def test_first_learning_date_must_be_iso_when_recorded(self):
        self.replace("phrase-bank.md", "- 首学日期：待填写", "- 首学日期：今天")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "first learning date must use ISO YYYY-MM-DD")

    def test_first_learning_date_cannot_be_in_the_future(self):
        future = date.today() + timedelta(days=1)
        self.replace(
            "phrase-bank.md", "- 首学日期：待填写", f"- 首学日期：{future.isoformat()}"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "first learning date cannot be later than today")

    def test_first_learning_date_requires_matching_lesson_heading(self):
        self.replace("phrase-bank.md", "- 首学日期：待填写", "- 首学日期：2026-08-15")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "first learning date 2026-08-15 has no matching progress.md lesson heading",
        )

    def test_substantive_evidence_requires_substantive_phrase_fields(self):
        self.replace(
            "phrase-bank.md", "- 情境：测试旅行场景", "- 情境：待填写"
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对标牌 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "substantive evidence cannot use unresolved phrase field '情境'",
        )

    def test_substantive_evidence_rejects_unselected_modality_enum(self):
        self.replace(
            "phrase-bank.md", "- 模态：混合", "- 模态：声音／文字／混合／其他"
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对标牌 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "substantive evidence cannot use unresolved phrase field '模态'",
        )

    def test_retained_requires_evidence_after_first_learning_date(self):
        today = date.today()
        self.replace("phrase-bank.md", "- 首学日期：待填写", f"- 首学日期：{today.isoformat()}")
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 延迟读标牌 | `none` | `retained` | `direct_task` | `meaning_response` | response: 延迟任务成功 | {today.isoformat()} | 2026-08-18 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "retained evidence date must be later than first learning date")

    def test_retained_after_first_learning_date_passes(self):
        today = date.today()
        first_learning = today - timedelta(days=1)
        self.set_lesson_date(today.isoformat())
        self.replace(
            "phrase-bank.md", "- 首学日期：待填写", f"- 首学日期：{first_learning.isoformat()}"
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 延迟读标牌 | `none` | `retained` | `direct_task` | `meaning_response` | response: 延迟任务成功 | {today.isoformat()} | 2026-08-18 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_retained_evidence_date_requires_matching_lesson_heading(self):
        today = date.today()
        first_learning = today - timedelta(days=1)
        self.replace(
            "phrase-bank.md", "- 首学日期：待填写", f"- 首学日期：{first_learning.isoformat()}"
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 延迟读标牌 | `none` | `retained` | `direct_task` | `meaning_response` | response: 延迟任务成功 | {today.isoformat()} | 2026-08-18 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            f"evidence date {today.isoformat()} has no matching progress.md lesson heading",
        )

    def test_every_substantive_evidence_date_requires_matching_lesson_heading(self):
        today = date.today()
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对标牌 | {today.isoformat()} | 下次复测 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            f"evidence date {today.isoformat()} has no matching progress.md lesson heading",
        )

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

    def test_tts_native_claim_is_checked_per_source_field(self):
        self.set_complete_tts_source()
        self.replace(
            "phrase-bank.md",
            "- 声音引擎或说话人：系统韩语 TTS 声音",
            "- 声音引擎或说话人：母语者录音",
        )
        self.replace(
            "phrase-bank.md",
            "- 来源支持内容：完整表达的合成声音",
            "- 来源支持内容：TTS 不是母语者录音，只供排练",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "source class tts is presented as a native recording in field '声音引擎或说话人'"
        )

    def test_tts_native_claim_check_covers_every_audio_source_field(self):
        self.set_complete_tts_source()
        self.replace(
            "phrase-bank.md",
            "- 目标变体：韩国标准语",
            "- 目标变体：母语者录音所用变体",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "source class tts is presented as a native recording in field '目标变体'"
        )

    def test_native_tts_claim_is_checked_per_source_field(self):
        self.set_complete_native_source()
        self.replace(
            "phrase-bank.md",
            "- 交付方式：课程内原始音频播放器",
            "- 交付方式：课程内合成语音（TTS）播放器",
        )
        self.replace(
            "phrase-bank.md",
            "- 技术验证：来源文件可解码并已人工播放",
            "- 技术验证：已确认非 TTS",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "synthetic speech is labelled as native_traceable in field '交付方式'"
        )

    def test_native_source_rejects_system_speech_engine_claim(self):
        self.set_complete_native_source()
        self.replace(
            "phrase-bank.md",
            "- 声音引擎或说话人：可追溯母语说话人 A",
            "- 声音引擎或说话人：系统语音引擎",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "synthetic speech is labelled as native_traceable in field '声音引擎或说话人'",
        )

    def test_pronunciation_above_new_rejects_tts_reference_source(self):
        self.set_complete_tts_source()
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| pronunciation | 检查重音 | `none` | `independent` | `direct_task` | `audio` | file:learner-pronunciation.wav | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "pronunciation evidence requires native_official or native_traceable source class"
        )

    def test_pronunciation_above_new_requires_complete_native_source_fields(self):
        self.replace(
            "phrase-bank.md", "- 来源类别：`pending`", "- 来源类别：`native_traceable`"
        )
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| pronunciation | 检查重音 | `none` | `independent` | `direct_task` | `audio` | attachment:pronunciation-001 | 2026-08-16 | 2026-08-17 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "pronunciation evidence cannot use unresolved audio source field '表达与语域核实'"
        )

    def test_pronunciation_with_native_source_and_audio_reference_passes(self):
        self.set_complete_native_source()
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| pronunciation | 检查重音 | `none` | `independent` | `direct_task` | `audio` | attachment:pronunciation-001 | 2026-08-16 | 2026-08-17 |",
        )
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

    def test_progress_requires_travel_mission_map(self):
        self.replace(
            "progress.md",
            "| 任务编号 | 任务域 | 胜利条件 | 证据要求 | 状态 | 最近证据 | 下一变化 |",
            "| 任务 | 任务域 | 胜利条件 | 证据要求 | 状态 | 最近证据 | 下一变化 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "missing table header 任务编号 | 任务域 | 胜利条件")

    def test_progress_requires_a2_style_screen(self):
        self.replace(
            "progress.md",
            "| 筛查编号 | 状态 | 达标任务域 | 能力覆盖 | 现实检查 | 结论 |",
            "| 编号 | 状态 | 达标任务域 | 能力覆盖 | 现实检查 | 结论 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "missing table header 筛查编号 | 状态 | 达标任务域")

    def test_a2_style_screen_requires_exactly_one_a2s01_row(self):
        self.replace(
            "progress.md",
            "| A2S01 | `not_ready` | — | — | — | 只报告单项任务的实际证据阶梯 |",
            "| A2S02 | `not_ready` | — | — | — | 只报告单项任务的实际证据阶梯 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "expected exactly one A2S01 screen row")

    def test_a2_style_screen_status_uses_declared_enum(self):
        self.set_a2_screen("ready")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid A2-style screen state 'ready'")

    def test_a2_not_ready_screen_cannot_claim_summary_or_formal_a2(self):
        self.replace(
            "progress.md",
            "| A2S01 | `not_ready` | — | — | — | 只报告单项任务的实际证据阶梯 |",
            "| A2S01 | `not_ready` | transport | listening | M01 | 正式 A2 已通过 |",
        )
        report = validate_workspace.validate(self.workspace)
        for label in ("达标任务域", "能力覆盖", "现实检查"):
            self.assert_error_contains(
                report, f"A2-style not_ready screen requires placeholder '{label}'"
            )
        self.assert_error_contains(
            report, "A2-style not_ready conclusion must exactly be"
        )

    def test_progress_lesson_date_heading_cannot_be_in_the_future(self):
        future = date.today() + timedelta(days=1)
        self.replace("progress.md", "### 2026-08-16", f"### {future.isoformat()}")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "lesson date heading cannot be later than today")

    def test_progress_lesson_date_heading_allows_a_status_suffix(self):
        self.replace("progress.md", "### 2026-08-16", f"### {date.today().isoformat()}（进行中）")
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对标牌 | {date.today().isoformat()} | 下次复测 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_progress_lesson_section_rejects_non_iso_level_three_heading(self):
        self.replace("progress.md", "### 2026-08-16", "### 第二天")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "lesson heading must start with ISO YYYY-MM-DD")

    def test_mission_ids_must_be_positive_m01_style_and_unique(self):
        self.replace("progress.md", "| M01 | transport |", "| M00 | transport |")
        self.replace("progress.md", "| M02 | lodging |", "| M03 | lodging |")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid mission ID 'M00'")
        self.assert_error_contains(report, "duplicate mission ID M03")

    def test_mission_status_uses_declared_enum(self):
        self.set_mission("M01", "P001:reading:core", "mastered")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid mission state 'mastered'")

    def test_mission_evidence_requirement_uses_exact_three_part_format(self):
        self.set_mission("M01", "P001", "training")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid evidence requirement 'P001'")

    def test_mission_evidence_requirement_phrase_must_exist(self):
        self.set_mission("M01", "P999:reading:core", "training")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "unknown phrase reference P999")

    def test_mission_evidence_requirement_dimension_and_role_use_declared_enums(self):
        self.set_mission(
            "M01", "P001:speaking:main; P001:reading:core", "training"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid evidence requirement dimension 'speaking'")
        self.assert_error_contains(report, "invalid evidence requirement role 'main'")

    def test_duplicate_exact_mission_evidence_requirement_is_rejected(self):
        self.set_mission(
            "M01", "P001:reading:core, P001:reading:core", "training"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "duplicate evidence requirement P001:reading:core")

    def test_one_evidence_row_cannot_fill_multiple_roles_in_same_mission(self):
        self.set_mission(
            "M01", "P001:reading:core, P001:reading:follow_up", "training"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "evidence P001:reading cannot use multiple roles in the same mission",
        )

    def test_passed_mission_requires_core_and_follow_up_or_repair_roles(self):
        self.set_mission("M01", "P001:reading:core", "same_session_passed")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "passed mission requires core plus follow_up or repair evidence requirements"
        )

    def test_passed_mission_rejects_unresolved_summary_cells(self):
        self.replace(
            "progress.md",
            "| M01 | transport | 待用户选择具体任务 | — | `not_selected` | — | — |",
            "| M01 | transport | 待用户选择具体任务 | P001:reading:core, P001:writing:follow_up | `same_session_passed` | — | — |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "passed mission cannot use unresolved '胜利条件'")
        self.assert_error_contains(report, "passed mission cannot use unresolved '最近证据'")
        self.assert_error_contains(report, "passed mission cannot use unresolved '下一变化'")

    def test_same_session_mission_checks_each_exact_requirement(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读站牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对站牌 | 2026-08-16 | 2026-08-17 |",
        )
        self.set_mission(
            "M01",
            "P001:reading:core, P001:interaction:follow_up",
            "same_session_passed",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "requirement P001:interaction:follow_up needs independent evidence or higher",
        )

    def test_changed_condition_mission_checks_each_exact_requirement(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `flexible` | `direct_task` | `meaning_response` | response: 换地点仍读对 | 2026-08-16 | 2026-08-17 |",
        )
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 填写目的地 | `none` | `independent` | `direct_task` | `target_text` | response: 서울역 | 2026-08-16 | 2026-08-17 |",
        )
        self.set_mission(
            "M01", "P001:reading:core; P001:writing:follow_up", "changed_condition_passed"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "requirement P001:writing:follow_up needs flexible evidence or higher"
        )

    def test_delayed_mission_checks_each_exact_requirement(self):
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 延迟读标牌 | `none` | `retained` | `direct_task` | `meaning_response` | response: 隔天仍读对 | 2026-08-16 | 2026-08-17 |",
        )
        self.replace("phrase-bank.md", "- 首学日期：待填写", "- 首学日期：2026-08-15")
        self.set_mission(
            "M01", "P001:reading:core, P001:writing:repair", "delayed_passed"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "requirement P001:writing:repair needs retained evidence"
        )

    def test_valid_same_session_mission_path_passes(self):
        self.set_target_script("hangul")
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读标牌 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对标牌 | 2026-08-16 | 2026-08-17 |",
        )
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| writing | 填写目的地 | `none` | `independent` | `direct_task` | `target_text` | response: 서울역 | 2026-08-16 | 2026-08-17 |",
        )
        self.set_mission(
            "M01", "P001:reading:core; P001:writing:follow_up", "same_session_passed"
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_valid_delayed_mission_path_passes(self):
        today = date.today()
        first_learning = today - timedelta(days=1)
        self.set_target_script("hangul")
        self.set_lesson_date(today.isoformat())
        self.replace(
            "phrase-bank.md", "- 首学日期：待填写", f"- 首学日期：{first_learning.isoformat()}"
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| reading | 延迟读标牌 | `none` | `retained` | `direct_task` | `meaning_response` | response: 延迟任务成功 | {today.isoformat()} | 2026-08-18 |",
        )
        self.replace(
            "phrase-bank.md",
            "| writing | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            f"| writing | 延迟填表 | `none` | `retained` | `direct_task` | `target_text` | response: 서울역 | {today.isoformat()} | 2026-08-18 |",
        )
        self.set_mission(
            "M01", "P001:reading:core, P001:writing:repair", "delayed_passed"
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_field_checked_requires_independent_real_interaction_requirement(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 真人购票 | `full` | `cued` | `real_person` | `action` | action: 在完整提示下完成 | 2026-08-16 | 2026-08-17 |",
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读车票 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对车票 | 2026-08-16 | 2026-08-17 |",
        )
        self.set_mission(
            "M01", "P001:reading:core, P001:interaction:follow_up", "field_checked"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "requirement P001:interaction:follow_up needs independent evidence or higher"
        )

    def test_field_checked_rejects_independent_simulation(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | AI 购票 | `none` | `independent` | `simulation` | `target_text` | response: 完成购票对话 | 2026-08-16 | 2026-08-17 |",
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读车票 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对车票 | 2026-08-16 | 2026-08-17 |",
        )
        self.set_mission(
            "M01", "P001:reading:core, P001:interaction:repair", "field_checked"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "field_checked requires an independent interaction requirement from real_person or real_world_task",
        )

    def test_valid_real_world_field_check_passes(self):
        self.replace(
            "phrase-bank.md",
            "| interaction | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| interaction | 现场购票 | `none` | `independent` | `real_world_task` | `action` | action: 成功买到车票 | 2026-08-16 | 2026-08-17 |",
        )
        self.replace(
            "phrase-bank.md",
            "| reading | 待填写 | `not_applicable` | `new` | `not_applicable` | `not_applicable` | 待填写 | 待填写 | 待填写 |",
            "| reading | 读车票 | `none` | `independent` | `direct_task` | `meaning_response` | response: 读对车票 | 2026-08-16 | 2026-08-17 |",
        )
        self.set_mission(
            "M01", "P001:reading:core, P001:interaction:repair", "field_checked"
        )
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_a2_ready_gate_requires_five_qualifying_travel_domains(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.set_mission_state("M04", "delayed_passed", "training")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style ready state requires at least 5 unique qualifying travel domains"
        )

    def test_a2_ready_gate_counts_only_canonical_travel_domains(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace("progress.md", "| M04 | shopping |", "| M04 | sightseeing |")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style ready state requires at least 5 unique qualifying travel domains"
        )

    def test_a2_ready_gate_requires_communication_repair_domain(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md", "| M06 | communication_repair |", "| M06 | emergency_help |"
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style ready state requires qualifying communication_repair domain"
        )

    def test_a2_ready_gate_requires_repair_role_in_communication_repair_mission(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "P005:spoken_production:core, P005:interaction:repair | `delayed_passed`",
            "P005:spoken_production:core, P005:interaction:follow_up | `delayed_passed`",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "qualifying communication_repair mission requires a repair evidence requirement"
        )

    def test_a2_ready_gate_requires_distinct_core_phrase_per_travel_domain(self):
        self.set_full_retained_evidence_and_ready_missions()
        replacements = (
            ("P002:reading:core", "P001:reading:core"),
            ("P003:interaction:core", "P001:interaction:core"),
            ("P004:writing:core", "P001:writing:core"),
            ("P005:spoken_production:core", "P001:spoken_production:core"),
        )
        for old, new in replacements:
            self.replace("progress.md", old, new)
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "A2-style ready state requires at least 5 qualifying travel domains with distinct core phrase identities",
        )

    def test_a2_ready_gate_rejects_exactly_cloned_core_phrase_identities(self):
        self.set_full_retained_evidence_and_ready_missions()
        for phrase_id in ("P002", "P003", "P004", "P005"):
            self.set_phrase_identity(
                phrase_id, "표현 하나", "完成交通请求", "표현 하나"
            )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "A2-style ready state requires at least 5 qualifying travel domains with distinct core phrase identities",
        )

    def test_a2_ready_gate_normalizes_whitespace_and_invisible_clone_identity(self):
        self.set_full_retained_evidence_and_ready_missions()
        variants = {
            "P002": ("표현  하나", "完成交通请求", "표현  하나"),
            "P003": ("표현\u200b 하나", "完成\u200c交通请求", "표현\u200b 하나"),
            "P004": ("표현\u00a0하나", "完成交通请求", "표현\u00a0하나"),
            "P005": ("표현 하나", "完成交通请求", "표현 하나"),
        }
        for phrase_id, identity in variants.items():
            self.set_phrase_identity(phrase_id, *identity)
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "A2-style ready state requires at least 5 qualifying travel domains with distinct core phrase identities",
        )

    def test_a2_ready_gate_requires_retained_exact_requirement_for_all_dimensions(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "phrase-bank.md",
            "| pronunciation | 延迟旅行任务 | `none` | `retained` |",
            "| pronunciation | 延迟旅行任务 | `none` | `independent` |",
            count=5,
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style ready state missing retained exact requirements for: pronunciation"
        )

    def test_a2_ready_gate_requires_at_least_one_field_checked_mission(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.set_mission_state("M03", "field_checked", "delayed_passed")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style ready state requires at least one field_checked mission"
        )

    def test_a2_ready_gate_requires_substantive_screen_summary(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "| A2S01 | `evidence_consistent_in_tested_tasks` | transport, lodging, eating, shopping, communication_repair | listening, spoken_production, reading, writing, interaction, pronunciation | M03 | 证据与已测试旅行任务中的 A2 风格表现一致；正式 CEFR 未确认 |",
            "| A2S01 | `evidence_consistent_in_tested_tasks` | — | — | — | — |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "A2-style ready screen cannot use unresolved '达标任务域'")
        self.assert_error_contains(report, "A2-style ready screen cannot use unresolved '能力覆盖'")
        self.assert_error_contains(report, "A2-style ready screen cannot use unresolved '现实检查'")
        self.assert_error_contains(report, "A2-style ready screen cannot use unresolved '结论'")

    def test_a2_ready_gate_requires_substantive_profile_fields(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "profile.md",
            "- 可观察的目标：完成测试旅行任务",
            "- 可观察的目标：待填写",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report,
            "A2-style ready state requires substantive profile field '可观察的目标'",
        )

    def test_a2_ready_summary_rejects_unknown_and_nonqualifying_domains(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "transport, lodging, eating, shopping, communication_repair",
            "transport, lodging, eating, basic_help, moon, communication_repair",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style summary travel domain 'basic_help' is not qualifying"
        )
        self.assert_error_contains(
            report, "invalid A2-style summary travel domain 'moon'"
        )

    def test_a2_ready_summary_requires_five_domains_and_communication_repair(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "transport, lodging, eating, shopping, communication_repair",
            "transport; lodging; eating; shopping",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "A2-style summary requires at least 5 unique qualifying travel domains"
        )
        self.assert_error_contains(
            report, "A2-style summary requires communication_repair domain"
        )

    def test_a2_ready_summary_rejects_unknown_and_missing_ability_dimensions(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "listening, spoken_production, reading, writing, interaction, pronunciation",
            "listening; spoken_production; reading; writing; interaction; fluency",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(
            report, "invalid A2-style summary ability dimension 'fluency'"
        )
        self.assert_error_contains(
            report, "A2-style summary missing retained ability dimensions: pronunciation"
        )

    def test_a2_ready_summary_reality_refs_must_be_field_checked(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "| M03 | 证据与已测试旅行任务中的 A2 风格表现一致；正式 CEFR 未确认 |",
            "| M01; M99 | 证据与已测试旅行任务中的 A2 风格表现一致；正式 CEFR 未确认 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "A2-style summary mission M01 is not field_checked")
        self.assert_error_contains(
            report, "unknown A2-style summary mission reference 'M99'"
        )
        self.assert_error_contains(
            report, "A2-style summary requires at least one valid field_checked mission reference"
        )

    def test_a2_ready_summary_rejects_formal_cefr_claim(self):
        self.set_full_retained_evidence_and_ready_missions()
        self.replace(
            "progress.md",
            "| M03 | 证据与已测试旅行任务中的 A2 风格表现一致；正式 CEFR 未确认 |",
            "| M03 | 正式达到 A2 |",
        )
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "A2-style ready conclusion must exactly be")

    def test_valid_a2_style_ready_path_passes(self):
        self.set_full_retained_evidence_and_ready_missions()
        report = validate_workspace.validate(self.workspace)
        self.assertTrue(report.ok, report.errors)

    def test_unknown_phrase_heading_is_not_silently_ignored(self):
        self.replace("phrase-bank.md", "## P001 — 沟通意图", "## Q001 — 沟通意图")
        report = validate_workspace.validate(self.workspace)
        self.assert_error_contains(report, "invalid phrase heading 'Q001'")
        self.assert_error_contains(report, "no valid phrase blocks")

    def test_missing_evidence_table_header_is_reported(self):
        self.replace(
            "phrase-bank.md",
            "| 维度 | 任务 | 提示级别 | 结果 | 证据环境 | 回答媒介 | 表现记录 | 证据日期 | 下次复测 |",
            "| 维度 | 任务 | 提示级别 | 成果 | 证据环境 | 回答媒介 | 表现记录 | 证据日期 | 下次复测 |",
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
