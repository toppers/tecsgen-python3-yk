"""HRPHandlerPlugin.rb の移植（内部仕様9章）。HRP のハンドラ（CFG_INT, CRE_ISR, DEF_INH など）を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.plugin.HRPKernelObjectPlugin import HRPKernelObjectPlugin
from tecsgen.ruby_compat import gsub, rb_print, sym, to_s

_RX_ID = re.compile(r"(^|[^\$])\$id\$")


class HRPHandlerPlugin(HRPKernelObjectPlugin):
    def new_cell(self, cell: Any) -> None:
        """oyama: add to avoid Ruby exception in code generation phase."""
        domain_option = (
            cell.get_region().get_domain_root().get_domain_type().get_option()
        )
        if domain_option == "OutOfDomain" or domain_option != "kernel":
            self.cdl_error(
                "HRP9999 HRP handler '$1' must belong to kernel domain",
                cell.get_name(),
            )

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        k_id = sym("id")
        if val.get(k_id) is not None:
            val[k_id] = gsub(
                _RX_ID,
                "\\1" + f"{to_s(self._celltype.get_name())}_{to_s(cell.get_name())}",
                val[k_id],
            )
        # $cbp$の代わり
        name_array = cell.get_celltype().get_name_array(cell)
        cell_cbp = to_s(name_array[8])
        # CRE_XXXの生成
        domain_option = (
            cell.get_region().get_domain_root().get_domain_type().get_option()
        )
        arg = self._plugin_arg_str

        def v(name: str) -> Any:
            return val.get(sym(name))

        if domain_option == "OutOfDomain" or domain_option != "kernel":
            # 無所属 or ユーザドメインに属する場合
            raise RuntimeError(
                f"{to_s(arg).lower()} handler {v('id')} must belong to kernel domain."
            )
        elif arg == "CONFIG_INT":
            file.print(
                f"{tab}CFG_INT( {v('interruptNumber')}, {{ {v('attribute')}, {v('interruptPriority')} }});\n"
            )
        elif arg == "ISR":
            file.print(
                f"{tab}CRE_ISR({v('id')}, {{ {v('attribute')}, {cell_cbp}, {v('interruptNumber')}, tISR_start, {v('isrPriority')} }});\n"
            )
        elif arg == "DEF_INH":
            name_array = self._celltype.get_name_array(cell)
            start = self._celltype.subst_name("$id$_start", name_array)
            file.print(
                f"{tab}DEF_INH({v('interruptHandlerNumber')}, {{ {v('attribute')}, {start} }});\n"
            )
        elif arg == "DEF_EXC":
            name_array = self._celltype.get_name_array(cell)
            start = self._celltype.subst_name("$id$_start", name_array)
            file.print(
                f"{tab}DEF_EXC({v('cpuExceptionHandlerNumber')}, {{ {v('attribute')}, {start} }});\n"
            )
        elif arg == "INIT_ROUTINE":
            file.print(
                f"{tab}ATT_INI({{ {v('attribute')}, {cell_cbp}, tInitializeRoutine_start }});\n"
            )
        elif arg == "TERM_ROUTINE":
            file.print(
                f"{tab}ATT_TER({{ {v('attribute')}, {cell_cbp}, tTerminateRoutine_start }});\n"
            )
        else:
            raise RuntimeError(f"{arg} is unknown option")

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        arg = self._plugin_arg_str
        if arg == "ISR":
            # kernel.cdl の tISR で accessPattern1 ～ accessPattern4 が定義されているときの名残。
            pats = ", ".join(str(acv[sym(f"accessPattern{i}")]) for i in (1, 2, 3, 4))
            rb_print(
                f"*** Unsupported *** SAC_{arg}({val[sym('id')]}, {{ {pats} }});\n"
            )
        elif arg in (
            "CONFIG_INT",
            "DEF_INH",
            "DEF_EXC",
            "INIT_ROUTINE",
            "TERM_ROUTINE",
        ):
            pass  # nothing to do
        else:
            raise RuntimeError(f"{arg} is unknown option")
