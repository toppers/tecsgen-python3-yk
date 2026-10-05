"""`tecsgen-path` コマンド: 標準 CDL ライブラリ（tecs/）を含むディレクトリを標準出力へ書く。

Ruby 版 tecsgen の「tecsgen のディレクトリ」（`tecs/` を直下に持つ）に当たる。CMake などの
呼び出し側が、`${TECSGEN_DIR}/tecs` で標準 CDL ライブラリ・C ヘッダの場所を知るために使う
（`asp3_stm32cube_TECS` の `Asp3Tecs.cmake` の `ASP3_TECSGEN_DIR`）。

`tecsgen` コマンド自体には新しいオプションを足さない（CLI は Ruby 版と完全互換にする方針）。
そのため別のコマンドにした。出力は区切りを `/` にした1行（Windows でも）。
"""

from __future__ import annotations

import sys
from pathlib import Path

from tecsgen.cli import PACKAGE_DIR


def main() -> int:
    tecs = Path(PACKAGE_DIR) / "tecs"
    if not tecs.is_dir():
        print(f"tecsgen-path: bundled tecs/ not found: {tecs}", file=sys.stderr)
        return 1
    print(PACKAGE_DIR)
    return 0


def entry() -> None:
    """コンソールスクリプトの入口（終了コードを返す）。"""
    sys.exit(main())
