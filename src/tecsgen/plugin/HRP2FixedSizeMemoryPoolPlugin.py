"""HRP2FixedSizeMemoryPoolPlugin.rb の移植（内部仕様9章）。HRP2 固定長メモリプールの CRE_MPF/SAC_MPF を生成する。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import Y, sym, to_s


class HRP2FixedSizeMemoryPoolPlugin(HRP2KernelObjectPlugin):
    # Ruby 版の受け口名は tFixedSizeMemoryPool の実際の受け口（eGet…/eRelease…）と違うが、そのまま移す
    _ep: ClassVar[list[Any]] = [
        sym("eSendFixedSizeMemoryPool"),
        sym("eReceiveFixedSizeMemoryPool"),
        sym("eManageFixedSizeMemoryPool"),
        sym("eReferFixedSizeMemoryPool"),
    ]

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        """CRE_MPFの出力。"""
        file.print(tab)
        file.puts(
            f"CRE_MPF({to_s(val.get(Y.id))}, {{{to_s(val.get(Y.attribute))}, {to_s(val.get(Y.blockCount))}, {to_s(val.get(Y.blockSize))}, {to_s(val.get(Y.mpf))}, {to_s(val.get(Y.mpfmb))}}});"
        )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        """SAC_MPFの出力。"""
        file.puts(
            f"SAC_MPF({to_s(val.get(Y.id))}, {{{acv[0]}, {acv[1]}, {acv[2]}, {acv[3]}}});"
        )

    def get_entry_ports_name_list(self) -> Any:
        """tFixedSizeMemoryPoolの受け口リスト。"""
        return HRP2FixedSizeMemoryPoolPlugin._ep
