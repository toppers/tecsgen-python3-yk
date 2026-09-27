"""expression.rb の移植。式（`Expression`）と C_EXP。

式の要素（elements）は Ruby 版と同じく配列で、先頭が演算の種類（Symbol）。
例: `[:OP_ADD, lhs, rhs]`、`[:IDENTIFIER, NamespacePath]`、`[:INTEGER_CONSTANT, Token]`。
"""

from __future__ import annotations

import copy
import re
from typing import Any

from tecsgen.context import dbg_print
from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import (
    RubyArgumentError,
    RubyError,
    RubyNameError,
    RubyRuntimeError,
    Symbol,
    Y,
    gsub,
    rb_integer,
    rb_print,
    rb_puts,
    sprintf,
    str_hex,
    str_oct,
    to_s,
    truthy,
)

# 単項演算子（elements_check_dir_for_param の when 節）
_UNARY_OPS = (
    Y.OP_U_ASTER,
    Y.OP_SIZEOF_EXPR,
    Y.OP_SIZEOF_TYPE,
    Y.OP_U_PLUS,
    Y.OP_U_MINUS,
    Y.OP_U_TILDE,
    Y.OP_U_EXCLAM,
    Y.CAST,
    Y.OP_U_AMP,
    Y.PARENTHESES,
)
# 2項演算子
_BINARY_OPS = (
    Y.OP_SUBSC,
    Y.OP_DOT,
    Y.OP_REF,
    Y.OP_MULT,
    Y.OP_DIV,
    Y.OP_REMAIN,
    Y.OP_ADD,
    Y.OP_SUB,
    Y.OP_LSFT,
    Y.OP_RSFT,
    Y.OP_LT,
    Y.OP_GT,
    Y.OP_LE,
    Y.OP_GE,
    Y.OP_EQ,
    Y.OP_NE,
    Y.OP_AND,
    Y.OP_EOR,
    Y.OP_OR,
    Y.OP_LAND,
    Y.OP_LOR,
)
_LITERALS = (
    Y.INTEGER_CONSTANT,
    Y.FLOATING_CONSTANT,
    Y.OCTAL_CONSTANT,
    Y.HEX_CONSTANT,
    Y.CHARACTER_LITERAL,
    Y.STRING_LITERAL_LIST,
    Y.BOOL_CONSTANT,
)
_LITERALS_NO_BOOL = _LITERALS[:-1]

# elements_to_s の2項演算子と、その C の表記
_BINARY_TO_S = {
    Y.OP_MULT: "*",
    Y.OP_DIV: "/",
    Y.OP_REMAIN: "%",
    Y.OP_ADD: "+",
    Y.OP_SUB: "-",
    Y.OP_LSFT: "<<",
    Y.OP_RSFT: ">>",
    Y.OP_LT: "<",
    Y.OP_GT: ">",
    Y.OP_LE: "<=",
    Y.OP_GE: ">=",
    Y.OP_EQ: "==",
    Y.OP_NE: "!=",
    Y.OP_AND: "&",
    Y.OP_EOR: "^",
    Y.OP_OR: "|",
    Y.OP_LAND: "&&",
    Y.OP_LOR: "||",
}
_UNARY_TO_S = {
    Y.OP_U_AMP: "&",
    Y.OP_U_ASTER: "*",
    Y.OP_U_PLUS: "+",
    Y.OP_U_MINUS: "-",
    Y.OP_U_TILDE: "~",
    Y.OP_U_EXCLAM: "!",
}
_BINARY_RPN = {
    Y.OP_MULT: "*",
    Y.OP_DIV: "/",
    Y.OP_REMAIN: "%",
    Y.OP_ADD: "+",
    Y.OP_SUB: "-",
    Y.OP_LSFT: "<<",
    Y.OP_RSFT: ">>",
    Y.OP_LT: "<",
    Y.OP_GT: ">",
    Y.OP_LE: "<=",
    Y.OP_GE: ">=",
    Y.OP_EQ: "==",
    Y.OP_NE: "!=",
    Y.OP_AND: "&",
    Y.OP_EOR: "^",
    Y.OP_OR: "|",
    Y.OP_LAND: "&&",
    Y.OP_LOR: "||",
}
_UNARY_RPN = {
    Y.OP_SIZEOF_EXPR: "#s",
    Y.OP_SIZEOF_TYPE: "#S",
    Y.OP_U_AMP: "#&",
    Y.OP_U_ASTER: "#*",
    Y.OP_U_PLUS: "#+",
    Y.OP_U_MINUS: "#-",
    Y.OP_U_TILDE: "#~",
    Y.OP_U_EXCLAM: "#!",
}

