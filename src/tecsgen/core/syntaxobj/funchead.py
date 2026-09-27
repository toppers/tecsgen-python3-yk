"""funchead.rb の移植。関数頭部（`FuncHead`、signature に登録される関数）。

Ruby 版は `get_name` を2回定義している（後の定義が有効）。後の定義だけを移植した
（[[tecsgen-python3 パッケージ構成決定]]）。
"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import Y, rb_print, rb_puts


class FuncHead(BDNode):
    """@declarator:: Decl"""

    def __init__(self, declarator: Any, type_: Any, b_oneway: Any) -> None:
        from tecsgen.core.cdl_types import FuncType, PtrType
        from tecsgen.core.componentobj.signature import Signature

        super().__init__()
        declarator.set_type(type_)
        self._declarator = declarator
        self._declarator.set_owner(self)  # Decl (FuncHead)

        if isinstance(self._declarator.get_type(), FuncType) and b_oneway:
            self._declarator.get_type().set_oneway(b_oneway)
        self._declarator.get_type().check_struct_tag(Y.FUNCHEAD)

        # check if return type is pointer
        if isinstance(declarator.get_type(), FuncType) and (
            isinstance(declarator.get_type().get_type().get_original_type(), PtrType)
            and Signature.get_current().is_deviate() is False
        ):
            self.cdl_warning(
                "W3004 $1 pointer type has returned. specify deviate or stop return pointer",
                self._declarator.get_identifier(),
            )

    def get_declarator(self) -> Any:
        return self._declarator

    def is_oneway(self) -> bool:  # Ruby: is_oneway?
        if self._declarator.is_function():
            return self._declarator.get_type().is_oneway()
        return False

    def is_function(self) -> bool:  # Ruby: is_function?
        return self._declarator.is_function()

    def get_name(self) -> Any:
        """関数の名前を返す。"""
        return self._declarator.get_name()

    def get_type(self) -> Any:
        """関数型を返す。"""
        return self._declarator.get_type()

    def get_return_type(self) -> Any:
        """関数の戻り値の型を返す（関数ヘッダの定義として不完全な場合 nil）。"""
        if self.is_function():
            return self._declarator.get_type().get_type()
        return None

    def get_paramlist(self) -> Any:
        """関数の引数のリスト（ParamList）を返す（不完全な場合 nil）。"""
        if self.is_function():
            return self._declarator.get_type().get_paramlist()
        return None

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"FuncHead: {self.locale_str()}")
        self._declarator.show_tree(indent + 1)
