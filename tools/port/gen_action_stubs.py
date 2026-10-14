"""文法アクション（racc の _reduce_N）の Python の骨格を生成する。

bnf.y.rb・C_parser.y.rb の規則とアクションのソースを dump_grammar_rules.rb で取り出し、
アクションごとにメソッドの骨格を書く。各メソッドには規則と元の Ruby のアクションを
コメントで残す。本体の移植は P3 で手作業で行うので、**生成物は一度だけ作る**。
既にあるファイルは --force を付けない限り上書きしない。

骨格のうち、次の呼び出しだけは自動で移植する。字句解析の状態（TYPE_NAME の置換）を
変えるもので、構文解析の結果そのものに効くため。

- `set_in_specifier` / `unset_in_specifier`（CDL: 指定子 `[ ]` の内側だけの予約語）
- `set_no_type_name true|false`（C_parser）

それ以外のアクションは `self._unported(N)` を呼んで値をそのまま返す（racc の既定と同じ
`result`）。呼ばれた規則番号は記録されるので、P3 で移植漏れを検出できる。

表（*_tables.py）の REDUCE_TABLE と規則数・右辺の長さ・メソッド名が一致することを検査する。

使い方:
    uv run python tools/port/gen_action_stubs.py <移植元 tecsgen ディレクトリ> [--force]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from tecsgen.flowlib import c_parser_tables
from tecsgen.syntax import cdecl_tables, cdl_tables

ROOT = Path(__file__).resolve().parents[2]
DUMPER = Path(__file__).with_name("dump_grammar_rules.rb")
OUT_DIR = ROOT / "src" / "tecsgen"

TARGETS: tuple[tuple[str, ModuleType, str, str], ...] = (
    ("tecslib/core/bnf.y.rb", cdl_tables, "syntax/cdl_actions.py", "CdlActions"),
    (
        "tecslib/core/C_parser.y.rb",
        cdecl_tables,
        "syntax/cdecl_actions.py",
        "CdeclActions",
    ),
    (
        "flowlib/C_parser.y.rb",
        c_parser_tables,
        "flowlib/c_parser_actions.py",
        "TcflowActions",
    ),
)

LEXER_STATE_CALLS = [
    (re.compile(r"\bunset_in_specifier\b"), "self.unset_in_specifier()"),
    (re.compile(r"(?<!un)\bset_in_specifier\b"), "self.set_in_specifier()"),
    (re.compile(r"\bset_no_type_name\s+true\b"), "self.set_no_type_name(True)"),
    (re.compile(r"\bset_no_type_name\s+false\b"), "self.set_no_type_name(False)"),
]


def dump(path: Path) -> list[dict[str, Any]]:
    out = subprocess.run(
        ["ruby", str(DUMPER), str(path)], check=True, capture_output=True
    ).stdout
    return json.loads(out.decode("utf-8"))


def check(rules: list[dict[str, Any]], tables: ModuleType, src_name: str) -> None:
    table = tables.REDUCE_TABLE
    if len(rules) != len(table):
        raise SystemExit(f"{src_name}: {len(rules)} rules, table has {len(table)}")
    for rule, (length, _lhs, method) in zip(rules, table, strict=True):
        n = rule["ident"]
        if n == 0:
            continue  # $start
        if length != len(rule["symbols"]):
            raise SystemExit(f"{src_name}: rule {n} length mismatch")
        expected = f"_reduce_{n}" if rule["action"] else "_reduce_none"
        if method != expected:
            raise SystemExit(f"{src_name}: rule {n} method {method} != {expected}")


def lexer_state_calls(action: str) -> list[str]:
    """アクション中の、字句解析の状態を変える呼び出しを出現順に返す。"""
    found: list[tuple[int, str]] = []
    for pattern, call in LEXER_STATE_CALLS:
        found += [(m.start(), call) for m in pattern.finditer(action)]
    return [call for _, call in sorted(found)]


def render(
    src_name: str, rules: list[dict[str, Any]], class_name: str, tables_mod: str
) -> str:
    lines = [
        f'"""{src_name} の文法アクション（racc の _reduce_N）。',
        "",
        "tools/port/gen_action_stubs.py で骨格を生成し、本体は手で移植する。各メソッドの",
        "コメントは、規則（左辺 : 右辺）と移植元のアクション（行番号付き）。",
        "`self._unported(N)` が残っているメソッドは、まだ移植していない。",
        '"""',
        "",
        "# ruff: noqa: ARG002, N802",
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        f"from tecsgen.{tables_mod} import REDUCE_TABLE",
        "",
        "",
        f"class {class_name}:",
        '    """アクションの mixin。パーサ本体のクラスが継承する。"""',
        "",
        "    def _unported(self, rule: int) -> None:",
        '        """まだ移植していないアクションが呼ばれたことを記録する。"""',
        "        unported = self.__dict__.setdefault('unported_rules', set())",
        "        unported.add(rule)",
        "",
        "    # 字句解析の状態を変えるメソッド。パーサ本体のクラスが実装する",
        "    def set_in_specifier(self) -> None:",
        "        raise NotImplementedError",
        "",
        "    def unset_in_specifier(self) -> None:",
        "        raise NotImplementedError",
        "",
        "    def set_no_type_name(self, b_no_type_name: bool) -> None:",
        "        raise NotImplementedError",
        "",
    ]
    for rule in rules:
        action = rule["action"]
        if action is None:
            continue
        n = rule["ident"]
        rhs = " ".join(rule["symbols"]) or "/* empty */"
        lines.append(
            f"    def _reduce_{n}(self, val: list[Any], _values: list[Any], result: Any) -> Any:"
        )
        lines.append(f"        # {rule['target']} : {rhs}")
        lines.append(f"        # {src_name}:{rule['lineno']}")
        for src_line in action.strip("\n").split("\n"):
            lines.append(f"        #| {src_line.rstrip()}".rstrip())
        for call in lexer_state_calls(action):
            lines.append(f"        {call}")
        lines.append(f"        self._unported({n})")
        lines.append("        return result")
        lines.append("")
    lines.append("")
    lines.append("# アクションを持つ規則の番号（移植漏れの検査に使う）")
    lines.append(
        "ACTION_RULES = frozenset(i for i, r in enumerate(REDUCE_TABLE) if r[2].startswith('_reduce_') and r[2] != '_reduce_none')"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("--force", action="store_true")
    opts = ap.parse_args()
    outputs = []
    for src_name, tables, out_name, class_name in TARGETS:
        out = OUT_DIR / out_name
        if out.exists() and not opts.force:
            print(f"{out_name} exists; skipped (use --force to overwrite)")
            continue
        rules = dump(opts.source / src_name)
        check(rules, tables, src_name)
        text = render(
            Path(src_name).name, rules, class_name, tables.__name__.split(".", 1)[1]
        )
        out.write_text(text, encoding="utf-8", newline="\n")
        outputs.append(str(out))
        print(f"{src_name} -> {out_name}")
    if outputs:
        subprocess.run(
            [sys.executable, "-m", "ruff", "format", "--quiet", *outputs], check=True
        )


if __name__ == "__main__":
    main()
