"""paramdecl.rb の移植。関数パラメータの宣言（`ParamDecl`）。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import Y, rb_print, rb_puts, to_s, truthy


class ParamDecl(BDNode):
    """関数パラメータの宣言。

    @declarator:: Decl:  Token, ArrayType, FuncType, PtrType
    @direction:: :IN, :OUT, :INOUT, :SEND, :RECEIVE
    @size:: Expr   (size_is 引数)
    @count:: Expr   (count_is 引数)
    @max:: Expr (size_is の第二引数)
    @b_nullable:: Bool : nullable
    @string:: Expr or -1(if size not specified) （string 引数）
    @allocator:: Signature of allocator
    @b_ref:: bool : size_is, count_is, string_is 引数として参照されている

    1. 関数型でないこと
    2. ２次元以上の配列であって最も内側以外の添数があること
    3. in, out, ..., size_is, count_is, ... の重複指定がないこと
    4. ポインタレベルが適切なこと
    """

    def __init__(self, declarator: Any, specifier: Any, param_specifier: Any) -> None:
        from tecsgen.core.cdl_types import DefinedType, PtrType, StructType
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.signature import Signature

        super().__init__()
        self._declarator = declarator
        self._declarator.set_owner(self)  # Decl (ParamDecl)
        self._declarator.set_type(specifier)
        self._param_specifier = param_specifier
        self._b_ref = False
        self._b_nullable = False
        # 以下は Ruby では代入されるまで存在しない変数（nil と同じ扱い）
        self._direction: Any = None
        self._size: Any = None
        self._count: Any = None
        self._string: Any = None
        self._max: Any = None
        self._allocator: Any = None

        if self._declarator.is_function():  # (1)
            self.cdl_error("S2006 '$1' function", self.get_name())
            return

        res = self._declarator.check()
        if truthy(res):  # (2)
            self.cdl_error("S2007 '$1' $2", self.get_name(), res)
            return

        for i in self._param_specifier:
            i0 = i[0]  # (3)
            if i0 in (Y.IN, Y.OUT, Y.INOUT, Y.SEND, Y.RECEIVE):
                if self._direction is None:
                    self._direction = i0
                elif i0 == self._direction:
                    self.cdl_warning("W3001 $1: duplicate", i0)
                    continue
                else:
                    self.cdl_error("S2008 $1: inconsitent with previous one", i0)
                    continue

                if i0 in (Y.SEND, Y.RECEIVE):
                    self._allocator = Namespace.find(i[1])  # 1
                    if type(self._allocator) is not Signature:
                        self.cdl_error("S2009 $1: not found or not signature", i[1])
                        continue
                    elif not self._allocator.is_allocator():
                        # cdl_error( "S2010 $1: not allocator signature" , i[1] )
                        pass

            elif i0 == Y.SIZE_IS:
                if truthy(self._size):
                    self.cdl_error("S2011 size_is duplicate")
                else:
                    self._size = i[1]
            elif i0 == Y.COUNT_IS:
                if truthy(self._count):
                    self.cdl_error("S2012 count_is duplicate")
                else:
                    self._count = i[1]
            elif i0 == Y.STRING:
                if truthy(self._string):
                    self.cdl_error("S2013 string duplicate")
                elif truthy(i[1]):
                    self._string = i[1]
                else:
                    self._string = -1
            elif i0 == Y.MAX_IS:
                # max_is は、内部的なもの bnf.y.rb 参照
                # size_is で重複チェックされる
                self._max = i[1]
            elif i0 == Y.NULLABLE:
                self._b_nullable = True

        if self._direction is None:
            self.cdl_error("S2014 No direction specified. [in/out/inout/send/receive]")

        if (self._direction == Y.OUT or self._direction == Y.INOUT) and _eq(
            self._string, -1
        ):
            self.cdl_warning(
                "W3002 $1: this string might cause buffer over run", self.get_name()
            )

        # mikan ポインタの配列（添数有）のレベルが０
        ptr_level = self._declarator.get_ptr_level()

        # ----  set req_level, min_level & max_level  ----
        size_or_count = truthy(self._size) or truthy(self._count)
        if not (size_or_count or truthy(self._string)):  # (4)
            req_level = 1
        elif size_or_count and truthy(self._string):
            req_level = 2
        else:
            req_level = 1

        if self._direction == Y.RECEIVE:
            req_level += 1
        min_level = req_level
        max_level = req_level

        # IN without pointer specifier can be non-pointer type
        if self._direction == Y.IN and not (size_or_count or truthy(self._string)):
            min_level = 0

        # if size_is specified and pointer refer to struct, max_level increase
        if truthy(self._size):
            t = self._declarator.get_type().get_original_type()
            while isinstance(t, PtrType):
                t = t.get_referto().get_original_type()
            if isinstance(t, StructType):
                max_level += 1
        # ----  end req_level & max_level    ----

        if ptr_level < min_level:
            self.cdl_error(
                "S2014 $1 need pointer or more pointer",
                self._declarator.get_identifier(),
            )
        elif ptr_level > max_level and (
            # note: 構文解析段階で実行のため get_current 可
            Signature.get_current() is None
            or Signature.get_current().is_deviate() is False
        ):
            self.cdl_warning(
                "W3003 $1 pointer level mismatch", self._declarator.get_identifier()
            )

        t = self._declarator.get_type()
        while isinstance(t, DefinedType):
            t = t.get_original_type()

        if ptr_level > 0:
            # size_is, count_is, string をセット
            if self._direction == Y.RECEIVE and ptr_level > 1:
                t.get_type().set_scs(
                    self._size, self._count, self._string, self._max, self._b_nullable
                )
            else:
                t.set_scs(
                    self._size, self._count, self._string, self._max, self._b_nullable
                )

            # ポインタが指している先のデータ型を得る
            i = 0
            t2 = t
            while i < ptr_level:
                t2 = t2.get_referto()
                while isinstance(t2, DefinedType):
                    t2 = t2.get_original_type()
                i += 1

            # const 修飾が適切かチェック
            if self._direction == Y.IN:
                if not t2.is_const():
                    self.cdl_error(
                        "S2015 '$1' must be const for 'in' parameter $2",
                        self.get_name(),
                        type(t),
                    )
            elif t2.is_const() and Signature.get_current().is_deviate() is False:
                self.cdl_error(
                    "S2016 '$1' can not be const for $2 parameter",
                    self.get_name(),
                    self._direction,
                )
        else:
            # 非ポインタタイプ
            if (
                self._size is not None
                or self._count is not None
                or self._string is not None
                or self._max is not None
                or truthy(self._b_nullable)
            ):
                t.set_scs(
                    self._size, self._count, self._string, self._max, self._b_nullable
                )

    def check_struct_tag(self, kind: Any) -> None:
        self._declarator.get_type().check_struct_tag(Y.PARAMETER)

    def get_name(self) -> Any:
        return self._declarator.get_name()

    def get_size(self) -> Any:
        return self._size

    def get_count(self) -> Any:
        return self._count

    def get_string(self) -> Any:
        return self._string

    def get_max(self) -> Any:
        return self._max

    def clear_max(self) -> None:
        self._max = None
        self._declarator.get_type().clear_max()

    def is_nullable(self) -> bool:  # Ruby: is_nullable?
        return self._b_nullable

    def get_type(self) -> Any:
        return self._declarator.get_type()

    def get_direction(self) -> Any:
        return self._direction

    def get_declarator(self) -> Any:
        return self._declarator

    def get_allocator(self) -> Any:
        return self._allocator

    def referenced(self) -> None:
        self._b_ref = True

    def is_referenced(self) -> bool:  # Ruby: is_referenced?
        return self._b_ref

    def need_PPAllocator(self, b_opaque: bool = False) -> bool:
        """PPAllocator が必要か。

        Transparent RPC の場合 in で size_is, count_is, string のいずれかが指定されている場合
        oneway では PPAllocator が必要。Transparent PC で oneway かどうかは、ここでは判断しない。
        Opaque RPC の場合 size_is, count_is, string のいずれかが指定されている場合、PPAllocator が必要。
        """
        from tecsgen.core.cdl_types import PtrType

        if not b_opaque:
            if self._direction == Y.IN and isinstance(
                self._declarator.get_type().get_original_type(), PtrType
            ):
                return True
        elif self._direction in (Y.IN, Y.OUT, Y.INOUT) and isinstance(
            self._declarator.get_type().get_original_type(), PtrType
        ):
            return True
        return False

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"ParamDecl: direction: {to_s(self._direction)} {self.locale_str()}")
        self._declarator.show_tree(indent + 1)
        if truthy(self._size):
            rb_print("  " * (indent + 1))
            rb_puts("size:")
            self._size.show_tree(indent + 2)
        if truthy(self._count):
            rb_print("  " * (indent + 1))
            rb_puts("count:")
            self._count.show_tree(indent + 2)
        if truthy(self._string):
            rb_print("  " * (indent + 1))
            rb_puts("string:")
            if _eq(self._string, -1):
                rb_print("  " * (indent + 2))
                rb_puts("size is not specified")
            else:
                self._string.show_tree(indent + 2)
        if truthy(self._allocator):
            rb_print("  " * (indent + 1))
            rb_puts(f"allocator: signature: {to_s(self._allocator.get_name())}")


def _eq(a: Any, b: int) -> bool:
    """Ruby の `a == -1`（a が Expression なら偽）。"""
    return isinstance(a, int) and not isinstance(a, bool) and a == b
