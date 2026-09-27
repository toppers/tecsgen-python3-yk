"""decl.rb の移植。宣言（`Decl`）。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.core.tecsinfo import DeclTECSInfo
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    rb_downcase,
    rb_print,
    rb_puts,
    sym,
    to_s,
    truthy,
)


class Decl(DeclTECSInfo, BDNode):
    """宣言。@kind で示される各種の宣言。

    @identifer:: String
    @global_name:: String | nil : String(@kind=TYPEDEF||:CONSTANT), nil(@kind=その他)
                   set_kind にて設定される
    @type:: ArrayType, FuncType, PtrType, IntType, StructType
            VoidType, FloatType, DefinedType, BoolType
    @initializer:: constant_expression, mikan { initlist }
    @kind:: :VAR, :ATTRIBUTE, :PARAMETER, :TYPEDEF, :CONSTANT, :MEMBER, :FUNCHEAD(signatureの関数定義)
    @b_referenced:: bool

    以下は、@kind が :VAR, :ATTRIBUTE のときに有効
    @rw:: bool     # 古い文法では attr に指定可能だった（消すには generate の修正も必要）
    @omit:: bool
    @choice_list:: [String]  attr 初期値の選択肢
    以下は、@kind が :VAR, :ATTRIBUTE, :MEMBER のときに有効
    @size_is:: Expression or nil unless specified
    以下は、@kind が :MEMBER のときに有効
    @count_is:: Expression or nil unless specified
                attr, var の場合、count_is は指定できない
    @string:: Expression, -1 (length not specified) or nil (not specified)
    """

    def __init__(self, identifier: Any) -> None:
        super().__init__()
        self._identifier = identifier
        self._rw = False
        self._omit = False
        self._size_is: Any = None
        self._count_is: Any = None
        self._string: Any = None
        self._choice_list: Any = None
        self._b_referenced = False
        # 以下は Ruby では代入されるまで存在しない変数（nil と同じ扱い）
        self._initializer: Any = None
        self._type: Any = None
        self._kind: Any = None
        self._global_name: Any = None

    def set_initializer(self, initializer: Any) -> None:
        self._initializer = initializer

    def get_initializer(self) -> Any:
        return self._initializer

    def is_function(self) -> bool:  # Ruby: is_function?
        from tecsgen.core.cdl_types import FuncType

        return type(self._type) is FuncType

    def check(self) -> None:
        """Decl の意味的誤りをチェックする。"""
        from tecsgen.core.c_types import CArrayType
        from tecsgen.core.cdl_types import ArrayType

        # 構造体タグチェック（ポインタ型から構造体が参照されている場合は、タグの存在をチェックしない）
        self._type.check_struct_tag(self._kind)

        # 型のチェックを行う
        res = self._type.check()
        if truthy(res):
            self.cdl_error("S2002 $1: $2", self._identifier, res)

        # 不要の初期化子をチェックする
        if truthy(self._initializer):
            if self._kind in (Y.PARAMETER, Y.TYPEDEF, Y.MEMBER, Y.FUNCHEAD):
                self.cdl_error(
                    "S2003 $1: $2 cannot have initializer",
                    self._identifier,
                    rb_downcase(self._kind),
                )
            elif self._kind in (Y.VAR, Y.ATTRIBUTE, Y.CONSTANT):
                # ここでは代入可能かどうか、チェックしない
                # :VAR, :ATTRIBUTE, :CONSTANT はそれぞれでチェックする
                pass
            else:
                raise RubyRuntimeError("unknown kind in Delc::check")

        if (
            isinstance(self._type, ArrayType)
            and self._type.get_subscript() is None
            and self._omit is False
        ):
            if self._kind == Y.ATTRIBUTE:
                self.cdl_error(
                    "S2004 $1: array subscript must be specified or omit",
                    self._identifier,
                )
            elif self._kind == Y.VAR or self._kind == Y.MEMBER:
                if type(self._type) is CArrayType and self._kind == Y.MEMBER:
                    self.cdl_info(
                        "I9999 $1: array without subscript might not be handled",
                        self._identifier,
                    )
                else:
                    self.cdl_error(
                        "S2005 $1: array subscript must be specified", self._identifier
                    )

    def get_ptr_level(self) -> int:
        """ポインタレベルを得る（非ポインタ変数 = 0、ポインタ変数 = 1、二重ポインタ変数 = 2）。"""
        from tecsgen.core.cdl_types import DefinedType, PtrType

        level = 0
        t = self._type
        while True:
            if isinstance(t, PtrType):
                level += 1
                t = t.get_referto()
            # mikan ポインタの添数あり配列のポインタレベルは０でよい？
            elif isinstance(t, DefinedType):
                t = t.get_type()
            else:
                break
        return level

    def get_name(self) -> Any:
        return self._identifier

    def get_global_name(self) -> Any:
        return self._global_name

    def set_type(self, type_: Any) -> None:
        if not truthy(self._type):
            self._type = type_
        else:
            self._type.set_type(type_)  # 葉に設定

    def get_type(self) -> Any:
        return self._type

    def get_identifier(self) -> Any:
        return self._identifier

    # STAGE: B
    def set_kind(self, kind: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        self._kind = kind
        if kind in (Y.TYPEDEF, Y.CONSTANT):
            if to_s(Namespace.get_global_name()) == "":
                self._global_name = self._identifier
            else:
                self._global_name = sym(
                    f"{to_s(Namespace.get_global_name())}_{to_s(self._identifier)}"
                )
        else:
            self._global_name = None

    def get_kind(self) -> Any:
        return self._kind

    def set_specifier_list(self, spec_list: list[Any]) -> None:
        for spec in spec_list:
            s0 = spec[0]
            if s0 == Y.RW:
                self._rw = True
            elif s0 == Y.OMIT:
                self._omit = True
            elif s0 == Y.SIZE_IS:
                self._size_is = spec[1]
            elif s0 == Y.COUNT_IS:
                self._count_is = spec[1]
            elif s0 == Y.STRING:
                self._string = spec[1]
            elif s0 == Y.CHOICE:
                self._choice_list = spec[1]
            else:
                raise RubyRuntimeError(f"Unknown specifier {to_s(s0)}")

        if truthy(self._size_is) or truthy(self._count_is) or truthy(self._string):
            self._type.set_scs(self._size_is, self._count_is, self._string, None, False)

    def is_rw(self) -> bool:  # Ruby: is_rw?
        return self._rw

    def is_omit(self) -> bool:  # Ruby: is_omit?
        return self._omit

    def get_size_is(self) -> Any:
        return self._size_is

    def get_count_is(self) -> Any:
        return self._count_is

    def get_string(self) -> Any:
        return self._string

    def get_choice_list(self) -> Any:
        return self._choice_list

    def referenced(self) -> None:
        self._b_referenced = True

    def is_referenced(self) -> bool:  # Ruby: is_referenced?
        return self._b_referenced

    def is_type(self, type_: type) -> bool:  # Ruby: is_type?
        from tecsgen.core.cdl_types import DefinedType

        t = self._type
        while True:
            if isinstance(t, type_):
                return True
            if isinstance(t, DefinedType):
                t = t.get_type()
            else:
                return False

    def is_const(self) -> bool:  # Ruby: is_const?
        from tecsgen.core.cdl_types import DefinedType

        t = self._type
        while True:
            if t.is_const():
                return True
            if isinstance(t, DefinedType):
                t = t.get_type()
            else:
                return False

    def print_flowinfo(self, file: Any) -> None:
        if self._kind == Y.VAR:
            file.write(f"{to_s(self._identifier)} ")

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"Declarator: name: {to_s(self._identifier)} kind: {to_s(self._kind)} "
            f"global_name: {to_s(self._global_name)} {self.locale_str()}"
        )
        rb_print("  " * (indent + 1))
        rb_puts("type:")
        self._type.show_tree(indent + 2)
        if truthy(self._initializer):
            rb_print("  " * (indent + 1))
            rb_puts("initializer:")
            self._initializer.show_tree(indent + 2)
        else:
            rb_print("  " * (indent + 1))
            rb_puts("initializer: no")
        rb_print("  " * (indent + 1))
        rb_puts(
            f"size_is: {to_s(self._size_is)}, count_is: {to_s(self._count_is)}, "
            f"string: {to_s(self._string)} referenced: {to_s(self._b_referenced)} "
        )
