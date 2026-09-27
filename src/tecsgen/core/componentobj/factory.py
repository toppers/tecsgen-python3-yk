"""factory.rb の移植。セルタイプの factory / FACTORY（`Factory`）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import Y, no_method, rb_print, rb_puts, to_s, truthy


class Factory(BDNode):
    """@name:: string / @file_name:: string / @format:: string
    @arg_list:: Expression の elements と同じ形式 [ [:IDENTIFIER, String], ... ]
    @f_celltype:: bool : true: celltype factory, false: cell factory
    """

    _f_celltype: ClassVar[bool] = False

    @classmethod
    def reset(cls) -> None:
        Factory._f_celltype = False

    def __init__(self, name: Any, file_name: Any, format: Any, arg_list: Any) -> None:
        from tecsgen.core.componentobj.celltype import Celltype

        super().__init__()
        # インスタンス変数 @f_celltype（クラス変数 @@f_celltype とは別）
        self.__dict__["_f_celltype"] = Factory._f_celltype

        if name == Y.write:
            # write 関数
            self._name = name

            # write 関数の第一引数：出力先ファイル名（通常単一の文字列であるから、単一の文字列が返される）
            self._file_name = _val(file_name.eval_const(None))
            if type(self._file_name) is not str:
                # 文字列定数ではなかった
                self.cdl_error(
                    "S1132 $1: 1st parameter is not string(file name)", self._name
                )
                self._file_name = None

            # write 関数の第二引数：フォーマット文字列
            self._format = _val(format.eval_const(None))
            if type(self._format) is not str:
                self.cdl_error(
                    "S1133 $1: 2nd parameter is not string(fromat)", self._name
                )
                self._format = None

            # 第三引数以降を引数リストとする mikan 引数のチェック
            self._arg_list = arg_list
        else:
            self.cdl_error("S1134 $1: unknown factory function", name)
        Celltype.new_factory(self)

    def check_arg(self, celltype: Any) -> None:
        from tecsgen.core.syntaxobj.decl import Decl

        if not truthy(self._arg_list):
            return

        if truthy(self._f_celltype):
            self.cdl_error("S1135 celltype factory can't have parameter(s)")
            return

        for elements in self._arg_list:
            e0 = elements[0]
            if e0 == Y.IDENTIFIER:  # 1
                obj = celltype.find(elements[1])
                if obj is None:
                    self.cdl_error("S1136 '$1': not found", elements[1])
                elif type(obj) is not Decl or obj.get_kind() != Y.ATTRIBUTE:
                    self.cdl_error("S1137 '$1': not attribute", elements[1])
            elif e0 == Y.STRING_LITERAL:
                pass
            else:
                self.cdl_error("S1138 internal error Factory.check_arg()")

    @classmethod
    def set_f_celltype(cls, f_celltype: Any) -> None:
        Factory._f_celltype = f_celltype

    def get_f_celltype(self) -> Any:
        return self.__dict__.get("_f_celltype")

    def get_name(self) -> Any:
        return self._name

    def get_file_name(self) -> Any:
        return self._file_name

    def get_format(self) -> Any:
        return self._format

    def get_arg_list(self) -> Any:
        return self._arg_list

    def show_tree(self, indent: int) -> None:
        from tecsgen.ruby_compat import inspect

        rb_print("  " * indent)
        rb_puts(f"Factory: name: {to_s(self._name)}")
        if truthy(self._arg_list):
            rb_print("  " * (indent + 1))
            rb_puts("argument(s):")
            for lst in self._arg_list:
                rb_print("  " * (indent + 2))
                rb_print(f'"{inspect(lst)}"\n')


def _val(x: Any) -> Any:
    """`x.val`（nil なら NoMethodError）。"""
    if x is None:
        raise no_method("val", None)
    return x.val
