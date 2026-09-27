"""paramlist.rb の移植。関数パラメータリスト（`ParamList`）。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.namedlist import NamedList
from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import rb_integer, rb_print, rb_puts, to_s, truthy


class ParamList(BDNode):
    """関数パラメータリスト。@param_list:: NamedList : item: ParamDecl"""

    def __init__(self, paramdecl: Any) -> None:
        super().__init__()
        self._param_list = NamedList(paramdecl, "parameter")
        for p in self._param_list.get_items():
            p.set_owner(self)  # ParamDecl

    def add_param(self, paramdecl: Any) -> None:
        if paramdecl is None:  # 既にエラー
            return
        self._param_list.add_item(paramdecl)
        paramdecl.set_owner(self)  # ParamDecl

    def get_items(self) -> list[Any]:
        return self._param_list.get_items()

    def check_param(self) -> None:
        """size_is, count_is, string の引数の式をチェックする。

        変数は前方参照可能なため、関数頭部の構文解釈が終わった後にチェックする。
        """
        from tecsgen.core.cdl_types import IntType, VoidType

        for i in self._param_list.get_items():
            if i is None:  # i == nil : エラー時
                continue
            # Ruby のブロック内の変数は、繰り返しのたびに新しくなる（未代入なら nil）
            val: Any = None
            val2: Any = None

            if type(i.get_type()) is VoidType:
                # 単一の void 型はここにはこない
                self.cdl_error("S2027 '$1' parameter cannot be void type", i.get_name())

            size = i.get_size()  # Expression
            if truthy(size):
                val = size.eval_const(self._param_list)
                if val is None:  # 定数式でないか？
                    # mikan 変数を含む式：単一の変数のみ OK
                    t = size.get_type(self._param_list)
                    if not isinstance(t, IntType):
                        self.cdl_error("S2017 size_is argument is not integer type")
                    else:
                        size.check_dir_for_param(
                            self._param_list, i.get_direction(), "size_is"
                        )
                elif val != rb_integer(val):
                    self.cdl_error(
                        "S2018 '$1' size_is parameter not integer",
                        i.get_declarator().get_identifier(),
                    )
                elif val <= 0:
                    self.cdl_error(
                        "S2019 '$1' size_is parameter negative or zero",
                        i.get_declarator().get_identifier(),
                    )

            mx = i.get_max()
            if truthy(mx):
                val2 = mx.eval_const(self._param_list)
                if val2 is None:
                    self.cdl_error(
                        "S2028 '$1' max (size_is 2nd parameter) not constant",
                        i.get_name(),
                    )
                elif val2 != rb_integer(val2) or val2 <= 0:
                    self.cdl_error(
                        "S2029 '$1' max (size_is 2nd parameter) negative or zero, or not integer",
                        i.get_name(),
                    )

            if val is not None and val2 is not None:
                if val < val2:
                    self.cdl_warning(
                        "W3005 '$1' size_is always lower than max. max is ignored",
                        i.get_name(),
                    )
                    i.clear_max()
                else:
                    self.cdl_error(
                        "S2030 '$1' both size_is and max are const. size_is larger than max",
                        i.get_name(),
                    )

            count = i.get_count()  # Expression
            if truthy(count):
                val = count.eval_const(self._param_list)
                if val is None:  # 定数式でないか？
                    t = count.get_type(self._param_list)
                    if not isinstance(t, IntType):
                        self.cdl_error("S2020 count_is argument is not integer type")
                    else:
                        count.check_dir_for_param(
                            self._param_list, i.get_direction(), "count_is"
                        )
                elif val != rb_integer(val):
                    self.cdl_error(
                        "S2021 '$1' count_is parameter not integer",
                        i.get_declarator().get_identifier(),
                    )
                elif val <= 0:
                    self.cdl_error(
                        "S2022 '$1' count_is parameter negative or zero",
                        i.get_declarator().get_identifier(),
                    )

            string = i.get_string()  # Expression
            if not _is_minus1(string) and truthy(string):
                val = string.eval_const(self._param_list)
                if val is None:  # 定数式でないか？
                    t = string.get_type(self._param_list)
                    if not isinstance(t, IntType):
                        self.cdl_error("S2023 string argument is not integer type")
                    else:
                        string.check_dir_for_param(
                            self._param_list, i.get_direction(), "string"
                        )
                elif val != rb_integer(val):
                    self.cdl_error(
                        "S2024 '$1' string parameter not integer",
                        i.get_declarator().get_identifier(),
                    )
                elif val <= 0:
                    self.cdl_error(
                        "S2025 '$1' string parameter negative or zero",
                        i.get_declarator().get_identifier(),
                    )

    def check_struct_tag(self, kind: Any) -> None:
        for p in self._param_list.get_items():
            p.check_struct_tag(kind)

    def need_PPAllocator(self, b_opaque: bool = False) -> bool:
        """Push Pop Allocator が必要か？"""
        return any(i.need_PPAllocator(b_opaque) for i in self._param_list.get_items())

    def find(self, name: Any) -> Any:
        return self._param_list.get_item(name)

    def to_str(self, b_name: bool) -> str:
        """文字列化。b_name:: Bool: パラメータ名を含める。

        Ruby 版は `str += delim + decl.get_type` と型オブジェクトを String に足しているので、
        パラメータが1つでもあると TypeError になる（呼ばれない前提のコード）。そのまま再現する。
        """
        from tecsgen.ruby_compat import RubyTypeError, class_name

        s = "("
        delim = ""
        for paramdecl in self._param_list.get_items():
            decl = paramdecl.get_declarator()
            t = decl.get_type()
            if not isinstance(t, str):
                raise RubyTypeError(
                    f"no implicit conversion of {class_name(type(t))} into String"
                )
            s += delim + t
            if b_name:
                s += " " + to_s(decl.get_name())
            s += decl.get_type_post()
            delim = ", "
        s += ")"
        return s

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"ParamList: {self.locale_str()}")
        self._param_list.show_tree(indent + 1)


def _is_minus1(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x == -1
