"""HRP2EventflagPlugin.rb の移植（内部仕様9章）。HRP2 イベントフラグの CRE_FLG/SAC_FLG を生成する。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import Y, sym, to_s


class HRP2EventflagPlugin(HRP2KernelObjectPlugin):
    _ep: ClassVar[list[Any]] = [
        sym("eSetEventflag"),
        sym("eWaitEventflag"),
        sym("eManageEventflag"),
        sym("eReferEventflag"),
    ]

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        """CRE_FLGの出力。"""
        file.print(tab)
        file.puts(
            f"CRE_FLG({to_s(val.get(Y.id))}, {{{to_s(val.get(Y.attribute))}, {to_s(val.get(Y.flagPattern))}}});"
        )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        """SAC_FLGの出力。"""
        file.puts(
            f"SAC_FLG({to_s(val.get(Y.id))}, {{{acv[0]}, {acv[1]}, {acv[2]}, {acv[3]}}});"
        )

    def get_entry_ports_name_list(self) -> Any:
        """tEventflagの受け口リスト。"""
        return HRP2EventflagPlugin._ep
