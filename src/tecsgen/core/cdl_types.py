"""types.rb の移植（Python 標準ライブラリの types と区別するため cdl_types と改名）。

CDL の型（`Type` とその子クラス）。`HasType` は @type を内部に持つ型の mixin。
"""

from __future__ import annotations

import copy
from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.generate import StructTypeGenerate
from tecsgen.core.syntaxobj.node import Node
from tecsgen.core.tecsinfo import TypeTECSInfo
from tecsgen.ruby_compat import (
    RubyNameError,
    RubyRuntimeError,
    Y,
    dualmethod,
    rb_print,
    rb_puts,
    rb_to_i,
    sym,
    to_s,
    truthy,
)


class HasType:
    """@type を内部に持つ型のための mixin（DefinedType, PtrType, ArrayType）。

    @b_cloned::Bool  : true if @type is cloned

    本当は typedef された時の Decl の要素のみ clone すればよいのだが、get_type, get_original_type で
    取り出されたとき、set_scs, set_qualifier されたときに無条件で clone する (無駄にメモリを使用する)
    """

    _type: Any

    def initHasType(self) -> None:
        self._b_cloned = False

    def clone_type(self) -> None:
        """@type をクローンする。"""
        self._type = copy.copy(self._type)
        self._b_cloned = True


class Type(TypeTECSInfo, Node):
    """@b_const : bool / @b_volatile : bool"""

    # tecsinfo.rb がクラス本体で定義するクラス変数
    _typeinfo_printed: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        Type._typeinfo_printed = {}

    def set_qualifier(self, qualifier: Any) -> None:
        if qualifier == Y.CONST:
            self._b_const = True
        elif qualifier == Y.VOLATILE:
            self._b_volatile = True
        else:
            raise RubyRuntimeError(f"Unknown qualifier {to_s(qualifier)}")

    def is_const(self) -> bool:  # Ruby: is_const?
        return bool(truthy(self._b_const))

    def is_volatile(self) -> bool:  # Ruby: is_volatile?
        return bool(truthy(self._b_volatile))

    def is_void(self) -> bool:  # Ruby: is_void?
        if isinstance(self, DefinedType):
            return self._type.is_void()
        return isinstance(self, VoidType)

    def set_scs(
        self,
        size: Any,
        count: Any,
        string: Any,
        max: Any = None,
        b_nullable: Any = False,
    ) -> None:
        """size_is, count_is, string を設定する。派生クラスでオーバーライドする（デフォルトではエラー）。"""
        s = ""
        delim = ""
        if truthy(size):
            s = "size_is"
            delim = ", "
        if truthy(count):
            s = f"{s}{delim}count_is"
            delim = ", "
        if truthy(string):
            s = f"{s}{delim}string"
            delim = ", "
        if truthy(b_nullable):
            s = f"{s}{delim}nullable"
            delim = ", "
        self.cdl_error("T1003 $1: unsuitable specifier for $2", s, type(self))

    def clear_max(self) -> None:
        raise RubyRuntimeError(f"clear_max called: {to_s(type(self))}")

    def get_type_str(self) -> str:
        s = ""
        if truthy(self._b_const):
            s = f"{s}const "
        if truthy(self._b_volatile):
            s = f"{s}volatile "
        return s

    def get_type_str_post(self) -> str:
        # Ruby の Type は get_type_str_post を定義しない（子クラスが定義する）
        from tecsgen.ruby_compat import no_method

        raise no_method("get_type_str_post", self)

    def check(self) -> Any:
        """型をチェックする。型に誤りがあれば、エラー文字列を返す。"""
        return None

    def check_struct_tag(self, kind: Any) -> None:
        """struct の tag をチェックする（tag が存在しなければエラーを出力する）。"""
        return

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        """初期化可能かチェックする（型に対し正当な初期化子が与えられているか）。"""
        return

    def cast(self, const_val: Any) -> None:
        """const_val を指定の型にキャストする。派生クラスでオーバーライドしていないとエラー。"""
        self.cdl_error("T1004 cannot cast to $1", type(self))

    def equal(self, type2: Any) -> bool:  # Ruby: equal?
        """型が一致するかのチェック（型名の字面でチェック）。"""
        return (self.get_type_str() == type2.get_type_str()) and (
            self.get_type_str_post() == type2.get_type_str_post()
        )

    def get_bit_size(self) -> int:
        """bit size を得る。IntType, FloatType 以外は0。"""
        return 0

    def get_original_type(self) -> Any:
        """元の型を得る（typedef された型の場合、その元の型。それ以外は自分自身）。"""
        return self

    def has_pointer(self) -> bool:  # Ruby: has_pointer?
        return False

    def has_sized_pointer(self) -> bool:  # Ruby: has_sized_pointer?
        return False

    def has_unsized_string(self) -> bool:  # Ruby: has_unsized_string?
        return False

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"const={to_s(self._b_const)} volatile={to_s(self._b_volatile)} {self.locale_str()}"
        )
        rb_print("  " * indent)
        rb_puts(
            f"has_pointer={to_s(self.has_pointer())} has_sized_pointer={to_s(self.has_sized_pointer())} "
            f"has_unsized_string={to_s(self.has_unsized_string())}"
        )


