"""ATK1ResourcePlugin.rb の移植。TOPPERS/ATK1（OSEK）のリソース定義（`RESOURCE_tecsgen.oil`）を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import gsub, sym, to_s

_RX_QUOTED = re.compile(r'^"(.*)"$', re.MULTILINE)


def _unquote(obj: Any) -> str:
    return gsub(_RX_QUOTED, r"\1", to_s(obj))


class ATK1ResourcePlugin(CelltypePlugin):
    def gen_factory(self, file: Any) -> None:
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        ctx = get_context()
        ct = self._celltype

        f2 = CFile.open(f"{ctx.gen}/RESOURCE_tecsgen.oil", "w")
        # Ruby 版は AppFile で作成中の factory ヘッダ（global_name ではなく name）を直接 "w" で開く
        f3 = CFile.open(f"{ctx.gen}/{to_s(ct.get_name())}_factory.{ctx.h_suffix}", "w")

        for cell in ct.get_cell_list():
            if not cell.is_generate():
                continue
            name = to_s(cell.get_name())
            if name == "RES_SCHEDULER":
                cell.set_specified_id(1)
                continue

            f3.print(f"DeclareResource( {name} );\n")
            f2.print(f"\tRESOURCE {name} {{\n")

            # PROPERTY
            jl = cell.get_join_list()
            join = jl.get_item(sym("property"))
            if join is not None:
                s = _unquote(join.get_rhs())
                if s == "LINKED":
                    f2.print(f"\t\tRESOURCEPROPERTY = {s} {{\n")
                    join2 = jl.get_item(sym("linkedResource"))
                    f2.print(f"\t\t\tLINKEDRESOURCE = {_unquote(join2.get_rhs())};\n")
                    f2.print("\t\t};\n")
                else:
                    f2.print(f"\t\tRESOURCEPROPERTY = {s};\n")

            f2.print("\t};\n")
            f2.print("\n")

        f2.close()
        f3.close()
