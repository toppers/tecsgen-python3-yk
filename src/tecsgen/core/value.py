"""value.rb の移植。整数、浮動小数などの値を扱うクラス（`BaseVal` とその子クラス）。

TECS の CDL で扱う値は、整数・浮動小数・文字列・ブール値に分類される
（集成型（構造体、配列）と C_EXP はここでは扱わない）。

Ruby の演算子メソッドは Python の特殊メソッドで表す（`*` → `__mul__` など）。
Ruby で `==`・`!=` の代わりに使っている `eq`・`neq`、`!` の `not`（Python では `not_`）、
`&&`・`||` の `lAND`・`lOR` は同名のメソッドにする。`==` は上書きしない
（Ruby 版も上書きしていない）。
"""

from __future__ import annotations

import math
from typing import Any

from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    no_method,
    rb_lshift,
    rb_rshift,
    rb_to_f,
    rb_to_i,
    sprintf,
    to_s,
    truthy,
)


def _float_mod(a: float, b: float) -> float:
    """Ruby の Float#%（床除算の剰余。符号は除数に合わせる。Python の % と同じ）。"""
    if math.isinf(a):
        return math.nan
    return a % b


class BaseVal(Node):
    """このクラスで定義済みの演算子は、エラーとなる。型により演算可能な場合、演算子をオーバーライドする。"""

    def __invert__(self) -> Any:
        return self.unsupport("~")

    def __neg__(self) -> Any:
        return self.unsupport("unary -")

    def __pos__(self) -> Any:
        return self.unsupport("unary +")

    def not_(self) -> Any:  # Ruby: not
        return self.unsupport("!")

    def __mul__(self, val: Any) -> Any:
        return self.unsupport("*")

    def __truediv__(self, val: Any) -> Any:
        return self.unsupport("/")

    def __mod__(self, val: Any) -> Any:
        return self.unsupport("%")

    def __add__(self, val: Any) -> Any:
        return self.unsupport("+")

    def __sub__(self, val: Any) -> Any:
        return self.unsupport("-")

    def __lshift__(self, val: Any) -> Any:
        return self.unsupport("<<")

    def __rshift__(self, val: Any) -> Any:
        return self.unsupport(">>")

    def __gt__(self, val: Any) -> Any:
        return self.unsupport(">")

    def __lt__(self, val: Any) -> Any:
        return self.unsupport("<")

    def __ge__(self, val: Any) -> Any:
        return self.unsupport(">=")

    def __le__(self, val: Any) -> Any:
        return self.unsupport("<=")

    def eq(self, val: Any) -> Any:  # == val
        return self.unsupport("==")

    def neq(self, val: Any) -> Any:  # != val
        return self.unsupport("!=")

    def __and__(self, val: Any) -> Any:
        return self.unsupport("&")

    def __xor__(self, val: Any) -> Any:
        return self.unsupport("^")

    def __or__(self, val: Any) -> Any:
        return self.unsupport("|")

    def lAND(self, val: Any) -> Any:
        return self.unsupport("&&")

    def lOR(self, val: Any) -> Any:
        return self.unsupport("||")

    def cast(self, type_: Any) -> Any:
        return self.unsupport("CAST")

    def unsupport(self, op: str) -> None:
        self.cdl_error("V1001 $1: unable for $2", op, type(self))

    # Python の比較演算子を上書きしたので、ハッシュ値は識別子のままにする
    __hash__ = object.__hash__

    def to_s(self) -> str:
        raise RubyRuntimeError("to_s not overridden")

    def to_b(self) -> Any:
        self.cdl_error("V1002 $1: cannot cast to bool (implicitly)", type(self))
        return False

    def to_i(self) -> Any:
        self.cdl_error("V1003 $1: cannot cast to integer (implicitly)", type(self))
        return 1

    def to_f(self) -> Any:
        self.cdl_error("V1004 $1: cannot cast to float (implicitly)", type(self))
        return 1.0


