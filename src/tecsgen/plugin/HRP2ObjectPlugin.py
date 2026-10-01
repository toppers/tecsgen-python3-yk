"""HRP2ObjectPlugin.rb の移植（内部仕様9章）。HRP2 カーネルオブジェクト（セマフォなど）の CRE_*/SAC_* を生成する。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import sym

_API: dict[str, list[str]] = {
    "SEMAPHORE": ["SEM", "id", "attribute", "count", "max"],
    "EVENTFLAG": ["FLG", "id", "attribute", "flagPattern"],
    "DATAQUEUE": ["DTQ", "id", "attribute", "count", "dtqmb"],
    "PRIORITY_DATAQUEUE": [
        "PDQ",
        "id",
        "attribute",
        "count",
        "maxDataPriority",
        "pdqmb",
    ],
    "FIXED_SIZE_MEMORYPOOL": [
        "MPF",
        "id",
        "attribute",
        "blockCount",
        "blockSize",
        "mpf",
        "mpfmb",
    ],
    "KERNEL": ["SYS"],
    "MESSAGE_BUFFER": ["MBF", "id", "attribute", "maxSize", "bufferSize", "mbfmb"],
}


class HRP2ObjectPlugin(HRP2KernelObjectPlugin):
    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        """CRE_XXXの出力。"""
        arg = self._plugin_arg_str
        if arg not in _API:
            raise RuntimeError(f"{arg} is unknown")
        elif arg != "KERNEL":
            arg_list = [f"{val.get(sym(attr))}" for attr in _API[arg][2:]]
            file.print(tab)
            file.puts(
                f"CRE_{_API[arg][0]}({val.get(sym('id'))}, {{ {', '.join(arg_list)} }});"
            )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        """SAC_XXXの出力。"""
        arg = self._plugin_arg_str
        if arg not in _API:
            raise RuntimeError(f"{arg} is unknown")
        elif arg != "KERNEL":
            file.puts(
                f"SAC_{_API[arg][0]}({val.get(sym('id'))}, {{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]}}});"
            )
        else:
            file.puts(
                f"SAC_{_API[arg][0]}({{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]} }});"
            )