class DefinedType(HasType, Type):
    """@type_name::string / @typedef::Typedef / @type:: kind_of Type"""

    def __init__(self, type_name: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.syntaxobj.typedef import Typedef

        super().__init__()
        self._type_name = type_name

        # mikan type_name が path になっていないため暫定
        self._typedef = Namespace.find([type_name])  # 1

        if self._typedef is None:
            self.cdl_error("T1005 '$1' not defined", type_name)
        elif type(self._typedef) is not Typedef:
            self.cdl_error(
                "T1006 '$1' not type name. expecting type name here", type_name
            )
        self._type = _call(self._typedef, "get_declarator").get_type()
        self.initHasType()

    def get_type(self) -> Any:
        self.clone_type()
        return self._type

    def get_type_str(self) -> str:
        return f"{super().get_type_str()}{to_s(self._type_name)}"

    def get_type_str_post(self) -> str:
        return ""

    def get_size(self) -> Any:
        return self._type.get_size()

    def is_nullable(self) -> Any:  # Ruby: is_nullable?
        return self._type.is_nullable()

    def set_qualifier(self, qualifier: Any) -> None:
        """qualifier(const, volatile) の設定。"""
        self.clone_type()
        self._type.set_qualifier(qualifier)
        super().set_qualifier(qualifier)

    def set_scs(
        self,
        size: Any,
        count: Any,
        string: Any,
        max: Any = None,
        b_nullable: Any = False,
    ) -> None:
        self.clone_type()
        self._type.set_scs(size, count, string, max, b_nullable)

    def clear_max(self) -> None:
        self._type.clear_max()

    def get_original_type(self) -> Any:
        self.clone_type()
        return self._type.get_original_type()

    def check(self) -> Any:  # 意味的誤りがあれば、文字列を返す
        return None  # typedef の段階で意味チェックされている

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        self.get_type().check_init(locale, ident, initializer, kind, attribute)

    def has_pointer(self) -> bool:
        return self._type.has_pointer()

    def has_sized_pointer(self) -> bool:
        return self._type.has_sized_pointer()

    def has_unsized_string(self) -> bool:
        return self._type.has_unsized_string()

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        if self._typedef is None:
            rb_puts(
                f"DefinedType: {to_s(self._type_name)} is missing, const={to_s(self._b_const)} "
                f"volatile={to_s(self._b_volatile)} {self.locale_str()}"
            )
        else:
            rb_puts(
                f"DefinedType: {to_s(self._type_name)}, const={to_s(self._b_const)} "
                f"volatile={to_s(self._b_volatile)}"
            )
        super().show_tree(indent + 1)
        _call(self._typedef, "show_tree", indent + 1)
        self._type.show_tree(indent + 1)


class VoidType(Type):
    def check(self) -> Any:
        return None

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        self.cdl_error2(
            locale, "T1007 $1: void type variable cannot have initializer", ident
        )

    def get_type_str(self) -> str:
        return f"{super().get_type_str()}void"

    def get_type_str_post(self) -> str:
        return ""

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"VoidType {self.locale_str()}")
        super().show_tree(indent + 1)


class BoolType(Type):
    def check(self) -> Any:
        return None

    def get_type_str(self) -> str:
        return f"{super().get_type_str()}bool_t"

    def get_type_str_post(self) -> str:
        return ""

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"BoolType {self.locale_str()}")
        super().show_tree(indent + 1)


