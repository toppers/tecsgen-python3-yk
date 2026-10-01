"""test/region/Plugin1.rb の Python 版。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import sym, to_s


class Plugin1(ThroughPlugin):
    # Ruby の `@@generated_celltype = {}`（through/Plugin1.py と同じ。ロード時に共有辞書が空になる）
    ThroughPlugin._generated_celltype.clear()

    def __init__(
        self,
        cell_name: Any,
        plugin_arg: Any,
        next_cell: Any,
        next_cell_port_name: Any,
        next_cell_port_subscript: Any,
        signature: Any,
        celltype: Any,
        caller_cell: Any,
    ) -> None:
        super().__init__(
            cell_name,
            plugin_arg,
            next_cell,
            next_cell_port_name,
            next_cell_port_subscript,
            signature,
            celltype,
            caller_cell,
        )
        self._cell_name = cell_name
        self._next_cell = next_cell
        self._next_cell_port_name = next_cell_port_name
        self._signature = signature
        self._entry_port_name = sym("throughEntry")

    def get_cell_name(self) -> Any:
        return self._cell_name

    def get_through_entry_port_name(self) -> Any:
        return self._entry_port_name

    def gen_through_cell_code(self, file: Any) -> None:
        self.gen_plugin_decl_code(file)

        nest = self._region.gen_region_str_pre(file)
        nest_str = "  " * nest
        if self._next_cell_port_subscript:
            subscript = "[" + to_s(self._next_cell_port_subscript) + "]"
        else:
            subscript = ""

        file.print(
            f"{nest_str}cell tPlugin1_{to_s(self._signature.get_name())} {to_s(self._cell_name)} {{\n"
            f"{nest_str}  cCall = {self._next_cell.get_namespace_path().get_path_str()}."
            f"{to_s(self._next_cell_port_name)}{subscript};\n"
            f"{nest_str}}};\n"
        )

        self._region.gen_region_str_post(file)
