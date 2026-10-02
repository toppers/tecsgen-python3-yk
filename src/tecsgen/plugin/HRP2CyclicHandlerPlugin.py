"""HRP2CyclicHandlerPlugin.rb の移植（内部仕様9章）。HRP2 周期ハンドラの CRE_CYC/SAC_CYC を生成する。

Ruby 版はカーネルドメインを region の古い API（region_type が :DOMAIN で、param が :KERNEL_DOMAIN）で判定する。
`domain(HRP2, "trusted")` で宣言した region では region_type が :DOMAIN にならないので、必ず
「must belong to kernel domain.」の例外になる（else の枝には入れない）。Ruby 版の Region には
`get_param` が無い（:DOMAIN のとき NoMethodError になる）が、その経路は実在しない。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import Y, sym, to_s


class HRP2CyclicHandlerPlugin(HRP2KernelObjectPlugin):
    _ep: ClassVar[list[Any]] = [
        sym("eStartCyclic"),
        sym("eStopCyclic"),
        sym("eManageCyclic"),
        sym("eReferCyclic"),
    ]

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        name = f"{to_s(self._celltype.get_name())}_{to_s(cell.get_name())}"
        val[Y.id] = re.sub(
            r"(^|[^$])\$id\$",
            lambda m: m.group(1) + name,
            to_s(val.get(Y.id)),
            flags=re.MULTILINE,
        )
        # $cbp$  #983
        name_array = self._celltype.get_name_array(cell)
        cell_cbp = name_array[8]  # CBP
        # CRE_XXXの生成
        if cell.get_region().get_region_type() != Y.DOMAIN:
            # 無所属 or ユーザドメインに属する場合
            raise RuntimeError(
                f"cyclic handler {to_s(val.get(Y.id))} must belong to kernel domain."
            )
        file.print(
            f"{tab}CRE_CYC({to_s(val.get(Y.id))}, {{ {to_s(val.get(Y.attribute))}, {to_s(cell_cbp)}, tCyclicHandler_start, {to_s(val.get(Y.cyclicTime))}, {to_s(val.get(Y.cyclicPhase))} }});\n"
        )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        file.puts(
            f"SAC_CYC({to_s(val.get(Y.id))}, {{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]} }});"
        )

    def get_entry_ports_name_list(self) -> Any:
        """tCyclicHandlerの受け口リスト。"""
        return HRP2CyclicHandlerPlugin._ep
