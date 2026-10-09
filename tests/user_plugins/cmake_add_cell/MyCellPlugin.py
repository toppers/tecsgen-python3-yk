from __future__ import annotations

from typing import Any

from tecsgen.core.tecsgen import CMake
from tecsgen.plugin.CellPlugin import CellPlugin


class MyCellPlugin(CellPlugin):
    def __init__(self, cell: Any, option: Any) -> None:
        super().__init__(cell, option)
        CMake.add_source("cell_plugin.c")
        CMake.add_define("K_CELL=1")
        CMake.add_include("inc_cell")
        CMake.add_line("# from cell")
