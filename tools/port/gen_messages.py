"""Ruby 版のメッセージ定義から src/tecsgen/messages/messages_*.py を生成する。

Ruby の文字列リテラル（エスケープ、複数行リテラル）の解釈を Ruby 自身に任せるため、
dump_messages.rb で JSON に書き出してから Python モジュールに変換する。

使い方:
    uv run python tools/port/gen_messages.py <移植元 tecsgen ディレクトリ>

例: uv run python tools/port/gen_messages.py E:/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033/tecsgen
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DUMPER = Path(__file__).with_name("dump_messages.rb")
OUT_DIR = ROOT / "src" / "tecsgen" / "messages"

# Ruby 側のクラス変数名 → Python 側の変数名
TABLES = ("error_message", "warning_message", "info_message", "comment")


def dump(path: Path) -> dict[str, dict[str, str]]:
    out = subprocess.run(
        ["ruby", str(DUMPER), str(path)], check=True, capture_output=True
    ).stdout
    return json.loads(out.decode("utf-8"))


def render(src_name: str, tables: dict[str, dict[str, str]]) -> str:
    unknown = set(tables) - set(TABLES)
    if unknown:
        raise SystemExit(f"{src_name}: unexpected class variables {sorted(unknown)}")
    lines = [
        f'"""{src_name} から tools/port/gen_messages.py で生成。手で編集しないこと。"""',
        "",
    ]
    for name in TABLES:
        if name not in tables:
            continue
        lines.append(f"{name}: dict[str, str] = {{")
        for key, value in tables[name].items():
            lines.append(f"    {key!r}: {value!r},")
        lines.append("}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    src_root = Path(sys.argv[1])
    msg_dir = src_root / "tecslib" / "messages"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "__init__.py").write_text(
        '"""言語別メッセージ表。TECS_LANG が言語名からモジュールを選ぶ。"""\n',
        encoding="utf-8",
        newline="\n",
    )
    for rb in sorted(msg_dir.glob("messages_*.rb")):
        text = render(rb.name, dump(rb))
        (OUT_DIR / f"{rb.stem}.py").write_text(text, encoding="utf-8", newline="\n")
        print(f"{rb.name} -> {rb.stem}.py")


if __name__ == "__main__":
    main()
