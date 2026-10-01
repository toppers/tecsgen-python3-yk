"""HRPObjectPlugin.rb の移植（内部仕様9章）。HRP カーネルオブジェクト（セマフォなど）の CRE_*/SAC_* を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.plugin.HRPKernelObjectPlugin import HRPKernelObjectPlugin
from tecsgen.ruby_compat import sym

_API: dict[str, list[str]] = {
    "SEMAPHORE": ["SEM", "id", "attribute", "initialCount", "maxCount"],
    "EVENTFLAG": ["FLG", "id", "attribute", "flagPattern"],
    "DATAQUEUE": ["DTQ", "id", "attribute", "dataCount", "dataqueueManagementBuffer"],
    "PRIORITY_DATAQUEUE": [
        "PDQ",
        "id",
        "attribute",
        "dataCount",
        "maxDataPriority",
        "priorityDataqueueManagementBuffer",
    ],
    "FIXED_SIZE_MEMORYPOOL": [
        "MPF",
        "id",
        "attribute",
        "blockCount",
        "blockSize",
        "memoryPool",
        "memoryPoolManagementBuffer",
    ],
    "KERNEL": ["SYS"],
    "MESSAGE_BUFFER": [
        "MBF",
        "id",
        "attribute",
        "maxMessageSize",
        "bufferSize",
        "mbfmb",
    ],
    "MUTEX": ["MTX", "id", "attribute", "ceilingPriority"],
}

_RX_TA_CEILING = re.compile(r"\bTA_CEILING\b")


class HRPObjectPlugin(HRPKernelObjectPlugin):
    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        """CRE_XXXの出力。"""
        arg = self._plugin_arg_str
        if arg not in _API:
            raise RuntimeError(f"{arg} is unknown")
        elif arg != "KERNEL":
            params = _API[arg]
            if arg == "MUTEX" and _RX_TA_CEILING.search(val[sym("attribute")]) is None:
                sliced = params[2:-1]  # :ceilingPriority を外す
            else:
                sliced = params[2:]
            arg_list = [f"{val[sym(attr)]}" for attr in sliced]
            file.print(tab)
            file.puts(
                f"CRE_{params[0]}({val[sym('id')]}, {{ {', '.join(arg_list)} }});"
            )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        """SAC_XXXの出力。"""
        arg = self._plugin_arg_str
        pats = ", ".join(str(acv[sym(f"accessPattern{i}")]) for i in (1, 2, 3, 4))
        if arg not in _API:
            raise RuntimeError(f"{arg} is unknown")
        elif arg != "KERNEL":
            file.puts(f"SAC_{_API[arg][0]}({val[sym('id')]}, {{ {pats} }});")
        else:
            file.puts(f"SAC_{_API[arg][0]}({{ {pats} }});")