class PointerVal(BaseVal):
    """Pointer 値（IntegerVal の Pointer 版）。整数値のキャスト演算により生成される。

    @int_val:: IntegerVal: IntegerVal でなくてはならない
    @ptr_type:: PtrType: ポインタの指す先の型
    """

    def __init__(self, int_val: Any, ptr_type: Any) -> None:
        super().__init__()
        self._int_val = int_val
        self._ptr_type = ptr_type

    def get_type(self) -> Any:
        """ポインタの指す先の型を得る（PointerVal 専用のメソッド）。"""
        return self._ptr_type

    def cast(self, type_: Any) -> Any:
        from tecsgen.core.cdl_types import FloatType, IntType, PtrType

        t = type_.get_original_type()  # typedef の元を得る
        if isinstance(t, IntType):
            val = t.check_and_clip(self._int_val, Y.IntType)
            return IntegerVal(val)
        if isinstance(t, FloatType):
            self.cdl_error("V1005 Cannot cast pointer to float")
            return FloatVal(self._int_val)
        if isinstance(t, PtrType):
            return PointerVal(self._int_val, type_)
        self.cdl_error("V1006 pointer value cannot cast to $1", type(type_))
        return None

    def to_s(self) -> str:
        return (
            f"({self._ptr_type.get_type_str()}{self._ptr_type.get_type_str_post()})"
            f"{sprintf('0x%X', self._int_val)}"
        )

    def to_b(self) -> Any:
        self.cdl_error("V1007 convert pointer value to bool")
        return False

    def to_i(self) -> Any:
        self.cdl_error("V1008 convert pointer value to integer without cast")
        return 0  # Ruby 版は未定義の @val.to_i（nil.to_i = 0）


