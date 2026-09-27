"""typedef.rb の移植。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import rb_print, rb_puts


class Typedef(BDNode):
    """@declarator:: Decl"""

    @staticmethod
    def new_decl_list(type_spec_qual_list: Any, decl_list: list[Any]) -> list[Any]:
        for decl in decl_list:
            Typedef(type_spec_qual_list, decl)
        return decl_list

    def __init__(self, type_spec_qual_list: Any, decl: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        super().__init__()
        decl.set_type(type_spec_qual_list)
        self._declarator = decl
        decl.set_owner(self)  # Decl(Typedef)

        Namespace.new_typedef(self)

    def get_name(self) -> Any:
        return self._declarator.get_name()

    def get_declarator(self) -> Any:
        return self._declarator

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"Typedef: {self.locale_str()}")
        self._declarator.show_tree(indent + 1)