class IntType(Type):
    """@bit_size:: -11: char, -1: char_t, -2: short, -3: int, -4: long, -5: long long, 8, 16, 32, 64, 128
    @sign:: :SIGNED, :UNSIGNED, nil
    """

    def __init__(self, bit_size: int) -> None:
        super().__init__()
        self._bit_size = bit_size
        self._sign: Any = None

    def set_sign(self, sign: Any, b_uint: bool = False) -> None:
        if truthy(self._sign):
            if self._sign != sign:
                self.cdl_error("T1008 ambigous signed or unsigned")
        elif b_uint is False and self._bit_size > 0:
            if sign == Y.SIGNED:
                self.cdl_warning(
                    "W2001 signed int$1_t: obsolete. use int$2_t",
                    self._bit_size,
                    self._bit_size,
                )
            else:
                self.cdl_warning(
                    "W2002 unsinged int$1_t: obsolete. use uint$2_t",
                    self._bit_size,
                    self._bit_size,
                )

        self._sign = sign

        if self._sign != Y.SIGNED and self._sign != Y.UNSIGNED:
            raise RubyRuntimeError(f"set_sign: unknown sign: {to_s(self._sign)}")

    def check(self) -> Any:
        return None

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        from tecsgen.core.expression import C_EXP, Expression
        from tecsgen.core.generator import Token
        from tecsgen.core.value import FloatVal, IntegerVal

        val = initializer  # C_EXP, Array
        if type(val) is Expression:
            val = val.eval_const2(None, attribute)
            # 評価の結果 C_EXP や Array となる可能性がある

        if type(val) is Token:  # StringVal 導入により、もはや Token は来ないはず
            self.cdl_error2(locale, "T1009 $1: $2: not integer", ident, val)
            return
        elif isinstance(val, C_EXP):
            return
        elif isinstance(val, FloatVal):
            self.cdl_error2(
                locale, "T1011 $1: need cast to assign float to integer", ident
            )
            return
        elif type(val) is list:
            self.cdl_error2(
                locale, "T1017 $1: unsuitable initializer for scalar type", ident
            )
            return
        elif val is None:
            self.cdl_error2(locale, "T1010 $1: initializer is not constant", ident)
            return

        if not isinstance(val, IntegerVal):
            self.cdl_error2(locale, "T1012 $1: $2: not integer", ident, val)
            return

        v = val.to_i()
        mx = self.get_max()
        mn = self.get_min()
        dbg_print(
            f"sign={to_s(self._sign)} ident={to_s(ident)} val={v} max={to_s(mx)} min={to_s(mn)}\n"
        )

        if mx is not None and v > mx:
            if self._sign == Y.SIGNED or self._sign is None:
                self.cdl_error2(locale, "T1013 $1: too large (max=$2)", ident, mx)
            else:
                self.cdl_error2(locale, "T1016 $1: too large (max=$2)", ident, mx)

        if mn is not None and v < mn:
            if self._sign == Y.SIGNED or self._sign is None:
                self.cdl_error2(
                    locale, "T1014 $1: too large negative value (min=$2)", ident, mn
                )
            else:
                self.cdl_error2(locale, "T1015 $1: negative value for unsigned", ident)

    def check_and_clip(self, in_val: Any, from_type: Any = Y.IntType) -> int:
        """最大値、最小値をチェックしてクリップする（キャスト演算）。

        in_val:: IntegerVal, FloatVal: この型にキャストする値
        from_type:: Symbol: :IntType, :FloatType  IntType の場合はビット数でクリップ、FloatType の場合は最大値でクリップ
        """
        bit_size = self.get_bit_size()

        if bit_size == -1:
            bit_size = 8
        val = rb_to_i(in_val)
        mx = self.get_max()
        mn = self.get_min()
        if mx is not None and val > mx:
            if from_type == Y.IntType:
                rval = ((1 << bit_size) - 1) & val  # bit 数でクリップ
            else:
                rval = mx  # 最大値でクリップ (FloatType)
            self.cdl_warning(
                "W2003 $1: too large to cast to $2, clipped($3)",
                in_val,
                self.get_type_str(),
                rval,
            )
        elif mn is not None and val < mn:
            if from_type == Y.IntType:
                rval = ((1 << bit_size) - 1) & val
                dbg_print(
                    f"check_and_clip: negative={to_s(in_val)} to unsigned={rval}  "
                    f"{(1 << bit_size) - 1} bit_size={bit_size}\n"
                )
            else:
                rval = mn
            if self._sign == Y.SIGNED or self._sign is None:
                self.cdl_warning(
                    "W2004 $1: too small to cast to $2, clipped($3)",
                    in_val,
                    self.get_type_str(),
                    rval,
                )
            else:  # @sign == :UNSIGNED || @sign == nil (char の場合)
                self.cdl_warning(
                    "W2005 $1: negative value for unsigned: convert to $2", in_val, rval
                )
        else:
            rval = val
        return rval

    def get_min(self) -> int | None:
        if self._sign == Y.SIGNED or self._sign is None:
            bit_sz = (
                8 if self._bit_size == -1 else self._bit_size
            )  # char_t は、有符号に扱う
            if bit_sz in (8, 16, 32, 64, 128):
                return -(1 << (bit_sz - 1))
            return None  # -1, -2, -3, -4, -5, -11
        return 0  # @sign == :UNSIGNED

    def get_max(self) -> int | None:
        if self._bit_size == -1:
            if self._sign is None:
                return 255  # char_t は、無符号に扱う
            bit_sz = 8
        else:
            bit_sz = self._bit_size
        if self._sign == Y.SIGNED or self._sign is None:
            if bit_sz in (8, 16, 32, 64, 128):
                return (1 << (bit_sz - 1)) - 1
            return None  # -1, -2, -3, -4, -5, -11
        # @sign == :UNSIGNED
        if bit_sz in (8, 16, 32, 64, 128):
            return (1 << bit_sz) - 1
        return None  # -2, -3, -4, -5, -11

    def get_type_str(self) -> str:
        """C 言語における型名（修飾子付き）。"""
        s = super().get_type_str()

        if self._sign == Y.SIGNED:
            sign = ""
            sign_l = "signed "
        elif self._sign == Y.UNSIGNED:
            sign = "u"
            sign_l = "unsigned "
        else:
            sign = ""
            sign_l = ""

        bs = self._bit_size
        if bs == -1:  # char_t 型
            if self._sign == Y.SIGNED:
                sign = "s"
            s = f"{s}{sign}char_t"
        elif bs == -11:  # char 型(obsolete)
            s = f"{s}{sign_l}char"
        elif bs == -2:  # short 型
            s = f"{s}{sign_l}short"
        elif bs == -3:  # int 型
            s = f"{s}{sign_l}int"
        elif bs == -4:  # long 型
            s = f"{s}{sign_l}long"
        elif bs == -5:  # long long 型
            s = f"{s}{sign_l}long long"
        elif bs in (8, 16, 32, 64, 128):  # int16, int32, int64, int128 型
            s = f"{s}{sign}int{bs}_t"
        return s

    def get_type_str_post(self) -> str:
        """C 言語における型名（後置文字列）。"""
        return ""

    def get_bit_size(self) -> int:
        return self._bit_size

    def get_sign(self) -> Any:
        return self._sign

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"{to_s(type(self))} bit_size={self._bit_size} sign={to_s(self._sign)} "
            f"const={to_s(self._b_const)} volatile={to_s(self._b_volatile)} {self.locale_str()}"
        )
        super().show_tree(indent + 1)