class IntegerVal(BaseVal):
    """整数値。@val:: Integer / @str:: string: literal / @sign:: :SIGNED | :UNSIGNED
    @size:: :NORMAL | :SHORT | :LONG | :LONGLONG
    """

    def __init__(
        self, val: Any, str: Any = None, sign: Any = Y.SIGNED, size: Any = Y.NORMAL
    ) -> None:
        super().__init__()
        self._val = rb_to_i(val)
        self._str = str
        self._sign = sign
        self._size = size

    def __invert__(self) -> Any:
        return IntegerVal(~self._val)

    def __neg__(self) -> Any:
        return IntegerVal(-self._val)

    def __pos__(self) -> Any:
        return self

    def not_(self) -> Any:
        # Ruby 版は否定せずに to_b をそのまま返す（そのまま再現する）
        return BoolVal(self.to_b())

    def __mul__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return FloatVal(rb_to_f(self._val) * val.to_f())
        return IntegerVal(self._val * rb_to_i(val))

    def __truediv__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            v2 = val.to_f()  # to_f を2回評価しない
            if v2 == 0.0:
                self.cdl_error("V1009 / : divieded by zero")
                return FloatVal(1.0)
            return FloatVal(rb_to_f(self._val) / v2)
        v2 = rb_to_i(val)  # to_i を2回評価しない
        if v2 == 0:
            self.cdl_error("V1010 / : divieded by zero")
            return IntegerVal(1)
        return IntegerVal(self._val // v2)

    def __mod__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            v2 = val.to_f()
            if v2 == 0.0:
                self.cdl_error("V1011 % : divieded by zero")
                return FloatVal(1.0)
            return FloatVal(_float_mod(rb_to_f(self._val), v2))
        v2 = rb_to_i(val)
        if v2 == 0:
            self.cdl_error("V1012 % : divieded by zero")
            return IntegerVal(1)
        return IntegerVal(self._val % v2)

    def __add__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return FloatVal(rb_to_f(self._val) + val.to_f())
        return IntegerVal(self._val + rb_to_i(val))

    def __sub__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return FloatVal(rb_to_f(self._val) - val.to_f())
        return IntegerVal(self._val - rb_to_i(val))

    def __lshift__(self, val: Any) -> Any:
        return IntegerVal(rb_lshift(self._val, rb_to_i(val)))

    def __rshift__(self, val: Any) -> Any:
        return IntegerVal(rb_rshift(self._val, rb_to_i(val)))

    def __gt__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return BoolVal(rb_to_f(self._val) > val.to_f())
        return BoolVal(self._val > rb_to_i(val))

    def __lt__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return BoolVal(rb_to_f(self._val) < val.to_f())
        return BoolVal(self._val < rb_to_i(val))

    def __ge__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return BoolVal(rb_to_f(self._val) >= val.to_f())
        return BoolVal(self._val >= rb_to_i(val))

    def __le__(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return BoolVal(rb_to_f(self._val) <= val.to_f())
        return BoolVal(self._val <= rb_to_i(val))

    def eq(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return BoolVal(rb_to_f(self._val) == val.to_f())
        return BoolVal(self._val == rb_to_i(val))

    def neq(self, val: Any) -> Any:
        if isinstance(val, FloatVal):
            return BoolVal(rb_to_f(self._val) != val.to_f())
        return BoolVal(self._val != rb_to_i(val))

    def __and__(self, val: Any) -> Any:
        return IntegerVal(self._val & rb_to_i(val))

    def __xor__(self, val: Any) -> Any:
        return IntegerVal(self._val ^ rb_to_i(val))

    def __or__(self, val: Any) -> Any:
        return IntegerVal(self._val | rb_to_i(val))

    def lAND(self, val: Any) -> Any:
        a = self.to_b()
        return BoolVal(val.to_b() if truthy(a) else a)

    def lOR(self, val: Any) -> Any:
        a = self.to_b()
        return BoolVal(a if truthy(a) else val.to_b())

    def cast(self, type_: Any) -> Any:
        from tecsgen.core.cdl_types import BoolType, FloatType, IntType, PtrType

        t = type_.get_original_type()  # typedef の元を得る
        if isinstance(t, IntType):
            val = t.check_and_clip(self._val, Y.IntType)
            return IntegerVal(val)
        if isinstance(t, FloatType):
            return FloatVal(self._val)
        if isinstance(t, PtrType):
            return PointerVal(self._val, type_)
        if isinstance(t, BoolType):
            # Ruby 版は Integer に無い to_b を呼んで NoMethodError になる
            raise no_method("to_b", self._val)
        self.cdl_error("V1013 integer value cannot cast to $1", type(type_))
        return None

    def to_s(self) -> str:
        if truthy(self._str):
            return to_s(self._str)
        return str(self._val)

    def to_b(self) -> Any:
        return self._val != 0

    def to_i(self) -> Any:
        return self._val

    def to_f(self) -> Any:
        return rb_to_f(self._val)


class BoolVal(BaseVal):
    """bool 値。@val:: bool: true, false"""

    def __init__(self, val: Any) -> None:
        super().__init__()
        if val is True or val is False:
            self._val = val
        elif rb_to_i(val) != 0:
            self._val = True
        else:
            self._val = False

    def not_(self) -> Any:
        return BoolVal(not self._val)

    def eq(self, val: Any) -> Any:
        if isinstance(val, BoolVal):
            return BoolVal(self.to_i() == val.to_i())
        self.cdl_error("V1014 comparing bool value with '$1'", type(val))
        return BoolVal(False)

    def neq(self, val: Any) -> Any:
        if isinstance(val, BoolVal):
            return BoolVal(self.to_i() != val.to_i())
        self.cdl_error("V1015 comparing bool value with '$1'", type(val))
        return BoolVal(False)

    def lAND(self, val: Any) -> Any:
        a = self.to_b()
        return BoolVal(val.to_b() if truthy(a) else a)

    def lOR(self, val: Any) -> Any:
        a = self.to_b()
        return BoolVal(a if truthy(a) else val.to_b())

    def cast(self, type_: Any) -> Any:
        from tecsgen.core.cdl_types import BoolType, FloatType, IntType

        t = type_.get_original_type()  # typedef の元を得る
        val = 1 if self._val else 0
        if isinstance(t, IntType):
            return IntegerVal(val)
        if isinstance(t, FloatType):
            return FloatVal(val)
        if isinstance(t, BoolType):
            return self
        self.cdl_error("V1016 bool value cannot cast to $1", type(type_))
        return None

    def to_s(self) -> str:
        return "true" if self._val else "false"

    def to_b(self) -> Any:
        return self._val

    def to_i(self) -> Any:
        return 0 if self._val is False else 1

    def to_f(self) -> Any:
        return 0.0 if self._val is False else 1.0

    @property
    def val(self) -> Any:  # Ruby: attr_reader :val
        return self._val


class FloatVal(BaseVal):
    """実数値。@val:: Float"""

    def __init__(self, val: Any) -> None:
        super().__init__()
        self._val = rb_to_f(val)

    def __neg__(self) -> Any:
        return FloatVal(-self._val)

    def __pos__(self) -> Any:
        return self

    def __mul__(self, val: Any) -> Any:
        return FloatVal(self._val * rb_to_f(val))

    def __truediv__(self, val: Any) -> Any:
        v2 = rb_to_f(val)  # to_f を2回評価しない
        if v2 == 0.0:
            self.cdl_error("V1017 / : divieded by zero")
            return FloatVal(1.0)
        return FloatVal(self._val / v2)

    def __mod__(self, val: Any) -> Any:
        v2 = rb_to_f(val)
        if v2 == 0.0:
            self.cdl_error("V1018 % : divieded by zero")
            return FloatVal(1.0)
        return FloatVal(_float_mod(self._val, v2))

    def __add__(self, val: Any) -> Any:
        return FloatVal(self._val + rb_to_f(val))

    def __sub__(self, val: Any) -> Any:
        return FloatVal(self._val - rb_to_f(val))

    def __gt__(self, val: Any) -> Any:
        return BoolVal(self._val > rb_to_f(val))

    def __lt__(self, val: Any) -> Any:
        return BoolVal(self._val < rb_to_f(val))

    def __ge__(self, val: Any) -> Any:
        return BoolVal(self._val >= rb_to_f(val))

    def __le__(self, val: Any) -> Any:
        return BoolVal(self._val <= rb_to_f(val))

    def eq(self, val: Any) -> Any:
        return BoolVal(self._val == rb_to_f(val))

    def neq(self, val: Any) -> Any:
        return BoolVal(self._val != rb_to_f(val))

    def cast(self, type_: Any) -> Any:
        from tecsgen.core.cdl_types import FloatType, IntType

        t = type_.get_original_type()  # typedef の元を得る
        if isinstance(t, IntType):
            val = t.check_and_clip(self._val, Y.FloatType)
            return IntegerVal(val)
        if isinstance(t, FloatType):
            return self
        self.cdl_error("V1019 floating value cannot cast to $1", type_)
        return self

    def to_b(self) -> Any:
        self.cdl_error("V1020 convert floating value to bool without cast")
        return rb_to_i(self._val)

    def to_i(self) -> Any:
        self.cdl_error("V1021 convert floating value to integer without cast")
        return rb_to_i(self._val)

    def to_s(self) -> str:
        return to_s(self._val)

    def to_f(self) -> Any:
        return self._val


class StringVal(BaseVal):
    """文字列リテラル。@str:: Token / @specifier:: :WIDE, :NORMAL"""

    def __init__(self, s: Any, spec: Any = Y.NORMAL) -> None:
        super().__init__()
        self._str = s
        self._specifier = spec  # mikan L"str" wide 文字列未対応

    def cast(self, type_: Any) -> Any:
        """string の cast はできない（mikan ポインタ型への cast はできるべき）。"""
        from tecsgen.core.cdl_types import FloatType, IntType, PtrType

        t = type_.get_original_type()  # typedef の元を得る
        if isinstance(t, IntType):
            return self.cdl_error("V1022 string cannot cast to integer")
        if isinstance(t, FloatType):
            return self.cdl_error("V1023 string cannot cast to float")
        if isinstance(t, PtrType):
            return self.cdl_error("V1024 string cannot cast to pointer")
        return self.cdl_error("V1025 string cannot cast to $1", type_)

    def to_s(self) -> str:
        return to_s(self._str)

    @property
    def val(self) -> Any:
        return to_s(self._str)  # Token で扱われていた名残 (val を取り出す)
