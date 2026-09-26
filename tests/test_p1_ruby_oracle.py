"""Ruby 版を正解とする P1 の差分テスト。

tests/ruby/p1_oracle.rb が移植元のソースを読み込み、同じ入力に対する Ruby 版の結果を返す。
Ruby か移植元のソースが無い環境では飛ばす。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest
from conftest import RUBY_SRC, ruby_available

from tecsgen.context import TecsgenContext
from tecsgen.core import generator as generator_mod
from tecsgen.core.messages import TECSMsg
from tecsgen.core.tecs_lang import TECS_LANG, TecsLangError
from tecsgen.ruby_compat import inspect, sub_first, to_s

pytestmark = pytest.mark.skipif(
    not ruby_available(), reason="Ruby か移植元ソースが無い"
)

ORACLE = Path(__file__).parent / "ruby" / "p1_oracle.rb"


def run_oracle(cases: list[dict[str, Any]], tmp_path: Path) -> list[Any]:
    case_file = tmp_path / "cases.json"
    case_file.write_text(json.dumps(cases, ensure_ascii=False), encoding="utf-8")
    out = subprocess.run(
        ["ruby", str(ORACLE), str(RUBY_SRC), str(case_file)],
        check=True,
        capture_output=True,
    ).stdout
    return json.loads(out.decode("utf-8"))


# Ruby の置換文字列として特別な意味を持つ並びを含む引数
TRICKY_ARGS = [
    "plain",
    "back\\slash",
    "\\\\double",
    "\\1group",
    "\\0whole",
    "\\&amp",
    "pre\\`",
    "post\\'",
    "\\k<x>",
    "$2dollar",
    "trailing\\",
    "",
]


def python_message(kind: str, body: str, args: list[Any]) -> str:
    msg = (
        TECSMsg.get_error_message(body)
        if kind == "error"
        else TECSMsg.get_warning_message(body)
    )
    for count, a in enumerate(args, start=1):
        msg = sub_first(generator_mod._arg_pattern(count), to_s(a), msg)
    return msg


def _python_message_or_raise(c: dict[str, Any]) -> str:
    try:
        return python_message(c["type"], c["body"], c["args"])
    except IndexError:
        return "!IndexError"


@pytest.mark.parametrize("lang", ["en_US", "ja_JP"])
def test_message_substitution_matches_ruby(
    lang: str, tmp_path: Path, fresh_state: TecsgenContext
) -> None:
    if lang == "ja_JP":
        TECS_LANG.setup(fresh_state, {"LANG": "ja_JP.UTF-8"})
    cases: list[dict[str, Any]] = []
    # 全メッセージ番号 × 置換引数（本文は Ruby 版の呼び出し側と同じく "番号 英文" の形）
    for table, kind in (
        (TECSMsg._error_message, "error"),
        (TECSMsg._warning_message, "warning"),
    ):
        for i, num in enumerate(table):
            arg = TRICKY_ARGS[i % len(TRICKY_ARGS)]
            args = [arg, 42, None, "x$1y"]
            cases.append(
                {
                    "kind": "message",
                    "lang": lang,
                    "type": kind,
                    "body": f"{num} body $1 $2",
                    "args": args,
                }
            )
    # 表に無い番号・番号の無い本文
    cases.append(
        {
            "kind": "message",
            "lang": lang,
            "type": "error",
            "body": "Z9999 unknown '$1'",
            "args": ["\\1"],
        }
    )
    cases.append(
        {
            "kind": "message",
            "lang": lang,
            "type": "error",
            "body": "no number $1",
            "args": ["a"],
        }
    )
    cases.append(
        {
            "kind": "message",
            "lang": lang,
            "type": "error",
            "body": "x\nS2001 second line",
            "args": [],
        }
    )

    expected = run_oracle(cases, tmp_path)
    actual = [_python_message_or_raise(c) for c in cases]
    mismatches = [
        (c, e, a) for c, e, a in zip(cases, expected, actual, strict=True) if e != a
    ]
    assert mismatches == []


LANG_CASES: list[tuple[dict[str, str], str | None]] = [
    ({}, None),
    ({"LANG": "C"}, None),
    ({"LANG": "C.UTF-8"}, None),
    ({"LANG": "ja_JP.UTF-8"}, None),
    ({"LANG": "ja_JP.eucJP"}, None),
    ({"LANG": "ja_JP.SJIS"}, None),
    ({"LANG": "ja_JP.ujis@cjknarrow"}, None),
    ({"LANG": "ja_JP"}, None),
    ({"LANG": "fr_FR.UTF-8"}, None),
    ({"LANG": "en_US.ISO8859-1"}, None),
    ({"LANG": "C", "TECSGEN_LANG": "ja_JP.eucJP"}, None),
    ({"LANG": "C", "TECSGEN_FILE_LANG": "ja_JP.SJIS"}, None),
    ({"LANG": "ja_JP.UTF-8", "TECSGEN_FILE_LANG": "C"}, None),
    ({"LANG": "C"}, "euc"),
    ({"LANG": "C"}, "sjis"),
    ({"LANG": "C"}, "utf8"),
    ({"LANG": "ja_JP.UTF-8"}, "none"),
    ({"LANG": "C"}, "bogus"),
]


def test_lang_setup_matches_ruby(tmp_path: Path) -> None:
    cases = [{"kind": "lang", "env": env, "kcode": kcode} for env, kcode in LANG_CASES]
    expected = run_oracle(cases, tmp_path)
    for (env, kcode), exp in zip(LANG_CASES, expected, strict=True):
        ctx = TecsgenContext(kcode=kcode)
        try:
            TECS_LANG.setup(ctx, env)
        except TecsLangError as e:
            assert exp == {"exit": e.code}, (env, kcode)
            continue
        actual = {
            "lang_file": ctx.lang_file,
            "charset_file": ctx.charset_file,
            "lang_console": ctx.lang_console,
            "charset_console": ctx.charset_console,
            "file_encode": ctx.ruby19_file_encode,
        }
        assert actual == exp, (env, kcode)


def test_parse_lang_matches_ruby(tmp_path: Path) -> None:
    langs = [
        "",
        "C",
        "ja_JP.eucJP@cjknarrow",
        "ja_JP.",
        "@mod",
        ".UTF-8",
        "a.b.c@d@e",
        "x@y.z",
    ]
    expected = run_oracle([{"kind": "parse_lang", "lang": s} for s in langs], tmp_path)
    assert [list(TECS_LANG.parse_lang(s)) for s in langs] == expected


def test_to_s_and_inspect_match_ruby(tmp_path: Path) -> None:
    values: list[Any] = [
        None, True, False, 0, -12, 1.0, 0.1, 1.5e20, 1e16, 1e15, 1e-5, 0.0001, -2.5e-7,
        "str", 'q"uote', r"back\slash", "tab\tnl\n", "#{x}", "#$y", "#@z", "#plain",
        [1, "a", None, [2.0]], 1.5e15, 1234567890123456.8, 1234567890123456.0, 1.5e16,
        12345678901234567.0, 5e-4, 1.2345e-4, -0.0, 0.0, 100.0, 123.456,
    ]  # fmt: skip
    # Hash#inspect は Ruby 3.4 で書式が変わったため対象外（正解データは Ruby 3.2 で採取）。
    # 制御文字の inspect は Ruby では文字列の文字コードで変わる（UTF-8 は "\u0001"、バイナリは
    # "\x01"）。Python 版は CDL 由来のバイナリ文字列に合わせて "\x01" を出すので、ここでは比べない
    cases = [{"kind": "to_s", "value": v} for v in values]
    cases += [{"kind": "inspect", "value": v} for v in values]
    expected = run_oracle(cases, tmp_path)
    actual = [to_s(v) for v in values] + [inspect(v) for v in values]
    assert actual == expected