class FloatType(Type):
    """@bit_size:: 32, 64, (80), -32, -64, -128"""

    def __init__(self, bit_size: int) -> None:
        super().__init__()
        self._bit_size = bit_size

    def check(self) -> Any:
        return None

    # mikan Float 型の C_EXP 対応 (generate.rb にも変更必要)
    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        from tecsgen.core.expression import C_EXP, Expression
        from tecsgen.core.generator import Token
        from tecsgen.core.value import FloatVal, IntegerVal

        val = initializer
        if type(val) is Expression:
            val = val.eval_const2(None, attribute)
            # 評価の結果 C_EXP や Array となる可能性がある

        if type(val) is Token:
            self.cdl_error2(locale, "T1018 $1: $2: not number", ident, val)
            return
        elif type(val) is list:
            self.cdl_error2(
                locale, "T1020 $1: unsuitable initializer for scalar type", ident
            )
            return
        elif type(val) is C_EXP:
            return
        elif val is None:
            self.cdl_error2(locale, "T1019 $1: initializer is not constant", ident)
            return
        elif not isinstance(val, IntegerVal) and not isinstance(val, FloatVal):
            self.cdl_error2(locale, "T1037 $1: not number", ident)
            return
        return

    def get_type_str(self) -> str:
        s = super().get_type_str()
        bs = self._bit_size
        if bs == 32:
            s = f"{s}float32_t"
        elif bs == 64:
            s = f"{s}double64_t"
        elif bs == -32:
            s = f"{s}float"
        elif bs == -64:
            s = f"{s}double"
        elif bs == -128:
            s = f"{s}long double"
        return s

    def get_type_str_post(self) -> str:
        return ""

    def get_bit_size(self) -> int:
        return self._bit_size

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"FloatType bit_size={self._bit_size} qualifier={to_s(self._qualifier)} {self.locale_str()}"
        )
        super().show_tree(indent + 1)


class EnumType(Type):  # mikan
    """@bit_size:: -1: enum, 8, 16, 32, 64, 128 / @element:: [] / @element_val:: []"""

    def __init__(self, bit_size: int) -> None:
        super().__init__()
        self._bit_size = bit_size

    def check(self) -> Any:
        return None  # mikan enum check

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"EnumType bit_size={self._bit_size} qualifier={to_s(self._qualifier)} {self.locale_str()}"
        )
        super().show_tree(indent + 1)