_ELEMETS_TYPO = (
    "undefined local variable or method `elemets' for an instance of Expression"
)


def _is_token(x: Any) -> bool:
    from tecsgen.core.generator import Token

    return type(x) is Token


class Expression(Node):
    """@elements: array / @b_in_C:Bool : import_C 内の式 / @b_checked:Bool : 式はチェックされている"""

    MAX_NEST_LEVEL = 64  # 簡易のループ検出（参照のネストを 64 まで許可する）

    def __init__(self, elements: Any, locale: Any = None) -> None:
        from tecsgen.core.generator import Generator

        super().__init__()
        if truthy(locale):
            self._locale = locale

        self._elements = elements
        self._b_in_C = Generator.parsing_C()
        self._b_checked = False

    def print(self) -> None:
        rb_puts(f"expr_string: {self.to_s()}")

    def to_s(self) -> str:
        """C 言語ソース向きの文字列を生成 (globa_name)。"""
        return self.elements_to_s(self._elements)

    def to_str(self, name_list: Any, pre: Any, post: Any) -> str:
        """C 言語ソース向きの文字列を生成 (globa_name)。"""
        return self.elements_to_s(self._elements, name_list, pre, post)

    def to_CDL_str(self) -> str:
        """CDL 表現の文字列を生成。"""
        return self.to_s()

    def eval_const(self, name_list: Any, name_list2: Any = None) -> Any:
        """定数式として評価する（トライしてみる）。

        name_list(NamedList|Nil): 式から参照可能なリスト。
        name_list2(NamedList|Nil): NamedList の要素は Decl (attribute, var) である。
        RETURN: 評価した定数。評価できなかった場合は nil を返す
        """
        from tecsgen.core.value import BoolVal, FloatVal, IntegerVal, PointerVal

        val = self.elements_eval_const(self._elements, name_list, name_list2, 0)
        self._b_checked = True
        if isinstance(val, IntegerVal):
            return val.to_i()
        if isinstance(val, FloatVal):
            return val.to_f()
        if isinstance(val, BoolVal):
            return val.to_i()
        if isinstance(val, PointerVal):
            return val.to_i()  # mikan エラー V1008 が発生してしまう
        # C_EXP, Array または nil ：そのまま返す
        return val

    def eval_const2(self, name_list: Any, name_list2: Any = None, nest: Any = 0) -> Any:
        """定数式として評価する2（IntegerVal, FloatVal をそのまま返す）。"""
        return self.elements_eval_const(self._elements, name_list, name_list2, nest)

    def get_type(self, namedList: Any) -> Any:
        """式の型を評価する。"""
        return self.elements_get_type(self._elements, namedList)

    def check_dir_for_param(self, namedList: Any, dir: Any, spec: Any) -> Any:
        return self.elements_check_dir_for_param(self._elements, namedList, dir, spec)

    def get_elements(self) -> Any:
        return self._elements

    def show_tree(self, indent: int) -> None:
        rb_puts("  " * indent + self.to_s())

    # --- private ------------------------------------------------------------

    def elements_to_s(
        self, elements: Any, name_list: Any = None, pre: Any = None, post: Any = None
    ) -> str:
        """式を文字列に変換する。"""
        if _is_token(elements):
            return to_s(elements)  # OP_DOT, OP_REF の右辺

        def sub(e: Any) -> str:
            return self.elements_to_s(e, name_list, pre, post)

        k = elements[0]
        if k == Y.IDENTIFIER:
            nsp = elements[1]
            if (
                nsp.is_name_only()
                and truthy(name_list)
                and truthy(name_list.get_item(nsp.get_name()))
            ):
                return f"{to_s(pre)}{to_s(nsp.get_name())}{to_s(post)}"
            return nsp.get_path_str()
        if k in _LITERALS:
            return to_s(elements[1])
        if k == Y.PARENTHESES:
            return f"({sub(elements[1])})"
        if k == Y.OP_SUBSC:
            return f"{sub(elements[1])}[{to_s(elements[2])}]"
        if k == Y.OP_DOT:
            return f"{sub(elements[1])}.{sub(elements[2])}"
        if k == Y.OP_REF:
            return f"{sub(elements[1])}->{sub(elements[2])}"
        if k == Y.OP_SIZEOF_EXPR:
            return f"sizeof({sub(elements[1])})"
        if k == Y.OP_SIZEOF_TYPE:
            return f"sizeof({to_s(elements[1])}) mikan"
        if k in _UNARY_TO_S:
            return f"{_UNARY_TO_S[k]}{sub(elements[1])}"
        if k == Y.CAST:
            return f"({elements[1].get_type_str()}){sub(elements[2])}"
        if k in _BINARY_TO_S:
            return f"{sub(elements[1])}{_BINARY_TO_S[k]}{sub(elements[2])}"
        if k == Y.OP_CEX:
            return f"{sub(elements[1])}?{sub(elements[2])}:{sub(elements[3])}"
        raise RubyNameError(_ELEMETS_TYPO)

    def get_rpn(self, param_list: Any = None, name_list2: Any = None) -> str:
        """逆ポーランド文字列化。param_list:: ParamlList  関数の引数リスト"""
        return self.elements_rpn(self._elements, param_list, name_list2)

    def elements_rpn(
        self, elements: Any, name_list: Any = None, name_list2: Any = None
    ) -> str:
        """逆ポーランド文字列化 (private)。

        Ruby 版の2項演算子の右辺は `elements_rpn( elements[2], "", name_list, name_list2 )` と
        引数が1つ多く、ArgumentError になる（そのまま再現する）。
        """
        if _is_token(elements):
            # Ruby 版の print は Expression#print（引数なし）なので ArgumentError になる
            raise RubyArgumentError("wrong number of arguments (given 1, expected 0)")

        k = elements[0]
        if k == Y.IDENTIFIER:
            nsp = elements[1]
            if nsp.is_name_only():
                for count, nm in enumerate(name_list.get_items()):
                    if nsp.get_name() == nm.get_name():
                        return f" ${count}"
                raise RubyRuntimeError("not found parameter")
            raise RubyRuntimeError("not unexpected parameter")
        if k in _LITERALS:
            return to_s(elements[1])
        if k == Y.PARENTHESES:
            return self.elements_rpn(elements[1], name_list, name_list2)
        if k == Y.OP_DOT:
            return self.elements_rpn(elements[1], name_list, name_list2) + " ."
        if k == Y.OP_REF:
            return self.elements_rpn(elements[1], name_list, name_list2) + " ->"
        if k in _UNARY_RPN:
            return (
                self.elements_rpn(elements[1], name_list, name_list2)
                + " "
                + _UNARY_RPN[k]
            )
        if k in (Y.OP_SUBSC, Y.CAST) or k in _BINARY_RPN:
            self.elements_rpn(elements[1], name_list, name_list2)
            raise RubyArgumentError(
                "wrong number of arguments (given 4, expected 1..3)"
            )
        if k == Y.OP_CEX:
            return (
                self.elements_rpn(elements[1], name_list, name_list2)
                + " "
                + self.elements_rpn(elements[2], name_list, name_list2)
                + " "
                + self.elements_rpn(elements[3], name_list, name_list2)
                + " ?:"
            )
        raise RubyNameError(_ELEMETS_TYPO)

    def elements_eval_const(
        self, elements: Any, name_list: Any, name_list2: Any = None, nest: Any = None
    ) -> Any:
        """定数式(elements)を評価する。評価できなかった場合は nil を返す。"""
        from tecsgen.core.cdl_types import BoolType
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.syntaxobj.decl import Decl
        from tecsgen.core.syntaxobj.paramdecl import ParamDecl
        from tecsgen.core.value import BoolVal, FloatVal, IntegerVal, StringVal

        k = elements[0]
        if k == Y.IDENTIFIER:
            nsp = elements[1]
            obj: Any = None
            if nsp.is_name_only():
                if truthy(name_list):
                    obj = name_list.get_item(nsp.get_name())
                if obj is None and truthy(name_list2):
                    obj = name_list2.get_item(nsp.get_name())

            # 見つからなければ定数定義から探す
            if obj is None:
                obj = Namespace.find(nsp)  # mikan namespace の対応 #1

            if obj is None:
                self.cdl_error("E1001 $1: not found", nsp.get_path_str())
                return None
            if type(obj) is Join:
                # Join の場合： cell の中の attribute, var, call のどれかが見つかった
                if type(obj.get_definition()) is not Decl:
                    self.cdl_error("E1002 $1: not constant (port)", nsp.get_path_str())
                    return None
                return obj.get_rhs().eval_const2(name_list, name_list2, nest)
            if type(obj) is not Decl:
                # Decl でない場合： 定数でもない
                if type(obj) is not ParamDecl:
                    # mikan paramdecl は無視する（ParamList から呼ばれたとき）
                    self.cdl_error("E1003 $1: not constant", nsp.get_path_str())
                else:
                    obj.referenced()
                return None
            # Decl
            obj.referenced()
            ini = obj.get_initializer()
            if ini is None:
                # 初期化子の存在しない変数   # mikan ここへくるのは、通常ありえないはず（未検証）
                return IntegerVal(0)
            if type(ini) is Expression or type(ini) is C_EXP:
                return ini.eval_const2(name_list, name_list2, nest)
            return ini  # Array の場合
        if k == Y.BOOL_CONSTANT:
            if elements[1] is True:
                return BoolVal(True)
            if elements[1] is False:
                return BoolVal(False)
            raise RubyError('uncaught throw "BOOL constant error"')
        if k == Y.INTEGER_CONSTANT:
            return IntegerVal(elements[1].val)
        if k == Y.FLOATING_CONSTANT:
            return FloatVal(elements[1].val)
        if k == Y.OCTAL_CONSTANT:
            return IntegerVal(str_oct(elements[1].val), elements[1].val)
        if k == Y.HEX_CONSTANT:
            return IntegerVal(str_hex(elements[1].val), elements[1].val)
        if k == Y.CHARACTER_LITERAL:
            return self._eval_character_literal(elements[1])
        if k == Y.STRING_LITERAL_LIST:
            return StringVal(elements[1])
        if k == Y.PARENTHESES:
            return self.elements_eval_const(elements[1], name_list, name_list2, nest)
        if k == Y.OP_SUBSC:
            self.cdl_error("E1004 cannot evaluate '[]' operator")
            return None
        if k == Y.OP_DOT:
            self.cdl_error("E1005 cannot evaluate '.' operator")
            return None
        if k == Y.OP_REF:
            self.cdl_error("E1006 cannot evaluate '->' operator")
            return None
        if k == Y.OP_SIZEOF_EXPR or k == Y.OP_SIZEOF_TYPE:
            if not self._b_checked:
                if truthy(self._b_in_C):
                    self.cdl_info(
                        "I9999 cannot evaluate 'sizeof' operator. this might causes later error."
                    )
                elif k == Y.OP_SIZEOF_EXPR:
                    self.cdl_error("E1007 cannot evaluate 'sizeof' operator")
                else:
                    self.cdl_error("E1008 cannot evaluate 'sizeof' operator")
            return None
        if k == Y.OP_U_AMP:
            self.cdl_error("E1009 cannot evaluate '&' operator")
            return None

        def ev(i: int) -> Any:
            return self.elements_eval_const(elements[i], name_list, name_list2, nest)

        if k == Y.OP_U_ASTER:
            val = ev(1)
            if not self.evaluable(val):
                return None
            return val
        if k == Y.OP_U_PLUS:
            val = ev(1)
            if not self.evaluable(val):
                return None
            return +val  # BaseVal はすべて +@ を持つ
        if k == Y.OP_U_MINUS:
            val = ev(1)
            if not self.evaluable(val):
                return None
            return -val
        if k == Y.OP_U_TILDE:
            val = ev(1)
            if not self.evaluable(val):
                return None
            if isinstance(val, IntegerVal):
                return ~val
            return None
        if k == Y.OP_U_EXCLAM:
            val = ev(1)
            if not self.evaluable(val):
                return None
            val = val.cast(BoolType())
            # nil は not に応答しない（respond_to?( "not" ) が偽）
            if val is None:
                return None
            return val.not_()
        if k == Y.CAST:
            val = ev(2)
            if not self.evaluable(val):
                return None
            return val.cast(elements[1])
        if k in _EVAL_BINARY:
            lhs = ev(1)
            rhs = ev(2)
            if not self.evaluable(rhs, lhs):
                return None
            return _EVAL_BINARY[k](lhs, rhs)
        if k == Y.OP_CEX:
            lhs = ev(1)
            mhs = ev(2)
            rhs = ev(3)
            if not self.evaluable(rhs, mhs, lhs):
                return None
            if truthy(_call(lhs.cast(BoolType()), "val")):
                return mhs
            return rhs
        return None

    def _eval_character_literal(self, token: Any) -> Any:
        from tecsgen.context import get_context
        from tecsgen.core.value import IntegerVal

        s = token.val.replace("'", "")
        length = len(
            s
        )  # Shift_JIS のときは文字数、それ以外はバイト数（1バイト＝1文字）
        if length == 1:
            total = 0
            # each_byte は、ファイルの文字コードでのバイト列をたどる
            for b in s.encode(get_context().file_codec, "surrogateescape"):
                total = total * 256 + b
            return IntegerVal(total, token.val)
        if s[0:1] == "\\":
            c = s[1:2]
            table = {"0": 0, "n": 10, "r": 13, "t": 15, "\\": 92}
            if c in table:
                return IntegerVal(table[c], token.val)
        rb_print(sprintf("len=%d c=%c\n", length, s[1:2] or "\0"))
        raise RubyNameError("uninitialized constant Expression::Error")

    def elements_get_type(self, elements: Any, namedList: Any) -> Any:
        from tecsgen.core.cdl_types import DefinedType

        t = self.elements_get_type_sub(elements, namedList)
        # 返された方が DefinedType の場合 元の型を返す
        if isinstance(t, DefinedType):
            t = t.get_type()
        return t

    def elements_get_type_sub(self, elements: Any, namedList: Any) -> Any:
        from tecsgen.core.cdl_types import BoolType, IntType, PtrType

        k = elements[0]
        if k == Y.IDENTIFIER:
            nsp = elements[1]
            paramdecl: Any
            if nsp.is_name_only() and truthy(namedList):  # 1202
                paramdecl = namedList.get_item(nsp.get_name())
            else:
                paramdecl = None
            if paramdecl is None or paramdecl is False:
                if truthy(namedList):  # 1202
                    self.cdl_error(
                        "E1012 $1: not found in parameter list", nsp.get_path_str()
                    )
                else:
                    # namedList = nil: initializer.get_type( attribute ) から呼ばれた場合
                    # この場合、E1001 が出るので、ここでは出さない
                    dbg_print(
                        f"elements_get_type_sub: {nsp.get_path_str()} not found (namedList==nil)"
                    )
                return IntType(32)  # dummy result
            return paramdecl.get_type()
        if k == Y.OP_U_ASTER:
            t = self.elements_get_type(elements[1], namedList)
            if not isinstance(t, PtrType):
                self.cdl_error("E1013 '*': operand is not pointer value")
                return IntType(8)  # IntType を返しておく
            return t.get_referto()
        if k in (Y.OP_U_PLUS, Y.OP_U_MINUS):
            # mikan operand が適切な型かチェックしていない
            return self.elements_get_type(elements[1], namedList)
        if k in (Y.OP_ADD, Y.OP_SUB, Y.OP_MULT, Y.OP_DIV, Y.OP_REMAIN):
            # mikan operand が適切な型かチェックしていない＆左辺の型を採用している
            return self.elements_get_type(elements[1], namedList)
        if k == Y.OP_U_TILDE:
            return self.elements_get_type(elements[1], namedList)
        if k in (Y.OP_AND, Y.OP_EOR, Y.OP_OR, Y.OP_LSFT, Y.OP_RSFT):
            return BoolType()
        if k == Y.OP_U_EXCLAM:
            return BoolType()
        if k in (
            Y.OP_LT,
            Y.OP_GT,
            Y.OP_LE,
            Y.OP_GE,
            Y.OP_EQ,
            Y.OP_NE,
            Y.OP_LAND,
            Y.OP_LOR,
            Y.OP_CEX,
            Y.CAST,
        ):
            self.cdl_error("E1014 $1: elements_get_type: sorry not supported", k)
        return None

    def elements_check_dir_for_param(
        self,
        elements: Any,
        namedList: Any,
        dir: Any,
        spec: Any,
    ) -> Any:
        """式が size_is, count_is, string の引数である場合の方向のチェック。

        Ruby 版の case 文は、単項演算子の when 節が行末のカンマで次の行に続いているため、
        `elements_check_dir_for_param( elements[1], ... )` の呼び出しが when の値になり、
        節の本体は空になる。そのため
        - 単項演算子のときは何もせず nil を返す
        - それより後の when 節（2項・3項演算子など）に当たるときは、先に左辺（elements[1]）を
          when の値として評価する（2項演算子の左辺は2回チェックされる）
        IDENTIFIER の節は nil を返すので、2項演算子の `&&` は右辺を評価しない。これらも再現する。
        """
        k = elements[0]
        if k == Y.IDENTIFIER:
            nsp = elements[1]
            if nsp.is_name_only():
                paramdecl = namedList.get_item(nsp.get_name())
            else:
                paramdecl = None

            if (
                paramdecl is None or paramdecl is False
            ):  # if nil already error in element_get_type
                return None

            direct = paramdecl.get_direction()
            judge = False
            req_direct: Any = None
            if spec in ("size_is", "string"):
                if dir in (Y.IN, Y.OUT, Y.INOUT, Y.SEND):
                    if direct == Y.IN or direct == Y.INOUT:
                        judge = True
                    req_direct = "in or inout"
                elif dir == Y.RECEIVE:
                    if direct == Y.OUT or direct == Y.INOUT:
                        judge = True
                    req_direct = "out or inout"
            elif spec == "count_is":
                if dir in (Y.IN, Y.SEND):
                    if direct == Y.IN or direct == Y.INOUT:
                        judge = True
                    req_direct = "in or inout"
                elif dir in (Y.OUT, Y.RECEIVE):
                    # mikan out で count_is のみ指定されている場合 in でなくてはならない
                    if direct == Y.OUT or direct == Y.INOUT:
                        judge = True
                    req_direct = "out or inout"
                elif dir == Y.INOUT:
                    if direct == Y.INOUT:
                        judge = True
                    req_direct = "inout"

            if judge is False:
                self.cdl_error(
                    "E1015 '$1': direction mismatch for $2, $3 required",
                    nsp.get_path_str(),
                    spec,
                    req_direct,
                )
            return None

        if k in _LITERALS_NO_BOOL:
            return True

        # 単項演算子（本体が空の when 節）
        if k in _UNARY_OPS:
            return None
        # 上の when 節の最後の値として評価される呼び出し（結果は Symbol に一致しない）
        self.elements_check_dir_for_param(elements[1], namedList, dir, spec)

        # 2項演算子
        if k in _BINARY_OPS:
            r = self.elements_check_dir_for_param(elements[1], namedList, dir, spec)
            if not truthy(r):
                return r
            return self.elements_check_dir_for_param(elements[2], namedList, dir, spec)

        # 3項演算子
        if k == Y.OP_CEX:
            r = self.elements_check_dir_for_param(elements[1], namedList, dir, spec)
            if not truthy(r):
                return r
            r = self.elements_check_dir_for_param(elements[2], namedList, dir, spec)
            if not truthy(r):
                return r
            return self.elements_check_dir_for_param(elements[3], namedList, dir, spec)

        self.cdl_error("E1016 $1: elements_check_dir_for_param: sorry not supported", k)
        return None

    def get_allocator_rhs_elements(self, alloc_type: Any) -> Any:
        """式がアロケータ指定子の右辺として妥当かチェックし、正しければ分解した値を返す。

        alloc_type::Symbol  :NORMAL_ALLOC|:INTERNAL_ALLOC|:RELAY_ALLOC
          :NORMAL_ALLOC      [ cell_nsp, ep_name ]               # rhs = cell_nsp.ep_name
          :INTERNAL_ALLOC    [ ep_name ]                         # rhs = ep_name
          :RELAY_ALLOC       [ cp_name, func_name, param_name ]  # rhs = cp_name.func_name.param_name
        """
        ele = self._elements
        if alloc_type == Y.NORMAL_ALLOC:
            if ele[0] != Y.OP_DOT or ele[1][0] != Y.IDENTIFIER:  # 1
                self.cdl_error("E1017 $1: rhs not 'Cell.ePort' form", to_s(ele[0]))
                return None
            # Ruby 版は未定義のローカル変数 elements を参照して NameError になる
            raise RubyNameError(
                "undefined local variable or method `elements' for an instance of Expression"
            )
        if alloc_type == Y.INTERNAL_ALLOC:
            if ele[0] == Y.IDENTIFIER:
                if ele[1].is_name_only():
                    return [ele[1].get_path()[0]]  # mikan a::b
                self.cdl_error("E1018 $1: namespace cannot be specified", to_s(ele[1]))
            else:
                self.cdl_error(
                    "E1019 $1: rhs not in 'allocator_entry_port' form", to_s(ele[1])
                )
            return None
        if alloc_type == Y.RELAY_ALLOC:
            if (
                ele[0] != Y.OP_DOT
                or ele[1][0] != Y.OP_DOT
                or ele[1][1][0] != Y.IDENTIFIER
                or not ele[1][1][1].is_name_only()
                or not _is_token(ele[1][2])
                or not _is_token(ele[2])
            ):  # 1
                self.cdl_error(
                    "E1020 rhs not in 'call_port.func.param' form ($1)", to_s(ele[0])
                )  # S1086
            func_name = ele[1][2]
            cp_name = ele[1][1][1].get_name()
            param_name = ele[2].to_sym()
            return [cp_name, func_name, param_name]
        return None

    def clone_for_composite(self) -> Expression:
        """Expression のクローンを作成する。"""
        cl = copy.copy(self)
        elements = self.clone_elements(self._elements)
        cl.set_elements(elements)
        return cl

    def clone_elements(self, elements: list[Any]) -> list[Any]:
        """elements のクローンを作成（Array のディープコピー）。"""
        return [self.clone_elements(e) if type(e) is list else e for e in elements]

    def set_elements(self, elements: Any) -> None:
        self._elements = elements

    def analyze_cell_join_expression(self) -> Any:
        """セル結合の式を解析する。

        Cell.eEntry  => [ :OP_DOT, [ :IDENTIFIER, token ], token ]
        Cell.eEntry[expression] => [ :OP_SUBSC, [ :OP_DOT, [ :IDENTIFIER, token ], token ], expression ]
        Return: [ NamespacePath(cell_name), Integer(subscript) or nil, Token(port_name)]
        """
        elements = self._elements
        if elements[0] == Y.OP_SUBSC:  # 右辺：受け口配列？
            subscript = elements[2].eval_const(None)  # 受け口配列の添数
            elements = elements[1]  # mikan 配列だった場合
        else:
            subscript = None

        if elements[0] != Y.OP_DOT or elements[1][0] != Y.IDENTIFIER:  # 1
            return None

        nsp = elements[1][1]  # NamespacePath
        port_name = elements[2].val
        return [nsp, subscript, port_name]

    @staticmethod
    def create_cell_join_expression(
        nsp: Any, subscript: Any, port_name: Any, locale: Any = None
    ) -> Expression:
        """セルへの結合の式を生成する（analyze_cell_join_expression と対になっている）。"""
        from tecsgen.core.generator import Token

        if type(port_name) is not Symbol:
            raise RubyRuntimeError("port_name: not Symbol")

        if truthy(subscript):
            elements: list[Any] = [
                Y.OP_SUBSC,
                [Y.OP_DOT, [Y.IDENTIFIER, nsp], Token(port_name, None, None, None)],
                # Ruby 版はクラスメソッドの中の @locale（常に nil）を渡している
                Expression.create_integer_constant(subscript, None),
            ]
        else:
            elements = [
                Y.OP_DOT,
                [Y.IDENTIFIER, nsp],
                Token(port_name, None, None, None),
            ]
        return Expression(elements, locale)

    @staticmethod
    def create_integer_constant(val: Any, locale: Any = None) -> Expression:
        """整数定数の式を生成する。val:: Integer : 値： 整数"""
        from tecsgen.core.generator import Token

        if val != rb_integer(val) or val < 0:
            raise RubyRuntimeError(
                f"create_integer_constant: not integer or negative: {to_s(val)}"
            )
        return Expression(
            [Y.INTEGER_CONSTANT, Token(val, None, None, None)],
            locale,
        )

    def analyze_single_identifier(self) -> Any:
        """単一の識別子の式を解析する。Return: NamespacePath(Identifier)"""
        elements = self._elements
        if elements[0] == Y.IDENTIFIER:
            return elements[1]
        return None

    @staticmethod
    def create_single_identifier(nsp: Any, locale: Any) -> Expression:
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        if type(nsp) is not NamespacePath:
            raise RubyRuntimeError(
                f"create_single_identifier: not NamespacePath: {to_s(nsp)}"
            )
        return Expression([Y.IDENTIFIER, nsp])

    def evaluable(self, *v: Any) -> bool:  # Ruby: evaluable?
        """評価可能かチェックする（すべてが BaseVal の子クラス（値）であれば評価可能）。"""
        from tecsgen.core.value import BaseVal

        return all(isinstance(val, BaseVal) for val in v)


