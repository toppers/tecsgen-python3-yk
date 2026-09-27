"""C_parser.y.rb の文法アクション（racc の _reduce_N）。

tools/port/gen_action_stubs.py で骨格を生成し、本体を手で移植した（P3）。racc と同じく、
アクションが result に代入しない規則では、右辺の先頭の値（val[0]）が結果になる。
`set_no_type_name` は字句解析の状態（TYPE_NAME への置換）を変える（P2 で移植）。
"""

from __future__ import annotations

from typing import Any

from tecsgen.syntax.cdecl_tables import REDUCE_TABLE


def _m() -> Any:
    """モデルのモジュール群（循環 import を避けるため、使うときに読み込む）。"""
    from tecsgen.syntax import _model

    return _model


class CdeclActions:
    """アクションの mixin。パーサ本体のクラスが継承する。"""

    def _unported(self, rule: int) -> None:
        """まだ移植していないアクションが呼ばれたことを記録する。"""
        unported = self.__dict__.setdefault("unported_rules", set())
        unported.add(rule)

    # 字句解析の状態を変えるメソッド。パーサ本体のクラスが実装する
    def set_in_specifier(self) -> None:
        raise NotImplementedError

    def unset_in_specifier(self) -> None:
        raise NotImplementedError

    def set_no_type_name(self, b_no_type_name: bool) -> None:
        raise NotImplementedError

    def next_token(self) -> Any:
        raise NotImplementedError

    # --- 式 --------------------------------------------------------------------

    def _reduce_2(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.IDENTIFIER, val[0]]

    def _reduce_3(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.INTEGER_CONSTANT, val[0]]

    def _reduce_4(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.FLOATING_CONSTANT, val[0]]

    def _reduce_5(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OCTAL_CONSTANT, val[0]]

    def _reduce_6(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.HEX_CONSTANT, val[0]]

    def _reduce_7(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.CHARACTER_LITERAL, val[0]]

    def _reduce_8(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.STRING_LITERAL_LIST, val[0]]

    def _reduce_9(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.PARENTHESES, val[1].get_elements()]

    def _reduce_10(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_11(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[1])
        return result

    def _reduce_13(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_SUBSC, val[0], val[2]]

    def _reduce_17(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_DOT, val[0], val[2]]

    def _reduce_18(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_REF, val[0], val[2]]

    def _reduce_19(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_20(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_26(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0], val[1]]

    def _reduce_27(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_SIZEOF_EXPR, val[1]]

    def _reduce_28(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_SIZEOF_TYPE, val[1]]

    def _reduce_29(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_30(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_31(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.OP_U_AMP

    def _reduce_32(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.OP_U_ASTER

    def _reduce_33(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.OP_U_PLUS

    def _reduce_34(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.OP_U_MINUS

    def _reduce_35(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.OP_U_TILDE

    def _reduce_36(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.OP_U_EXCLAM

    def _reduce_38(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.CAST, val[1], val[3]]

    def _reduce_40(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_MULT, val[0], val[2]]

    def _reduce_41(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_DIV, val[0], val[2]]

    def _reduce_42(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_REMAIN, val[0], val[2]]

    def _reduce_44(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_ADD, val[0], val[2]]

    def _reduce_45(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_SUB, val[0], val[2]]

    def _reduce_47(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LSFT, val[0], val[2]]

    def _reduce_48(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_RSFT, val[0], val[2]]

    def _reduce_50(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LT, val[0], val[2]]

    def _reduce_51(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_GT, val[0], val[2]]

    def _reduce_52(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LE, val[0], val[2]]

    def _reduce_53(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_GE, val[0], val[2]]

    def _reduce_55(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_EQ, val[0], val[2]]

    def _reduce_56(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_NE, val[0], val[2]]

    def _reduce_58(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_AND, val[0], val[2]]

    def _reduce_60(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_EOR, val[0], val[2]]

    def _reduce_62(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_OR, val[0], val[2]]

    def _reduce_64(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LAND, val[0], val[2]]

    def _reduce_66(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LOR, val[0], val[2]]

    def _reduce_68(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_CEX, val[0], val[2].get_elements(), val[4]]

    def _reduce_82(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # expression : assignment_expression
        return _m().Expression(val[0])

    def _reduce_83(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # expression : expression "," assignment_expression  （',' の後ろを採用）
        return _m().Expression(val[2])

    def _reduce_84(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # constant_expression : conditional_expression
        return _m().Expression(val[0])

    # --- 宣言 ------------------------------------------------------------------

    def _reduce_86(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : storage_class
        return _m().CIntType(-3)  # storage class は無視

    def _reduce_88(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_qualifier
        r = _m().CIntType(-3)
        r.set_qualifier(val[0])
        return r

    def _reduce_89(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]  # storage class は無視

    def _reduce_90(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_specifier declaration_specifiers
        return val[1].merge(val[0])

    def _reduce_91(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[1].set_qualifier(val[0])
        return val[1]

    def _reduce_94(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_95(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_97(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].set_initializer(val[2])
        return result

    def _reduce_102(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CVoidType()

    def _reduce_103(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CIntType(-11)

    def _reduce_104(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CIntType(-2)

    def _reduce_105(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CIntType(-3)

    def _reduce_106(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CIntType(64)

    def _reduce_107(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CIntType(-3)

    def _reduce_108(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CIntType(-4)

    def _reduce_109(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        self.set_no_type_name(True)
        r = m.CIntType(-3)
        r.set_sign(m.Y.SIGNED)
        return r

    def _reduce_110(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        self.set_no_type_name(True)
        r = m.CIntType(-3)
        r.set_sign(m.Y.UNSIGNED)
        return r

    def _reduce_111(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CFloatType(-32)

    def _reduce_112(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CFloatType(-64)

    def _reduce_113(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CBoolType()

    def _reduce_114(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return val[0]

    def _reduce_115(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CVoidType()

    def _reduce_116(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return _m().CVoidType()

    def _reduce_117(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : TYPEOF  typeof( ... ) の括弧の中を読み飛ばす（パーサを通さずにトークンを消費する）
        token = self.next_token()
        if token and token[1].val == "(":
            depth = 1
            while depth > 0:
                token = self.next_token()
                if token is None:
                    break
                if token[1].val == "(":
                    depth += 1
                elif token[1].val == ")":
                    depth -= 1
        self.set_no_type_name(True)
        return _m().CVoidType()

    def _reduce_118(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : TYPE_NAME
        self.set_no_type_name(True)
        return _m().CDefinedType(val[0].val)

    def _reduce_119(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @1 : /* empty */
        _m().StructType.set_define(True)
        return result

    def _reduce_120(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : struct_term struct_tag "{" @1 struct_declaration_list "}"
        _m().StructType.end_of_parse()
        self.set_no_type_name(True)
        return val[1]

    def _reduce_121(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @2 : /* empty */
        m = _m()
        r = m.CStructType()
        m.StructType.set_define(True)
        return r

    def _reduce_122(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().StructType.end_of_parse()
        self.set_no_type_name(True)
        return val[1]

    def _reduce_123(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.StructType.set_define(False)
        m.StructType.end_of_parse()
        self.set_no_type_name(True)
        return val[1]

    def _reduce_124(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return result

    def _reduce_127(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_tag : IDENTIFIER
        r = _m().CStructType(val[0].val)
        self.set_no_type_name(True)
        return r

    def _reduce_128(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declaration : declaration_specifiers struct_declarator_list ";"
        m = _m()
        for i in val[1]:  # i: Decl
            i.set_type(val[0])
            i.set_kind(m.Y.MEMBER)
            i.check()
            m.CStructType.new_member(i)
        return val[1]

    def _reduce_132(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1].merge(val[0])

    def _reduce_133(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        r = _m().CIntType(-3)
        r.set_qualifier(val[0])
        return r

    def _reduce_134(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[1].set_qualifier(val[0])
        return val[1]

    def _reduce_135(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_136(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_139(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return result

    def _reduce_140(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return result

    def _reduce_141(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return result

    def _reduce_142(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(True)
        return result

    def _reduce_164(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.CONST

    def _reduce_165(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.VOLATILE

    def _reduce_170(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer direct_declarator
        val[1].set_type(val[0])
        return val[1]

    def _reduce_172(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer TYPE_NAME
        r = _m().Decl(val[1].val)
        r.set_type(val[0])
        return r

    def _reduce_173(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Decl(val[0].val)

    def _reduce_174(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_175(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].set_type(_m().CArrayType(val[2]))
        return val[0]

    def _reduce_176(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].set_type(_m().CArrayType())
        return val[0]

    def _reduce_177(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" parameter_type_list ")"  （引数は捨てる）
        val[0].set_type(_m().CFuncType())
        return val[0]

    def _reduce_178(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].set_type(_m().CFuncType())
        return val[0]

    def _reduce_179(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().CPtrType()

    def _reduce_180(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        r = _m().CPtrType()
        r.set_qualifier(val[1])
        return r

    def _reduce_181(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[1].set_type(_m().CPtrType())
        return val[1]

    def _reduce_182(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        ptrtype = _m().CPtrType()
        ptrtype.set_qualifier(val[1])
        val[2].set_type(ptrtype)
        return val[2]

    def _reduce_200(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.warning("W6003 need 'void' for no parameter")
        return result

    def _reduce_202(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.warning("W6004 need 'void' for no parameter")
        return result

    def _reduce_204(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_205(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_206(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_207(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().C_EXP(val[2])

    def _reduce_208(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_209(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].append(val[2])
        return val[0]

    def _reduce_212(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # extension_statement : statement
        self.set_no_type_name(False)
        return result

    def _reduce_221(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF type_specifier_qualifier_list declarator_list ";"
        m = _m()
        for i in val[2]:
            i.set_kind(m.Y.TYPEDEF)
        m.Typedef.new_decl_list(val[1], val[2])
        return result

    def _reduce_222(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_223(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_258(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().NamespacePath(val[0].val, False)

    def _reduce_259(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().NamespacePath(val[1].val, True)

    def _reduce_260(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0].append_bang(val[2].val)

    def _reduce_261(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # asm_statement : _ASM
        # ';' が表れるまで、トークンを読み飛ばす（文字列やコメント内の ';' は対象にならない）
        while True:
            token = self.next_token()
            if token is None:
                from tecsgen.ruby_compat import no_method

                raise no_method("[]", None)
            if token[1].val == ";":
                break
        return result


# アクションを持つ規則の番号（移植漏れの検査に使う）
ACTION_RULES = frozenset(
    i
    for i, r in enumerate(REDUCE_TABLE)
    if r[2].startswith("_reduce_") and r[2] != "_reduce_none"
)
