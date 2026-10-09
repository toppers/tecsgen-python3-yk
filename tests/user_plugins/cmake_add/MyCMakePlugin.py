"""tools/golden/inputs/cmake_add/MyCMakePlugin.rb の Python 版（CMake.add_* を呼ぶ合成プラグイン）。

`CMakeLists.tecsgen.cmake` は生成の最初に書かれるので、`gen_factory` で足した `too_late.c` は
出力に反映されない（Ruby 版と同じ）。
"""

from __future__ import annotations

from typing import Any

from tecsgen.core.tecsgen import CMake
from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import sym


class MyCMakePlugin(CelltypePlugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        CMake.add_source("plugin_a.c")
        CMake.add_source("plugin_a.c")
        CMake.add_source(sym("sym_b"))
        CMake.add_include("$(BASE_DIR)/inc")
        CMake.add_include("/abs/path\\win")
        CMake.add_define("FOO=1")
        CMake.add_define(42)
        CMake.add_link_option("-Wl,--gc-sections")
        CMake.add_custom_command("add_custom_command(OUTPUT x COMMAND y)")
        CMake.add_line("# line1")
        CMake.add_line("set(X 1)")
        CMake.add_line("# line1")

    def new_cell(self, cell: Any) -> None:
        CMake.add_source("from_new_cell.c")

    def gen_factory(self, file: Any) -> None:
        CMake.add_source("too_late.c")