def _call(obj: Any, name: str, *args: Any) -> Any:
    if obj is None:
        from tecsgen.ruby_compat import no_method

        raise no_method(name.rstrip("_"), None)
    attr = getattr(obj, name)
    return attr(*args) if callable(attr) else attr


_EVAL_BINARY: dict[Any, Any] = {
    Y.OP_MULT: lambda a, b: a * b,
    Y.OP_DIV: lambda a, b: a / b,
    Y.OP_REMAIN: lambda a, b: a % b,
    Y.OP_ADD: lambda a, b: a + b,
    Y.OP_SUB: lambda a, b: a - b,
    Y.OP_LSFT: lambda a, b: a << b,
    Y.OP_RSFT: lambda a, b: a >> b,
    Y.OP_LT: lambda a, b: a < b,
    Y.OP_GT: lambda a, b: a > b,
    Y.OP_LE: lambda a, b: a <= b,
    Y.OP_GE: lambda a, b: a >= b,
    Y.OP_EQ: lambda a, b: a.eq(b),
    Y.OP_NE: lambda a, b: a.neq(b),
    Y.OP_AND: lambda a, b: a & b,
    Y.OP_EOR: lambda a, b: a ^ b,
    Y.OP_OR: lambda a, b: a | b,
    Y.OP_LAND: lambda a, b: a.lAND(b),
    Y.OP_LOR: lambda a, b: a.lOR(b),
}


