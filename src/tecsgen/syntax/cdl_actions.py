"""bnf.y.rb の文法アクション（racc の _reduce_N）。

tools/port/gen_action_stubs.py で骨格を生成し、本体を手で移植した（P3）。各メソッドの
コメントは、規則（左辺 : 右辺）と移植元の行番号。racc と同じく、アクションが result に
代入しない規則では、右辺の先頭の値（val[0]）が結果になる。
"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.syntax.cdl_tables import REDUCE_TABLE


def _m() -> Any:
    """モデルのモジュール群（循環 import を避けるため、使うときに読み込む）。"""
    from tecsgen.syntax import _model

    return _model


_DQUOTED = re.compile(r"\"(.*)\"")


class CdlActions:
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

    # --- 式 (bnf.y.rb:53-) -----------------------------------------------------

    def _reduce_2(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : namespace_identifier
        return [_m().Y.IDENTIFIER, val[0]]

    def _reduce_3(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : TRUE
        return [_m().Y.BOOL_CONSTANT, True]

    def _reduce_4(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : FALSE
        return [_m().Y.BOOL_CONSTANT, False]

    def _reduce_5(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : INTEGER_CONSTANT
        return [_m().Y.INTEGER_CONSTANT, val[0]]

    def _reduce_6(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : FLOATING_CONSTANT
        return [_m().Y.FLOATING_CONSTANT, val[0]]

    def _reduce_7(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : OCTAL_CONSTANT
        return [_m().Y.OCTAL_CONSTANT, val[0]]

    def _reduce_8(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : HEX_CONSTANT
        return [_m().Y.HEX_CONSTANT, val[0]]

    def _reduce_9(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : CHARACTER_LITERAL
        return [_m().Y.CHARACTER_LITERAL, val[0]]

    def _reduce_10(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : string_literal_list
        return [_m().Y.STRING_LITERAL_LIST, val[0]]

    def _reduce_11(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : "(" expression ")"
        return [_m().Y.PARENTHESES, val[1].get_elements()]

    def _reduce_13(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # string_literal_list : string_literal_list STRING_LITERAL
        # 連接した文字列を1つの文字列にまとめる
        m = _m()
        s = (
            '"'
            + m.gsub(_DQUOTED, "\\1", val[0].val)
            + m.gsub(_DQUOTED, "\\1", val[1].val)
            + '"'
        )
        return m.Token(s, val[0].file, val[0].lineno, val[0].col)

    def _reduce_15(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "[" expression "]"
        return [_m().Y.OP_SUBSC, val[0], val[2]]

    def _reduce_16(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "." IDENTIFIER
        return [_m().Y.OP_DOT, val[0], val[2]]

    def _reduce_17(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "->" IDENTIFIER
        return [_m().Y.OP_REF, val[0], val[2]]

    def _reduce_19(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : unary_operator cast_expression
        return [val[0], val[1]]

    def _reduce_20(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : SIZEOF unary_expression
        return [_m().Y.OP_SIZEOF_EXPR, val[1]]

    def _reduce_21(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : SIZEOF "(" type_name ")"
        return [_m().Y.OP_SIZEOF_TYPE, val[1]]

    def _reduce_22(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "&"
        return _m().Y.OP_U_AMP

    def _reduce_23(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "*"
        return _m().Y.OP_U_ASTER

    def _reduce_24(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "+"
        return _m().Y.OP_U_PLUS

    def _reduce_25(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "-"
        return _m().Y.OP_U_MINUS

    def _reduce_26(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "~"
        return _m().Y.OP_U_TILDE

    def _reduce_27(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "!"
        return _m().Y.OP_U_EXCLAM

    def _reduce_29(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cast_expression : "(" type_name ")" cast_expression
        return [_m().Y.CAST, val[1], val[3]]

    def _reduce_31(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_MULT, val[0], val[2]]

    def _reduce_32(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_DIV, val[0], val[2]]

    def _reduce_33(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_REMAIN, val[0], val[2]]

    def _reduce_35(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_ADD, val[0], val[2]]

    def _reduce_36(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_SUB, val[0], val[2]]

    def _reduce_38(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LSFT, val[0], val[2]]

    def _reduce_39(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_RSFT, val[0], val[2]]

    def _reduce_41(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LT, val[0], val[2]]

    def _reduce_42(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_GT, val[0], val[2]]

    def _reduce_43(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LE, val[0], val[2]]

    def _reduce_44(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_GE, val[0], val[2]]

    def _reduce_46(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_EQ, val[0], val[2]]

    def _reduce_47(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_NE, val[0], val[2]]

    def _reduce_49(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_AND, val[0], val[2]]

    def _reduce_51(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_EOR, val[0], val[2]]

    def _reduce_53(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_OR, val[0], val[2]]

    def _reduce_55(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LAND, val[0], val[2]]

    def _reduce_57(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OP_LOR, val[0], val[2]]

    def _reduce_59(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # conditional_expression : logical_or_expression "?" expression ":" conditional_expression
        return [_m().Y.OP_CEX, val[0], val[2].get_elements(), val[4]]

    def _reduce_60(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # expression : conditional_expression
        return _m().Expression(val[0])

    def _reduce_61(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # constant_expression : conditional_expression
        return _m().Expression(val[0])

    # --- 宣言 (bnf.y.rb:219-) --------------------------------------------------

    def _reduce_62(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration : type_specifier_qualifier_list init_declarator_list ";"
        for i in val[1]:  # i: Decl
            i.set_type(val[0])
        return val[1]

    def _reduce_64(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_qualifier type_specifier
        val[1].set_qualifier(val[0])
        return val[1]

    def _reduce_65(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator
        return [val[0]]

    def _reduce_66(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator_list "," init_declarator
        result.append(val[2])
        return result

    def _reduce_68(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator : declarator "=" initializer
        val[0].set_initializer(val[2])
        return result

    def _reduce_69(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().VoidType()

    def _reduce_70(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().FloatType(32)

    def _reduce_71(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().FloatType(64)

    def _reduce_74(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : TYPE_NAME
        return _m().DefinedType(val[0].val)

    def _reduce_77(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().BoolType()

    def _reduce_78(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.Generator.warning("W5002 float: obsolete type. use float32_t")
        return m.FloatType(32)

    def _reduce_79(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.Generator.warning("W5003 double: obsolete type. use double64_t")
        return m.FloatType(64)

    def _reduce_80(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : DESCRIPTOR "(" namespace_identifier ")"
        return _m().DescriptorType(val[2])

    def _reduce_81(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(-1)

    def _reduce_82(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        r = m.IntType(-1)
        r.set_sign(m.Y.SIGNED, True)
        return r

    def _reduce_83(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        r = m.IntType(-1)
        r.set_sign(m.Y.UNSIGNED, True)
        return r

    def _reduce_84(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(-11)

    def _reduce_85(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(-2)

    def _reduce_86(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(-3)

    def _reduce_87(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(-4)

    def _reduce_88(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(8)

    def _reduce_89(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(16)

    def _reduce_90(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(32)

    def _reduce_91(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(64)

    def _reduce_92(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().IntType(128)

    def _unsigned(self, bits: int) -> Any:
        m = _m()
        r = m.IntType(bits)
        r.set_sign(m.Y.UNSIGNED, True)
        return r

    def _reduce_93(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return self._unsigned(8)

    def _reduce_94(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return self._unsigned(16)

    def _reduce_95(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return self._unsigned(32)

    def _reduce_96(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return self._unsigned(64)

    def _reduce_97(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return self._unsigned(128)

    def _reduce_98(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.SIGNED

    def _reduce_99(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.UNSIGNED

    def _reduce_100(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # sign_int_type : sign int_type
        val[1].set_sign(val[0])
        return val[1]

    def _reduce_102(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @1 : /* empty */
        _m().StructType.set_define(True)
        return result

    def _reduce_103(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : STRUCT struct_tag "{" @1 struct_declaration_list "}"
        _m().StructType.end_of_parse()
        return val[1]

    def _reduce_104(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @2 : /* empty */  tag が無い場合、内部名を与える
        m = _m()
        r = m.StructType(m.sym(f"TAG__{m.Generator._no_struct_tag_num}__"))
        m.Generator._no_struct_tag_num += 1
        m.StructType.set_define(True)
        return r

    def _reduce_105(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : STRUCT @2 "{" struct_declaration_list "}"
        _m().StructType.end_of_parse()
        return val[1]

    def _reduce_106(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : STRUCT struct_tag
        m = _m()
        m.StructType.set_define(False)
        m.StructType.end_of_parse()
        return val[1]

    def _reduce_109(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_tag : IDENTIFIER
        return _m().StructType(val[0].val)

    def _reduce_110(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declaration : type_specifier_qualifier_list struct_declarator_list ";"
        m = _m()
        for i in val[1]:  # i: Decl
            i.set_type(val[0])
            i.set_kind(m.Y.MEMBER)
            i.check()
            m.StructType.new_member(i)
        return val[1]

    def _reduce_111(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declaration : spec_L pointer_specifier_list spec_R type_specifier_qualifier_list struct_declarator_list ";"
        m = _m()
        for i in val[4]:  # i: Decl
            i.set_type(val[3])
            i.set_kind(m.Y.MEMBER)
            i.set_specifier_list(val[1])
            i.check()
            m.StructType.new_member(i)
        return val[4]

    def _reduce_112(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_113(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_114(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.STRING, -1]

    def _reduce_115(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.STRING, val[2]]

    def _reduce_116(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.SIZE_IS, val[2]]

    def _reduce_117(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.COUNT_IS, val[2]]

    def _reduce_119(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier_qualifier_list : type_qualifier type_specifier_qualifier_list
        val[1].set_qualifier(val[0])
        return val[1]

    def _reduce_120(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_121(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_126(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().EnumType(-1)

    def _reduce_127(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().EnumType(8)

    def _reduce_128(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().EnumType(16)

    def _reduce_129(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().EnumType(32)

    def _reduce_130(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().EnumType(64)

    def _reduce_131(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().EnumType(128)

    def _reduce_136(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.CONST

    def _reduce_137(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.VOLATILE

    def _reduce_138(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer direct_declarator
        val[1].set_type(val[0])
        return val[1]

    def _reduce_140(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : IDENTIFIER
        return _m().Decl(val[0].val)

    def _reduce_141(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_142(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "[" constant_expression "]"
        val[0].set_type(_m().ArrayType(val[2]))
        return val[0]

    def _reduce_143(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "[" "]"
        val[0].set_type(_m().ArrayType())
        return val[0]

    def _reduce_144(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" parameter_type_list ")"
        val[0].set_type(_m().FuncType(val[2]))
        return val[0]

    def _reduce_145(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" ")"
        m = _m()
        m.Generator.warning("W5010 need 'void' for no parameter")
        val[0].set_type(m.FuncType())
        return val[0]

    def _reduce_146(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().PtrType()

    def _reduce_147(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        r = _m().PtrType()
        r.set_qualifier(val[1])
        return r

    def _reduce_148(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[1].set_type(_m().PtrType())
        return val[1]

    def _reduce_149(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        ptrtype = _m().PtrType()
        ptrtype.set_qualifier(val[1])
        val[2].set_type(ptrtype)
        return val[2]

    def _reduce_152(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().ParamList(val[0])

    def _reduce_153(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].add_param(val[2])
        return result

    def _reduce_154(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : parameter_specifier_list_bracket declaration_specifiers declarator
        m = _m()
        val[2].set_kind(m.Y.PARAMETER)
        paramdecl = m.ParamDecl(val[2], val[1], val[0])
        val[2].check()
        return paramdecl

    def _reduce_155(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.error("G1001 need specifier for '$1'", val[1].get_name())
        return None

    def _reduce_156(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        if type(val[0]) is not m.VoidType:
            m.Generator.error("G1002 need parameter name")
        return None

    def _reduce_157(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        if type(val[1]) is not m.VoidType:
            m.Generator.error("G1003 need parameter name")
        return None

    def _reduce_158(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_159(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_160(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return result + val[2]

    def _reduce_161(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.IN]]

    def _reduce_162(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.OUT]]

    def _reduce_163(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.INOUT]]

    def _reduce_164(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.SEND, val[2]]]

    def _reduce_165(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.RECEIVE, val[2]]]

    def _reduce_166(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.STRING, None]]

    def _reduce_167(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.STRING, val[2]]]

    def _reduce_168(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.SIZE_IS, val[2]]]

    def _reduce_169(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        return [[m.Y.SIZE_IS, val[2]], [m.Y.MAX_IS, val[4]]]

    def _reduce_170(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.COUNT_IS, val[2]]]

    def _reduce_171(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.NULLABLE]]

    def _reduce_173(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_name : type_specifier_qualifier_list abstract_declarator
        if _m().truthy(val[1]):
            val[1].set_type(val[0])
            return val[1]
        return val[0]  # エラー：仮で val[0] を返す

    def _reduce_177(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_178(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.error("G1004 impossible array type")
        return None

    def _reduce_179(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.error("G1005 impossible array type")
        return None

    def _reduce_180(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.error("G1006 impossible array type")
        return None

    def _reduce_181(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.error("G1007 impossible array type")
        return None

    def _reduce_182(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.error("G1008 impossible function type")
        return None

    def _reduce_184(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.Generator.warning("W5011 need 'void' for no parameter")
        val[0].set_type(m.FuncType())
        return val[0]

    def _reduce_185(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].set_type(_m().FuncType(val[2]))
        return val[0]

    def _reduce_186(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_187(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_188(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_189(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : C_EXP "(" string_literal_list ")"
        return _m().C_EXP(val[2])

    def _reduce_190(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_191(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].append(val[2])
        return val[0]

    # --- 文 (bnf.y.rb:718-) ----------------------------------------------------

    def _reduce_196(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_statement : spec_L statement_specifier_list spec_R statement
        m = _m()
        obj = val[3]
        if not isinstance(obj, (m.Cell, m.Signature, m.Celltype, m.CompositeCelltype)):
            m.Generator.get_statement_specifier()  # クリア
            m.Generator.error("G1009 unexpected specifier")
        return result

    def _reduce_211(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.add_statement_specifier(val[0])
        return result

    def _reduce_212(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.add_statement_specifier(val[2])
        return result

    def _reduce_213(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.ACTIVE]

    def _reduce_214(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.ALLOCATOR, val[2]]

    def _reduce_215(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.CALLBACK]

    def _reduce_216(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.CONTEXT, val[2].val]

    def _reduce_217(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.DEVIATE]

    def _reduce_218(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.GENERATE, val[2].val, val[4].val]

    def _reduce_219(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.ID, val[2]]

    def _reduce_220(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.IDX_IS_ID]

    def _reduce_221(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.PROTOTYPE]

    def _reduce_222(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.PSEUDO_ACTIVE]

    def _reduce_223(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.RESTRICT, val[2]]

    def _reduce_224(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.SINGLETON]

    def _reduce_225(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.THROUGH, val[2], val[4], val[6]]

    def _reduce_226(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_227(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_228(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc : port_name "." func_name "." param_name "=" initializer
        return [_m().Y.NORMAL_ALLOC, val[0], None, val[2], val[4], val[6]]

    def _reduce_229(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.NORMAL_ALLOC, val[0], val[2], val[5], val[7], val[9]]

    def _reduce_230(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_231(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_232(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0].val, None, val[3]]

    def _reduce_233(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0].val, val[2].val, val[5]]

    def _reduce_234(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_235(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_240(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # const_statement : declaration
        m = _m()
        for decl in val[0]:
            decl.set_kind(m.Y.CONSTANT)
            m.Namespace.new_const_decl(decl)
            decl.check()
        return result

    def _reduce_241(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import_C : IMPORT_C "(" STRING_LITERAL ")" ";"
        m = _m()
        m.Generator.set_import_C(True)
        m.Import_C(val[2])
        m.Generator.set_import_C(False)
        return result

    def _reduce_242(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import_C : IMPORT_C "(" STRING_LITERAL "," STRING_LITERAL ")" ";"
        m = _m()
        m.Generator.set_import_C(True)
        m.Import_C(val[2], val[4])
        m.Generator.set_import_C(False)
        return result

    def _reduce_243(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import : IMPORT "(" STRING_LITERAL ")" ";"
        _m().Import(val[2])
        return result

    def _reduce_244(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import : IMPORT "(" AB_STRING_LITERAL ")" ";"
        _m().Import(val[2], True)
        return result

    def _reduce_245(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # generate_statement : GENERATE "(" plugin_name "," namespace_identifier "," plugin_arg ")" ";"
        _m().Generate(val[2].val, val[4], val[6])
        return result

    def _reduce_246(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF type_specifier_qualifier_list declarator_list ";"
        m = _m()
        for i in val[2]:  # i:Decl
            i.set_kind(m.Y.TYPEDEF)
        m.Typedef.new_decl_list(val[1], val[2])
        for i in val[2]:
            i.check()
        return result

    def _reduce_247(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF "[" typedef_specifier "]" type_specifier_qualifier_list declarator_list ";"
        m = _m()
        for i in val[5]:
            i.set_kind(m.Y.TYPEDEF)
        m.Typedef.new_decl_list(val[4], val[5])
        for i in val[5]:
            i.check()
        return result

    def _reduce_250(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_251(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_252(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace : NAMESPACE namespace_NAME "{" statement_list "}" ";"
        val[1].end_of_parse()
        return result

    def _reduce_253(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Namespace(val[0].val)

    def _reduce_256(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().NamespacePath(val[0].val, False)

    def _reduce_257(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().NamespacePath(val[1].val, True)

    def _reduce_258(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0].append_bang(val[2].val)

    def _reduce_260(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # signature : SIGNATURE signature_NAME "{" function_head_list "}" ";"
        return val[1].end_of_parse(val[3])

    def _reduce_261(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Signature(val[0].val)

    def _reduce_262(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().NamedList(None, "function")

    def _reduce_263(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0].add_item(val[1])

    def _reduce_264(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # function_head : type_specifier_qualifier_list declarator ";"
        m = _m()
        if val[1].is_function():
            r = m.FuncHead(val[1], val[0], False)
            val[1].set_kind(m.Y.FUNCHEAD)
            val[1].check()
            return r
        # mikan 関数の配列も以下のメッセージになる
        m.Generator.error("G1010 Not function")
        return None

    def _reduce_265(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # function_head : spec_L ONEWAY spec_R type_specifier_qualifier_list declarator ";"
        m = _m()
        if val[4].is_function():
            return m.FuncHead(val[4], val[3], True)
        m.Generator.error("G1011 Not function")
        return None

    def _reduce_266(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype : CELLTYPE celltype_NAME "{" celltype_statement_list "}" ";"
        val[1].end_of_parse()
        return val[1]

    def _reduce_267(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Celltype(val[0].val)

    def _reduce_270(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_celltype_statement : celltype_statement
        m = _m()
        if isinstance(val[0], m.Port):
            m.Celltype.new_port(val[0])
        return result

    def _reduce_271(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_celltype_statement : spec_L celltype_statement_specifier_list spec_R celltype_statement
        m = _m()
        if isinstance(val[3], m.Port):
            val[3].set_specifier(val[1])  # 設定順序あり
            m.Celltype.new_port(val[3])
        else:
            # Port 以外では指定子はエラー
            m.Generator.error("G1012 $1 : cannot put specifier here", val[1])
        return result

    def _reduce_277(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_278(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_279(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.INLINE]

    def _reduce_280(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.ALLOCATOR, val[2]]

    def _reduce_281(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OPTIONAL]

    def _reduce_282(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.REF_DESC]

    def _reduce_283(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.DYNAMIC]

    def _reduce_284(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OMIT]

    def _reduce_285(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_286(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_287(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_288(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_289(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.INTERNAL_ALLOC, val[0].val, val[2].val, val[4]]

    def _reduce_290(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.RELAY_ALLOC, val[0].val, val[2].val, val[4]]

    def _reduce_291(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port : port_type namespace_signature_name port_name ";"
        return _m().Port(val[2].val, val[1], val[0])

    def _reduce_292(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Port(val[2].val, val[1], val[0], "[]")

    def _reduce_293(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Port(val[2].val, val[1], val[0], val[4])

    def _reduce_294(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Port(val[2].val, val[1], val[0], None, val[4], val[6].val)

    def _reduce_295(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.CALL

    def _reduce_296(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Y.ENTRY

    def _reduce_297(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_299(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return None

    def _reduce_300(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Celltype.new_attribute(val[0])
        return result

    def _reduce_301(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Celltype.new_attribute(val[1])
        return result

    def _reduce_302(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_declaration : declaration
        m = _m()
        for i in val[0]:  # i:Decl
            i.set_kind(m.Y.ATTRIBUTE)
            i.check()
        return val[0]

    def _reduce_303(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_declaration : spec_L attribute_specifier spec_R declaration
        m = _m()
        for i in val[3]:
            i.set_kind(m.Y.ATTRIBUTE)  # 設定順序あり
            i.set_specifier_list([val[1]])
            i.check()
        return val[3]

    def _reduce_304(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OMIT]

    def _reduce_305(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.SIZE_IS, val[2]]

    def _reduce_306(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.CHOICE, val[3]]

    def _reduce_307(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_308(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_310(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return None

    def _reduce_311(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Celltype.new_var(val[0])
        return result

    def _reduce_312(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Celltype.new_var(val[1])
        return result

    def _reduce_313(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var_declaration : declaration
        m = _m()
        for i in val[0]:
            i.set_kind(m.Y.VAR)
            i.check()
        return result

    def _reduce_314(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        for i in val[3]:
            i.set_kind(m.Y.VAR)  # 設定順序あり
            i.set_specifier_list([val[1]])
            i.check()
        return val[3]

    def _reduce_315(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.SIZE_IS, val[2]]

    def _reduce_316(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # require : REQUIRE namespace_identifier "." port_name ";"
        _m().Celltype.new_require(val[1], val[3])
        return result

    def _reduce_317(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # require : REQUIRE port_name "=" namespace_identifier "." port_name ";"
        _m().Celltype.new_require(val[3], val[5], val[1].val)
        return result

    def _reduce_319(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Factory.set_f_celltype(False)
        return result

    def _reduce_320(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Factory.set_f_celltype(True)
        return result

    def _reduce_323(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Factory(val[0].val, val[2], val[4], None)
        return result

    def _reduce_324(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Factory(val[0].val, val[2], val[4], val[6])
        return result

    def _reduce_326(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.IDENTIFIER, val[0].val]]

    def _reduce_327(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append([_m().Y.IDENTIFIER, val[2].val])
        return result

    def _reduce_328(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [[_m().Y.STRING_LITERAL, val[0].val]]

    def _reduce_329(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append([_m().Y.STRING_LITERAL, val[2].val])
        return result

    def _reduce_330(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @3 : /* empty */
        _m().Cell.new_def()
        return result

    def _reduce_331(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Cell.end_of_parse(True)

    def _reduce_332(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Cell.end_of_parse(False)

    def _reduce_333(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Cell(val[0])

    def _reduce_334(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # Ruby の result は Cell.set_name の最後の式の値（この値は使われない）
        _m().Cell.set_name(val[0].val)
        return None

    def _reduce_338(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_join : spec_L join_specifier_list spec_R join
        val[3].set_specifier_list(val[1])
        return result

    def _reduce_339(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].set_specifier_list([])
        return result

    def _reduce_340(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        result.append(val[2])
        return result

    def _reduce_341(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_342(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.THROUGH, val[2], val[4]]

    def _reduce_345(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join : cae_name "[" "]" "=" expression ";"
        m = _m()
        r = m.Join(val[0].val, -1, val[4])
        m.Cell.new_join(r, True)
        return r

    def _reduce_346(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        r = m.Join(val[0].val, val[2], val[5])
        m.Cell.new_join(r, True)
        return r

    def _reduce_347(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        r = m.Join(val[0].val, None, val[2])
        m.Cell.new_join(r, True)
        return r

    def _reduce_348(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        r = m.Join(val[0].val, None, [m.Y.COMPOSITE, val[4]])
        m.Cell.new_join(r, True)
        return r

    def _reduce_350(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        rj = m.ReverseJoin(val[0].val, None, val[2], val[4].val)
        m.Cell.new_reverse_join(rj)
        return result

    def _reduce_351(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        rj = m.ReverseJoin(val[0].val, None, val[2], val[4].val, val[6])
        m.Cell.new_reverse_join(rj)
        return result

    def _reduce_352(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        rj = m.ReverseJoin(val[0].val, val[2], val[5], val[7].val)
        m.Cell.new_reverse_join(rj)
        return result

    def _reduce_353(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        rj = m.ReverseJoin(val[0].val, val[2], val[5], val[7].val, val[9])
        m.Cell.new_reverse_join(rj)
        return result

    def _reduce_355(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().CompositeCelltype.end_of_parse()
        return val[1]

    def _reduce_356(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().CompositeCelltype(val[0].val)

    def _reduce_359(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        if isinstance(val[0], m.Port):
            m.CompositeCelltype.new_port(val[0])  # 遅延して登録
        return result

    def _reduce_360(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        if isinstance(val[3], m.Port):
            val[3].set_specifier(m.Generator.get_statement_specifier())
            m.CompositeCelltype.new_port(val[3])  # 遅延して登録 (set_specifier 後)
        elif isinstance(val[3], m.Cell):
            pass  # Cell.end_of_parse にて設定
        else:
            m.Generator.get_statement_specifier()  # クリア
            m.Generator.error("G1013 unexpected specifier")
        return result

    def _reduce_365(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.add_statement_specifier(val[0])
        return [val[0]]

    def _reduce_366(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Generator.add_statement_specifier(val[2])
        val[0].append(val[2])
        return val[0]

    def _reduce_367(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.ALLOCATOR, val[2]]

    def _reduce_368(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OMIT]

    def _reduce_369(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.OPTIONAL]

    def _reduce_370(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.REF_DESC]

    def _reduce_371(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [_m().Y.DYNAMIC]

    def _reduce_372(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0]

    def _reduce_373(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return None

    def _reduce_374(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().CompositeCelltype.new_attribute(val[0])
        return result

    def _reduce_375(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().CompositeCelltype.new_attribute(val[1])
        return result

    def _reduce_376(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Cell.new_def()
        return result

    def _reduce_377(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Cell.end_of_parse(True)

    def _reduce_378(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Cell.end_of_parse(False)

    def _reduce_379(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # internal_namespace_celltype_NAME : namespace_identifier（result へ代入しない）
        _m().Cell(val[0], True)
        return result

    def _reduce_380(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Cell.set_name(val[0].val)
        return result

    def _reduce_385(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Cell.external_join(val[0].val, val[4].val, True)
        return result

    def _reduce_386(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Cell.external_join(val[0].val, val[2].val, False)
        return result

    def _reduce_387(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.CompositeCelltype.new_join(val[0].val, val[2].val, val[4].val, m.Y.ENTRY)
        return result

    def _reduce_388(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.CompositeCelltype.new_join(val[2].val, val[4].val, val[6].val, m.Y.ENTRY)
        return result

    # --- region (bnf.y.rb:1405-) -----------------------------------------------

    def _reduce_392(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.end_of_parse()
        return result

    def _reduce_393(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.end_of_parse()
        return result

    def _reduce_396(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_in_through(val[2].val, val[4].val)
        return result

    def _reduce_397(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_in_through()
        return result

    def _reduce_398(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_out_through(val[2].val, val[4].val)
        return result

    def _reduce_399(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_out_through()
        return result

    def _reduce_400(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_to_through(val[2], val[4].val, val[6].val)
        return result

    def _reduce_401(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_to_through(val[2], None, None)
        return result

    def _reduce_402(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_from_through(val[2], val[4].val, val[6].val)
        return result

    def _reduce_403(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.new_from_through(val[2], None, None)
        return result

    def _reduce_404(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.Region.set_type(m.Y.NODE)
        return result

    def _reduce_405(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        m = _m()
        m.Region.set_type(m.Y.LINKUNIT)
        return result

    def _reduce_406(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.set_domain(val[2].val, val[4])
        return result

    def _reduce_407(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        _m().Region.set_class(val[2].val, val[4])
        return result

    def _reduce_408(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().Region(val[0].val)

    def _reduce_417(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_cell : spec_L statement_specifier_list spec_R cell
        m = _m()
        obj = val[3]
        if not isinstance(obj, m.Cell):
            m.Generator.get_statement_specifier()  # クリア
            m.Generator.error("G9999 unexpected specifier")
        return result

    def _reduce_418(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0].val]

    def _reduce_419(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # spec_L : "["
        self.set_in_specifier()
        return result

    def _reduce_420(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # spec_R : "]"
        self.unset_in_specifier()
        return result

    # --- __tool_info__ (bnf.y.rb:1495-) ----------------------------------------

    def _reduce_421(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # tool_info : TOOL_INFO "(" JSON_string ")" JSON_object
        m = _m()
        m.TOOL_INFO(m.sym(val[2]), val[4])
        return result

    def _reduce_422(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_423(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return {_m().sym(val[0]): val[2]}

    def _reduce_424(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0][_m().sym(val[2])] = val[4]
        return result

    def _reduce_429(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0].val

    def _reduce_430(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[0].val

    def _reduce_431(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return val[1]

    def _reduce_432(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return []

    def _reduce_433(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return [val[0]]

    def _reduce_434(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        val[0].append(val[2])
        return result

    def _reduce_435(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_string : STRING_LITERAL
        # Ruby の gsub! は、置換が無ければ nil を返す（トークンの値は書き換えられる）
        m = _m()
        s = val[0].val
        if _DQUOTED.search(s) is None:
            return None
        val[0].val = m.gsub(_DQUOTED, "\\1", s)
        return val[0].val

    def _reduce_436(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().rb_to_i(val[0].val)

    def _reduce_437(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().rb_to_f(val[0].val)

    def _reduce_438(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # Ruby 版は符号のトークン（val[0]）を数値にしている（"-".to_i = 0）
        return -_m().rb_to_i(val[0].val)

    def _reduce_439(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return -_m().rb_to_f(val[0].val)

    def _reduce_440(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().rb_to_i(val[0].val)

    def _reduce_441(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        return _m().rb_to_f(val[0].val)


# アクションを持つ規則の番号（移植漏れの検査に使う）
ACTION_RULES = frozenset(
    i
    for i, r in enumerate(REDUCE_TABLE)
    if r[2].startswith("_reduce_") and r[2] != "_reduce_none"
)