class StructType(StructTypeGenerate, Type):
    """@tag:: / @b_define:: true if define, false if refer / @members_decl:: NamedList
    @definition:: StructType / @b_has_pointer_member:: bool / @b_has_sized_pointer_member:: bool
    @b_has_unsized_string_member:: bool / @b_hasTag:: bool
    @member_types_symbol:: Symbol : tag が無い時のみ設定 (それ以外では nil)
    """

    _structtype_current_stack: ClassVar[list[Any]] = []
    _structtype_current_sp: ClassVar[int] = -1

    # tag なし struct
    _no_struct_tag_num: ClassVar[int] = 0
    _no_tag_struct_list: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        StructType._structtype_current_stack = []
        StructType._structtype_current_sp = -1
        StructType._no_struct_tag_num = 0
        StructType._no_tag_struct_list = {}

    def __init__(self, tag: Any = None) -> None:
        from tecsgen.core.generator import _set_at

        super().__init__()
        self._tag = tag
        self._b_hasTag = truthy(tag)
        StructType._structtype_current_sp += 1
        _set_at(
            StructType._structtype_current_stack,
            StructType._structtype_current_sp,
            self,
        )
        self._b_has_pointer_member = False
        self._b_has_sized_pointer_member = False
        self._b_has_unsized_string_member = False
        self._member_types_symbol: Any = None

    @staticmethod
    def _current() -> Any:
        from tecsgen.core.generator import _get_at

        return _get_at(
            StructType._structtype_current_stack, StructType._structtype_current_sp
        )

    @dualmethod
    def set_define(cls, b_define: Any) -> None:
        StructType._current().set_define(b_define)

    @set_define.instance
    def set_define(self, b_define: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.syntaxobj.namedlist import NamedList

        self._b_define = b_define
        if truthy(self._b_define):
            self._members_decl = NamedList(None, f"in struct {to_s(self._tag)}")
        else:
            self._definition = Namespace.find_tag(self._tag)

    @dualmethod
    def new_member(cls, member_decl: Any) -> None:
        StructType._current().new_member(member_decl)

    @new_member.instance
    def new_member(self, member_decl: Any) -> None:
        member_decl.set_owner(self)  # Decl (StructType)
        self._members_decl.add_item(member_decl)
        if member_decl.get_type().has_pointer():
            self._b_has_pointer_member = True
        if member_decl.get_type().has_sized_pointer():
            self._b_has_sized_pointer_member = True
        if member_decl.get_type().has_unsized_string():
            self._b_has_unsized_string_member = True

    def check(self) -> Any:
        return None

    def check_struct_tag(self, kind: Any) -> None:
        """構造体のタグをチェックする（declarator の時点でチェックする）。"""
        from tecsgen.core.componentobj.namespace import Namespace

        if self._tag is None:
            return
        st = Namespace.find_tag(self._tag)
        if st is None:
            self.cdl_error("T1022 struct $1: not defined", self._tag)

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.expression import C_EXP, Expression

        st = Namespace.find_tag(self._tag)
        if st is None:
            self.cdl_error2(locale, "T1023 struct $1: not defined", self._tag)
            return

        # 初期化子が式の場合、型（タグ）が一致するかチェック
        if type(initializer) is Expression:
            t = initializer.get_type(attribute)
            if not isinstance(t, StructType):
                s = t.get_type_str() if truthy(t) else "unknown"
                self.cdl_error2(
                    locale,
                    "T1038 $1: initializer type mismatch. '$2' & '$3'",
                    ident,
                    self.get_type_str(),
                    s,
                )
            elif self._tag != t.get_name():
                self.cdl_error2(
                    locale,
                    "T1039 $1: struct tag mismatch $2 and $3",
                    ident,
                    self._tag,
                    t.get_name(),
                )
            initializer = initializer.eval_const(attribute)

        if type(initializer) is list:
            for i, d in enumerate(st.get_members_decl().get_items()):
                if i < len(initializer) and truthy(initializer[i]):
                    d.get_type().check_init(
                        locale,
                        f"{to_s(ident)}.{to_s(d.get_identifier())}",
                        initializer[i],
                        kind,
                    )
        elif type(initializer) is C_EXP:
            pass  # C_EXP は 無常件に OK
        else:
            self.cdl_error2(
                locale, "T1024 $1: unsuitable initializer for struct", ident
            )

    @dualmethod
    def end_of_parse(cls) -> None:
        StructType._current().end_of_parse()
        StructType._structtype_current_sp -= 1

    @end_of_parse.instance
    def end_of_parse(self) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        if (
            self._members_decl is None
        ):  # @b_define = false またはメンバーのない構造体（エラー）
            return
        for md in self._members_decl.get_items():
            size = md.get_size_is()
            if truthy(size):
                val = size.eval_const(self._members_decl)
                if val is None:
                    t = size.get_type(self._members_decl)
                    if not isinstance(t, IntType):
                        self.cdl_error("T1025 size_is argument is not integer type")
            count = md.get_count_is()
            if truthy(count):
                val = count.eval_const(self._members_decl)
                if val is None:
                    t = count.get_type(self._members_decl)
                    if not isinstance(t, IntType):
                        self.cdl_error("T1026 count_is argument is not integer type")
            string = md.get_string()
            if _is_minus1(string):
                pass  # 長さ指定なし
            elif truthy(string):
                val = string.eval_const(self._members_decl)
                if val is None:
                    t = string.get_type(self._members_decl)
                    if not isinstance(t, IntType):
                        self.cdl_error("T1027 string argument is not integer type")

        if self._tag is None:
            self._member_types_symbol = self.get_member_types_symbol()
            prev = StructType._no_tag_struct_list.get(self._member_types_symbol)
            if truthy(prev):
                self._tag = prev
            else:
                self._tag = sym(f"TAG_{StructType._no_struct_tag_num}_TECS_internal__")
                StructType._no_struct_tag_num += 1
                StructType._no_tag_struct_list[self._member_types_symbol] = self._tag
                Namespace.new_structtype(self)
        elif truthy(self._b_define):
            Namespace.new_structtype(self)

    def get_name(self) -> Any:
        return self._tag

    def get_type_str(self) -> str:  # mikan struct get_type_str
        s = super().get_type_str()

        if self._b_hasTag:
            # typedef struct tag StructType; の形式の場合
            # struct の本体は、別に生成される
            return f"{s}struct {to_s(self._tag)}"

        # typedef struct { int a; } StructType; の形式の場合
        s += "struct {"
        for i in self._members_decl.get_items():
            s += (
                f"{i.get_type().get_type_str()} {to_s(i.get_name())}"
                f"{i.get_type().get_type_str_post()};"
            )
        s += "} "
        return s

    def get_type_str_post(self) -> str:
        return ""

    def get_members_decl(self) -> Any:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.syntaxobj.namedlist import NamedList

        if truthy(self._members_decl):
            return self._members_decl

        st = Namespace.find_tag(self._tag)
        if truthy(st):
            return st.get_members_decl()

        # 不完全型の場合。
        # import_C の中では構造体のメンバー定義がないものもありうる.
        # TECS CDL では、構造体メンバーを先に定義する必要があり、ここへは来ないはず。
        return NamedList(None, f"in struct {to_s(self._tag)}")

    def has_pointer(self) -> bool:
        if truthy(self._definition):
            return self._definition.has_pointer()
        return self._b_has_pointer_member

    def has_sized_pointer(self) -> bool:
        if truthy(self._definition):
            return self._definition.has_sized_pointer()
        return self._b_has_sized_pointer_member

    def has_unsized_string(self) -> bool:
        if truthy(self._definition):
            return self._definition.has_unsized_string()
        return self._b_has_unsized_string_member

    def same(self, another: Any) -> bool:  # Ruby: same?
        """同じ構造体かどうかチェックする（すべてのメンバの名前と型が一致する）。"""
        md = another.get_members_decl()
        if self._members_decl is None or md is None:
            return False

        md1 = self._members_decl.get_items()
        md2 = md.get_items()
        if len(md1) != len(md2):
            return False

        for a, b in zip(md1, md2, strict=True):
            if (
                a.get_name() != b.get_name()
                or a.get_type().get_type_str() != b.get_type().get_type_str()
                or a.get_type().get_type_str_post() != b.get_type().get_type_str_post()
            ):
                return False
        return True

    def get_member_types_symbol(self) -> Any:
        mts = ""
        for member in self._members_decl.get_items():
            mts += (
                member.get_type().get_type_str()
                + member.get_type().get_type_str_post()
                + ";"
            )
        return sym(mts)

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"StructType tag: {to_s(self._tag)} qualifier={to_s(self._qualifier)} "
            f"has_pointer={to_s(self._b_has_pointer_member)} {self.locale_str()}"
        )
        super().show_tree(indent + 1)
        if truthy(self._b_define):
            self._members_decl.show_tree(indent + 1)


