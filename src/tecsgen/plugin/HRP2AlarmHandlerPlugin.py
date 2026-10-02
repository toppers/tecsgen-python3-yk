"""HRP2AlarmHandlerPlugin.rb の移植（内部仕様9章）。HRP2 アラームハンドラの CRE_ALM/SAC_ALM を生成する。

カーネルドメインの判定が region の古い API のままで、必ず例外になる点は HRP2CyclicHandlerPlugin と同じ。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import Y, sym, to_s


class HRP2AlarmHandlerPlugin(HRP2KernelObjectPlugin):
    _ep: ClassVar[list[Any]] = [
        sym("eStartAlarm"),
        sym("eStopAlarm"),
        sym("eManageAlarm"),
        sym("eReferAlarm"),
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
                f"alarm handler {to_s(val.get(Y.id))} must belong to kernel domain."
            )
        file.print(
            f"{tab}CRE_ALM({to_s(val.get(Y.id))}, {{ {to_s(val.get(Y.attribute))}, {to_s(cell_cbp)}, tAlarmHandler_start }});\n"
        )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        file.puts(
            f"SAC_ALM({to_s(val.get(Y.id))}, {{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]} }});"
        )

    def get_entry_ports_name_list(self) -> Any:
        """tAlarmの受け口リスト。"""
        return HRP2AlarmHandlerPlugin._ep
