#!/usr/bin/env python3
"""Validate a language-learning workspace's Markdown state contract."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys


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
    "来源链接或文件",
    "目标变体",
    "交付方式",
    "来源支持内容",
    "技术验证",
    "首学日期",
    "备注",
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
)

EVIDENCE_HEADER = (
    "维度",
    "任务",
    "提示级别",
    "结果",
    "证据环境",
    "表现记录",
    "证据日期",
    "下次复测",
)
FUNCTION_HEADER = ("功能编号", "沟通功能", "本期优先级", "状态", "语块编号", "最近证据", "下一步")
RETEST_HEADER = ("编号", "维度", "到期日", "无答案任务", "提示级别", "迁移条件", "安排原因")

FIELD_RE = re.compile(r"^\s*-\s+([^：:\n]+?)\s*[：:]\s*(.*?)\s*$")
PHRASE_HEADING_RE = re.compile(r"^##\s+(P\d{3,})\s*(?:[—–-]\s*.*)?$")
POSSIBLE_PHRASE_HEADING_RE = re.compile(r"^##\s+((?:P\S+)|(?:[A-Za-z]\d+))")
FUNCTION_ID_RE = re.compile(r"F(?:0[1-9]|[12]\d|30)\Z")
PHRASE_ID_RE = re.compile(r"P\d{3,}\Z")
TABLE_SEPARATOR_RE = re.compile(r":?-{3,}:?\Z")


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
    if lowered in {"pending", "todo", "tbd", "unknown", "n/a", "na", "not_applicable", "不适用"}:
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
            "尚未",
            "未填写",
            "未测试",
            "未安排",
            "yyyy-mm-dd",
            "<",
        )
    )


def validate_profile(lines: list[str], errors: list[str]) -> None:
    fields = parse_fields(lines)
    require_fields("profile.md", fields, PROFILE_FIELDS, errors)


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

    source_text = " ".join(
        field_value(fields, label)
        for label in ("来源链接或文件", "交付方式", "来源支持内容", "技术验证")
    )
    native_pattern = r"native_official|native_traceable|母语者(?:录音|音频|发音|示范|原声)|真人(?:录音|音频|发音)|native[- ]speaker (?:recording|audio|model|voice)|native (?:recording|audio|model|voice)"
    native_negation = r"不是母语者|并非母语者|非母语者|未由母语者|(?:与|和)母语者.*(?:不同|有别)|不同于母语者|不等于母语者|不能(?:证明|作为|充当).*母语者|不(?:代表|构成).*母语者|not (?:a )?native|different from .*native|cannot (?:prove|establish|serve as).*native"
    tts_pattern = r"\btts\b|合成语音|synthetic (?:speech|voice|audio)"
    tts_negation = r"不是\s*tts|并非\s*tts|非\s*tts|不是合成语音|并非合成语音|not (?:tts|synthetic)"

    if source_class == "tts" and has_affirmative_claim(
        source_text, native_pattern, native_negation
    ):
        errors.append(
            f"phrase-bank.md:{phrase_id}: source class tts is presented as a native recording"
        )
    if source_class in {"native_official", "native_traceable"} and has_affirmative_claim(
        source_text, tts_pattern, tts_negation
    ):
        errors.append(
            f"phrase-bank.md:{phrase_id}: synthetic speech is labelled as {source_class}"
        )


def validate_evidence_table(
    phrase_id: str,
    lines: list[str],
    start: int,
    end: int,
    phrase_fields: dict[str, list[tuple[int, str]]],
    errors: list[str],
) -> None:
    table = find_table(
        "phrase-bank.md", lines, start, end, EVIDENCE_HEADER, errors, phrase_id
    )
    if table is None:
        return

    seen_dimensions: dict[str, int] = {}
    source_class = field_value(phrase_fields, "来源类别")
    for line_number, cells in table.rows:
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

        if dimension not in DIMENSIONS:
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
        if result not in RESULT_STATES:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid result state '{result}'; "
                f"expected one of: {', '.join(RESULT_STATES)}"
            )
            continue
        if environment not in EVIDENCE_ENVIRONMENTS:
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: invalid evidence environment "
                f"'{environment}'; expected one of: {', '.join(EVIDENCE_ENVIRONMENTS)}"
            )

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
        if result not in {"new", "not_applicable"} and environment == "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: result {result} requires "
                "a recorded evidence environment"
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
        if result == "new" and environment != "not_applicable" and prompt == "not_applicable":
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: attempted new result requires "
                "a recorded prompt level"
            )
        if (
            dimension == "pronunciation"
            and result not in {"new", "not_applicable"}
            and environment == "self_report"
        ):
            errors.append(
                f"phrase-bank.md:{phrase_id}: line {line_number}: pronunciation evidence "
                "cannot be upgraded from self_report"
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
        if dimension == "listening" and result not in {"new", "not_applicable"}:
            for label in (
                "来源链接或文件",
                "目标变体",
                "交付方式",
                "来源支持内容",
                "技术验证",
            ):
                value = field_value(phrase_fields, label)
                if is_placeholder(value):
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: listening evidence "
                        f"cannot use unresolved audio source field '{label}' value '{value}'"
                    )

        if result not in {"new", "not_applicable"} or (
            result == "new" and environment != "not_applicable"
        ):
            for column in ("任务", "表现记录", "证据日期", "下次复测"):
                if is_placeholder(row[column]):
                    errors.append(
                        f"phrase-bank.md:{phrase_id}: line {line_number}: result {result} "
                        f"cannot use unresolved '{column}' value '{row[column]}'"
                    )

    missing_dimensions = [dimension for dimension in DIMENSIONS if dimension not in seen_dimensions]
    if missing_dimensions:
        errors.append(
            f"phrase-bank.md:{phrase_id}: missing evidence dimensions: {', '.join(missing_dimensions)}"
        )


def validate_phrase_bank(lines: list[str], errors: list[str]) -> tuple[int, set[str]]:
    blocks = phrase_blocks(lines, errors)
    for phrase_id, start, end in blocks:
        fields = parse_fields(lines, start + 1, end)
        require_fields("phrase-bank.md", fields, PHRASE_FIELDS, errors, phrase_id)

        function_id = field_value(fields, "起步功能编号")
        if function_id and not is_placeholder(function_id) and function_id != "not_applicable":
            if not FUNCTION_ID_RE.fullmatch(function_id):
                errors.append(
                    f"phrase-bank.md:{phrase_id}: invalid starter function ID '{function_id}'; "
                    "expected F01-F30 or not_applicable"
                )

        validate_source_claims(phrase_id, fields, errors)
        validate_evidence_table(phrase_id, lines, start + 1, end, fields, errors)
    return len(blocks), {phrase_id for phrase_id, _, _ in blocks}


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


def validate_progress(lines: list[str], phrase_ids: set[str], errors: list[str]) -> None:
    fields = parse_fields(lines)
    require_fields("progress.md", fields, PROGRESS_FIELDS, errors)
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
        validate_profile(documents["profile.md"], report.errors)
    if "phrase-bank.md" in documents:
        report.phrase_count, phrase_ids = validate_phrase_bank(
            documents["phrase-bank.md"], report.errors
        )
    if "progress.md" in documents:
        validate_progress(documents["progress.md"], phrase_ids, report.errors)
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
