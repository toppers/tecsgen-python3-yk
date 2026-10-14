"""racc が生成したパーサ（bnf.tab.rb・C_parser.tab.rb）の LALR 表を Python モジュールに変換する。

表の解釈を Ruby 自身に任せるため、dump_racc_tables.rb で JSON に書き出してから変換する。

使い方:
    uv run python tools/port/gen_racc_tables.py <移植元 tecsgen ディレクトリ>

生成物:
    src/tecsgen/syntax/cdl_tables.py    ← tecslib/core/bnf.tab.rb（Generator）
    src/tecsgen/syntax/cdecl_tables.py  ← tecslib/core/C_parser.tab.rb（C_parser）
    src/tecsgen/flowlib/c_parser_tables.py ← flowlib/C_parser.tab.rb（TCFLOW_Cparser。tcflow 用）

トークンは、Ruby の Symbol（:IDENTIFIER）も String（"{"）も Python では str で表す。
両者で同じ名前が現れないことをここで検査する。EOF（Ruby の false）は表に含めず、
ランタイムが 0 番として扱う。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DUMPER = Path(__file__).with_name("dump_racc_tables.rb")
OUT_DIR = ROOT / "src" / "tecsgen"

# (移植元 tecsgen ディレクトリからの相対パス, クラス名, src/tecsgen からの出力先)
TARGETS = (
    ("tecslib/core/bnf.tab.rb", "Generator", "syntax/cdl_tables.py"),
    ("tecslib/core/C_parser.tab.rb", "C_parser", "syntax/cdecl_tables.py"),
    ("flowlib/C_parser.tab.rb", "TCFLOW_Cparser", "flowlib/c_parser_tables.py"),
)

INT_TABLES = (
    "action_table",
    "action_check",
    "action_default",
    "action_pointer",
    "goto_table",
    "goto_check",
    "goto_default",
    "goto_pointer",
)


def dump(path: Path, class_name: str) -> dict[str, Any]:
    out = subprocess.run(
        ["ruby", str(DUMPER), str(path), class_name], check=True, capture_output=True
    ).stdout
    return json.loads(out.decode("utf-8"))


def token_table(entries: list[list[Any]], src_name: str) -> dict[str, int]:
    table: dict[str, int] = {}
    kinds: dict[str, str] = {}
    for kind, name, token_id in entries:
        if kind == "falseclass":
            if token_id != 0:
                raise SystemExit(f"{src_name}: EOF token id is {token_id}, expected 0")
            continue
        if kind not in ("sym", "string"):
            raise SystemExit(f"{src_name}: unexpected token key type {kind}")
        if name in table:
            raise SystemExit(
                f"{src_name}: token {name!r} appears as both {kinds[name]} and {kind}"
            )
        table[name] = token_id
        kinds[name] = kind
    return table


def reduce_table(flat: list[Any]) -> list[tuple[int, int, str]]:
    if len(flat) % 3 != 0:
        raise SystemExit("reduce_table length is not a multiple of 3")
    return [(flat[i], flat[i + 1], flat[i + 2]) for i in range(0, len(flat), 3)]


def int_list(name: str, values: list[int | None], width: int = 16) -> list[str]:
    lines = [f"{name}: tuple[int | None, ...] = ("]
    for i in range(0, len(values), width):
        chunk = ", ".join(
            "None" if v is None else str(v) for v in values[i : i + width]
        )
        lines.append(f"    {chunk},")
    lines.append(")")
    return lines


def render(src_name: str, data: dict[str, Any]) -> str:
    if data["debug_parser"]:
        raise SystemExit(f"{src_name}: Racc_debug_parser is true; not supported")
    lines = [
        f'"""{src_name} の LALR 表。tools/port/gen_racc_tables.py で生成。手で編集しないこと。',
        "",
        f"{data['racc_version_comment']}（Racc_arg の並びは racc/parser.rb の _racc_setup を参照）",
        '"""',
        "",
    ]
    for name in INT_TABLES:
        lines += int_list(name.upper(), data[name])
        lines.append("")
    lines.append(f"NT_BASE = {data['nt_base']}")
    lines.append(f"SHIFT_N = {data['shift_n']}")
    lines.append(f"REDUCE_N = {data['reduce_n']}")
    lines.append(f"USE_RESULT = {bool(data['use_result'])}")
    lines.append("")
    lines.append(
        "# (右辺の長さ, 左辺の記号番号, アクションのメソッド名)。添字は規則番号"
    )
    lines.append("REDUCE_TABLE: tuple[tuple[int, int, str], ...] = (")
    for entry in reduce_table(data["reduce_table"]):
        lines.append(f"    {entry!r},")
    lines.append(")")
    lines.append("")
    lines.append("# トークン名 → 記号番号（EOF の 0 番は含めない）")
    lines.append("TOKEN_TABLE: dict[str, int] = {")
    for name, token_id in token_table(data["token_table"], src_name).items():
        lines.append(f"    {name!r}: {token_id},")
    lines.append("}")
    lines.append("")
    lines.append("# 記号番号 → 名前（racc の token_to_str）")
    lines.append("TOKEN_TO_S_TABLE: tuple[str, ...] = (")
    for name in data["token_to_s_table"]:
        lines.append(f"    {name!r},")
    lines.append(")")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    source = Path(sys.argv[1])
    outputs = []
    for src_name, class_name, out_name in TARGETS:
        text = render(Path(src_name).name, dump(source / src_name, class_name))
        out = OUT_DIR / out_name
        out.write_text(text, encoding="utf-8", newline="\n")
        outputs.append(str(out))
        print(f"{src_name} -> {out_name}")
    # 生成物を ruff format の結果と同じ形にそろえる（ruff format --check を通すため）
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--quiet", *outputs], check=True
    )


if __name__ == "__main__":
    main()