class FuncType(Type):
    """@paramlist:: ParamList / @type:: return type / @b_oneway:: bool
    @has_in / @has_inout / @has_out / @has_send / @has_receive:: bool
    """

    def __init__(self, paramlist: Any = None) -> None:
        from tecsgen.core.syntaxobj.paramlist import ParamList

        super().__init__()

        self._has_in = False
        self._has_inout = False
        self._has_out = False
        self._has_send = False
        self._has_receive = False

        self._paramlist = paramlist
        self._b_oneway = False
        if truthy(paramlist):
            paramlist.check_param()
        else:
            self._paramlist = ParamList(None)
        self._paramlist.set_owner(self)  # ParamList
        for p in self._paramlist.get_items():
            d = p.get_direction()
            if d == Y.IN:
                self._has_in = True
            elif d == Y.INOUT:
                self._has_inout = True
            elif d == Y.OUT:
                self._has_out = True
            elif d == Y.SEND:
                self._has_send = True
            elif d == Y.RECEIVE:
                self._has_receive = True
            else:
                raise RubyRuntimeError("unkown direction")

    def check(self) -> Any:  # 意味的誤りがあれば、文字列を返す
        if type(self._type) is ArrayType:  # 配列を返す関数
            return "function returning array"
        if type(self._type) is FuncType:  # 関数を返す関数
            return "function returning function"
        return self._type.check()  # 関数の return する型のチェック

    def check_struct_tag(self, kind: Any) -> None:
        self._type.check_struct_tag(kind)
        # ParamDecl でもチェックされるので、ここではチェックしない

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        self.cdl_error2(locale, "T1028 $1: cannot initialize function pointer", ident)

    def set_type(self, type_: Any) -> None:
        if not truthy(self._type):
            self._type = type_
        else:
            self._type.set_type(type_)

    def get_type(self) -> Any:
        """return type を返す（get_return_type とすべきだった）。"""
        return self._type

    def get_type_str(self) -> str:
        return self._type.get_type_str()

    def get_type_str_post(self) -> str:
        # 型だけを返す (仮引数の名前を含めない)
        return self._paramlist.to_str(False)

    def get_paramlist(self) -> Any:
        return self._paramlist

    def set_oneway(self, b_oneway: Any) -> None:
        self._b_oneway = b_oneway

        if (
            self._type.get_type_str() != "ER" and self._type.get_type_str() != "void"
        ) or self._type.get_type_str_post() != "":
            self.cdl_error(
                "T1029 oneway function cannot return type '$1$2', 'void' or 'ER' is permitted",
                self._type.get_type_str(),
                self._type.get_type_str_post(),
            )

        if truthy(self._paramlist):
            for p in self._paramlist.get_items():
                if p.get_direction() != Y.IN and p.get_direction() != Y.SEND:
                    self.cdl_error(
                        "T1030 oneway function cannot have $1 parameter for '$2'",
                        p.get_direction(),
                        p.get_name(),
                    )

    def is_oneway(self) -> Any:  # Ruby: is_oneway?
        return self._b_oneway

    def need_PPAllocator(self, b_opaque: bool = False) -> bool:
        """Push Pop Allocator が必要か？"""
        if truthy(self._b_oneway) or b_opaque:
            return self._paramlist.need_PPAllocator(b_opaque)
        return False

    def has_in(self) -> bool:  # Ruby: has_in?
        return self._has_in

    def has_inout(self) -> bool:
        return self._has_inout

    def has_out(self) -> bool:
        return self._has_out

    def has_send(self) -> bool:
        return self._has_send

    def has_receive(self) -> bool:
        return self._has_receive

    def has_inward(self) -> bool:
        """入力方向のパラメータを持つか。"""
        return self._has_in or self._has_inout or self._has_send

    def has_outward(self) -> bool:
        """出力方向のパラメータを持つか。"""
        return self._has_inout or self._has_out or self._has_receive

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        if truthy(self._b_oneway):
            rb_puts(f"FunctType:  oneway=true {self.locale_str()}")
        else:
            rb_puts(f"FunctType:  oneway=false {self.locale_str()}")
        super().show_tree(indent + 1)
        if truthy(self._paramlist):
            self._paramlist.show_tree(indent + 1)
        rb_print("  " * (indent + 1))
        rb_puts("return type:")
        self._type.show_tree(indent + 2)


