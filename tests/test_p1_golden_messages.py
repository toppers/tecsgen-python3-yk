"""正解データ（Ruby 版の実行結果）の標準出力と、移植したメッセージ表・出力書式の突き合わせ。

Generator.error2 などが出す行は `<file>:<line>:<col>: error: <番号> <本文>` の形になる。
正解データの全行について、番号から引いた本文（`$n` は任意の文字列）と一致することを確かめる。
正解データは LANG=C（en_US）で採取している。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from conftest import GOLDEN

from tecsgen.core.messages import TECSMsg

LINE_RE = re.compile(
    r"^(?:(?P<loc>[^\n]*?:\d+:\d+): )?(?P<kind>error|warning|info): (?P<msg>.*)$"
)
NUM_RE = re.compile(r"^[A-Z0-9]+")


def first_line(s: str) -> str:
    return s.split("\n", 1)[0]


def golden_cases() -> list[Path]:
    return sorted(p.parent for p in GOLDEN.rglob("meta.json"))


def template_regex(num: str, template: str) -> re.Pattern[str]:
    parts = re.split(r"\$\d", template)
    return re.compile(
        re.escape(num + " ") + ".*".join(re.escape(p) for p in parts) + r"\Z"
    )


@pytest.mark.skipif(not GOLDEN.is_dir(), reason="正解データが無い")
def test_golden_report_lines_match_message_tables() -> None:
    tables = {
        "error": TECSMsg._error_message,
        "warning": TECSMsg._warning_message,
        "info": TECSMsg._info_message,
    }
    checked = 0
    problems: list[str] = []
    for case in golden_cases():
        for line in (
            (case / "stdout.txt")
            .read_text(encoding="utf-8", errors="surrogateescape")
            .splitlines()
        ):
            m = LINE_RE.match(line)
            if not m:
                continue
            msg = m.group("msg")
            num_m = NUM_RE.match(msg)
            template = tables[m.group("kind")].get(num_m.group(0)) if num_m else None
            if template is None:
                # 表に無い番号は、呼び出し側の本文がそのまま出る（ここでは形だけ確かめる）
                continue
            checked += 1
            assert num_m is not None
            # 本文が複数行のメッセージ（P1004 など）は、1行目だけを比べる
            if not template_regex(num_m.group(0), first_line(template)).match(msg):
                problems.append(f"{case.name}: {line}")
    assert problems == []
    assert checked > 600  # 表に番号がある行の数（2026-09-27 の正解データで684行）


# 件数の行（print_report）と出力行数が合わない正解データ。いずれも Ruby 版自体の挙動
COUNT_EXCEPTIONS = {
    # 意味解析中に SystemStackError（expression.rb の elements_eval_const の無限再帰）で異常終了し、
    # print_report まで到達しない（stderr.txt に Ruby の例外）
    "ErrorCase/attribute-err",
    # エラー行が出るのに件数の行が無く、終了コードも 0。原因は未調査（P5 のプラグイン移植時に確認する — TBC）
    "celltypePlugin",
}


@pytest.mark.skipif(not GOLDEN.is_dir(), reason="正解データが無い")
def test_golden_error_counts_match_report_lines() -> None:
    """meta.json のエラー・警告数（Ruby 版の print_report から採取）と、出力された行数が一致する。"""
    mismatches: list[str] = []
    for case in golden_cases():
        meta = json.loads((case / "meta.json").read_text(encoding="utf-8"))
        kinds = [
            m.group("kind")
            for line in (case / "stdout.txt")
            .read_text(encoding="utf-8", errors="surrogateescape")
            .splitlines()
            if (m := LINE_RE.match(line))
        ]
        n_error, n_warning = kinds.count("error"), kinds.count("warning")
        if meta["id"] in COUNT_EXCEPTIONS:
            continue
        if (meta["errors"], meta["warnings"]) != (n_error, n_warning):
            mismatches.append(
                f"{meta['id']}: meta=({meta['errors']}, {meta['warnings']}) lines=({n_error}, {n_warning})"
            )
    assert mismatches == []
    assert all((GOLDEN / c / "meta.json").is_file() for c in COUNT_EXCEPTIONS)