class C_EXP(Node):
    """@c_exp_string : string

    Ruby 版の initialize は super を呼ばないので、@locale を持たない（clone_for_composite で設定される）。
    """

    def __init__(self, c_exp_string: Any, b_renew: bool = False) -> None:
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        if b_renew:
            self._c_exp_string = c_exp_string
        else:
            # 前後の " を取り除く
            s = CDLString.remove_dquote(to_s(c_exp_string))
            self._c_exp_string = CDLString.escape(s)

    def clone_for_composite(self, ct_name: Any, cell_name: Any, locale: Any) -> C_EXP:
        """composite の attribute に現れる C_EXP を文字列置換して生成しなおす。"""
        dbg_print(
            f"C_EXP: {to_s(ct_name)} {to_s(cell_name)} {to_s(self._c_exp_string)}\n"
        )

        self._locale = locale
        s = gsub(_CT_PAT, "\\1" + to_s(ct_name), self._c_exp_string)
        s = gsub(_CELL_PAT, "\\1" + to_s(cell_name), s)
        s = gsub(_ID_PAT, "\\1" + f"{to_s(ct_name)}_{to_s(cell_name)}", s)
        return C_EXP(s, True)

    def get_c_exp_string(self) -> Any:
        return self._c_exp_string

    def eval_const(self, name_list: Any, name_list2: Any = None) -> C_EXP:
        """C_EXP の引き数文字列を返す（便宜上 eval_const で対応）。"""
        return self

    def eval_const2(
        self, name_list: Any, name_list2: Any = None, nest: Any = None
    ) -> C_EXP:
        return self

    def to_s(self) -> str:
        return to_s(self._c_exp_string)

    def to_CDL_str(self) -> str:
        return f'C_EXP( "{self.to_s()}" )'

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"C_EXP: {to_s(self._c_exp_string)}")


# Ruby の ^ は行頭に当たる（Python では re.M が必要）
_CT_PAT = re.compile(r"(^|[^\$])\$ct\$", re.MULTILINE)
_CELL_PAT = re.compile(r"(^|[^\$])\$cell\$", re.MULTILINE)
_ID_PAT = re.compile(r"(^|[^\$])\$id\$", re.MULTILINE)
