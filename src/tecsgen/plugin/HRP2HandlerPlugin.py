"""HRP2HandlerPlugin.rb の移植（内部仕様9章）。HRP2 のハンドラ（CRE_ALM, CRE_CYC, CFG_INT など）を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import gsub, sym, to_s

_RX_ID = re.compile(r"(^|[^\$])\$id\$")


class HRP2HandlerPlugin(HRP2KernelObjectPlugin):
    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        k_id = sym("id")
        if val.get(k_id) is not None:
            val[k_id] = gsub(
                _RX_ID,
                "\\1" + f"{to_s(self._celltype.get_name())}_{to_s(cell.get_name())}",
                val[k_id],
            )
        # $cbp$  #983
        name_array = self._celltype.get_name_array(cell)
        cell_cbp = to_s(name_array[8])  # CBP
        # CRE_XXXの生成
        domain_option = (
            cell.get_region().get_domain_root().get_domain_type().get_option()
        )
        arg = self._plugin_arg_str

        def v(name: str) -> Any:
            return val.get(sym(name))

        if domain_option == "OutOfDomain" or domain_option != "trusted":
            # 無所属 or ユーザドメインに属する場合
            raise RuntimeError(
                f"{to_s(arg).lower()} handler {v('id')} must belong to kernel domain."
            )
        elif arg == "ALARM":
            file.print(
                f"{tab}CRE_ALM({v('id')}, {{ {v('attribute')}, {cell_cbp}, tAlarmHandler_start }});\n"
            )
        elif arg == "CYCLIC":
            file.print(
                f"{tab}CRE_CYC({v('id')}, {{ {v('attribute')}, {cell_cbp}, tCyclicHandler_start, {v('cyclicTime')}, {v('cyclicPhase')} }});\n"
            )
        elif arg == "CONFIG_INT":
            file.print(
                f"{tab}CFG_INT( {v('interruptNumber')}, {{ {v('attribute')}, {v('interruptPriority')} }});\n"
            )
        elif arg == "ISR":
            file.print(
                f"{tab}ATT_ISR({{ {v('attribute')}, {cell_cbp}, {v('interruptNumber')}, tISR_start, {v('priority')} }});\n"
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
        k_id = sym("id")
        if arg == "ALARM":
            file.puts(
                f"SAC_ALM({val.get(k_id)}, {{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]} }});"
            )
        elif arg == "CYCLIC":
            file.puts(
                f"SAC_CYC({val.get(k_id)}, {{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]} }});"
            )
        elif arg in ("CONFIG_INT", "ISR", "INIT_ROUTINE", "TERM_ROUTINE"):
            pass  # nothing to do
        else:
            raise RuntimeError(f"{arg} is unknown option")