class ArrayType(HasType, Type):
    """@type:: element type / @subscript:: Expression, nil if '[]'"""

    def __init__(self, subscript: Any = None) -> None:
        super().__init__()
        self._subscript = subscript
        self.initHasType()

    def set_type(self, type_: Any) -> None:
        if not truthy(self._type):
            self._type = type_
        else:
            self._type.set_type(type_)

    def set_qualifier(self, qualifier: Any) -> None:
        """qualifier(const, volatile) の設定。"""
        self.clone_type()
        self._type.set_qualifier(qualifier)
        super().set_qualifier(qualifier)

    def is_const(self) -> bool:
        """配列要素が const なら const。"""
        return self._type.is_const()

    def is_volatile(self) -> bool:
        """配列要素が volatile なら volatile。"""
        return self._type.is_volatile()

    def get_type(self) -> Any:
        return self._type

    def get_subscript(self) -> Any:
        return self._subscript

    def get_type_str(self) -> str:
        return f"{self._type.get_type_str()}"

    def get_type_str_post(self) -> str:
        if truthy(self._subscript):
            return f"[{to_s(self._subscript.eval_const(None))}]{self._type.get_type_str_post()}"
        return f"[]{self._type.get_type_str_post()}"

    def check(self) -> Any:  # 意味的誤りがあれば、文字列を返す
        if type(self._type) is FuncType:  # 関数の配列
            return "array of function"
        if type(self._type) is ArrayType and not truthy(self._type.get_subscript()):
            return "subscript not specified"  # 添数なし配列の配列
        return self._type.check()  # 配列要素の型をチェック

    def check_struct_tag(self, kind: Any) -> None:
        self._type.check_struct_tag(kind)

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        if type(initializer) is list:
            # 要素数が指定されている場合、初期化要素数をチェック
            if truthy(self._subscript):
                n_sub = self._subscript.eval_const(None)
                if truthy(n_sub) and len(initializer) > n_sub:
                    self.cdl_error2(
                        locale,
                        "T9999 $1: too many initializer, $2 for $3",
                        ident,
                        len(initializer),
                        n_sub,
                    )
            for index, i in enumerate(initializer):
                self._type.check_init(locale, f"{to_s(ident)}[{index}]", i, kind, None)
        else:
            self.cdl_error2(locale, "T1031 $1: unsuitable initializer for array", ident)

    def has_pointer(self) -> bool:
        return self._type.has_pointer()

    def has_sized_pointer(self) -> bool:
        return self._type.has_sized_pointer()

    def has_unsized_string(self) -> bool:
        return self._type.has_unsized_string()

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"ArrayType: {self.locale_str()}")
        super().show_tree(indent + 1)
        rb_print("  " * (indent + 1))
        rb_puts("type:")
        self._type.show_tree(indent + 2)
        rb_print("  " * (indent + 1))
        rb_puts("subscript:")
        if truthy(self._subscript):
            self._subscript.show_tree(indent + 2)
        else:
            rb_print("  " * (indent + 2))
            rb_puts("no subscript")


class PtrType(HasType, Type):
    """@type:: refer to / @size:: Expr, or nil / @count:: Expr, or nil
    @string:: Expr or -1(if size not specified), or nil
    """

    def __init__(self, referto: Any = None) -> None:
        super().__init__()
        self._type = referto
        self._size: Any = None
        self._count: Any = None
        self._string: Any = None
        self.initHasType()

    def set_type(self, type_: Any) -> None:
        if not truthy(self._type):
            self._type = type_
        else:
            self._type.set_type(type_)  # 枝先の type を設定

    def get_type_str(self) -> str:
        parenthes = "(" if isinstance(self._type, (ArrayType, FuncType)) else ""
        return f"{self._type.get_type_str()}{parenthes}*"

    def get_type_str_post(self) -> str:
        parenthes = ")" if isinstance(self._type, (ArrayType, FuncType)) else ""
        return f"{parenthes}{self._type.get_type_str_post()}"

    def check(self) -> Any:  # 意味的誤りがあれば、文字列を返す
        if self._type is None:
            return None
        return self._type.check()

    def check_struct_tag(self, kind: Any) -> None:
        if (
            kind != Y.MEMBER
        ):  # 構造体メンバーの場合、ポインタの先の構造体タグをチェックしない
            self._type.check_struct_tag(kind)

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        from tecsgen.core.c_types import CDefinedType
        from tecsgen.core.expression import C_EXP, Expression
        from tecsgen.core.value import IntegerVal, PointerVal, StringVal

        if type(initializer) is Expression:
            val = initializer.eval_const2(None, attribute)
            if isinstance(val, PointerVal):
                t2 = val.get_type()  # PtrType
                t1: Any = self
                while isinstance(t1, PtrType) and isinstance(t2, PtrType):
                    t1 = t1.get_type()
                    t2 = t2.get_type()
                    if type(t1) is type(t2) and t1.get_bit_size() == t2.get_bit_size():
                        pass
                    elif (
                        (isinstance(t1, CDefinedType) or isinstance(t2, CDefinedType))
                        and t1.get_type_str() == t2.get_type_str()
                        and truthy(t1.get_type_str_post())
                        and truthy(t2.get_type_str_post())
                    ):
                        pass  # int8_t などが、一方は .h に定義されているケース
                    else:
                        self.cdl_error2(
                            locale, "T1032 $1: incompatible pointer type", ident
                        )
                        break
            elif isinstance(val, IntegerVal):
                if val.to_i() != 0:
                    self.cdl_error2(
                        locale,
                        "T1033 $1: need cast to assign integer to pointer",
                        ident,
                    )
            elif isinstance(val, StringVal):
                # 文字列定数  mikan L"wide string"
                if (
                    self._type.get_bit_size() != -1 and self._type.get_bit_size() != -11
                ):  # -1: char_t
                    self.cdl_error2(
                        locale, "T1034 $1: unsuitable string constant", ident
                    )
            elif type(val) is list:
                for i, ini in enumerate(val):
                    self._type.check_init(
                        locale, f"{to_s(ident)}[{i}]", ini, kind, None
                    )
            elif type(val) is C_EXP:
                pass  # tecsgen V1.8.RC11 から C_EXP も可とする
            else:
                self.cdl_error2(
                    locale, "T1035 $1: unsuitable initializer for pointer", ident
                )
        elif type(initializer) is list:
            if self._size is None and self._count is None:
                self.cdl_error2(
                    locale,
                    "T9999 $1: non-size_is pointer cannot have array initializer",
                    ident,
                )
            for i, ini in enumerate(initializer):
                self._type.check_init(locale, f"{to_s(ident)}[{i}]", ini, kind, None)
        elif type(initializer) is C_EXP:
            pass
        else:
            self.cdl_error2(
                locale, "T1036 $1: unsuitable initializer for pointer", ident
            )

    def get_referto(self) -> Any:
        self.clone_type()
        return self._type

    def set_scs(
        self,
        size: Any,
        count: Any,
        string: Any,
        max: Any = None,
        b_nullable: Any = False,
    ) -> None:
        self._size = size
        self._count = count
        self._max = max
        self._b_nullable = b_nullable

        # string は最も左側の ptr に作用する
        if isinstance(self._type, PtrType):
            # ptr_level が 2 以上であることは ParamDecl#initializer でチェックされる
            self.clone_type()
            self._type.set_scs(None, None, string, None, False)
        elif isinstance(self._type, VoidType) and (
            truthy(size) or truthy(count) or truthy(string)
        ):
            s = ""
            if truthy(size):
                s = "size_is"
            if truthy(count):
                s += ", "  # Ruby 版は str が "" でも真なので、常に ", " を付ける
                s += "count_is"
            if truthy(string):
                s += ", "
                s += "string"
            self.cdl_error("T1040 $1 specified for void pointer type", s)
        else:
            self._string = string

        if self._size is not None and self._b_nullable is not False:
            self.cdl_error(
                "T9999 size_is & nullable cannot be specified simultaneously. "
                "If size is zero, pointer must be null"
            )

    def clear_max(self) -> None:
        self._max = None

    def get_size(self) -> Any:
        return self._size

    def get_count(self) -> Any:
        return self._count

    def get_string(self) -> Any:
        return self._string

    def get_max(self) -> Any:
        """size_is の最大値。"""
        return self._max

    def is_nullable(self) -> Any:  # Ruby: is_nullable?
        return self._b_nullable

    def get_type(self) -> Any:
        self.clone_type()
        return self._type

    def has_pointer(self) -> bool:
        return True

    def has_sized_pointer(self) -> bool:
        from tecsgen.core.expression import Expression

        return (
            self._size is not None
            or self._count is not None
            or type(self._string) is Expression
            or self._type.has_sized_pointer()
        )

    def has_unsized_string(self) -> bool:
        return _is_minus1(self._string) or self._type.has_unsized_string()

    def show_tree(self, indent: int) -> None:
        from tecsgen.core.expression import Expression

        rb_print("  " * indent)
        rb_puts(
            f"PtrType: qualifier={to_s(self._qualifier)}, nullable={to_s(self._b_nullable)} "
            f"{self.locale_str()}"
        )
        super().show_tree(indent + 1)
        rb_print("  " * (indent + 1))
        if truthy(self._size):
            rb_print(f"size={to_s(self._size)}, ")
        else:
            rb_print("size=nil, ")
        if truthy(self._max):
            rb_print(f"max={to_s(self._size)}, ")
        else:
            rb_print("max=nil, ")
        if truthy(self._count):
            rb_print(f"count={to_s(self._count)}, ")
        else:
            rb_print("count=nil, ")
        if truthy(self._string):
            if type(self._string) is Expression:
                rb_print(f"string={to_s(self._string)}\n")
            else:
                rb_print("string=yes\n")
        else:
            rb_print("string=nil\n")

        rb_print("  " * (indent + 1))
        rb_puts("type:")
        self._type.show_tree(indent + 2)


