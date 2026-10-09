from __future__ import annotations

from typing import Any

from tecsgen.core.tecsgen import CMake
from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.plugin.MultiPlugin import MultiPlugin


class MyMultiCelltypePlugin(CelltypePlugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        CMake.add_source("multi_plugin.c")
        CMake.add_define("K_MULTI=1")
        CMake.add_include("inc_multi")
        CMake.add_line("# from multi")


class MyMultiPlugin(MultiPlugin):
    @classmethod
    def get_plugin(cls, super_class: Any) -> Any:
        if super_class is CelltypePlugin:
            return MyMultiCelltypePlugin
        return None
