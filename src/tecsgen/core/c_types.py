"""ctypes.rb の移植（Python 標準ライブラリの ctypes と区別するため c_types と改名）。

C_parser（import_C）で定義される型。C の型は TECS の型を継承し、mixin の `CType` を持つ
（Ruby の `include CType`。MRO は Ruby の ancestors と同じく CType がスーパークラスより前）。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tecsgen.core.cdl_types import (
    ArrayType,
    BoolType,
    DefinedType,
    EnumType,
    FloatType,
    FuncType,
    IntType,
    PtrType,
    StructType,
    Type,
    VoidType,
)
from tecsgen.ruby_compat import RubyRuntimeError, Y, sym, to_s, truthy

# 型検査のときだけ CType を Type の子として扱う（mixin から Type のメソッドを呼ぶため）
_CTypeBase: Any = Type if TYPE_CHECKING else object


class CType(_CTypeBase):
    """C_parser で定義される型（CIntType, CFloatType など）に include するもの。"""

    _qualifier: Any
    _bit_size: Any
    _sign: Any
    _b_const: Any
    _b_volatile: Any

    def merge(self, another: Any) -> Any:
        """構文要素 type_specifier が複数指定されている場合に merge する。

        merge は const(CIntType) unsigned(CIntTtype), long(CIntType), などと他の型をマージする。
        mikan C の文法を厳密にはチェックしていない  long struct 等もできてしまう
        """
        if type(self) is CIntType and type(another) is CIntType:
            if another.get_bit_size() != -3:
                if self._bit_size == -4 and another.get_bit_size() == -4:
                    self._bit_size = -5  # long long
                else:
                    # self は int 型、another の bit_size が (int 以外であれば)そちらにする
                    self._bit_size = another.get_bit_size()

            if truthy(another.get_sign()):
                # another で sign が指定されていれば、そちらのものを採用する mikan 矛盾のチェック
                self._sign = another.get_sign()

            if another.is_const():
                self._b_const = True
            if another.is_volatile():
                self._b_volatile = True
            return self
        if type(self) is CIntType:
            return another.merge(self)
        if type(self) is CDefinedType:
            # mikan unsigned などとの merge の不正検出
            if another.is_const():
                self._b_const = True
            if another.is_volatile():
                self._b_volatile = True
            return self
        if type(self) is CStructType:
            if another.is_const():
                self._b_const = True
            if another.is_volatile():
                self._b_volatile = True
            return self
        if type(self) is CFloatType:
            # mikan long double
            self.to_long()
            return self
        if type(self) is CVoidType:
            if another.is_const():
                self._b_const = True
            if another.is_volatile():
                self._b_volatile = True
            return self
        raise RubyRuntimeError(f"merge: unknown type {to_s(type(self))}")

    def set_qualifier(self, qualifier: Any) -> None:
        """qualifier を設定する（元の Type クラスでは矛盾チェックしない）。"""
        if truthy(self._qualifier):
            self.cdl_error(
                "C1004 $1: qualifier redefined. previous one: $2",
                qualifier,
                self._qualifier,
            )
        super().set_qualifier(qualifier)


class CDefinedType(CType, DefinedType):
    def __init__(self, type_name: Any) -> None:
        super().__init__(type_name)
        # サイズが明瞭の C 言語の型について、TECS CDL の組込み型と同等に扱う
        sizes = {
            "int8_t": 8,
            "int16_t": 16,
            "int32_t": 32,
            "int64_t": 64,
            "int128_t": 128,
        }
        usizes = {
            "uint8_t": 8,
            "uint16_t": 16,
            "uint32_t": 32,
            "uint64_t": 64,
            "uint128_t": 128,
        }
        if isinstance(type_name, str):
            name = to_s(type_name)
            if type_name == sym(name) and name in sizes:
                self._type = IntType(sizes[name])
            elif type_name == sym(name) and name in usizes:
                self._type = IntType(usizes[name])
                self._type.set_sign(Y.UNSIGNED, True)


class CVoidType(CType, VoidType):
    pass


class CBoolType(CType, BoolType):
    pass


class CIntType(CType, IntType):
    def set_sign(self, sign: Any, b_uint: bool = False) -> None:
        super().set_sign(sign, b_uint)


class CFloatType(CType, FloatType):
    def to_long(self) -> None:
        if self._bit_size != -64:
            self.cdl_warning("W9999 long specified for $1", self.get_type_str())
        else:
            self._bit_size = -128  # @bit_size = -128 : long double


class CEnumType(CType, EnumType):  # mikan
    pass


class CStructType(CType, StructType):
    pass


class CFuncType(CType, FuncType):
    pass


class CArrayType(CType, ArrayType):
    pass


class CPtrType(CType, PtrType):
    pass