class DescriptorType(Type):
    """動的結合で渡すデスクリプタ型。@signature_nsp::NamespacePath

    Ruby 版の initialize は super を呼ばないので、@locale を持たない。
    """

    _descriptors: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        DescriptorType._descriptors = {}

    def __init__(self, signature_nsp: Any) -> None:
        self._signature_nsp = signature_nsp
        DescriptorType._descriptors[self] = False

    def get_type_str(self) -> str:
        return f"Descriptor( {to_s(self._signature_nsp.get_global_name())} )"

    def get_type_str_post(self) -> str:
        return ""

    def set_qualifier(self, qualifier: Any) -> None:
        # Ruby 版は未定義の変数 qualfier を参照して NameError になる
        raise RubyNameError(
            "undefined local variable or method `qualfier' for an instance of DescriptorType"
        )

    def check(self) -> Any:
        return None

    def check_init(
        self,
        locale: Any,
        ident: Any,
        initializer: Any,
        kind: Any,
        attribute: Any = None,
    ) -> None:
        if kind == Y.PARAMETER:
            pass  # 引数は初期化できない
        else:
            self.cdl_error2(locale, "T9999 Descriptor cannot be used for $1", kind)

    @dualmethod
    def check_signature(cls) -> None:
        for desc, val in list(DescriptorType._descriptors.items()):
            if val is not True:
                desc.check_signature()
                DescriptorType._descriptors[desc] = True

    @check_signature.instance
    def check_signature(self) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.signature import Signature

        obj = Namespace.find(self._signature_nsp)
        if not isinstance(obj, Signature):
            self.cdl_error(
                "T9999 '$1': not signature or not found", to_s(self._signature_nsp)
            )
        elif obj.has_descriptor():
            pass

    def get_signature(self) -> Any:
        from tecsgen.core.componentobj.namespace import Namespace

        return Namespace.find(self._signature_nsp)


def _is_minus1(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x == -1


def _call(obj: Any, name: str, *args: Any) -> Any:
    """`obj.name(*args)`。obj が nil なら Ruby と同じ NoMethodError にする。"""
    if obj is None:
        from tecsgen.ruby_compat import no_method

        raise no_method(name, None)
    return getattr(obj, name)(*args)
