"""HRP2SemaphorePlugin.rb の移植（内部仕様9章）。HRP2 セマフォの CRE_SEM/SAC_SEM を生成する。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import Y, sym, to_s


class HRP2SemaphorePlugin(HRP2KernelObjectPlugin):
    _ep: ClassVar[list[Any]] = [
        sym("eSignalSemaphore"),
        sym("eWaitSemaphore"),
        sym("eManageSemaphore"),
        sym("eReferSemaphore"),
    ]

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        """CRE_SEMの出力。"""
        file.print(tab)
        file.puts(
            f"CRE_SEM({to_s(val.get(Y.id))}, {{{to_s(val.get(Y.attribute))}, {to_s(val.get(Y.count))}, {to_s(val.get(Y.max))}}});"
        )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        """SAC_SEMの出力。"""
        file.puts(
            f"SAC_SEM({to_s(val.get(Y.id))}, {{{acv[0]}, {acv[1]}, {acv[2]}, {acv[3]}}});"
        )

    def get_entry_ports_name_list(self) -> Any:
        """tSemaphoreの受け口リスト。"""
        return HRP2SemaphorePlugin._ep
