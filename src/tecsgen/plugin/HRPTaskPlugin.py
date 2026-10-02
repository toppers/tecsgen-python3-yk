"""HRPTaskPlugin.rb の移植（内部仕様9章）。HRP のタスク（CRE_TSK/SAC_TSK）を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.context import dbg_print
from tecsgen.plugin.HRPKernelObjectPlugin import HRPKernelObjectPlugin
from tecsgen.ruby_compat import gsub, sym, to_s

_RX_ID = re.compile(r"(^|[^\$])\$id\$")


class HRPTaskPlugin(HRPKernelObjectPlugin):
    def new_cell(self, cell: Any) -> None:
        """oyama: add to avoid Ruby exception in code generation phase."""
        region = cell.get_region()
        dbg_print(
            f"HRPTaskCelltypePlugin new_cell={to_s(cell.get_name())} region={to_s(region.get_name())}\n"
        )
        domain_option = (
            cell.get_region().get_domain_root().get_domain_type().get_option()
        )
        if domain_option == "OutOfDomain":
            self.cdl_error(
                "HRP9999 HRP task '$1' must belong to a domain", cell.get_name()
            )

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        """CRE_TSKの出力。"""
        k_id = sym("id")
        val[k_id] = gsub(
            _RX_ID,
            "\\1" + f"{to_s(self._celltype.get_name())}_{to_s(cell.get_name())}",
            val[k_id],
        )
        # $cbp$の代わり
        cell_idx = to_s(self._celltype.get_name_array(cell)[7])
        # CRE_TSKの生成
        dbg_print("assign task plugin\n")
        domain_option = (
            cell.get_region().get_domain_root().get_domain_type().get_option()
        )
        attribute = val.get(sym("attribute"))
        priority = val.get(sym("priority"))
        stack_size = val.get(sym("stackSize"))
        system_stack_size = val.get(sym("systemStackSize"))
        if domain_option != "OutOfDomain":
            if system_stack_size == "0":
                # システムスタックの定義を省略
                file.print(
                    f"CRE_TSK({val[k_id]}, {{ {attribute}, {cell_idx}, tTask_start, {priority}, {stack_size}, NULL }});\n"
                )
            else:
                # システムスタックの定義を追加
                file.print(
                    f"CRE_TSK({val[k_id]}, {{ {attribute}, {cell_idx}, tTask_start, {priority}, {stack_size}, NULL, {system_stack_size}, NULL }});\n"
                )
        else:
            # 無所属のタスクは存在してはならないため，エラーとする
            raise RuntimeError(f"task {val[k_id]} must belong to a domain.")

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        """SAC_TSKの出力。"""
        pats = ", ".join(str(acv[sym(f"accessPattern{i}")]) for i in (1, 2, 3, 4))
        file.puts(f"SAC_TSK({val[sym('id')]}, {{ {pats} }});")
