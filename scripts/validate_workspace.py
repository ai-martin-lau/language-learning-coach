#!/usr/bin/env python3
"""Validate a language-learning workspace's Markdown state contract."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import re
import shlex
import sys
import unicodedata

import validate_audio


EXIT_INTERNAL = 1
EXIT_INVALID = 2
EXIT_INPUT = 3

REQUIRED_FILES = (
    "profile.md",
    "phrase-bank.md",
    "progress.md",
    "function-map.md",
)

DIMENSIONS = (
    "listening",
    "spoken_production",
    "reading",
    "writing",
    "interaction",
    "pronunciation",
)
EVIDENCE_ENVIRONMENTS = (
    "direct_task",
    "simulation",
    "real_person",
    "real_world_task",
    "self_report",
    "not_applicable",
)
RESPONSE_MEDIA = (
    "meaning_response",
    "target_text",
    "romanization",
    "audio",
    "action",
    "self_report",
    "not_applicable",
)
TARGET_SCRIPTS = (
    "latin",
    "hangul",
    "japanese",
    "arabic",
    "cyrillic",
    "greek",
    "hebrew",
    "devanagari",
    "thai",
    "han",
    "other",
    "not_applicable",
)
RESULT_STATES = (
    "new",
    "recognized",
    "cued",
    "independent",
    "flexible",
    "retained",
    "not_applicable",
)
PROMPT_LEVELS = ("model", "full", "partial", "intent", "none", "not_applicable")
SOURCE_CLASSES = (
    "native_official",
    "native_traceable",
    "tts",
    "not_applicable",
    "pending",
)
FUNCTION_PRIORITIES = ("now", "later", "not_relevant", "pending")
FUNCTION_STATES = (
    "not_selected",
    "planned",
    "active",
    "evidenced",
    "retested",
    "not_applicable",
)
MISSION_STATES = (
    "planned",
    "training",
    "same_session_passed",
    "changed_condition_passed",
    "delayed_passed",
    "field_checked",
    "not_selected",
)
MISSION_ROLES = ("core", "follow_up", "repair")
ERROR_CATEGORIES = (
    "meaning",
    "form_retrieval",
    "register",
    "script",
    "interaction_repair",
    "pronunciation",
    "other",
)
ERROR_PATTERN_STATES = ("observing", "recurring", "resolved")
MICRO_IMMERSION_STATES = ("off", "on")
A2_SCREEN_STATES = ("not_ready", "evidence_consistent_in_tested_tasks")
A2_READY_CONCLUSION = "证据与已测试任务中的 A2 风格表现一致；正式 CEFR 未确认"
A2_NOT_READY_CONCLUSION = "只报告单项任务的实际证据阶梯"
FOUNDATION_TYPES = (
    "symbol_sound",
    "spelling_sound",
    "stress",
    "connected_speech",
    "form_component",
)
SOUND_FOUNDATION_TYPES = (
    "symbol_sound",
    "spelling_sound",
    "stress",
    "connected_speech",
)
TRANSLITERATION_SUPPORTS = ("full", "partial", "none", "accessibility_required")
FOUNDATION_FADE_TARGETS = {
    "full": ("partial", "none"),
    "partial": ("none",),
    "none": ("none",),
    "accessibility_required": ("accessibility_required", "none"),
}
FOUNDATION_ANCHOR_FIELDS = ("情境", "目标表达", "含义或交际功能")
A2_CORE_DOMAINS = (
    "personal_information",
    "routines_immediate_environment",
    "needs_transactions",
    "time_place_directions",
    "preferences_social_exchange",
    "communication_repair",
    "short_texts_writing",
)

PROFILE_FIELDS = (
    "目标语言",
    "语言变体／地区",
    "主要模态",
    "学习状态",
    "开始日期",
    "可观察的目标",
    "优先情境",
    "期望期限",
    "听力理解",
    "口语产出",
    "阅读",
    "写作",
    "互动",
    "发音",
    "已有学习经历",
    "声音特征",
    "文字系统与转写",
    "目标文字脚本",
    "语法与词形",
    "语域、方言或双言现象",
    "每日最低任务",
    "固定触发点",
    "可立即打开的材料",
    "低动力备用动作",
    "习惯设置状态",
    "可用设备与音频／视频条件",
    "偏好的反馈方式",
    "兴趣主题",
    "可持续产出方式",
    "可接触的人、社群或内容",
    "可行的真人或现实任务检查点",
    "不希望使用的材料或方式",
    "首选权威来源",
    "已确认的发音、拼写或变体规范",
    "尚待核实的问题",
)

PHRASE_FIELDS = (
    "起步功能编号",
    "情境",
    "模态",
    "目标表达",
    "含义或交际功能",
    "学习者自己的版本",
    "可替换槽位",
    "常见回应或追问",
    "沟通修复表达",
    "变体与语域",
    "发音、转写或动作提示",
    "来源类别",
    "表达与语域核实",
    "来源链接或文件",
    "目标变体",
    "声音引擎或说话人",
    "交付方式",
    "来源支持内容",
    "技术验证",
    "首学日期",
    "备注",
)
SUBSTANTIVE_PHRASE_FIELDS = (
    "情境",
    "模态",
    "目标表达",
    "含义或交际功能",
    "学习者自己的版本",
    "变体与语域",
)

AUDIO_SOURCE_FIELDS = (
    "表达与语域核实",
    "来源链接或文件",
    "目标变体",
    "声音引擎或说话人",
    "交付方式",
    "来源支持内容",
    "技术验证",
)

PROGRESS_FIELDS = (
    "到期项目",
    "本次唯一重点",
    "最小完成任务",
    "建议时长",
    "独白／情境预演／短日记",
    "兴趣输入",
    "真人或现实任务检查点",
    "当前检查点证据",
    "微沉浸状态",
    "微沉浸触发与单项动作",
)

EVIDENCE_HEADER = (
    "维度",
    "任务",
    "提示级别",
    "结果",
    "证据环境",
    "回答媒介",
    "表现记录",
    "证据日期",
    "下次复测",
)
FUNCTION_HEADER = ("功能编号", "沟通功能", "本期优先级", "状态", "语块编号", "最近证据", "下一步")
MISSION_HEADER = ("任务编号", "任务域", "胜利条件", "证据要求", "状态", "最近证据", "下一变化")
A2_SCREEN_HEADER = ("筛查编号", "状态", "达标任务域", "能力覆盖", "现实检查", "结论")
RETEST_HEADER = ("编号", "维度", "到期日", "无答案任务", "提示级别", "迁移条件", "安排原因")
ERROR_PATTERN_HEADER = (
    "模式编号",
    "类别",
    "观察日期",
    "关联语块",
    "观察到的问题",
    "下一辨别任务",
    "状态",
)
FOUNDATION_HEADER = (
    "支线编号",
    "类型",
    "学习单位或规律",
    "锚定语块",
    "当前转写支架",
    "首学日期",
    "复测任务",
    "答案可见性",
    "复测转写支架",
    "变化条件",
    "到期日",
)

FIELD_RE = re.compile(r"^\s*-\s+([^：:\n]+?)\s*[：:]\s*(.*?)\s*$")
PHRASE_HEADING_RE = re.compile(r"^##\s+(P\d{3,})\s*(?:[—–-]\s*.*)?$")
POSSIBLE_PHRASE_HEADING_RE = re.compile(r"^##\s+((?:P\S+)|(?:[A-Za-z]\d+))")
FUNCTION_ID_RE = re.compile(r"F(?:0[1-9]|[12]\d|30)\Z")
PHRASE_ID_RE = re.compile(r"P\d{3,}\Z")
MISSION_ID_RE = re.compile(r"M\d{2,}\Z")
ERROR_PATTERN_ID_RE = re.compile(r"E\d{2,}\Z")
FOUNDATION_ID_RE = re.compile(r"S\d{2,}\Z")
TABLE_SEPARATOR_RE = re.compile(r":?-{3,}:?\Z")
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
LESSON_DATE_HEADING_RE = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})(?:\s*.*)?$")
LESSON_SECTION_HEADING = "## 课次记录"
LESSON_TEMPLATE_HEADING = "### YYYY-MM-DD"
PERFORMANCE_REFERENCE_RE = {
    "meaning_response": re.compile(
        r"^response:\s*(?P<payload>\S.*)", flags=re.IGNORECASE
    ),
    "target_text": re.compile(
        r"^response:\s*(?P<payload>\S.*)", flags=re.IGNORECASE
    ),
    "romanization": re.compile(
        r"^response:\s*(?P<payload>\S.*)", flags=re.IGNORECASE
    ),
    "audio": re.compile(
        r"^(?P<kind>file|attachment):\s*(?P<payload>\S.*)",
        flags=re.IGNORECASE,
    ),
    "action": re.compile(
        r"^action:\s*(?P<payload>\S.*)", flags=re.IGNORECASE
    ),
    "self_report": re.compile(
        r"^self_report:\s*(?P<payload>\S.*)", flags=re.IGNORECASE
    ),
}
UNANSWERED_PAYLOAD_RE = re.compile(
    r"等待用户作答|(?:(?:仍|尚)在)?等(?:待)?(?:用户|学习者)(?:作答|回答|回应)|"
    r"仍未收到(?:用户)?回答|awaiting (?:the )?(?:user|learner)(?:'s)? "
    r"(?:answer|response)|(?:user|learner) response (?:not|still not) received",
    flags=re.IGNORECASE,
)
SELF_REPORT_PAYLOAD_RE = re.compile(
    r"自述|自报|self[-_ ]?report(?:ed|s|ing)?", flags=re.IGNORECASE
)
FULL_PROMPT_ACTION_RE = re.compile(
    r"(?<!未)(?<!非)(?<!没有)(?<!不是)在完整提示下|(?<!not )with (?:a )?full prompt",
    flags=re.IGNORECASE,
)

HAN_RANGES = (
    (0x3400, 0x4DBF),
    (0x4E00, 0x9FFF),
    (0xF900, 0xFAFF),
    (0x20000, 0x2FA1F),
)
SCRIPT_RANGES = {
    "latin": ((0x0041, 0x005A), (0x0061, 0x007A), (0x00C0, 0x024F), (0x1E00, 0x1EFF)),
    "hangul": (
        (0x1100, 0x11FF),
        (0x3130, 0x318F),
        (0xA960, 0xA97F),
        (0xAC00, 0xD7AF),
        (0xD7B0, 0xD7FF),
    ),
    "japanese": ((0x3040, 0x30FF), (0x31F0, 0x31FF), (0xFF66, 0xFF9D)) + HAN_RANGES,
    "arabic": ((0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF)),
    "cyrillic": ((0x0400, 0x052F),),
    "greek": ((0x0370, 0x03FF), (0x1F00, 0x1FFF)),
    "hebrew": ((0x0590, 0x05FF),),
    "devanagari": ((0x0900, 0x097F),),
    "thai": ((0x0E00, 0x0E7F),),
    "han": HAN_RANGES,
}

RESULT_RANK = {
    "new": 0,
    "recognized": 1,
    "cued": 2,
    "independent": 3,
    "flexible": 4,
    "retained": 5,
}


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    phrase_count: int = 0
    function_count: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class MarkdownTable:
    header_line: int
    rows: tuple[tuple[int, tuple[str, ...]], ...]


@dataclass(frozen=True)
class EvidenceRecord:
    dimension: str
    result: str
    environment: str


@dataclass(frozen=True)
class PhraseMetadata:
    core_fields: tuple[tuple[str, str], ...]
    source_class: str
    audio_source_fields: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class EvidenceRequirement:
    phrase_id: str
    dimension: str
    role: str

    @property
    def reference(self) -> str:
        return f"{self.phrase_id}:{self.dimension}:{self.role}"


@dataclass(frozen=True)
class MissionRecord:
    mission_id: str
    domain: str
    state: str
    requirements: tuple[EvidenceRequirement, ...]


def clean_value(value: str) -> str:
    """Remove lightweight Markdown code formatting from a scalar value."""

    return value.strip().strip("`").strip()


def markdown_cells(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return tuple(clean_value(cell) for cell in stripped.strip("|").split("|"))


def parse_fields(lines: list[str], start: int = 0, end: int | None = None) -> dict[str, list[tuple[int, str]]]:
    fields: dict[str, list[tuple[int, str]]] = {}
    for index in range(start, len(lines) if end is None else end):
        match = FIELD_RE.match(lines[index])
        if match:
            fields.setdefault(match.group(1).strip(), []).append((index + 1, match.group(2).strip()))
    return fields


def require_fields(
    filename: str,
    fields: dict[str, list[tuple[int, str]]],
    required: tuple[str, ...],
    errors: list[str],
    context: str = "",
) -> None:
    prefix = f"{filename}{':' + context if context else ''}"
    for label in required:
        occurrences = fields.get(label, [])
        if not occurrences:
            errors.append(f"{prefix}: missing field '{label}'")
        elif len(occurrences) > 1:
            lines = ", ".join(str(line) for line, _ in occurrences)
            errors.append(f"{prefix}: duplicate field '{label}' on lines {lines}")


def field_value(fields: dict[str, list[tuple[int, str]]], label: str) -> str:
    occurrences = fields.get(label)
    return clean_value(occurrences[0][1]) if occurrences else ""


def find_table(
    filename: str,
    lines: list[str],
    start: int,
    end: int,
    expected_header: tuple[str, ...],
    errors: list[str],
    context: str,
) -> MarkdownTable | None:
    matches: list[int] = []
    for index in range(start, end):
        if markdown_cells(lines[index]) == expected_header:
            matches.append(index)

    prefix = f"{filename}:{context}"
    if not matches:
        errors.append(f"{prefix}: missing table header {' | '.join(expected_header)}")
        return None
    if len(matches) > 1:
        line_numbers = ", ".join(str(index + 1) for index in matches)
        errors.append(f"{prefix}: duplicate table header on lines {line_numbers}")

    header_index = matches[0]
    row_index = header_index + 1
    separator = markdown_cells(lines[row_index]) if row_index < end else None
    if (
        separator is None
        or len(separator) != len(expected_header)
        or any(not TABLE_SEPARATOR_RE.fullmatch(cell) for cell in separator)
    ):
        errors.append(f"{prefix}: missing or invalid table separator after line {header_index + 1}")
    else:
        row_index += 1

    rows: list[tuple[int, tuple[str, ...]]] = []
    while row_index < end:
        cells = markdown_cells(lines[row_index])
        if cells is None:
            break
        if any(cells):
            rows.append((row_index + 1, cells))
        row_index += 1
    return MarkdownTable(header_index + 1, tuple(rows))


def is_placeholder(value: str) -> bool:
    plain = clean_value(value)
    lowered = plain.casefold()
    if not plain or re.fullmatch(r"[-—–…]+", plain):
        return True
    if lowered in {
        "pending",
        "todo",
        "tbd",
        "unknown",
        "n/a",
        "na",
        "not_applicable",
        "不适用",
        "声音／文字／混合／其他",
        "声音/文字/混合/其他",
    }:
        return True
    return lowered.startswith(
        (
            "待填写",
            "待确认",
            "待用户",
            "待测试",
            "待安排",
            "待复测",
            "待建立",
            "尚待",
            "尚未",
            "未填写",
            "未测试",
            "未安排",
            "yyyy-mm-dd",
            "<",
        )
    )


def parse_iso_date(value: str) -> date | None:
    plain = clean_value(value)
    if not ISO_DATE_RE.fullmatch(plain):
        return None
    try:
        return date.fromisoformat(plain)
    except ValueError:
        return None


def validate_profile(lines: list[str], errors: list[str]) -> tuple[str, dict[str, str]]:
    fields = parse_fields(lines)
    require_fields("profile.md", fields, PROFILE_FIELDS, errors)
    values = {label: field_value(fields, label) for label in PROFILE_FIELDS}
    target_script = field_value(fields, "目标文字脚本")
    if not is_placeholder(target_script) and target_script not in TARGET_SCRIPTS:
        errors.append(
            f"profile.md: invalid target script '{target_script}'; expected one of: "
            f"{', '.join(TARGET_SCRIPTS)}"
        )
    return target_script, values


def validate_lesson_dates(lines: list[str], errors: list[str]) -> set[date]:
    lesson_dates: set[date] = set()
    section_indexes = [index for index, line in enumerate(lines) if line.strip() == LESSON_SECTION_HEADING]
    if not section_indexes:
        errors.append(f"progress.md: missing section '{LESSON_SECTION_HEADING}'")
        return lesson_dates
    if len(section_indexes) > 1:
        line_numbers = ", ".join(str(index + 1) for index in section_indexes)
        errors.append(
            f"progress.md: duplicate section '{LESSON_SECTION_HEADING}' on lines {line_numbers}"
        )

    start = section_indexes[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## ") and not lines[index].startswith("### "):
            end = index
            break

    for index in range(start, end):
        line = lines[index].strip()
        if not line.startswith("### "):
            continue
        if line == LESSON_TEMPLATE_HEADING:
            continue
        match = LESSON_DATE_HEADING_RE.match(line)
        if match is None:
            errors.append(
                f"progress.md: line {index + 1}: lesson heading must start with ISO "
                f"YYYY-MM-DD, found '{clean_value(line[4:])}'"
            )
            continue
        value = clean_value(match.group(1))
        lesson_date = parse_iso_date(value)
        if lesson_date is None:
            errors.append(
                f"progress.md: line {index + 1}: lesson date heading must use ISO YYYY-MM-DD, "
                f"found '{value}'"
            )
        elif lesson_date > date.today():
            errors.append(
                f"progress.md: line {index + 1}: lesson date heading cannot be later than today, "
                f"found '{value}'"
            )
        else:
            lesson_dates.add(lesson_date)
    return lesson_dates


def phrase_blocks(lines: list[str], errors: list[str]) -> list[tuple[str, int, int]]:
    blocks: list[tuple[str, int, int]] = []
    headings: list[tuple[str, int]] = []
    for index, line in enumerate(lines):
        possible = POSSIBLE_PHRASE_HEADING_RE.match(line)
        if not possible:
            continue
        match = PHRASE_HEADING_RE.match(line)
        if not match or int(match.group(1)[1:]) == 0:
            errors.append(
                f"phrase-bank.md: line {index + 1}: invalid phrase heading '{possible.group(1)}'; "
                "expected P001 or higher"
            )
            continue
        headings.append((match.group(1), index))

    seen: dict[str, int] = {}
    for position, (phrase_id, start) in enumerate(headings):
        if phrase_id in seen:
            errors.append(
                f"phrase-bank.md: line {start + 1}: duplicate phrase ID {phrase_id}; "
                f"first seen on line {seen[phrase_id]}"
            )
        else:
            seen[phrase_id] = start + 1
        end = headings[position + 1][1] if position + 1 < len(headings) else len(lines)
        blocks.append((phrase_id, start, end))
    if not blocks:
        errors.append("phrase-bank.md: no valid phrase blocks; expected P001 or higher")
    return blocks


def has_affirmative_claim(value: str, pattern: str, negated_pattern: str) -> bool:
    lowered = clean_value(value).casefold()
    if not re.search(pattern, lowered, flags=re.IGNORECASE):
        return False
    return not re.search(negated_pattern, lowered, flags=re.IGNORECASE)


def validate_source_claims(
    phrase_id: str, fields: dict[str, list[tuple[int, str]]], errors: list[str]
) -> None:
    source_class = field_value(fields, "来源类别")
    if source_class and source_class not in SOURCE_CLASSES:
        errors.append(
            f"phrase-bank.md:{phrase_id}: invalid source class '{source_class}'; "
            f"expected one of: {', '.join(SOURCE_CLASSES)}"
        )
        return

    native_pattern = r"native_official|native_traceable|母语者(?:录音|音频|发音|示范|原声)|真人(?:录音|音频|发音)|native[- ]speaker (?:recording|audio|model|voice)|native (?:recording|audio|model|voice)"
    native_negation = r"不是母语者|并非母语者|非母语者|未由母语者|(?:与|和)母语者.*(?:不同|有别)|不同于母语者|不等于母语者|不能(?:证明|作为|充当).*母语者|不(?:代表|构成).*母语者|not (?:a )?native|different from .*native|cannot (?:prove|establish|serve as).*native"
    tts_pattern = (
        r"\btts\b|合成语音|系统语音(?:引擎)?|语音合成器|"
        r"synthetic (?:speech|voice|audio)|system (?:speech|voice)(?: engine)?|"
        r"voice engine|speech synthesizer"
    )
    tts_negation = r"不是\s*tts|并非\s*tts|非\s*tts|不是合成语音|并非合成语音|not (?:tts|synthetic)"

    for label in AUDIO_SOURCE_FIELDS:
        value = field_value(fields, label)
        if source_class == "tts" and has_affirmative_claim(
            value, native_pattern, native_negation
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: source class tts is presented as a native "
                f"recording in field '{label}'"
            )
        if source_class in {"native_official", "native_traceable"} and has_affirmative_claim(
            value, tts_pattern, tts_negation
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: synthetic speech is labelled as {source_class} "
                f"in field '{label}'"
            )


def payload_contains_script(payload: str, target_script: str) -> bool:
    ranges = SCRIPT_RANGES[target_script]
    for character in unicodedata.normalize("NFKC", payload):
        if not unicodedata.category(character).startswith("L"):
            continue
        codepoint = ord(character)
        if any(start <= codepoint <= end for start, end in ranges):
            return True
    return False


def normalized_phrase_identity(
    fields: dict[str, list[tuple[int, str]]],
) -> tuple[str, str, str]:
    normalized_fields: list[str] = []
    for label in ("目标表达", "含义或交际功能", "学习者自己的版本"):
        normalized = unicodedata.normalize(
            "NFKC", clean_value(field_value(fields, label))
        ).casefold()
        without_format_controls = "".join(
            character
            for character in normalized
            if unicodedata.category(character) != "Cf"
        )
        normalized_fields.append(" ".join(without_format_controls.split()))
    return tuple(normalized_fields)


def phrase_metadata(
    fields: dict[str, list[tuple[int, str]]],
) -> PhraseMetadata:
    return PhraseMetadata(
        core_fields=tuple(
            (label, field_value(fields, label)) for label in FOUNDATION_ANCHOR_FIELDS
        ),
        source_class=field_value(fields, "来源类别"),
        audio_source_fields=tuple(
            (label, field_value(fields, label)) for label in AUDIO_SOURCE_FIELDS
        ),
    )


def validate_audio_file_reference(
    phrase_id: str,
    line_number: int,
    payload: str,
    workspace: Path,
    errors: list[str],
) -> None:
    try:
        parts = shlex.split(payload)
    except ValueError as exc:
        errors.append(
            f"phrase-bank.md:{phrase_id}: line {line_number}: invalid audio file payload: {exc}"
        )
        return
    if not parts:
        errors.append(
            f"phrase-bank.md:{phrase_id}: line {line_number}: audio file payload has no path"
        )
        return

    raw_path = Path(parts[0])
    try:
        workspace_root = workspace.resolve()
        audio_path = (
            raw_path.resolve()
            if raw_path.is_absolute()
            else (workspace_root / raw_path).resolve()
        )
    except (OSError, RuntimeError) as exc:
        errors.append(
            f"phrase-bank.md:{phrase_id}: line {line_number}: audio path cannot be resolved: "
            f"{exc}"
        )
        return
    if not raw_path.is_absolute():
        try:
            audio_path.relative_to(workspace_root)
        except ValueError:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: relative audio file must "
                "stay inside the workspace"
            )
            return

    if not audio_path.exists():
        errors.append(
            f"phrase-bank.md:{phrase_id}: line {line_number}: audio file does not exist: "
            f"{audio_path}"
        )
        return
    if not audio_path.is_file():
        errors.append(
            f"phrase-bank.md:{phrase_id}: line {line_number}: audio path is not a regular file: "
            f"{audio_path}"
        )
        return
    try:
        validate_audio.validate(audio_path)
    except (OSError, NotImplementedError, validate_audio.ValidationError) as exc:
        errors.append(
            f"phrase-bank.md:{phrase_id}: line {line_number}: audio file failed validation: "
            f"{exc}"
        )


def validate_evidence_table(
    phrase_id: str,
    lines: list[str],
    start: int,
    end: int,
    phrase_fields: dict[str, list[tuple[int, str]]],
    workspace: Path,
    target_script: str,
    lesson_dates: set[date],
    errors: list[str],
) -> tuple[EvidenceRecord, ...]:
    table = find_table(
        "phrase-bank.md", lines, start, end, EVIDENCE_HEADER, errors, phrase_id
    )
    if table is None:
        return ()

    seen_dimensions: dict[str, int] = {}
    records: list[EvidenceRecord] = []
    has_substantive_evidence = False
    source_class = field_value(phrase_fields, "来源类别")
    for line_number, cells in table.rows:
        row_error_count = len(errors)
        if len(cells) != len(EVIDENCE_HEADER):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: expected "
                f"{len(EVIDENCE_HEADER)} evidence columns, found {len(cells)}"
            )
            continue
        row = dict(zip(EVIDENCE_HEADER, cells))
        dimension = row["维度"]
        prompt = row["提示级别"]
        result = row["结果"]
        environment = row["证据环境"]
        response_medium = row["回答媒介"]

        dimension_valid = dimension in DIMENSIONS
        if not dimension_valid:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid dimension '{dimension}'; "
                f"expected one of: {', '.join(DIMENSIONS)}"
            )
        elif dimension in seen_dimensions:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: duplicate dimension {dimension}; "
                f"first seen on line {seen_dimensions[dimension]}"
            )
        else:
            seen_dimensions[dimension] = line_number

        if prompt not in PROMPT_LEVELS:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid prompt level '{prompt}'; "
                f"expected one of: {', '.join(PROMPT_LEVELS)}"
            )
        result_valid = result in RESULT_STATES
        if not result_valid:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid result state '{result}'; "
                f"expected one of: {', '.join(RESULT_STATES)}"
            )
        environment_valid = environment in EVIDENCE_ENVIRONMENTS
        if not environment_valid:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid evidence environment "
                f"'{environment}'; expected one of: {', '.join(EVIDENCE_ENVIRONMENTS)}"
            )
        response_medium_valid = response_medium in RESPONSE_MEDIA
        if not response_medium_valid:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid response medium "
                f"'{response_medium}'; expected one of: {', '.join(RESPONSE_MEDIA)}"
            )

        if not result_valid:
            continue

        if result == "not_applicable" and prompt != "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: not_applicable result "
                "requires not_applicable prompt level"
            )
        if result == "recognized" and prompt == "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: recognized result "
                "requires a recorded prompt level"
            )
        if result in {"independent", "flexible", "retained"} and prompt != "none":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: {result} result requires "
                "prompt level none"
            )
        if result == "cued" and prompt in {"none", "not_applicable"}:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: cued result requires an actual prompt"
            )
        if result == "not_applicable" and environment != "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: result not_applicable requires "
                "evidence environment not_applicable"
            )
        if result == "not_applicable" and response_medium != "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: result not_applicable requires "
                "response medium not_applicable"
            )
        if result not in {"new", "not_applicable"} and environment == "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: result {result} requires "
                "a recorded evidence environment"
            )
        if result not in {"new", "not_applicable"} and response_medium == "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: result {result} requires "
                "a recorded response medium"
            )
        if (
            dimension == "interaction"
            and result not in {"new", "not_applicable"}
            and environment not in {"simulation", "real_person", "real_world_task", "self_report"}
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: interaction evidence cannot "
                f"use environment '{environment}'"
            )
        if result == "new" and environment == "not_applicable" and prompt != "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: untested new result requires "
                "prompt level not_applicable"
            )
        if (
            result == "new"
            and environment == "not_applicable"
            and response_medium != "not_applicable"
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: untested new result requires "
                "response medium not_applicable"
            )
        if result == "new" and environment != "not_applicable" and prompt == "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: attempted new result requires "
                "a recorded prompt level"
            )
        if (
            result == "new"
            and environment != "not_applicable"
            and response_medium == "not_applicable"
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: attempted new result requires "
                "a recorded response medium"
            )
        if (
            result not in {"new", "not_applicable"}
            and (environment == "self_report" or response_medium == "self_report")
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: self_report cannot upgrade "
                f"{dimension} above new"
            )
        if (
            dimension in {"spoken_production", "pronunciation"}
            and result not in {"new", "not_applicable"}
            and response_medium != "audio"
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: {dimension} above new requires "
                "response medium audio"
            )
        if (
            dimension == "writing"
            and result not in {"new", "not_applicable"}
            and response_medium != "target_text"
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: writing above new requires "
                "response medium target_text"
            )
        if (
            dimension == "listening"
            and result not in {"new", "not_applicable"}
            and source_class in {"", "pending", "not_applicable"}
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: listening evidence requires "
                "a delivered audio source class"
            )
        if (
            dimension == "pronunciation"
            and result not in {"new", "not_applicable"}
            and source_class not in {"native_official", "native_traceable"}
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: pronunciation evidence "
                "requires native_official or native_traceable source class"
            )
        if dimension in {"listening", "pronunciation"} and result not in {
            "new",
            "not_applicable",
        }:
            for label in AUDIO_SOURCE_FIELDS:
                value = field_value(phrase_fields, label)
                if is_placeholder(value):
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: {dimension} evidence "
                        f"cannot use unresolved audio source field '{label}' value '{value}'"
                    )

        substantive = result not in {"new", "not_applicable"} or (
            result == "new" and environment != "not_applicable"
        )
        if substantive:
            has_substantive_evidence = True
            for column in ("任务", "表现记录", "证据日期", "下次复测"):
                if is_placeholder(row[column]):
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: result {result} "
                        f"cannot use unresolved '{column}' value '{row[column]}'"
                    )
            reference_pattern = PERFORMANCE_REFERENCE_RE.get(response_medium)
            if reference_pattern is not None:
                reference_match = reference_pattern.match(clean_value(row["表现记录"]))
                if reference_match is None:
                    if response_medium == "audio":
                        required_reference = "'file:' or 'attachment:'"
                    else:
                        prefix = (
                            response_medium
                            if response_medium in {"self_report", "action"}
                            else "response"
                        )
                        required_reference = f"'{prefix}:'"
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: response medium "
                        f"{response_medium} requires performance reference {required_reference}"
                    )
                else:
                    payload = reference_match.group("payload").strip()
                    if is_placeholder(payload):
                        errors.append(
                            f"phrase-bank.md:{phrase_id}: line {line_number}: response medium "
                            f"{response_medium} cannot use unresolved performance reference "
                            f"payload '{payload}'"
                        )
                    if UNANSWERED_PAYLOAD_RE.search(payload):
                        errors.append(
                            f"phrase-bank.md:{phrase_id}: line {line_number}: performance "
                            "reference payload still awaits the learner response"
                        )
                    if (
                        response_medium
                        in {"meaning_response", "target_text", "romanization"}
                        and SELF_REPORT_PAYLOAD_RE.search(payload)
                    ):
                        errors.append(
                            f"phrase-bank.md:{phrase_id}: line {line_number}: {response_medium} "
                            "performance payload cannot be self-report"
                        )
                    if (
                        response_medium == "action"
                        and result in {"independent", "flexible", "retained"}
                        and FULL_PROMPT_ACTION_RE.search(payload)
                    ):
                        errors.append(
                            f"phrase-bank.md:{phrase_id}: line {line_number}: {result} action "
                            "payload contradicts prompt level none"
                        )
                    if response_medium == "target_text":
                        if target_script == "not_applicable":
                            errors.append(
                                f"phrase-bank.md:{phrase_id}: line {line_number}: target_text "
                                "evidence cannot use target script not_applicable"
                            )
                        elif is_placeholder(target_script):
                            errors.append(
                                f"phrase-bank.md:{phrase_id}: line {line_number}: target_text "
                                "evidence requires a declared target script"
                            )
                        elif (
                            target_script in SCRIPT_RANGES
                            and not payload_contains_script(payload, target_script)
                        ):
                            errors.append(
                                f"phrase-bank.md:{phrase_id}: line {line_number}: target_text "
                                f"performance payload contains no {target_script} script "
                                "characters"
                            )
                    if (
                        response_medium == "audio"
                        and reference_match.group("kind").casefold() == "file"
                    ):
                        validate_audio_file_reference(
                            phrase_id, line_number, payload, workspace, errors
                        )

            evidence_date = parse_iso_date(row["证据日期"])
            if evidence_date is None:
                errors.append(
                    f"phrase-bank.md:{phrase_id}: line {line_number}: evidence date must use "
                    f"ISO YYYY-MM-DD, found '{row['证据日期']}'"
                )
            elif evidence_date > date.today():
                errors.append(
                    f"phrase-bank.md:{phrase_id}: line {line_number}: evidence date cannot be "
                    f"later than today, found '{row['证据日期']}'"
                )
            elif evidence_date not in lesson_dates:
                errors.append(
                    f"phrase-bank.md:{phrase_id}: line {line_number}: evidence date "
                    f"{evidence_date.isoformat()} has no matching progress.md lesson heading"
                )

            if result == "retained":
                first_learning_value = field_value(phrase_fields, "首学日期")
                first_learning_date = parse_iso_date(first_learning_value)
                if first_learning_date is None:
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: retained result requires "
                        "first learning date in ISO YYYY-MM-DD"
                    )
                elif evidence_date is not None and evidence_date <= first_learning_date:
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: retained evidence date "
                        "must be later than first learning date"
                    )

        if (
            len(errors) == row_error_count
            and dimension_valid
            and result_valid
            and environment_valid
            and response_medium_valid
        ):
            records.append(EvidenceRecord(dimension, result, environment))

    if has_substantive_evidence:
        for label in SUBSTANTIVE_PHRASE_FIELDS:
            value = field_value(phrase_fields, label)
            if is_placeholder(value):
                errors.append(
                    f"phrase-bank.md:{phrase_id}: substantive evidence cannot use unresolved "
                    f"phrase field '{label}' value '{value}'"
                )

    missing_dimensions = [dimension for dimension in DIMENSIONS if dimension not in seen_dimensions]
    if missing_dimensions:
        errors.append(
            f"phrase-bank.md:{phrase_id}: missing evidence dimensions: {', '.join(missing_dimensions)}"
        )
    return tuple(records)


def validate_phrase_bank(
    lines: list[str],
    workspace: Path,
    target_script: str,
    lesson_dates: set[date],
    errors: list[str],
) -> tuple[
    int,
    set[str],
    dict[str, tuple[EvidenceRecord, ...]],
    dict[str, tuple[str, str, str]],
    dict[str, PhraseMetadata],
]:
    blocks = phrase_blocks(lines, errors)
    evidence_by_phrase: dict[str, tuple[EvidenceRecord, ...]] = {}
    phrase_identities: dict[str, tuple[str, str, str]] = {}
    phrase_metadata_by_id: dict[str, PhraseMetadata] = {}
    for phrase_id, start, end in blocks:
        fields = parse_fields(lines, start + 1, end)
        require_fields("phrase-bank.md", fields, PHRASE_FIELDS, errors, phrase_id)
        phrase_identities.setdefault(phrase_id, normalized_phrase_identity(fields))
        phrase_metadata_by_id.setdefault(phrase_id, phrase_metadata(fields))

        function_id = field_value(fields, "起步功能编号")
        if function_id and not is_placeholder(function_id) and function_id != "not_applicable":
            if not FUNCTION_ID_RE.fullmatch(function_id):
                errors.append(
                    f"phrase-bank.md:{phrase_id}: invalid starter function ID '{function_id}'; "
                    "expected F01-F30 or not_applicable"
                )

        first_learning_value = field_value(fields, "首学日期")
        if not is_placeholder(first_learning_value):
            first_learning_date = parse_iso_date(first_learning_value)
            if first_learning_date is None:
                errors.append(
                    f"phrase-bank.md:{phrase_id}: first learning date must use ISO YYYY-MM-DD, "
                    f"found '{first_learning_value}'"
                )
            elif first_learning_date > date.today():
                errors.append(
                    f"phrase-bank.md:{phrase_id}: first learning date cannot be later than today, "
                    f"found '{first_learning_value}'"
                )
            elif first_learning_date not in lesson_dates:
                errors.append(
                    f"phrase-bank.md:{phrase_id}: first learning date "
                    f"{first_learning_date.isoformat()} has no matching progress.md lesson heading"
                )

        validate_source_claims(phrase_id, fields, errors)
        records = validate_evidence_table(
            phrase_id,
            lines,
            start + 1,
            end,
            fields,
            workspace,
            target_script,
            lesson_dates,
            errors,
        )
        evidence_by_phrase[phrase_id] = evidence_by_phrase.get(phrase_id, ()) + records
    return (
        len(blocks),
        {phrase_id for phrase_id, _, _ in blocks},
        evidence_by_phrase,
        phrase_identities,
        phrase_metadata_by_id,
    )


def phrase_references(value: str) -> list[str]:
    if is_placeholder(value):
        return []
    return [part for part in re.split(r"[,，、/\s]+", clean_value(value)) if part]


def validate_function_map(lines: list[str], phrase_ids: set[str], errors: list[str]) -> int:
    table = find_table(
        "function-map.md", lines, 0, len(lines), FUNCTION_HEADER, errors, "function map"
    )
    if table is None:
        return 0

    seen: dict[str, int] = {}
    for line_number, cells in table.rows:
        if len(cells) != len(FUNCTION_HEADER):
            errors.append(
                f"function-map.md: line {line_number}: expected {len(FUNCTION_HEADER)} columns, "
                f"found {len(cells)}"
            )
            continue
        row = dict(zip(FUNCTION_HEADER, cells))
        function_id = row["功能编号"]
        if not FUNCTION_ID_RE.fullmatch(function_id):
            errors.append(
                f"function-map.md: line {line_number}: invalid function ID '{function_id}'; "
                "expected F01-F30"
            )
            continue
        if function_id in seen:
            errors.append(
                f"function-map.md: line {line_number}: duplicate function ID {function_id}; "
                f"first seen on line {seen[function_id]}"
            )
        else:
            seen[function_id] = line_number

        if not row["沟通功能"] or is_placeholder(row["沟通功能"]):
            errors.append(
                f"function-map.md: line {line_number}: function {function_id} has no communicative function"
            )
        if row["本期优先级"] not in FUNCTION_PRIORITIES:
            errors.append(
                f"function-map.md: line {line_number}: invalid priority '{row['本期优先级']}'; "
                f"expected one of: {', '.join(FUNCTION_PRIORITIES)}"
            )
        if row["状态"] not in FUNCTION_STATES:
            errors.append(
                f"function-map.md: line {line_number}: invalid function state '{row['状态']}'; "
                f"expected one of: {', '.join(FUNCTION_STATES)}"
            )
        for phrase_id in phrase_references(row["语块编号"]):
            if not PHRASE_ID_RE.fullmatch(phrase_id):
                errors.append(
                    f"function-map.md: line {line_number}: invalid phrase reference '{phrase_id}'"
                )
            elif phrase_id not in phrase_ids:
                errors.append(
                    f"function-map.md: line {line_number}: unknown phrase reference {phrase_id}"
                )

    expected_ids = [f"F{number:02d}" for number in range(1, 31)]
    missing = [function_id for function_id in expected_ids if function_id not in seen]
    if missing:
        errors.append(f"function-map.md: missing function IDs: {', '.join(missing)}")
    return len(seen)


def parse_evidence_requirements(
    value: str,
    line_number: int,
    phrase_ids: set[str],
    errors: list[str],
) -> tuple[EvidenceRequirement, ...]:
    if is_placeholder(value):
        return ()

    requirements: list[EvidenceRequirement] = []
    seen_references: set[str] = set()
    seen_evidence: set[tuple[str, str]] = set()
    for token in (
        part.strip()
        for part in re.split(r"[,，;；]+", clean_value(value))
        if part.strip()
    ):
        parts = tuple(part.strip() for part in token.split(":"))
        if len(parts) != 3 or any(not part for part in parts):
            errors.append(
                f"progress.md: line {line_number}: invalid evidence requirement '{token}'; "
                "expected P001:dimension:role"
            )
            continue
        phrase_id, dimension, role = parts
        valid = True
        if not PHRASE_ID_RE.fullmatch(phrase_id):
            errors.append(
                f"progress.md: line {line_number}: invalid phrase reference '{phrase_id}'"
            )
            valid = False
        elif phrase_id not in phrase_ids:
            errors.append(f"progress.md: line {line_number}: unknown phrase reference {phrase_id}")
            valid = False
        if dimension not in DIMENSIONS:
            errors.append(
                f"progress.md: line {line_number}: invalid evidence requirement dimension "
                f"'{dimension}'; expected one of: {', '.join(DIMENSIONS)}"
            )
            valid = False
        if role not in MISSION_ROLES:
            errors.append(
                f"progress.md: line {line_number}: invalid evidence requirement role '{role}'; "
                f"expected one of: {', '.join(MISSION_ROLES)}"
            )
            valid = False
        if not valid:
            continue

        requirement = EvidenceRequirement(phrase_id, dimension, role)
        if requirement.reference in seen_references:
            errors.append(
                f"progress.md: line {line_number}: duplicate evidence requirement "
                f"{requirement.reference}"
            )
            continue
        evidence_key = (phrase_id, dimension)
        if evidence_key in seen_evidence:
            errors.append(
                f"progress.md: line {line_number}: evidence {phrase_id}:{dimension} cannot "
                "use multiple roles in the same mission"
            )
            continue
        seen_references.add(requirement.reference)
        seen_evidence.add(evidence_key)
        requirements.append(requirement)
    return tuple(requirements)


def evidence_for_requirement(
    requirement: EvidenceRequirement,
    evidence_by_phrase: dict[str, tuple[EvidenceRecord, ...]],
) -> EvidenceRecord | None:
    return next(
        (
            record
            for record in evidence_by_phrase.get(requirement.phrase_id, ())
            if record.dimension == requirement.dimension
        ),
        None,
    )


def validate_mission_map(
    lines: list[str],
    phrase_ids: set[str],
    evidence_by_phrase: dict[str, tuple[EvidenceRecord, ...]],
    errors: list[str],
) -> tuple[MissionRecord, ...]:
    table = find_table(
        "progress.md", lines, 0, len(lines), MISSION_HEADER, errors, "A2 task map"
    )
    if table is None:
        return ()
    if not table.rows:
        errors.append("progress.md:A2 task map: must contain at least one mission row")
        return ()

    seen: dict[str, int] = {}
    mission_records: list[MissionRecord] = []
    passed_states = {
        "same_session_passed",
        "changed_condition_passed",
        "delayed_passed",
        "field_checked",
    }
    for line_number, cells in table.rows:
        if len(cells) != len(MISSION_HEADER):
            errors.append(
                f"progress.md: line {line_number}: expected {len(MISSION_HEADER)} mission columns, "
                f"found {len(cells)}"
            )
            continue
        row = dict(zip(MISSION_HEADER, cells))
        mission_id = row["任务编号"]
        mission_id_valid = bool(MISSION_ID_RE.fullmatch(mission_id)) and int(mission_id[1:]) > 0
        if not mission_id_valid:
            errors.append(
                f"progress.md: line {line_number}: invalid mission ID '{mission_id}'; "
                "expected M01 or higher"
            )
        elif mission_id in seen:
            errors.append(
                f"progress.md: line {line_number}: duplicate mission ID {mission_id}; "
                f"first seen on line {seen[mission_id]}"
            )
        else:
            seen[mission_id] = line_number

        state = row["状态"]
        if state not in MISSION_STATES:
            errors.append(
                f"progress.md: line {line_number}: invalid mission state '{state}'; "
                f"expected one of: {', '.join(MISSION_STATES)}"
            )

        requirements = parse_evidence_requirements(
            row["证据要求"], line_number, phrase_ids, errors
        )
        if state in passed_states:
            for label in ("任务域", "胜利条件", "最近证据", "下一变化"):
                if is_placeholder(row[label]):
                    errors.append(
                        f"progress.md: line {line_number}: passed mission cannot use unresolved "
                        f"'{label}' value '{row[label]}'"
                    )
            roles = {requirement.role for requirement in requirements}
            if "core" not in roles or not roles.intersection({"follow_up", "repair"}):
                errors.append(
                    f"progress.md: line {line_number}: passed mission requires core plus "
                    "follow_up or repair evidence requirements"
                )

        required_result = {
            "same_session_passed": "independent",
            "changed_condition_passed": "flexible",
            "delayed_passed": "retained",
            "field_checked": "independent",
        }.get(state)
        if required_result is not None:
            for requirement in requirements:
                record = evidence_for_requirement(requirement, evidence_by_phrase)
                if record is None or RESULT_RANK.get(record.result, -1) < RESULT_RANK[required_result]:
                    qualifier = " or higher" if required_result != "retained" else ""
                    errors.append(
                        f"progress.md: line {line_number}: requirement {requirement.reference} "
                        f"needs {required_result} evidence{qualifier}"
                    )

        if state == "field_checked" and not any(
            requirement.dimension == "interaction"
            and (record := evidence_for_requirement(requirement, evidence_by_phrase)) is not None
            and RESULT_RANK.get(record.result, -1) >= RESULT_RANK["independent"]
            and record.environment in {"real_person", "real_world_task"}
            for requirement in requirements
        ):
            errors.append(
                f"progress.md: line {line_number}: mission {mission_id} state field_checked "
                "requires an independent interaction requirement from real_person or real_world_task"
            )

        if mission_id_valid and state in MISSION_STATES:
            mission_records.append(
                MissionRecord(mission_id, row["任务域"], state, requirements)
            )
    return tuple(mission_records)


def validate_a2_style_screen(
    lines: list[str],
    missions: tuple[MissionRecord, ...],
    evidence_by_phrase: dict[str, tuple[EvidenceRecord, ...]],
    phrase_identities: dict[str, tuple[str, str, str]],
    profile_values: dict[str, str],
    errors: list[str],
) -> None:
    table = find_table(
        "progress.md", lines, 0, len(lines), A2_SCREEN_HEADER, errors, "A2-style screen"
    )
    if table is None:
        return
    if len(table.rows) != 1 or table.rows[0][1][0] != "A2S01":
        errors.append("progress.md:A2-style screen: expected exactly one A2S01 screen row")
        return

    line_number, cells = table.rows[0]
    if len(cells) != len(A2_SCREEN_HEADER):
        errors.append(
            f"progress.md: line {line_number}: expected {len(A2_SCREEN_HEADER)} A2-style "
            f"screen columns, found {len(cells)}"
        )
        return
    row = dict(zip(A2_SCREEN_HEADER, cells))
    state = row["状态"]
    if state not in A2_SCREEN_STATES:
        errors.append(
            f"progress.md: line {line_number}: invalid A2-style screen state '{state}'; "
            f"expected one of: {', '.join(A2_SCREEN_STATES)}"
        )
        return
    if state == "not_ready":
        for label in ("达标任务域", "能力覆盖", "现实检查"):
            if not is_placeholder(row[label]):
                errors.append(
                    f"progress.md: line {line_number}: A2-style not_ready screen requires "
                    f"placeholder '{label}', found '{row[label]}'"
                )
        if row["结论"] != A2_NOT_READY_CONCLUSION:
            errors.append(
                f"progress.md: line {line_number}: A2-style not_ready conclusion must exactly "
                f"be '{A2_NOT_READY_CONCLUSION}'"
            )
        return

    for label in ("目标语言", "语言变体／地区", "可观察的目标", "优先情境"):
        value = profile_values.get(label, "")
        if is_placeholder(value):
            errors.append(
                "progress.md:A2-style screen: A2-style ready state requires substantive "
                f"profile field '{label}'"
            )

    for label in ("达标任务域", "能力覆盖", "现实检查", "结论"):
        if is_placeholder(row[label]):
            errors.append(
                f"progress.md: line {line_number}: A2-style ready screen cannot use "
                f"unresolved '{label}' value '{row[label]}'"
            )
    if row["结论"] != A2_READY_CONCLUSION:
        errors.append(
            f"progress.md: line {line_number}: A2-style ready conclusion must exactly be "
            f"'{A2_READY_CONCLUSION}'"
        )

    qualifying = tuple(
        mission
        for mission in missions
        if mission.state in {"delayed_passed", "field_checked"}
        and mission.domain in A2_CORE_DOMAINS
    )
    domains = {mission.domain for mission in qualifying}
    if len(domains) < 5:
        errors.append(
            "progress.md:A2-style screen: A2-style ready state requires at least 5 unique "
            "qualifying A2 core domains"
        )
    if "communication_repair" not in domains:
        errors.append(
            "progress.md:A2-style screen: A2-style ready state requires qualifying "
            "communication_repair domain"
        )
    elif not any(
        requirement.role == "repair"
        for mission in qualifying
        if mission.domain == "communication_repair"
        for requirement in mission.requirements
    ):
        errors.append(
            "progress.md:A2-style screen: qualifying communication_repair mission requires "
            "a repair evidence requirement"
        )
    if not any(mission.state == "field_checked" for mission in qualifying):
        errors.append(
            "progress.md:A2-style screen: A2-style ready state requires at least one "
            "field_checked mission"
        )

    def summary_items(label: str) -> tuple[str, ...]:
        value = row[label]
        if is_placeholder(value):
            return ()
        items = tuple(
            item.strip()
            for item in re.split(r"[,，;；]+", clean_value(value))
            if item.strip()
        )
        duplicates = sorted({item for item in items if items.count(item) > 1})
        if duplicates:
            errors.append(
                f"progress.md: line {line_number}: A2-style summary '{label}' contains "
                f"duplicate items: {', '.join(duplicates)}"
            )
        return items

    summary_domains = summary_items("达标任务域")
    valid_summary_domains: set[str] = set()
    for domain in summary_domains:
        if domain not in A2_CORE_DOMAINS:
            errors.append(
                f"progress.md: line {line_number}: invalid A2-style summary core domain "
                f"'{domain}'"
            )
        elif domain not in domains:
            errors.append(
                f"progress.md: line {line_number}: A2-style summary core domain '{domain}' "
                "is not qualifying"
            )
        else:
            valid_summary_domains.add(domain)
    if len(valid_summary_domains) < 5:
        errors.append(
            "progress.md:A2-style screen: A2-style summary requires at least 5 unique "
            "qualifying A2 core domains"
        )
    if "communication_repair" not in valid_summary_domains:
        errors.append(
            "progress.md:A2-style screen: A2-style summary requires communication_repair domain"
        )

    core_phrase_identities_by_domain: dict[str, set[tuple[str, str, str]]] = {}
    for mission in qualifying:
        core_phrase_identities_by_domain.setdefault(mission.domain, set()).update(
            phrase_identities[requirement.phrase_id]
            for requirement in mission.requirements
            if requirement.role == "core"
            and requirement.phrase_id in phrase_identities
        )
    matched_core_phrase_identities: dict[tuple[str, str, str], str] = {}

    def assign_distinct_core(
        domain: str, visited: set[tuple[str, str, str]]
    ) -> bool:
        for identity in core_phrase_identities_by_domain.get(domain, set()):
            if identity in visited:
                continue
            visited.add(identity)
            current_domain = matched_core_phrase_identities.get(identity)
            if current_domain is None:
                matched_core_phrase_identities[identity] = domain
                return True
            if assign_distinct_core(current_domain, visited):
                matched_core_phrase_identities[identity] = domain
                return True
        return False

    distinct_core_assignments = sum(
        assign_distinct_core(domain, set())
        for domain in core_phrase_identities_by_domain
    )
    if distinct_core_assignments < 5:
        errors.append(
            "progress.md:A2-style screen: A2-style ready state requires at least 5 "
            "qualifying A2 core domains with distinct core phrase identities"
        )

    retained_dimensions: set[str] = set()
    for mission in qualifying:
        for requirement in mission.requirements:
            record = evidence_for_requirement(requirement, evidence_by_phrase)
            if record is not None and record.result == "retained":
                retained_dimensions.add(requirement.dimension)
    missing_dimensions = [
        dimension for dimension in DIMENSIONS if dimension not in retained_dimensions
    ]
    if missing_dimensions:
        errors.append(
            "progress.md:A2-style screen: A2-style ready state missing retained exact "
            f"requirements for: {', '.join(missing_dimensions)}"
        )

    summary_dimensions = summary_items("能力覆盖")
    valid_summary_dimensions: set[str] = set()
    for dimension in summary_dimensions:
        if dimension not in DIMENSIONS:
            errors.append(
                f"progress.md: line {line_number}: invalid A2-style summary ability "
                f"dimension '{dimension}'"
            )
        elif dimension not in retained_dimensions:
            errors.append(
                f"progress.md: line {line_number}: A2-style summary ability dimension "
                f"'{dimension}' has no retained exact requirement"
            )
        else:
            valid_summary_dimensions.add(dimension)
    missing_summary_dimensions = [
        dimension for dimension in DIMENSIONS if dimension not in valid_summary_dimensions
    ]
    if missing_summary_dimensions:
        errors.append(
            "progress.md:A2-style screen: A2-style summary missing retained ability "
            f"dimensions: {', '.join(missing_summary_dimensions)}"
        )

    missions_by_id = {mission.mission_id: mission for mission in missions}
    valid_field_checks: set[str] = set()
    for mission_id in summary_items("现实检查"):
        if not MISSION_ID_RE.fullmatch(mission_id) or mission_id not in missions_by_id:
            errors.append(
                f"progress.md: line {line_number}: unknown A2-style summary mission "
                f"reference '{mission_id}'"
            )
        elif missions_by_id[mission_id].state != "field_checked":
            errors.append(
                f"progress.md: line {line_number}: A2-style summary mission {mission_id} "
                "is not field_checked"
            )
        else:
            valid_field_checks.add(mission_id)
    if not valid_field_checks:
        errors.append(
            "progress.md:A2-style screen: A2-style summary requires at least one valid "
            "field_checked mission reference"
        )


def validate_sound_script_foundation(
    lines: list[str],
    target_script: str,
    phrase_metadata_by_id: dict[str, PhraseMetadata],
    lesson_dates: set[date],
    errors: list[str],
) -> None:
    table = find_table(
        "progress.md",
        lines,
        0,
        len(lines),
        FOUNDATION_HEADER,
        errors,
        "sound-script foundation",
    )
    if table is None:
        return
    if table.rows and is_placeholder(target_script):
        errors.append(
            "progress.md:sound-script foundation: unresolved or not_applicable target "
            "script cannot contain foundation rows"
        )

    seen_ids: dict[str, int] = {}
    for line_number, cells in table.rows:
        if len(cells) != len(FOUNDATION_HEADER):
            errors.append(
                f"progress.md: line {line_number}: expected {len(FOUNDATION_HEADER)} "
                f"foundation columns, found {len(cells)}"
            )
            continue
        row = dict(zip(FOUNDATION_HEADER, cells))

        foundation_id = row["支线编号"]
        foundation_id_valid = bool(FOUNDATION_ID_RE.fullmatch(foundation_id)) and int(
            foundation_id[1:]
        ) > 0
        if not foundation_id_valid:
            errors.append(
                f"progress.md: line {line_number}: invalid foundation ID "
                f"'{foundation_id}'; expected S01 or higher"
            )
        elif foundation_id in seen_ids:
            errors.append(
                f"progress.md: line {line_number}: duplicate foundation ID "
                f"{foundation_id}; first seen on line {seen_ids[foundation_id]}"
            )
        else:
            seen_ids[foundation_id] = line_number

        foundation_type = row["类型"]
        if foundation_type not in FOUNDATION_TYPES:
            errors.append(
                f"progress.md: line {line_number}: invalid foundation type "
                f"'{foundation_type}'; expected one of: {', '.join(FOUNDATION_TYPES)}"
            )

        learning_units = row["学习单位或规律"]
        if is_placeholder(learning_units):
            errors.append(
                f"progress.md: line {line_number}: foundation item has unresolved learning "
                f"units or rule '{learning_units}'"
            )
        else:
            units = tuple(part.strip() for part in re.split(r"[;；]", learning_units))
            if any(not unit for unit in units):
                errors.append(
                    f"progress.md: line {line_number}: foundation item has an empty "
                    "semicolon-separated learning unit"
                )
            if len(units) > 5:
                errors.append(
                    f"progress.md: line {line_number}: foundation item may contain at most "
                    "5 semicolon-separated learning units"
                )
            if any(unit and is_placeholder(unit) for unit in units):
                errors.append(
                    f"progress.md: line {line_number}: foundation item has unresolved "
                    f"learning units or rule '{learning_units}'"
                )

        phrase_id = row["锚定语块"]
        if not PHRASE_ID_RE.fullmatch(phrase_id):
            errors.append(
                f"progress.md: line {line_number}: foundation anchor must be exactly one "
                f"phrase ID, found '{phrase_id}'"
            )
        elif phrase_id not in phrase_metadata_by_id:
            errors.append(
                f"progress.md: line {line_number}: unknown phrase reference {phrase_id}"
            )
        else:
            metadata = phrase_metadata_by_id[phrase_id]
            for label, value in metadata.core_fields:
                if is_placeholder(value):
                    errors.append(
                        f"progress.md: line {line_number}: foundation anchor {phrase_id} "
                        f"has unresolved phrase field '{label}'"
                    )
            if foundation_type in SOUND_FOUNDATION_TYPES:
                missing_audio_fields = [
                    label
                    for label, value in metadata.audio_source_fields
                    if is_placeholder(value)
                ]
                if metadata.source_class not in {
                    "native_official",
                    "native_traceable",
                    "tts",
                } or missing_audio_fields:
                    detail = ", ".join(missing_audio_fields) or "来源类别"
                    errors.append(
                        f"progress.md: line {line_number}: {foundation_type} anchor "
                        f"{phrase_id} requires a complete traceable audio source; "
                        f"unresolved or undelivered: {detail}"
                    )

        current_transliteration = row["当前转写支架"]
        current_transliteration_valid = (
            current_transliteration in TRANSLITERATION_SUPPORTS
        )
        if not current_transliteration_valid:
            errors.append(
                f"progress.md: line {line_number}: invalid transliteration support "
                f"'{current_transliteration}'; expected one of: "
                f"{', '.join(TRANSLITERATION_SUPPORTS)}"
            )

        first_learning_value = row["首学日期"]
        first_learning_date = parse_iso_date(first_learning_value)
        if first_learning_date is None:
            errors.append(
                f"progress.md: line {line_number}: foundation first learning date must use "
                f"ISO YYYY-MM-DD, found '{first_learning_value}'"
            )
        elif first_learning_date > date.today():
            errors.append(
                f"progress.md: line {line_number}: foundation first learning date cannot be "
                f"in the future, found '{first_learning_value}'"
            )
        elif first_learning_date not in lesson_dates:
            errors.append(
                f"progress.md: line {line_number}: foundation first learning date "
                f"{first_learning_date.isoformat()} has no matching progress.md lesson heading"
            )

        retest_task = row["复测任务"]
        if is_placeholder(retest_task):
            errors.append(
                f"progress.md: line {line_number}: foundation retest cannot use unresolved "
                f"value '{retest_task}'"
            )

        answer_visibility = row["答案可见性"]
        if answer_visibility != "hidden":
            errors.append(
                f"progress.md: line {line_number}: foundation answer visibility must be "
                f"hidden, found '{answer_visibility}'"
            )

        retest_transliteration = row["复测转写支架"]
        retest_transliteration_valid = (
            retest_transliteration in TRANSLITERATION_SUPPORTS
        )
        if not retest_transliteration_valid:
            errors.append(
                f"progress.md: line {line_number}: invalid retest transliteration support "
                f"'{retest_transliteration}'; expected one of: "
                f"{', '.join(TRANSLITERATION_SUPPORTS)}"
            )
        elif (
            current_transliteration_valid
            and retest_transliteration
            not in FOUNDATION_FADE_TARGETS[current_transliteration]
        ):
            errors.append(
                f"progress.md: line {line_number}: retest transliteration "
                f"'{retest_transliteration}' does not fade current support "
                f"'{current_transliteration}'"
            )

        change_condition = row["变化条件"]
        if is_placeholder(change_condition):
            errors.append(
                f"progress.md: line {line_number}: foundation change condition cannot be "
                f"unresolved, found '{change_condition}'"
            )

        due_value = row["到期日"]
        due_date = parse_iso_date(due_value)
        if due_date is None:
            errors.append(
                f"progress.md: line {line_number}: foundation due date must use ISO "
                f"YYYY-MM-DD, found '{due_value}'"
            )
        elif first_learning_date is not None and due_date <= first_learning_date:
            errors.append(
                f"progress.md: line {line_number}: foundation due date must be later than "
                "first learning date"
            )


def validate_progress(
    lines: list[str],
    phrase_ids: set[str],
    phrase_metadata_by_id: dict[str, PhraseMetadata],
    evidence_by_phrase: dict[str, tuple[EvidenceRecord, ...]],
    phrase_identities: dict[str, tuple[str, str, str]],
    target_script: str,
    profile_values: dict[str, str],
    lesson_dates: set[date],
    errors: list[str],
) -> None:
    fields = parse_fields(lines)
    require_fields("progress.md", fields, PROGRESS_FIELDS, errors)
    if lesson_dates:
        for label in ("本次唯一重点", "最小完成任务"):
            if is_placeholder(field_value(fields, label)):
                errors.append(
                    f"progress.md: started workspace requires substantive '{label}'"
                )

    micro_immersion_status = field_value(fields, "微沉浸状态")
    if micro_immersion_status not in MICRO_IMMERSION_STATES:
        errors.append(
            "progress.md: invalid micro-immersion status "
            f"'{micro_immersion_status}'; expected one of: "
            f"{', '.join(MICRO_IMMERSION_STATES)}"
        )
    elif micro_immersion_status == "on" and is_placeholder(
        field_value(fields, "微沉浸触发与单项动作")
    ):
        errors.append(
            "progress.md: enabled micro-immersion requires a concrete trigger and action"
        )

    validate_sound_script_foundation(
        lines,
        target_script,
        phrase_metadata_by_id,
        lesson_dates,
        errors,
    )

    missions = validate_mission_map(lines, phrase_ids, evidence_by_phrase, errors)
    validate_a2_style_screen(
        lines,
        missions,
        evidence_by_phrase,
        phrase_identities,
        profile_values,
        errors,
    )
    error_table = find_table(
        "progress.md",
        lines,
        0,
        len(lines),
        ERROR_PATTERN_HEADER,
        errors,
        "recurring error queue",
    )
    if error_table is not None:
        seen_pattern_ids: dict[str, int] = {}
        for line_number, cells in error_table.rows:
            if len(cells) != len(ERROR_PATTERN_HEADER):
                errors.append(
                    f"progress.md: line {line_number}: expected "
                    f"{len(ERROR_PATTERN_HEADER)} recurring error columns, found {len(cells)}"
                )
                continue
            row = dict(zip(ERROR_PATTERN_HEADER, cells))
            pattern_id = row["模式编号"]
            pattern_id_valid = bool(ERROR_PATTERN_ID_RE.fullmatch(pattern_id)) and int(
                pattern_id[1:]
            ) > 0
            if not pattern_id_valid:
                errors.append(
                    f"progress.md: line {line_number}: invalid error pattern ID "
                    f"'{pattern_id}'; expected E01 or higher"
                )
            elif pattern_id in seen_pattern_ids:
                errors.append(
                    f"progress.md: line {line_number}: duplicate error pattern ID "
                    f"{pattern_id}; first seen on line {seen_pattern_ids[pattern_id]}"
                )
            else:
                seen_pattern_ids[pattern_id] = line_number

            category = row["类别"]
            if category not in ERROR_CATEGORIES:
                errors.append(
                    f"progress.md: line {line_number}: invalid error category "
                    f"'{category}'; expected one of: {', '.join(ERROR_CATEGORIES)}"
                )
            state = row["状态"]
            if state not in ERROR_PATTERN_STATES:
                errors.append(
                    f"progress.md: line {line_number}: invalid error pattern state "
                    f"'{state}'; expected one of: {', '.join(ERROR_PATTERN_STATES)}"
                )

            for label in ("观察到的问题", "下一辨别任务"):
                if is_placeholder(row[label]):
                    errors.append(
                        f"progress.md: line {line_number}: error pattern cannot use "
                        f"unresolved '{label}' value '{row[label]}'"
                    )

            raw_dates = (
                ()
                if is_placeholder(row["观察日期"])
                else tuple(
                    item.strip()
                    for item in re.split(r"[,，;；]+", row["观察日期"])
                    if item.strip()
                )
            )
            parsed_dates: list[date] = []
            seen_dates: set[date] = set()
            for raw_date in raw_dates:
                observation_date = parse_iso_date(raw_date)
                if observation_date is None:
                    errors.append(
                        f"progress.md: line {line_number}: invalid observation date "
                        f"'{raw_date}'; expected YYYY-MM-DD"
                    )
                    continue
                if observation_date in seen_dates:
                    errors.append(
                        f"progress.md: line {line_number}: duplicate observation date "
                        f"{observation_date.isoformat()}"
                    )
                    continue
                seen_dates.add(observation_date)
                parsed_dates.append(observation_date)
                if observation_date > date.today():
                    errors.append(
                        f"progress.md: line {line_number}: observation date "
                        f"{observation_date.isoformat()} cannot be in the future"
                    )
                if observation_date not in lesson_dates:
                    errors.append(
                        f"progress.md: line {line_number}: observation date "
                        f"{observation_date.isoformat()} has no matching lesson heading"
                    )
            if not raw_dates:
                errors.append(
                    f"progress.md: line {line_number}: error pattern requires at least one "
                    "observation date"
                )
            if state in {"recurring", "resolved"} and len(parsed_dates) < 2:
                errors.append(
                    f"progress.md: line {line_number}: {state} state requires at least 2 "
                    "distinct lesson dates"
                )

            raw_phrase_ids = (
                ()
                if is_placeholder(row["关联语块"])
                else tuple(
                    item.strip()
                    for item in re.split(r"[,，;；]+", row["关联语块"])
                    if item.strip()
                )
            )
            if not raw_phrase_ids:
                errors.append(
                    f"progress.md: line {line_number}: error pattern requires at least one "
                    "phrase reference"
                )
            for phrase_id in raw_phrase_ids:
                if not PHRASE_ID_RE.fullmatch(phrase_id):
                    errors.append(
                        f"progress.md: line {line_number}: invalid phrase reference "
                        f"'{phrase_id}'"
                    )
                elif phrase_id not in phrase_ids:
                    errors.append(
                        f"progress.md: line {line_number}: unknown phrase reference {phrase_id}"
                    )

    table = find_table(
        "progress.md", lines, 0, len(lines), RETEST_HEADER, errors, "retest queue"
    )
    if table is None:
        return
    for line_number, cells in table.rows:
        if len(cells) != len(RETEST_HEADER):
            errors.append(
                f"progress.md: line {line_number}: expected {len(RETEST_HEADER)} retest columns, "
                f"found {len(cells)}"
            )
            continue
        row = dict(zip(RETEST_HEADER, cells))
        phrase_id = row["编号"]
        if not is_placeholder(phrase_id):
            if not PHRASE_ID_RE.fullmatch(phrase_id):
                errors.append(
                    f"progress.md: line {line_number}: invalid phrase reference '{phrase_id}'"
                )
            elif phrase_id not in phrase_ids:
                errors.append(
                    f"progress.md: line {line_number}: unknown phrase reference {phrase_id}"
                )
        if row["维度"] not in DIMENSIONS:
            errors.append(
                f"progress.md: line {line_number}: invalid dimension '{row['维度']}'; "
                f"expected one of: {', '.join(DIMENSIONS)}"
            )
        if row["提示级别"] not in PROMPT_LEVELS:
            errors.append(
                f"progress.md: line {line_number}: invalid prompt level '{row['提示级别']}'; "
                f"expected one of: {', '.join(PROMPT_LEVELS)}"
            )


def validate(workspace: Path) -> ValidationReport:
    if not workspace.exists():
        raise OSError("workspace directory does not exist")
    if not workspace.is_dir():
        raise OSError("workspace path is not a directory")

    report = ValidationReport()
    phrase_ids: set[str] = set()
    evidence_by_phrase: dict[str, tuple[EvidenceRecord, ...]] = {}
    phrase_identities: dict[str, tuple[str, str, str]] = {}
    phrase_metadata_by_id: dict[str, PhraseMetadata] = {}
    target_script = ""
    profile_values: dict[str, str] = {}
    lesson_dates: set[date] = set()
    documents: dict[str, list[str]] = {}
    for filename in REQUIRED_FILES:
        path = workspace / filename
        if not path.exists():
            report.errors.append(f"{filename}: missing required file")
            continue
        if not path.is_file():
            report.errors.append(f"{filename}: expected a regular file")
            continue
        try:
            documents[filename] = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"{filename}: cannot read UTF-8 Markdown: {exc}")

    if "profile.md" in documents:
        target_script, profile_values = validate_profile(
            documents["profile.md"], report.errors
        )
    if "progress.md" in documents:
        lesson_dates = validate_lesson_dates(documents["progress.md"], report.errors)
    if "phrase-bank.md" in documents:
        (
            report.phrase_count,
            phrase_ids,
            evidence_by_phrase,
            phrase_identities,
            phrase_metadata_by_id,
        ) = validate_phrase_bank(
            documents["phrase-bank.md"],
            workspace,
            target_script,
            lesson_dates,
            report.errors,
        )
    if "progress.md" in documents:
        validate_progress(
            documents["progress.md"],
            phrase_ids,
            phrase_metadata_by_id,
            evidence_by_phrase,
            phrase_identities,
            target_script,
            profile_values,
            lesson_dates,
            report.errors,
        )
    if "function-map.md" in documents:
        report.function_count = validate_function_map(
            documents["function-map.md"], phrase_ids, report.errors
        )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a language-learning Markdown workspace without judging learner ability."
    )
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args(argv)

    try:
        report = validate(args.workspace)
    except OSError as exc:
        print(f"INPUT_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INPUT
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"INTERNAL_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INTERNAL

    if not report.ok:
        for error in report.errors:
            print(f"INVALID {error}", file=sys.stderr)
        print(f"INVALID errors={len(report.errors)}", file=sys.stderr)
        return EXIT_INVALID

    print(
        f"OK workspace={args.workspace} phrases={report.phrase_count} "
        f"functions={report.function_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
