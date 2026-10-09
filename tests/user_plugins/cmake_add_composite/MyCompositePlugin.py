from __future__ import annotations

from typing import Any

from tecsgen.core.tecsgen import CMake
from tecsgen.plugin.CompositePlugin import CompositePlugin


class MyCompositePlugin(CompositePlugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        CMake.add_source("composite_plugin.c")
        CMake.add_define("K_COMPOSITE=1")
        CMake.add_include("inc_composite")
        CMake.add_line("# from composite")
