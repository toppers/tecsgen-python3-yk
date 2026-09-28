"""CIfGenCellPlugin.rb の移植。セルの属するセルタイプに CIfGenCelltypePlugin を適用する。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.CellPlugin import CellPlugin
from tecsgen.ruby_compat import to_s


class CIfGenCellPlugin(CellPlugin):
    def gen_cdl_file(self, file: Any) -> None:
        """セルの属するセルタイプに対し、セルタイププラグインを適用する。

        現状実装では、すべてのセルに対してセルプラグインを適用するのと同じ
        （IDX マクロを特定セルに対してのみ出力するか、どうかの違い）。
        """
        ct = self._cell.get_celltype()
        file.print(
            f"/* apply CIfGenCelltypePlugin to celltype '{to_s(ct.get_name())}' "
            f"(celltype of cell '{to_s(self._cell.get_name())}') */\n"
            f'generate( CIfGenCelltypePlugin, {ct.get_namespace_path().get_path_str()}, "" ); \n'
            "\n"
        )
