"""compositecelltypejoin.rb の移植。CompositeCelltype 用の Join（CompositeCelltype が export するもの）。"""

from __future__ import annotations

from typing import Any

from tecsgen.context import dbg_print, dbg_printf
from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import RubyRuntimeError, Y, rb_print, rb_puts, to_s, truthy


class CompositeCelltypeJoin(BDNode):
    """@export_name:: string / @internal_cell_name:: string / @internal_cell_elem_name:: string
    @cell : Cell（in_compositeセル） / @port_decl:: Port | Decl
    """

    def __init__(
        self,
        export_name: Any,
        internal_cell_name: Any,
        internal_cell_elem_name: Any,
        cell: Any,
        port_decl: Any,
    ) -> None:
        super().__init__()
        self._export_name = export_name
        self._internal_cell_name = internal_cell_name
        self._internal_cell_elem_name = internal_cell_elem_name
        self._cell = cell
        self._port_decl = port_decl

    def match(self, cell: Any, port_decl: Any = None) -> bool:  # Ruby: match?
        """CompositeCelltypeJoin の対象セルか？（CompositeCelltypeJoin と cell の名前が一致するか）"""
        if truthy(port_decl):
            dbg_print("match?")
            dbg_printf(
                "  @cell:      %-20s      %08x\n",
                to_s(self._cell.get_name()),
                id(self._cell),
            )
            dbg_printf(
                "  @port_decl: %-20s      %08x\n",
                to_s(self._port_decl.get_name()),
                id(self._port_decl),
            )
            dbg_printf(
                "  cell:       %-20s      %08x\n", to_s(cell.get_name()), id(cell)
            )
            dbg_printf(
                "  port_decl:  %-20s      %08x\n",
                to_s(port_decl.get_name()),
                id(port_decl),
            )

        # recursive_composite で名前の一致に変更   060917
        return bool(
            self._cell.get_name() == cell.get_name()
            and (
                port_decl is None or self._port_decl.get_name() == port_decl.get_name()
            )
        )

    def check_dup_init(self) -> None:
        if self.get_port_type() != Y.CALL:
            return
        if truthy(self._cell.get_join_list().get_item(self._internal_cell_elem_name)):
            self.cdl_error(
                "S1131 '$1.$2' has duplicate initializer",
                self._internal_cell_name,
                self._internal_cell_elem_name,
            )

    def get_name(self) -> Any:
        return self._export_name

    def get_cell_name(self) -> Any:
        return self._internal_cell_name

    def get_cell(self) -> Any:
        return self._cell

    def get_cell_elem_name(self) -> Any:
        return self._internal_cell_elem_name

    def get_port_type(self) -> Any:
        """@port_decl が Port の場合のみ呼び出してよい。"""
        if truthy(self._port_decl):
            return self._port_decl.get_port_type()
        return None

    def get_port_decl(self) -> Any:
        return self._port_decl

    def get_allocator_instance(self) -> Any:
        from tecsgen.core.componentobj.port import Port

        if type(self._port_decl) is Port:
            return self._port_decl.get_allocator_instance()
        if truthy(self._port_decl):
            raise RubyRuntimeError(
                "CompositeCelltypeJoin#get_allocator_instance: not port"
            )
        return None

    def is_require(self) -> Any:  # Ruby: is_require?
        if truthy(self._port_decl):
            return self._port_decl.is_require()
        return None

    def is_allocator_port(self) -> Any:  # Ruby: is_allocator_port?
        if truthy(self._port_decl):
            return self._port_decl.is_allocator_port()
        return None

    def is_optional(self) -> Any:  # Ruby: is_optional?
        if truthy(self._port_decl):
            return self._port_decl.is_optional()
        return None

    def get_initializer(self) -> Any:
        """右辺が Decl ならば初期化子（式）を返す。"""
        from tecsgen.core.syntaxobj.decl import Decl

        if type(self._port_decl) is Decl:
            return self._port_decl.get_initializer()
        return None

    def get_size_is(self) -> Any:
        from tecsgen.core.syntaxobj.decl import Decl

        if type(self._port_decl) is Decl:
            return self._port_decl.get_size_is()
        return None

    def get_array_size(self) -> Any:
        """配列サイズを得る（nil: not array, "[]": 大きさ指定なし, Integer: 大きさ指定あり）。"""
        return self._port_decl.get_array_size()

    def get_signature(self) -> Any:
        """signature を得る（@port_decl が Port の時のみ呼び出してもよい）。"""
        return self._port_decl.get_signature()

    def get_type(self) -> Any:
        from tecsgen.core.syntaxobj.decl import Decl

        if type(self._port_decl) is Decl:
            return self._port_decl.get_type()
        return None

    def get_choice_list(self) -> Any:
        from tecsgen.core.syntaxobj.decl import Decl

        if type(self._port_decl) is Decl:
            return self._port_decl.get_choice_list()
        return None

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"CompositeCelltypeJoin: export_name: {to_s(self._export_name)} #<CompositeCelltypeJoin>"
        )
        rb_print("  " * (indent + 1))
        rb_puts(f"internal_cell_name: {to_s(self._internal_cell_name)}")
        rb_print("  " * (indent + 1))
        rb_puts(f"internal_cell_elem_name: {to_s(self._internal_cell_elem_name)}")
        if truthy(self._port_decl):
            self._port_decl.show_tree(indent + 1)
