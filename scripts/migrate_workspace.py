#!/usr/bin/env python3
"""Add the sound-script foundation section to a legacy workspace."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import stat
import sys
import tempfile


EXIT_INTERNAL = 1
EXIT_INVALID = 2
EXIT_INPUT = 3

PROGRESS_FILENAME = "progress.md"
FOUNDATION_HEADING = "## 声音—文字基础支线".encode()
FOUNDATION_TABLE_HEADER = (
    "| 支线编号 | 类型 | 学习单位或规律 | 锚定语块 | 当前转写支架 | "
    "首学日期 | 复测任务 | 答案可见性 | 复测转写支架 | 变化条件 | 到期日 |"
).encode()
RETEST_HEADING = "## 复测队列".encode()
TEMPLATE_PROGRESS = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "learning-workspace"
    / PROGRESS_FILENAME
)


class MigrationError(Exception):
    """A workspace cannot be migrated without guessing its structure."""


def line_offsets(data: bytes, expected: bytes) -> list[int]:
    offsets: list[int] = []
    offset = 0
    for line in data.splitlines(keepends=True):
        if line.rstrip(b"\r\n") == expected:
            offsets.append(offset)
        offset += len(line)
    return offsets


def current_foundation_section() -> bytes:
    try:
        template = TEMPLATE_PROGRESS.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"cannot read current progress template: {exc}") from exc

    starts = line_offsets(template, FOUNDATION_HEADING)
    ends = line_offsets(template, RETEST_HEADING)
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise RuntimeError("current progress template has no unique foundation section")

    section = template[starts[0] : ends[0]]
    if len(line_offsets(section, FOUNDATION_TABLE_HEADER)) != 1:
        raise RuntimeError("current progress template foundation section has no unique table")
    return section


def atomic_write(path: Path, data: bytes) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def migrate(workspace: Path) -> bool:
    if not workspace.exists():
        raise OSError("workspace directory does not exist")
    if not workspace.is_dir():
        raise OSError("workspace path is not a directory")

    progress = workspace / PROGRESS_FILENAME
    if not progress.exists():
        raise OSError(f"{PROGRESS_FILENAME} does not exist")
    if not progress.is_file():
        raise OSError(f"{PROGRESS_FILENAME} is not a regular file")

    original = progress.read_bytes()
    headings = line_offsets(original, FOUNDATION_HEADING)
    headers = line_offsets(original, FOUNDATION_TABLE_HEADER)
    if headers:
        if len(headers) == 1 and len(headings) == 1 and headings[0] < headers[0]:
            return False
        raise MigrationError(
            "progress.md has a malformed or duplicate foundation section"
        )
    if headings:
        raise MigrationError("progress.md has a foundation heading but no foundation table")

    anchors = line_offsets(original, RETEST_HEADING)
    if not anchors:
        raise MigrationError("progress.md is missing insertion anchor '## 复测队列'")
    if len(anchors) > 1:
        raise MigrationError("progress.md has multiple insertion anchors '## 复测队列'")

    insertion = current_foundation_section()
    migrated = original[: anchors[0]] + insertion + original[anchors[0] :]
    atomic_write(progress, migrated)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Add the current empty sound-script foundation table to a legacy workspace."
    )
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args(argv)

    try:
        changed = migrate(args.workspace)
    except MigrationError as exc:
        print(f"INVALID reason={exc}", file=sys.stderr)
        return EXIT_INVALID
    except OSError as exc:
        print(f"INPUT_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INPUT
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"INTERNAL_ERROR reason={exc}", file=sys.stderr)
        return EXIT_INTERNAL

    status = "changed" if changed else "unchanged"
    print(f"{status} workspace={args.workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
