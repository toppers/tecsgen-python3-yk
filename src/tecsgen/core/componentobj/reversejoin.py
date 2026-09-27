"""reversejoin.rb の移植。逆結合（`ReverseJoin`）。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.node import BDNode


class ReverseJoin(BDNode):
    """@ep_name:: Symbol / @ep_subscript:: Expression or nil / @cell_nsp: NamespacePath
    @cp_name:: Symbol / @cp_subscript:: Expression or nil
    """

    def __init__(
        self,
        ep_name: Any,
        ep_subscript: Any,
        cell_nsp: Any,
        cp_name: Any,
        cp_subscript: Any = None,
    ) -> None:
        super().__init__()
        self._ep_name = ep_name
        self._ep_subscript = ep_subscript
        self._cell_nsp = cell_nsp
        self._cp_name = cp_name
        self._cp_subscript = cp_subscript

    def get_name(self) -> Any:
        return self._ep_name

    def get_rhs_cell_and_port(self) -> list[Any]:
        return [self._ep_subscript, self._cell_nsp, self._cp_name, self._cp_subscript]
