"""bnf.y.rb の文法アクション（racc の _reduce_N）。

tools/port/gen_action_stubs.py で骨格を生成し、本体は手で移植する。各メソッドの
コメントは、規則（左辺 : 右辺）と移植元のアクション（行番号付き）。
`self._unported(N)` が残っているメソッドは、まだ移植していない。
"""

from __future__ import annotations

from typing import Any

from tecsgen.syntax.cdl_tables import REDUCE_TABLE


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

    def _reduce_2(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : namespace_identifier
        # bnf.y.rb:53
        #|  result = [ :IDENTIFIER, val[0] ]
        self._unported(2)
        return result

    def _reduce_3(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : TRUE
        # bnf.y.rb:55
        #|  result = [ :BOOL_CONSTANT, true ]
        self._unported(3)
        return result

    def _reduce_4(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : FALSE
        # bnf.y.rb:57
        #|  result = [ :BOOL_CONSTANT, false ]
        self._unported(4)
        return result

    def _reduce_5(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : INTEGER_CONSTANT
        # bnf.y.rb:59
        #|  result = [ :INTEGER_CONSTANT, val[0] ]
        self._unported(5)
        return result

    def _reduce_6(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : FLOATING_CONSTANT
        # bnf.y.rb:61
        #|  result = [ :FLOATING_CONSTANT, val[0] ]
        self._unported(6)
        return result

    def _reduce_7(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : OCTAL_CONSTANT
        # bnf.y.rb:63
        #|  result = [ :OCTAL_CONSTANT, val[0] ]
        self._unported(7)
        return result

    def _reduce_8(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : HEX_CONSTANT
        # bnf.y.rb:65
        #|  result = [ :HEX_CONSTANT, val[0] ]
        self._unported(8)
        return result

    def _reduce_9(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : CHARACTER_LITERAL
        # bnf.y.rb:67
        #|  result = [ :CHARACTER_LITERAL, val[0] ]
        self._unported(9)
        return result

    def _reduce_10(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : string_literal_list
        # bnf.y.rb:69
        #|  result = [ :STRING_LITERAL_LIST, val[0] ]
        self._unported(10)
        return result

    def _reduce_11(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : "(" expression ")"
        # bnf.y.rb:71
        #|  result = [ :PARENTHESES, val[1].get_elements ]
        self._unported(11)
        return result

    def _reduce_13(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # string_literal_list : string_literal_list STRING_LITERAL
        # bnf.y.rb:76
        #|             # 連接した文字列を1つの文字列にまとめる
        #|             str = "\"" + val[0].val.gsub( /\"(.*)\"/, "\\1" ) + val[1].val.gsub( /\"(.*)\"/, "\\1" ) + "\""
        #|             result = Token.new( str, val[0].file, val[0].lineno, val[0].col )
        self._unported(13)
        return result

    def _reduce_15(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "[" expression "]"
        # bnf.y.rb:86
        #|  result = [ :OP_SUBSC, val[0], val[2] ]
        self._unported(15)
        return result

    def _reduce_16(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "." IDENTIFIER
        # bnf.y.rb:88
        #|  result = [ :OP_DOT, val[0], val[2] ]
        self._unported(16)
        return result

    def _reduce_17(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "->" IDENTIFIER
        # bnf.y.rb:90
        #|  result = [ :OP_REF, val[0], val[2] ]
        self._unported(17)
        return result

    def _reduce_19(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : unary_operator cast_expression
        # bnf.y.rb:96
        #|  result = [ val[0], val[1] ]
        self._unported(19)
        return result

    def _reduce_20(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : SIZEOF unary_expression
        # bnf.y.rb:98
        #|  result = [ :OP_SIZEOF_EXPR, val[1] ]
        self._unported(20)
        return result

    def _reduce_21(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : SIZEOF "(" type_name ")"
        # bnf.y.rb:100
        #|  result = [ :OP_SIZEOF_TYPE, val[1] ]
        self._unported(21)
        return result

    def _reduce_22(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "&"
        # bnf.y.rb:103
        #|  result = :OP_U_AMP
        self._unported(22)
        return result

    def _reduce_23(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "*"
        # bnf.y.rb:104
        #|  result = :OP_U_ASTER
        self._unported(23)
        return result

    def _reduce_24(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "+"
        # bnf.y.rb:105
        #|  result = :OP_U_PLUS
        self._unported(24)
        return result

    def _reduce_25(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "-"
        # bnf.y.rb:106
        #|  result = :OP_U_MINUS
        self._unported(25)
        return result

    def _reduce_26(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "~"
        # bnf.y.rb:107
        #|  result = :OP_U_TILDE
        self._unported(26)
        return result

    def _reduce_27(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "!"
        # bnf.y.rb:108
        #|  result = :OP_U_EXCLAM
        self._unported(27)
        return result

    def _reduce_29(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cast_expression : "(" type_name ")" cast_expression
        # bnf.y.rb:113
        #|   result = [ :CAST, val[1], val[3] ]
        self._unported(29)
        return result

    def _reduce_31(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # multiplicative_expression : multiplicative_expression "*" cast_expression
        # bnf.y.rb:118
        #|  result = [ :OP_MULT, val[0], val[2] ]
        self._unported(31)
        return result

    def _reduce_32(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # multiplicative_expression : multiplicative_expression "/" cast_expression
        # bnf.y.rb:120
        #|  result = [ :OP_DIV, val[0], val[2] ]
        self._unported(32)
        return result

    def _reduce_33(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # multiplicative_expression : multiplicative_expression "%" cast_expression
        # bnf.y.rb:122
        #|  result = [ :OP_REMAIN, val[0], val[2] ]
        self._unported(33)
        return result

    def _reduce_35(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # additive_expression : additive_expression "+" multiplicative_expression
        # bnf.y.rb:127
        #|  result = [ :OP_ADD, val[0], val[2] ]
        self._unported(35)
        return result

    def _reduce_36(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # additive_expression : additive_expression "-" multiplicative_expression
        # bnf.y.rb:129
        #|  result = [ :OP_SUB, val[0], val[2] ]
        self._unported(36)
        return result

    def _reduce_38(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # shift_expression : shift_expression "<<" additive_expression
        # bnf.y.rb:134
        #|  result = [ :OP_LSFT, val[0], val[2] ]
        self._unported(38)
        return result

    def _reduce_39(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # shift_expression : shift_expression ">>" additive_expression
        # bnf.y.rb:136
        #|  result = [ :OP_RSFT, val[0], val[2] ]
        self._unported(39)
        return result

    def _reduce_41(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression "<" shift_expression
        # bnf.y.rb:141
        #|  result = [ :OP_LT, val[0], val[2] ]
        self._unported(41)
        return result

    def _reduce_42(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression ">" shift_expression
        # bnf.y.rb:143
        #|  result = [ :OP_GT, val[0], val[2] ]
        self._unported(42)
        return result

    def _reduce_43(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression "<=" shift_expression
        # bnf.y.rb:145
        #|  result = [ :OP_LE, val[0], val[2] ]
        self._unported(43)
        return result

    def _reduce_44(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression ">=" shift_expression
        # bnf.y.rb:147
        #|  result = [ :OP_GE, val[0], val[2] ]
        self._unported(44)
        return result

    def _reduce_46(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # equality_expression : equality_expression "==" relational_expression
        # bnf.y.rb:152
        #|  result = [ :OP_EQ, val[0], val[2] ]
        self._unported(46)
        return result

    def _reduce_47(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # equality_expression : equality_expression "!=" relational_expression
        # bnf.y.rb:154
        #|  result = [ :OP_NE, val[0], val[2] ]
        self._unported(47)
        return result

    def _reduce_49(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # and_expression : and_expression "&" equality_expression
        # bnf.y.rb:159
        #|  result = [ :OP_AND, val[0], val[2] ]
        self._unported(49)
        return result

    def _reduce_51(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # exclusive_or_expression : exclusive_or_expression "^" and_expression
        # bnf.y.rb:164
        #|  result = [ :OP_EOR, val[0], val[2] ]
        self._unported(51)
        return result

    def _reduce_53(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # inclusive_or_expression : inclusive_or_expression "|" exclusive_or_expression
        # bnf.y.rb:169
        #|  result = [ :OP_OR, val[0], val[2] ]
        self._unported(53)
        return result

    def _reduce_55(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # logical_and_expression : logical_and_expression "&&" inclusive_or_expression
        # bnf.y.rb:174
        #|  result = [ :OP_LAND, val[0], val[2] ]
        self._unported(55)
        return result

    def _reduce_57(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # logical_or_expression : logical_or_expression "||" logical_and_expression
        # bnf.y.rb:179
        #|  result = [ :OP_LOR, val[0], val[2] ]
        self._unported(57)
        return result

    def _reduce_59(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # conditional_expression : logical_or_expression "?" expression ":" conditional_expression
        # bnf.y.rb:184
        #|  result = [ :OP_CEX, val[0], val[2].get_elements, val[4] ]
        self._unported(59)
        return result

    def _reduce_60(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # expression : conditional_expression
        # bnf.y.rb:190
        #|             result = Expression.new( val[0] )
        #|             # result.print
        self._unported(60)
        return result

    def _reduce_61(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # constant_expression : conditional_expression
        # bnf.y.rb:197
        #|             result = Expression.new( val[0] )
        #|             # result.print
        #|
        #|             # res = result.eval_const( nil )
        #|             # if res then
        #|             #   puts "val: #{res}"
        #|             # else
        #|             #   puts "val: nil"
        #|             # end
        self._unported(61)
        return result

    def _reduce_62(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration : type_specifier_qualifier_list init_declarator_list ";"
        # bnf.y.rb:219
        #|             val[1].each { |i|    # i: Decl
        #|                 i.set_type( val[0] )
        #|             }
        #|             result = val[1]
        self._unported(62)
        return result

    def _reduce_64(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_qualifier type_specifier
        # bnf.y.rb:235
        #|             val[1].set_qualifier( val[0] )
        #|             result = val[1]
        self._unported(64)
        return result

    def _reduce_65(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator
        # bnf.y.rb:242
        #|  result = [val[0]]
        self._unported(65)
        return result

    def _reduce_66(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator_list "," init_declarator
        # bnf.y.rb:244
        #|  result << val[2]
        self._unported(66)
        return result

    def _reduce_68(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator : declarator "=" initializer
        # bnf.y.rb:249
        #|  val[0].set_initializer( val[2] )
        self._unported(68)
        return result

    def _reduce_69(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : VOID
        # bnf.y.rb:255
        #|  result = VoidType.new
        self._unported(69)
        return result

    def _reduce_70(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : FLOAT32_T
        # bnf.y.rb:256
        #|  result = FloatType.new(32)
        self._unported(70)
        return result

    def _reduce_71(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : DOUBLE64_T
        # bnf.y.rb:257
        #|  result = FloatType.new(64)
        self._unported(71)
        return result

    def _reduce_74(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : TYPE_NAME
        # bnf.y.rb:260
        #|  result = DefinedType.new( val[0].val )
        self._unported(74)
        return result

    def _reduce_77(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : BOOL_T
        # bnf.y.rb:264
        #|  result = BoolType.new
        self._unported(77)
        return result

    def _reduce_78(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : FLOAT
        # bnf.y.rb:269
        #|             Generator.warning( "W5002 float: obsolete type. use float32_t"  )
        #|             result = FloatType.new(32)
        self._unported(78)
        return result

    def _reduce_79(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : DOUBLE
        # bnf.y.rb:273
        #|             Generator.warning( "W5003 double: obsolete type. use double64_t"  )
        #|             result = FloatType.new(64)
        self._unported(79)
        return result

    def _reduce_80(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : DESCRIPTOR "(" namespace_identifier ")"
        # bnf.y.rb:277
        #|       # namespace_identifier: signature name
        #|             result = DescriptorType.new( val[2] )
        self._unported(80)
        return result

    def _reduce_81(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # char_type : CHAR_T
        # bnf.y.rb:282
        #|  result = IntType.new( -1 )
        self._unported(81)
        return result

    def _reduce_82(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # char_type : SCHAR_T
        # bnf.y.rb:284
        #|             result = IntType.new( -1 )
        #|             result.set_sign( :SIGNED, true )
        self._unported(82)
        return result

    def _reduce_83(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # char_type : UCHAR_T
        # bnf.y.rb:289
        #|             result = IntType.new( -1 )
        #|             result.set_sign( :UNSIGNED, true )
        self._unported(83)
        return result

    def _reduce_84(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : CHAR
        # bnf.y.rb:295
        #|             # Generator.warning( "W5004 char: obsolete type. use char_t"  )
        #|             result = IntType.new( -11 )
        self._unported(84)
        return result

    def _reduce_85(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : SHORT
        # bnf.y.rb:299
        #|  result = IntType.new( -2 )
        self._unported(85)
        return result

    def _reduce_86(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : INT
        # bnf.y.rb:300
        #|  result = IntType.new( -3 )
        self._unported(86)
        return result

    def _reduce_87(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : LONG
        # bnf.y.rb:301
        #|  result = IntType.new( -4 )
        self._unported(87)
        return result

    def _reduce_88(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : INT8_T
        # bnf.y.rb:325
        #|  result = IntType.new( 8 )
        self._unported(88)
        return result

    def _reduce_89(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : INT16_T
        # bnf.y.rb:326
        #|  result = IntType.new( 16 )
        self._unported(89)
        return result

    def _reduce_90(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : INT32_T
        # bnf.y.rb:327
        #|  result = IntType.new( 32 )
        self._unported(90)
        return result

    def _reduce_91(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : INT64_T
        # bnf.y.rb:328
        #|  result = IntType.new( 64 )
        self._unported(91)
        return result

    def _reduce_92(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : INT128_T
        # bnf.y.rb:329
        #|  result = IntType.new( 128 )
        self._unported(92)
        return result

    def _reduce_93(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : UINT8_T
        # bnf.y.rb:331
        #|             result = IntType.new( 8 )
        #|             result.set_sign( :UNSIGNED, true )
        self._unported(93)
        return result

    def _reduce_94(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : UINT16_T
        # bnf.y.rb:336
        #|             result = IntType.new( 16 )
        #|             result.set_sign( :UNSIGNED, true )
        self._unported(94)
        return result

    def _reduce_95(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : UINT32_T
        # bnf.y.rb:341
        #|             result = IntType.new( 32 )
        #|             result.set_sign( :UNSIGNED, true )
        self._unported(95)
        return result

    def _reduce_96(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : UINT64_T
        # bnf.y.rb:346
        #|             result = IntType.new( 64 )
        #|             result.set_sign( :UNSIGNED, true )
        self._unported(96)
        return result

    def _reduce_97(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # int_type : UINT128_T
        # bnf.y.rb:351
        #|             result = IntType.new( 128 )
        #|             result.set_sign( :UNSIGNED, true )
        self._unported(97)
        return result

    def _reduce_98(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # sign : SIGNED
        # bnf.y.rb:357
        #|  result = :SIGNED
        self._unported(98)
        return result

    def _reduce_99(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # sign : UNSIGNED
        # bnf.y.rb:358
        #|  result = :UNSIGNED
        self._unported(99)
        return result

    def _reduce_100(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # sign_int_type : sign int_type
        # bnf.y.rb:363
        #|             val[1].set_sign( val[0] )
        #|             result = val[1]
        self._unported(100)
        return result

    def _reduce_102(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @1 : /* empty */
        # bnf.y.rb:372
        #|  StructType.set_define( true )
        self._unported(102)
        return result

    def _reduce_103(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : STRUCT struct_tag "{" @1 struct_declaration_list "}"
        # bnf.y.rb:374
        #|             StructType.end_of_parse
        #|             result = val[1]
        self._unported(103)
        return result

    def _reduce_104(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @2 : /* empty */
        # bnf.y.rb:379
        #|             # tag が無い場合、内部名を与える
        #|             result = StructType.new( :"TAG__#{@@no_struct_tag_num}__" )
        #|             @@no_struct_tag_num += 1
        #|             StructType.set_define( true )
        self._unported(104)
        return result

    def _reduce_105(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : STRUCT @2 "{" struct_declaration_list "}"
        # bnf.y.rb:386
        #|             StructType.end_of_parse
        #|             result = val[1]
        self._unported(105)
        return result

    def _reduce_106(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : STRUCT struct_tag
        # bnf.y.rb:391
        #|             StructType.set_define( false )
        #|             StructType.end_of_parse
        #|             result = val[1]
        self._unported(106)
        return result

    def _reduce_109(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_tag : IDENTIFIER
        # bnf.y.rb:403
        #|  result = StructType.new( val[0].val )
        self._unported(109)
        return result

    def _reduce_110(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declaration : type_specifier_qualifier_list struct_declarator_list ";"
        # bnf.y.rb:408
        #|             val[1].each { |i|    # i: Decl
        #|                 i.set_type( val[0] )
        #|                 i.set_kind( :MEMBER )
        #|                 i.check
        #|                 StructType.new_member( i )
        #|             }
        #|             result = val[1]
        self._unported(110)
        return result

    def _reduce_111(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declaration : spec_L pointer_specifier_list spec_R type_specifier_qualifier_list struct_declarator_list ";"
        # bnf.y.rb:418
        #|             val[4].each { |i|    # i: Decl
        #|                 i.set_type( val[3] )
        #|                 i.set_kind( :MEMBER )
        #|                   i.set_specifier_list val[1]
        #|                 i.check
        #|                 StructType.new_member( i )
        #|             }
        #|             result = val[4]
        self._unported(111)
        return result

    def _reduce_112(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer_specifier_list : pointer_specifier
        # bnf.y.rb:430
        #|  result = [ val[0] ]
        self._unported(112)
        return result

    def _reduce_113(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer_specifier_list : pointer_specifier_list "," pointer_specifier
        # bnf.y.rb:431
        #|  result <<  val[2]
        self._unported(113)
        return result

    def _reduce_114(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer_specifier : STRING
        # bnf.y.rb:434
        #|  result = [:STRING,-1]
        self._unported(114)
        return result

    def _reduce_115(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer_specifier : STRING "(" expression ")"
        # bnf.y.rb:435
        #|  result = [:STRING,val[2]]
        self._unported(115)
        return result

    def _reduce_116(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer_specifier : SIZE_IS "(" expression ")"
        # bnf.y.rb:436
        #|  result = [:SIZE_IS,val[2]]
        self._unported(116)
        return result

    def _reduce_117(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer_specifier : COUNT_IS "(" expression ")"
        # bnf.y.rb:437
        #|  result = [:COUNT_IS,val[2]]
        self._unported(117)
        return result

    def _reduce_119(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier_qualifier_list : type_qualifier type_specifier_qualifier_list
        # bnf.y.rb:447
        #|             val[1].set_qualifier( val[0] )
        #|             result = val[1]
        self._unported(119)
        return result

    def _reduce_120(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declarator_list : struct_declarator
        # bnf.y.rb:457
        #|  result = [ val[0] ]
        self._unported(120)
        return result

    def _reduce_121(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declarator_list : struct_declarator_list "," struct_declarator
        # bnf.y.rb:459
        #|  result << val[2]
        self._unported(121)
        return result

    def _reduce_126(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # enum_type : ENUM
        # bnf.y.rb:472
        #|  result = EnumType.new( -1 )
        self._unported(126)
        return result

    def _reduce_127(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # enum_type : ENUM8
        # bnf.y.rb:473
        #|  result = EnumType.new( 8 )
        self._unported(127)
        return result

    def _reduce_128(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # enum_type : ENUM16
        # bnf.y.rb:474
        #|  result = EnumType.new( 16 )
        self._unported(128)
        return result

    def _reduce_129(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # enum_type : ENUM32
        # bnf.y.rb:475
        #|  result = EnumType.new( 32 )
        self._unported(129)
        return result

    def _reduce_130(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # enum_type : ENUM64
        # bnf.y.rb:476
        #|  result = EnumType.new( 64 )
        self._unported(130)
        return result

    def _reduce_131(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # enum_type : ENUM128
        # bnf.y.rb:477
        #|  result = EnumType.new( 128 )
        self._unported(131)
        return result

    def _reduce_136(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_qualifier : CONST
        # bnf.y.rb:488
        #|  result = :CONST
        self._unported(136)
        return result

    def _reduce_137(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_qualifier : VOLATILE
        # bnf.y.rb:489
        #|  result = :VOLATILE
        self._unported(137)
        return result

    def _reduce_138(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer direct_declarator
        # bnf.y.rb:493
        #|             val[1].set_type( val[0] )
        #|             result = val[1]
        self._unported(138)
        return result

    def _reduce_140(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : IDENTIFIER
        # bnf.y.rb:501
        #|  result = Decl.new( val[0].val )
        self._unported(140)
        return result

    def _reduce_141(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : "(" declarator ")"
        # bnf.y.rb:503
        #|  result = val[1]
        self._unported(141)
        return result

    def _reduce_142(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "[" constant_expression "]"
        # bnf.y.rb:505
        #|             val[0].set_type( ArrayType.new( val[2] ) )
        #|             result = val[0]
        self._unported(142)
        return result

    def _reduce_143(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "[" "]"
        # bnf.y.rb:510
        #|             val[0].set_type( ArrayType.new )
        #|             result = val[0]
        self._unported(143)
        return result

    def _reduce_144(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" parameter_type_list ")"
        # bnf.y.rb:515
        #|             val[0].set_type( FuncType.new( val[2] ) )
        #|             result = val[0]
        self._unported(144)
        return result

    def _reduce_145(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" ")"
        # bnf.y.rb:521
        #|             Generator.warning( "W5010 need 'void' for no parameter"  )
        #|             val[0].set_type( FuncType.new )
        #|             result = val[0]
        self._unported(145)
        return result

    def _reduce_146(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*"
        # bnf.y.rb:529
        #|  result = PtrType.new
        self._unported(146)
        return result

    def _reduce_147(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*" type_qualifier
        # bnf.y.rb:531
        #|             result = PtrType.new
        #|             result.set_qualifier( val[1] )
        self._unported(147)
        return result

    def _reduce_148(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*" pointer
        # bnf.y.rb:536
        #|             val[1].set_type(PtrType.new)
        #|             result = val[1]
        self._unported(148)
        return result

    def _reduce_149(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*" type_qualifier pointer
        # bnf.y.rb:541
        #|             ptrtype = PtrType.new
        #|             ptrtype.set_qualifier( val[1] )
        #|             val[2].set_type( ptrtype )
        #|             result = val[2]
        self._unported(149)
        return result

    def _reduce_152(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_list : parameter_declaration
        # bnf.y.rb:556
        #|  result = ParamList.new( val[0] )
        self._unported(152)
        return result

    def _reduce_153(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_list : parameter_list "," parameter_declaration
        # bnf.y.rb:558
        #|             val[0].add_param( val[2] )
        #|             # result = val[0] 不要
        self._unported(153)
        return result

    def _reduce_154(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : parameter_specifier_list_bracket declaration_specifiers declarator
        # bnf.y.rb:568
        #|             val[2].set_kind( :PARAMETER )
        #|             paramdecl = ParamDecl.new( val[2], val[1], val[0] )
        #|             val[2].check
        #|             result = paramdecl
        self._unported(154)
        return result

    def _reduce_155(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : declaration_specifiers declarator
        # bnf.y.rb:577
        #|             Generator.error( "G1001 need specifier for \'$1\'" , val[1].get_name )
        #|             result = nil
        self._unported(155)
        return result

    def _reduce_156(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : declaration_specifiers
        # bnf.y.rb:582
        #|             unless val[0].instance_of?( VoidType ) then
        #|                 Generator.error( "G1002 need parameter name"  )
        #|             end
        #|             result = nil
        self._unported(156)
        return result

    def _reduce_157(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : parameter_specifier_list_bracket declaration_specifiers
        # bnf.y.rb:590
        #|             unless val[1].instance_of?( VoidType ) then
        #|                 Generator.error( "G1003 need parameter name"  )
        #|             end
        #|             result = nil
        self._unported(157)
        return result

    def _reduce_158(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier_list_bracket : spec_L parameter_specifier_list spec_R
        # bnf.y.rb:598
        #|  result = val[1]
        self._unported(158)
        return result

    def _reduce_159(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier_list : parameter_specifier
        # bnf.y.rb:602
        #|  result = val[0]
        self._unported(159)
        return result

    def _reduce_160(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier_list : parameter_specifier_list "," parameter_specifier
        # bnf.y.rb:604
        #|  result = result + val[2]
        self._unported(160)
        return result

    def _reduce_161(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : IN
        # bnf.y.rb:607
        #|  result = [ [:IN]  ]
        self._unported(161)
        return result

    def _reduce_162(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : OUT
        # bnf.y.rb:608
        #|  result = [ [:OUT] ]
        self._unported(162)
        return result

    def _reduce_163(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : INOUT
        # bnf.y.rb:609
        #|  result = [ [:INOUT] ]
        self._unported(163)
        return result

    def _reduce_164(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : SEND "(" namespace_identifier ")"
        # bnf.y.rb:610
        #|  result = [ [:SEND,   val[2]] ]
        self._unported(164)
        return result

    def _reduce_165(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : RECEIVE "(" namespace_identifier ")"
        # bnf.y.rb:611
        #|  result = [ [:RECEIVE,val[2]] ]
        self._unported(165)
        return result

    def _reduce_166(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : STRING
        # bnf.y.rb:612
        #|  result = [ [:STRING,nil] ]
        self._unported(166)
        return result

    def _reduce_167(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : STRING "(" expression ")"
        # bnf.y.rb:613
        #|  result = [ [:STRING,  val[2]] ]
        self._unported(167)
        return result

    def _reduce_168(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : SIZE_IS "(" expression ")"
        # bnf.y.rb:614
        #|  result = [ [:SIZE_IS, val[2]] ]
        self._unported(168)
        return result

    def _reduce_169(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : SIZE_IS "(" expression "," constant_expression ")"
        # bnf.y.rb:616
        #|             result = [ [:SIZE_IS,val[2]], [:MAX_IS, val[4]] ]
        self._unported(169)
        return result

    def _reduce_170(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : COUNT_IS "(" expression ")"
        # bnf.y.rb:619
        #|  result = [ [:COUNT_IS,val[2]] ]
        self._unported(170)
        return result

    def _reduce_171(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_specifier : NULLABLE
        # bnf.y.rb:620
        #|  result = [ [:NULLABLE] ]
        self._unported(171)
        return result

    def _reduce_173(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_name : type_specifier_qualifier_list abstract_declarator
        # bnf.y.rb:625
        #|             if val[1] then
        #|                 val[1].set_type( val[0] )
        #|                 result = val[1]
        #|             else
        #|                 # エラー：仮で val[0] を返す
        #|                 result = val[0]
        #|             end
        self._unported(173)
        return result

    def _reduce_177(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : "(" abstract_declarator ")"
        # bnf.y.rb:643
        #|  result = val[1]
        self._unported(177)
        return result

    def _reduce_178(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : "[" "]"
        # bnf.y.rb:645
        #|             Generator.error( "G1004 impossible array type"  )
        #|             result = nil
        self._unported(178)
        return result

    def _reduce_179(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : "[" constant_expression "]"
        # bnf.y.rb:650
        #|             Generator.error( "G1005 impossible array type"  )
        #|             result = nil
        self._unported(179)
        return result

    def _reduce_180(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : direct_abstract_declarator "[" "]"
        # bnf.y.rb:655
        #|             Generator.error( "G1006 impossible array type"  )
        #|             result = nil
        self._unported(180)
        return result

    def _reduce_181(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : direct_abstract_declarator "[" constant_expression "]"
        # bnf.y.rb:660
        #|             Generator.error( "G1007 impossible array type"  )
        #|             result = nil
        self._unported(181)
        return result

    def _reduce_182(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : "(" ")"
        # bnf.y.rb:665
        #|             Generator.error( "G1008 impossible function type"  )
        #|             result = nil
        self._unported(182)
        return result

    def _reduce_184(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : direct_abstract_declarator "(" ")"
        # bnf.y.rb:671
        #|             Generator.warning( "W5011 need 'void' for no parameter"  )
        #|             val[0].set_type( FuncType.new )
        #|             result = val[0]
        self._unported(184)
        return result

    def _reduce_185(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : direct_abstract_declarator "(" parameter_type_list ")"
        # bnf.y.rb:677
        #|             val[0].set_type( FuncType.new( val[2] ) )
        #|             result = val[0]
        self._unported(185)
        return result

    def _reduce_186(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : constant_expression
        # bnf.y.rb:685
        #|  result = val[0]
        self._unported(186)
        return result

    def _reduce_187(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : "{" initializer_list "}"
        # bnf.y.rb:687
        #|  result = val[1]
        self._unported(187)
        return result

    def _reduce_188(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : "{" initializer_list "," "}"
        # bnf.y.rb:689
        #|  result = val[1]
        self._unported(188)
        return result

    def _reduce_189(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : C_EXP "(" string_literal_list ")"
        # bnf.y.rb:692
        #|  result = C_EXP.new( val[2] )
        self._unported(189)
        return result

    def _reduce_190(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer_list : initializer
        # bnf.y.rb:696
        #|             result = [ val[0] ]
        self._unported(190)
        return result

    def _reduce_191(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer_list : initializer_list "," initializer
        # bnf.y.rb:700
        #|             val[0] << val[2]
        #|             result = val[0]
        self._unported(191)
        return result

    def _reduce_196(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_statement : spec_L statement_specifier_list spec_R statement
        # bnf.y.rb:718
        #|             obj = val[3]
        #|             if obj.kind_of?( Cell ) || obj.kind_of?( Signature ) || obj.kind_of?( Celltype ) || obj.kind_of?( CompositeCelltype )then
        #|                 # cell, signature 以外は、指定子を置けない
        #|             else
        #|           Generator.get_statement_specifier   # クリア
        #|           Generator.error( "G1009 unexpected specifier"  )
        #|             end
        self._unported(196)
        return result

    def _reduce_211(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier_list : statement_specifier
        # bnf.y.rb:748
        #|  Generator.add_statement_specifier val[0]
        self._unported(211)
        return result

    def _reduce_212(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier_list : statement_specifier_list "," statement_specifier
        # bnf.y.rb:750
        #|  Generator.add_statement_specifier val[2]
        self._unported(212)
        return result

    def _reduce_213(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : ACTIVE
        # bnf.y.rb:753
        #|  result = [:ACTIVE]
        self._unported(213)
        return result

    def _reduce_214(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : ALLOCATOR "(" alloc_list ")"
        # bnf.y.rb:755
        #|  result = [ :ALLOCATOR, val[2] ]
        self._unported(214)
        return result

    def _reduce_215(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : CALLBACK
        # bnf.y.rb:757
        #|  result = [ :CALLBACK ]
        self._unported(215)
        return result

    def _reduce_216(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : CONTEXT "(" string_literal_list ")"
        # bnf.y.rb:759
        #|  result = [ :CONTEXT, val[2].val ]
        self._unported(216)
        return result

    def _reduce_217(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : DEVIATE
        # bnf.y.rb:761
        #|  result = [ :DEVIATE ]
        self._unported(217)
        return result

    def _reduce_218(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : GENERATE "(" plugin_name "," plugin_arg ")"
        # bnf.y.rb:763
        #|  result = [:GENERATE, val[2].val, val[4].val]
        self._unported(218)
        return result

    def _reduce_219(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : ID "(" constant_expression ")"
        # bnf.y.rb:765
        #|  result = [ :ID, val[2] ]
        self._unported(219)
        return result

    def _reduce_220(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : IDX_IS_ID
        # bnf.y.rb:766
        #|  result = [:IDX_IS_ID]
        self._unported(220)
        return result

    def _reduce_221(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : PROTOTYPE
        # bnf.y.rb:768
        #|  result = [ :PROTOTYPE ]
        self._unported(221)
        return result

    def _reduce_222(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : PSEUDO_ACTIVE
        # bnf.y.rb:769
        #|  result = [:PSEUDO_ACTIVE]
        self._unported(222)
        return result

    def _reduce_223(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : RESTRICT "(" restrict_list ")"
        # bnf.y.rb:771
        #|  result = [ :RESTRICT, val[2] ]
        self._unported(223)
        return result

    def _reduce_224(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : SINGLETON
        # bnf.y.rb:772
        #|  result = [:SINGLETON]
        self._unported(224)
        return result

    def _reduce_225(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # statement_specifier : THROUGH "(" port_name "," plugin_name "," plugin_arg ")"
        # bnf.y.rb:774
        #|  result = [ :THROUGH, val[2], val[4], val[6] ]
        self._unported(225)
        return result

    def _reduce_226(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc_list : alloc
        # bnf.y.rb:777
        #|  result = [ val[0] ]
        self._unported(226)
        return result

    def _reduce_227(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc_list : alloc_list "," alloc
        # bnf.y.rb:778
        #|  result << val[2]
        self._unported(227)
        return result

    def _reduce_228(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc : port_name "." func_name "." param_name "=" initializer
        # bnf.y.rb:782
        #|   result = [ :NORMAL_ALLOC, val[0], nil, val[2], val[4], val[6] ]
        self._unported(228)
        return result

    def _reduce_229(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc : port_name "[" constant_expression "]" "." func_name "." param_name "=" initializer
        # bnf.y.rb:784
        #|   result = [ :NORMAL_ALLOC, val[0], val[2], val[5], val[7], val[9] ]
        self._unported(229)
        return result

    def _reduce_230(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # restrict_list : restrict
        # bnf.y.rb:793
        #|     result = [val[0]]
        self._unported(230)
        return result

    def _reduce_231(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # restrict_list : restrict_list "," restrict
        # bnf.y.rb:795
        #|     result << val[2]
        self._unported(231)
        return result

    def _reduce_232(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # restrict : port_name "=" "{" region_name_list "}"
        # bnf.y.rb:799
        #|     result = [ val[0].val, nil, val[3] ]
        self._unported(232)
        return result

    def _reduce_233(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # restrict : port_name "." func_name "=" "{" region_name_list "}"
        # bnf.y.rb:801
        #|     result = [ val[0].val, val[2].val, val[5] ]
        self._unported(233)
        return result

    def _reduce_234(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_name_list : namespace_identifier
        # bnf.y.rb:805
        #|     result = [val[0]]
        self._unported(234)
        return result

    def _reduce_235(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_name_list : region_name_list "," namespace_identifier
        # bnf.y.rb:807
        #|     result << val[2]
        self._unported(235)
        return result

    def _reduce_240(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # const_statement : declaration
        # bnf.y.rb:823
        #|             val[0].each { |decl|
        #|                 decl.set_kind( :CONSTANT )
        #|                 Namespace.new_const_decl( decl )
        #|                 decl.check
        #|             }
        self._unported(240)
        return result

    def _reduce_241(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import_C : IMPORT_C "(" STRING_LITERAL ")" ";"
        # bnf.y.rb:833
        #|             @@import_C = true
        #|             Import_C.new( val[2] )
        #|             @@import_C = false
        self._unported(241)
        return result

    def _reduce_242(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import_C : IMPORT_C "(" STRING_LITERAL "," STRING_LITERAL ")" ";"
        # bnf.y.rb:839
        #|             @@import_C = true
        #|             Import_C.new( val[2], val[4] )
        #|             @@import_C = false
        self._unported(242)
        return result

    def _reduce_243(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import : IMPORT "(" STRING_LITERAL ")" ";"
        # bnf.y.rb:847
        #|  Import.new( val[2] )
        self._unported(243)
        return result

    def _reduce_244(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # import : IMPORT "(" AB_STRING_LITERAL ")" ";"
        # bnf.y.rb:849
        #|  Import.new( val[2], true )
        self._unported(244)
        return result

    def _reduce_245(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # generate_statement : GENERATE "(" plugin_name "," namespace_identifier "," plugin_arg ")" ";"
        # bnf.y.rb:854
        #|  Generate.new( val[2].val, val[4], val[6] )
        self._unported(245)
        return result

    def _reduce_246(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF type_specifier_qualifier_list declarator_list ";"
        # bnf.y.rb:858
        #|             val[2].each{ |i|       # i:Decl
        #|                 i.set_kind( :TYPEDEF )
        #|             }
        #|             Typedef.new_decl_list( val[1], val[2] )
        #|             val[2].each{ |i|       # i:Decl
        #|                 i.check
        #|             }
        self._unported(246)
        return result

    def _reduce_247(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF "[" typedef_specifier "]" type_specifier_qualifier_list declarator_list ";"
        # bnf.y.rb:868
        #|             val[5].each{ |i|       # i:Decl
        #|                 i.set_kind( :TYPEDEF )
        #|             }
        #|             Typedef.new_decl_list( val[4], val[5] )
        #|             val[5].each{ |i|       # i:Decl
        #|                 i.check
        #|             }
        self._unported(247)
        return result

    def _reduce_250(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator_list : declarator
        # bnf.y.rb:886
        #|  result = [ val[0] ]
        self._unported(250)
        return result

    def _reduce_251(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator_list : declarator_list "," declarator
        # bnf.y.rb:888
        #|  result << val[2]
        self._unported(251)
        return result

    def _reduce_252(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace : NAMESPACE namespace_NAME "{" statement_list "}" ";"
        # bnf.y.rb:892
        #| val[1].end_of_parse
        self._unported(252)
        return result

    def _reduce_253(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_NAME : IDENTIFIER
        # bnf.y.rb:896
        #| result = Namespace.new(val[0].val)
        self._unported(253)
        return result

    def _reduce_256(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_identifier : namespace_name
        # bnf.y.rb:904
        #|  result = NamespacePath.new( val[0].val, false )
        self._unported(256)
        return result

    def _reduce_257(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_identifier : "::" namespace_name
        # bnf.y.rb:905
        #|  result = NamespacePath.new( val[1].val, true )
        self._unported(257)
        return result

    def _reduce_258(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_identifier : namespace_identifier "::" namespace_name
        # bnf.y.rb:907
        #|  result = val[0].append!( val[2].val )
        self._unported(258)
        return result

    def _reduce_260(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # signature : SIGNATURE signature_NAME "{" function_head_list "}" ";"
        # bnf.y.rb:915
        #|  result = val[1].end_of_parse( val[3] )
        self._unported(260)
        return result

    def _reduce_261(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # signature_NAME : IDENTIFIER
        # bnf.y.rb:919
        #| result = Signature.new( val[0].val )
        self._unported(261)
        return result

    def _reduce_262(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # function_head_list : /* empty */
        # bnf.y.rb:925
        #|  result = NamedList.new( nil, "function" )
        self._unported(262)
        return result

    def _reduce_263(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # function_head_list : function_head_list function_head
        # bnf.y.rb:927
        #|  result = val[0].add_item( val[1] )
        self._unported(263)
        return result

    def _reduce_264(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # function_head : type_specifier_qualifier_list declarator ";"
        # bnf.y.rb:931
        #|             # val[1]: Decl
        #|             if val[1].is_function? then
        #|                 result = FuncHead.new( val[1], val[0], false )
        #|                 val[1].set_kind :FUNCHEAD
        #|                 val[1].check
        #|             else
        #|                 # mikan 関数の配列も以下のメッセージになる
        #|                 Generator.error( "G1010 Not function"  )
        #|                 result = nil
        #|             end
        self._unported(264)
        return result

    def _reduce_265(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # function_head : spec_L ONEWAY spec_R type_specifier_qualifier_list declarator ";"
        # bnf.y.rb:944
        #|             if val[4].is_function? then
        #|                 result = FuncHead.new( val[4], val[3], true )
        #|             else
        #|                 Generator.error( "G1011 Not function"  )
        #|                 result = nil
        #|             end
        self._unported(265)
        return result

    def _reduce_266(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype : CELLTYPE celltype_NAME "{" celltype_statement_list "}" ";"
        # bnf.y.rb:956
        #|             val[1].end_of_parse
        #|             result = val[1]
        self._unported(266)
        return result

    def _reduce_267(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_NAME : IDENTIFIER
        # bnf.y.rb:963
        #|  result = Celltype.new(val[0].val)
        self._unported(267)
        return result

    def _reduce_270(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_celltype_statement : celltype_statement
        # bnf.y.rb:971
        #|             if val[0].kind_of? Port then
        #|                 Celltype.new_port( val[0] )
        #|             end
        self._unported(270)
        return result

    def _reduce_271(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_celltype_statement : spec_L celltype_statement_specifier_list spec_R celltype_statement
        # bnf.y.rb:977
        #|             if val[3].kind_of? Port then
        #|                 val[3].set_specifier val[1]  # 設定順序あり
        #|                 Celltype.new_port( val[3] )
        #|             else
        #|                 # Port 以外では指定子はエラー
        #|                 Generator.error( "G1012 $1 : cannot put specifier here" , val[1] )
        #|             end
        self._unported(271)
        return result

    def _reduce_277(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier_list : celltype_statement_specifier
        # bnf.y.rb:997
        #|  result = [ val[0] ]
        self._unported(277)
        return result

    def _reduce_278(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier_list : celltype_statement_specifier_list "," celltype_statement_specifier
        # bnf.y.rb:999
        #|  result << val[2]
        self._unported(278)
        return result

    def _reduce_279(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier : INLINE
        # bnf.y.rb:1002
        #|  result = [ :INLINE ]
        self._unported(279)
        return result

    def _reduce_280(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier : ALLOCATOR "(" alloc_list2 ")"
        # bnf.y.rb:1003
        #|  result = [ :ALLOCATOR, val[2] ]
        self._unported(280)
        return result

    def _reduce_281(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier : OPTIONAL
        # bnf.y.rb:1004
        #|  result = [ :OPTIONAL ]
        self._unported(281)
        return result

    def _reduce_282(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier : REF_DESC
        # bnf.y.rb:1005
        #|  result = [ :REF_DESC ]
        self._unported(282)
        return result

    def _reduce_283(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier : DYNAMIC
        # bnf.y.rb:1006
        #|  result = [ :DYNAMIC ]
        self._unported(283)
        return result

    def _reduce_284(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # celltype_statement_specifier : OMIT
        # bnf.y.rb:1007
        #|  result = [ :OMIT ]
        self._unported(284)
        return result

    def _reduce_285(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc_list2 : alloc2
        # bnf.y.rb:1010
        #|  result = [ val[0] ]
        self._unported(285)
        return result

    def _reduce_286(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc_list2 : alloc
        # bnf.y.rb:1011
        #|  result = [ val[0] ]
        self._unported(286)
        return result

    def _reduce_287(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc_list2 : alloc_list2 "," alloc2
        # bnf.y.rb:1012
        #|  result << val[2]
        self._unported(287)
        return result

    def _reduce_288(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc_list2 : alloc_list2 "," alloc
        # bnf.y.rb:1013
        #|  result << val[2]
        self._unported(288)
        return result

    def _reduce_289(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc2 : port_name "." func_name "=" initializer
        # bnf.y.rb:1017
        #|   result = [ :INTERNAL_ALLOC, val[0].val, val[2].val, val[4] ]
        self._unported(289)
        return result

    def _reduce_290(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # alloc2 : port_name "." func_name "<=" initializer
        # bnf.y.rb:1019
        #|   result = [ :RELAY_ALLOC, val[0].val, val[2].val, val[4] ]
        self._unported(290)
        return result

    def _reduce_291(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port : port_type namespace_signature_name port_name ";"
        # bnf.y.rb:1025
        #|  result = Port.new( val[2].val, val[1], val[0] )
        self._unported(291)
        return result

    def _reduce_292(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port : port_type namespace_signature_name port_name "[" "]" ";"
        # bnf.y.rb:1027
        #|  result = Port.new( val[2].val, val[1], val[0], "[]" )
        self._unported(292)
        return result

    def _reduce_293(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port : port_type namespace_signature_name port_name "[" array_size "]" ";"
        # bnf.y.rb:1029
        #|  result = Port.new(val[2].val, val[1], val[0], val[4])
        self._unported(293)
        return result

    def _reduce_294(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port : port_type namespace_signature_name port_name "<=" namespace_identifier "." IDENTIFIER ";"
        # bnf.y.rb:1031
        #|  result = Port.new( val[2].val, val[1], val[0], nil, val[4], val[ 6 ].val )
        self._unported(294)
        return result

    def _reduce_295(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port_type : CALL
        # bnf.y.rb:1034
        #|  result = :CALL
        self._unported(295)
        return result

    def _reduce_296(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # port_type : ENTRY
        # bnf.y.rb:1035
        #|  result = :ENTRY
        self._unported(296)
        return result

    def _reduce_297(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_signature_name : namespace_identifier
        # bnf.y.rb:1039
        #|  result = val[0]
        self._unported(297)
        return result

    def _reduce_299(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute : ATTRIBUTE "{" attribute_declaration_list "}" ";"
        # bnf.y.rb:1048
        #|  result = nil
        self._unported(299)
        return result

    def _reduce_300(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_declaration_list : attribute_declaration
        # bnf.y.rb:1052
        #|  Celltype.new_attribute( val[0] )
        self._unported(300)
        return result

    def _reduce_301(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_declaration_list : attribute_declaration_list attribute_declaration
        # bnf.y.rb:1054
        #|  Celltype.new_attribute( val[1] )
        self._unported(301)
        return result

    def _reduce_302(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_declaration : declaration
        # bnf.y.rb:1059
        #|             val[0].each{ |i|       # i:Decl
        #|                 i.set_kind( :ATTRIBUTE )
        #|                 i.check
        #|             }
        #|             result = val[0]
        self._unported(302)
        return result

    def _reduce_303(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_declaration : spec_L attribute_specifier spec_R declaration
        # bnf.y.rb:1067
        #|             val[3].each{ |i|       # i:Decl
        #|                 i.set_kind( :ATTRIBUTE )   # 設定順序あり
        #|                 i.set_specifier_list( [val[1]] )
        #|                 i.check
        #|             }
        #|             result = val[3]
        self._unported(303)
        return result

    def _reduce_304(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_specifier : OMIT
        # bnf.y.rb:1077
        #|  result = [:OMIT]
        self._unported(304)
        return result

    def _reduce_305(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_specifier : SIZE_IS "(" expression ")"
        # bnf.y.rb:1078
        #|  result = [:SIZE_IS,val[2]]
        self._unported(305)
        return result

    def _reduce_306(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # attribute_specifier : CHOICE "=" "{" choice_list "}"
        # bnf.y.rb:1079
        #|   result = [:CHOICE,val[3]]
        self._unported(306)
        return result

    def _reduce_307(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # choice_list : choice_list "," choice_element
        # bnf.y.rb:1082
        #|   result << val[2]
        self._unported(307)
        return result

    def _reduce_308(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # choice_list : choice_element
        # bnf.y.rb:1083
        #|   result = [ val[0] ]
        self._unported(308)
        return result

    def _reduce_310(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var : VAR "{" var_declaration_list "}" ";"
        # bnf.y.rb:1091
        #|  result = nil
        self._unported(310)
        return result

    def _reduce_311(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var_declaration_list : var_declaration
        # bnf.y.rb:1095
        #|  Celltype.new_var( val[0] )
        self._unported(311)
        return result

    def _reduce_312(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var_declaration_list : var_declaration_list var_declaration
        # bnf.y.rb:1097
        #|  Celltype.new_var( val[1] )
        self._unported(312)
        return result

    def _reduce_313(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var_declaration : declaration
        # bnf.y.rb:1101
        #|             val[0].each{ |i|       # i:Decl
        #|                 i.set_kind( :VAR )
        #|                 i.check
        #|             }
        self._unported(313)
        return result

    def _reduce_314(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var_declaration : spec_L var_specifier spec_R declaration
        # bnf.y.rb:1108
        #|             val[3].each{ |i|       # i:Decl
        #|                 i.set_kind( :VAR )   # 設定順序あり
        #|                 i.set_specifier_list( [val[1]] )
        #|                 i.check
        #|             }
        #|             result = val[3]
        self._unported(314)
        return result

    def _reduce_315(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # var_specifier : SIZE_IS "(" expression ")"
        # bnf.y.rb:1118
        #|  result = [:SIZE_IS,val[2]]
        self._unported(315)
        return result

    def _reduce_316(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # require : REQUIRE namespace_identifier "." port_name ";"
        # bnf.y.rb:1123
        #|             Celltype.new_require( val[1], val[3] )
        self._unported(316)
        return result

    def _reduce_317(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # require : REQUIRE port_name "=" namespace_identifier "." port_name ";"
        # bnf.y.rb:1127
        #|             Celltype.new_require( val[3], val[5], val[1].val )
        self._unported(317)
        return result

    def _reduce_319(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # factory_head : FACTORY
        # bnf.y.rb:1136
        #|  Factory.set_f_celltype( false )
        self._unported(319)
        return result

    def _reduce_320(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # factory_head : CTFACTORY
        # bnf.y.rb:1137
        #|  Factory.set_f_celltype( true )
        self._unported(320)
        return result

    def _reduce_323(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # factory_function : factory_function_name "(" constant_expression "," constant_expression ")" ";"
        # bnf.y.rb:1145
        #|  Factory.new( val[0].val, val[2], val[4], nil    )
        self._unported(323)
        return result

    def _reduce_324(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # factory_function : factory_function_name "(" constant_expression "," constant_expression "," arg_list ")" ";"
        # bnf.y.rb:1147
        #|  Factory.new( val[0].val, val[2], val[4], val[6] )
        self._unported(324)
        return result

    def _reduce_326(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # arg_list : IDENTIFIER
        # bnf.y.rb:1154
        #|  result = [ [ :IDENTIFIER, val[0].val ] ]
        self._unported(326)
        return result

    def _reduce_327(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # arg_list : arg_list "," IDENTIFIER
        # bnf.y.rb:1156
        #|  result << [ :IDENTIFIER, val[2].val ]
        self._unported(327)
        return result

    def _reduce_328(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # arg_list : STRING_LITERAL
        # bnf.y.rb:1158
        #|  result = [ [ :STRING_LITERAL, val[0].val ] ]
        self._unported(328)
        return result

    def _reduce_329(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # arg_list : arg_list "," STRING_LITERAL
        # bnf.y.rb:1160
        #|  result << [ :STRING_LITERAL, val[2].val ]
        self._unported(329)
        return result

    def _reduce_330(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @3 : /* empty */
        # bnf.y.rb:1165
        #|  Cell.new_def
        self._unported(330)
        return result

    def _reduce_331(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cell : CELL namespace_celltype_NAME cell_NAME "{" @3 join_list "}" ";"
        # bnf.y.rb:1167
        #|  result = Cell.end_of_parse true
        self._unported(331)
        return result

    def _reduce_332(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cell : CELL namespace_celltype_NAME cell_NAME ";"
        # bnf.y.rb:1169
        #|  result = Cell.end_of_parse false
        self._unported(332)
        return result

    def _reduce_333(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_celltype_NAME : namespace_identifier
        # bnf.y.rb:1173
        #|  result = Cell.new(val[0])
        self._unported(333)
        return result

    def _reduce_334(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cell_NAME : IDENTIFIER
        # bnf.y.rb:1177
        #|  result = Cell.set_name(val[0].val)
        self._unported(334)
        return result

    def _reduce_338(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_join : spec_L join_specifier_list spec_R join
        # bnf.y.rb:1186
        #|  val[3].set_specifier_list( val[1] )
        self._unported(338)
        return result

    def _reduce_339(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_join : join
        # bnf.y.rb:1188
        #|  val[0].set_specifier_list( [] )
        self._unported(339)
        return result

    def _reduce_340(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join_specifier_list : join_specifier_list "," join_specifier
        # bnf.y.rb:1192
        #|  result << val[2]
        self._unported(340)
        return result

    def _reduce_341(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join_specifier_list : join_specifier
        # bnf.y.rb:1194
        #|  result = [val[0]]
        self._unported(341)
        return result

    def _reduce_342(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join_specifier : THROUGH "(" plugin_name "," plugin_arg ")"
        # bnf.y.rb:1198
        #|  result = [ :THROUGH, val[2], val[4] ]
        self._unported(342)
        return result

    def _reduce_345(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join : cae_name "[" "]" "=" expression ";"
        # bnf.y.rb:1214
        #|             result = Join.new( val[0].val,  -1, val[4] )
        #|             Cell.new_join( result, true )
        self._unported(345)
        return result

    def _reduce_346(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join : cae_name "[" array_index "]" "=" expression ";"
        # bnf.y.rb:1219
        #|             result = Join.new( val[0].val, val[2], val[5] )
        #|             Cell.new_join( result, true )
        self._unported(346)
        return result

    def _reduce_347(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join : cae_name "=" initializer ";"
        # bnf.y.rb:1224
        #|             result = Join.new( val[0].val, nil, val[2] )
        #|             Cell.new_join( result, true )
        self._unported(347)
        return result

    def _reduce_348(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # join : cae_name "=" COMPOSITE "." IDENTIFIER ";"
        # bnf.y.rb:1229
        #|             result = Join.new( val[0].val, nil, [ :COMPOSITE, val[4] ] )
        #|             Cell.new_join( result, true )
        self._unported(348)
        return result

    def _reduce_350(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # reverse_join : cae_name "<=" namespace_identifier "." port_name ";"
        # bnf.y.rb:1240
        #|             rj = ReverseJoin.new( val[0].val, nil, val[2], val[4].val )
        #|             Cell.new_reverse_join( rj )
        self._unported(350)
        return result

    def _reduce_351(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # reverse_join : cae_name "<=" namespace_identifier "." port_name "[" expression "]" ";"
        # bnf.y.rb:1246
        #|             rj = ReverseJoin.new( val[0].val, nil, val[2], val[4].val, val[6] )
        #|             Cell.new_reverse_join( rj )
        self._unported(351)
        return result

    def _reduce_352(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # reverse_join : cae_name "[" array_index "]" "<=" namespace_identifier "." port_name ";"
        # bnf.y.rb:1252
        #|             rj = ReverseJoin.new( val[0].val, val[2], val[5], val[7].val )
        #|             Cell.new_reverse_join( rj )
        self._unported(352)
        return result

    def _reduce_353(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # reverse_join : cae_name "[" array_index "]" "<=" namespace_identifier "." port_name "[" expression "]" ";"
        # bnf.y.rb:1258
        #|             rj = ReverseJoin.new( val[0].val, val[2], val[5], val[7].val, val[9] )
        #|             Cell.new_reverse_join( rj )
        self._unported(353)
        return result

    def _reduce_355(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype : COMPOSITE composite_celltype_NAME "{" composite_celltype_statement_list "}" ";"
        # bnf.y.rb:1270
        #|             CompositeCelltype.end_of_parse
        #|             result = val[1]
        self._unported(355)
        return result

    def _reduce_356(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_NAME : IDENTIFIER
        # bnf.y.rb:1277
        #|  result = CompositeCelltype.new(val[0].val)
        self._unported(356)
        return result

    def _reduce_359(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_composite_celltype_statement : composite_celltype_statement
        # bnf.y.rb:1285
        #|             if val[0].kind_of?( Port ) then
        #|                 CompositeCelltype.new_port( val[0] )   # 遅延して登録
        #|             end
        self._unported(359)
        return result

    def _reduce_360(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # specified_composite_celltype_statement : spec_L composite_celltype_statement_specifier_list spec_R composite_celltype_statement
        # bnf.y.rb:1291
        #|             if val[3].kind_of?( Port ) then
        #|                 # port 以外 val[3] に有効な値が入っていないので、以下のメソッドを適用できない
        #|                 # 現状 port, cell 以外は指定子を受け付けない
        #|                 # （しかし将来他の文も指定子を受け付ける可能性があるので、この位置に記述する）
        #|                 val[3].set_specifier( Generator.get_statement_specifier )
        #|                 CompositeCelltype.new_port( val[3] )   # 遅延して登録 (set_specifier 後)
        #|             elsif val[3].kind_of?( Cell ) then
        #|                 # Cell.end_of_parse にて設定
        #|             else
        #|           Generator.get_statement_specifier   # クリア
        #|           Generator.error( "G1013 unexpected specifier"  )
        #|             end
        self._unported(360)
        return result

    def _reduce_365(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier_list : composite_celltype_statement_specifier
        # bnf.y.rb:1315
        #|             Generator.add_statement_specifier val[0]
        #|             result = [ val[0] ]
        self._unported(365)
        return result

    def _reduce_366(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier_list : composite_celltype_statement_specifier_list "," composite_celltype_statement_specifier
        # bnf.y.rb:1320
        #|             Generator.add_statement_specifier val[2]
        #|             result = val[0] << val[2]
        self._unported(366)
        return result

    def _reduce_367(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier : ALLOCATOR "(" alloc_list2 ")"
        # bnf.y.rb:1326
        #|  result = [ :ALLOCATOR, val[2] ]
        self._unported(367)
        return result

    def _reduce_368(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier : OMIT
        # bnf.y.rb:1327
        #|  result = [ :OMIT ]
        self._unported(368)
        return result

    def _reduce_369(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier : OPTIONAL
        # bnf.y.rb:1328
        #|  result = [ :OPTIONAL ]
        self._unported(369)
        return result

    def _reduce_370(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier : REF_DESC
        # bnf.y.rb:1329
        #|  result = [ :REF_DESC ]
        self._unported(370)
        return result

    def _reduce_371(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_celltype_statement_specifier : DYNAMIC
        # bnf.y.rb:1330
        #|  result = [ :DYNAMIC ]
        self._unported(371)
        return result

    def _reduce_372(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_port : port
        # bnf.y.rb:1334
        #|             # CompositeCelltype.new_port( val[0] )
        #|             result = val[0]
        self._unported(372)
        return result

    def _reduce_373(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_attribute : ATTRIBUTE "{" composite_attribute_declaration_list "}" ";"
        # bnf.y.rb:1342
        #|  result = nil
        self._unported(373)
        return result

    def _reduce_374(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_attribute_declaration_list : attribute_declaration
        # bnf.y.rb:1346
        #|  CompositeCelltype.new_attribute( val[0] )
        self._unported(374)
        return result

    def _reduce_375(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # composite_attribute_declaration_list : composite_attribute_declaration_list attribute_declaration
        # bnf.y.rb:1348
        #|  CompositeCelltype.new_attribute( val[1] )
        self._unported(375)
        return result

    def _reduce_376(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @4 : /* empty */
        # bnf.y.rb:1353
        #|  Cell.new_def
        self._unported(376)
        return result

    def _reduce_377(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # internal_cell : CELL internal_namespace_celltype_NAME internal_cell_NAME "{" @4 internal_join_list "}" ";"
        # bnf.y.rb:1355
        #|  result = Cell.end_of_parse true
        self._unported(377)
        return result

    def _reduce_378(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # internal_cell : CELL internal_namespace_celltype_NAME internal_cell_NAME ";"
        # bnf.y.rb:1357
        #|  result = Cell.end_of_parse false
        self._unported(378)
        return result

    def _reduce_379(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # internal_namespace_celltype_NAME : namespace_identifier
        # bnf.y.rb:1361
        #|  Cell.new(val[0],true)
        self._unported(379)
        return result

    def _reduce_380(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # internal_cell_NAME : IDENTIFIER
        # bnf.y.rb:1365
        #|  Cell.set_name(val[0].val)
        self._unported(380)
        return result

    def _reduce_385(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # external_join : internal_cell_elem_name "=>" COMPOSITE "." export_name ";"
        # bnf.y.rb:1375
        #|     Cell.external_join( val[0].val, val[4].val, true )
        self._unported(385)
        return result

    def _reduce_386(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # external_join : internal_cell_elem_name "=>" export_name ";"
        # bnf.y.rb:1377
        #|     Cell.external_join( val[0].val, val[2].val, false )
        self._unported(386)
        return result

    def _reduce_387(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # export_join : export_name "=>" internal_ref_cell_name "." internal_cell_elem_name ";"
        # bnf.y.rb:1383
        #|             CompositeCelltype.new_join( val[0].val,
        #|                         val[2].val, val[4].val, :ENTRY )
        self._unported(387)
        return result

    def _reduce_388(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # export_join : COMPOSITE "." export_name "=>" internal_ref_cell_name "." internal_cell_elem_name ";"
        # bnf.y.rb:1388
        #|             CompositeCelltype.new_join( val[2].val,
        #|                         val[4].val, val[6].val, :ENTRY )
        self._unported(388)
        return result

    def _reduce_392(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region : spec_L region_specifier_list spec_R REGION region_NAME "{" region_statement "}" ";"
        # bnf.y.rb:1405
        #|  Region.end_of_parse
        self._unported(392)
        return result

    def _reduce_393(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region : REGION region_NAME "{" region_statement "}" ";"
        # bnf.y.rb:1407
        #|  Region.end_of_parse
        self._unported(393)
        return result

    def _reduce_396(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : IN_THROUGH "(" plugin_name "," plugin_arg ")"
        # bnf.y.rb:1415
        #|  Region.new_in_through( val[2].val, val[4].val )
        self._unported(396)
        return result

    def _reduce_397(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : IN_THROUGH "(" ")"
        # bnf.y.rb:1417
        #|  Region.new_in_through
        self._unported(397)
        return result

    def _reduce_398(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : OUT_THROUGH "(" plugin_name "," plugin_arg ")"
        # bnf.y.rb:1419
        #|  Region.new_out_through( val[2].val, val[4].val )
        self._unported(398)
        return result

    def _reduce_399(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : OUT_THROUGH "(" ")"
        # bnf.y.rb:1421
        #|  Region.new_out_through()
        self._unported(399)
        return result

    def _reduce_400(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : TO_THROUGH "(" namespace_region_NAME "," plugin_name "," plugin_arg ")"
        # bnf.y.rb:1423
        #|  Region.new_to_through( val[2], val[4].val, val[6].val )
        self._unported(400)
        return result

    def _reduce_401(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : TO_THROUGH "(" namespace_region_NAME ")"
        # bnf.y.rb:1425
        #|  Region.new_to_through( val[2], nil, nil )
        self._unported(401)
        return result

    def _reduce_402(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : FROM_THROUGH "(" namespace_region_NAME "," plugin_name "," plugin_arg ")"
        # bnf.y.rb:1427
        #|  Region.new_from_through( val[2], val[4].val, val[6].val )
        self._unported(402)
        return result

    def _reduce_403(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : FROM_THROUGH "(" namespace_region_NAME ")"
        # bnf.y.rb:1429
        #|  Region.new_from_through( val[2], nil, nil )
        self._unported(403)
        return result

    def _reduce_404(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : NODE
        # bnf.y.rb:1431
        #|  Region.set_type( :NODE )
        self._unported(404)
        return result

    def _reduce_405(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : LINKUNIT
        # bnf.y.rb:1433
        #|  Region.set_type( :LINKUNIT )
        self._unported(405)
        return result

    def _reduce_406(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : DOMAIN "(" domain_type "," domain_name ")"
        # bnf.y.rb:1435
        #|  Region.set_domain( val[2].val, val[4] )
        self._unported(406)
        return result

    def _reduce_407(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_specifier : CLASS "(" class_type "," class_name ")"
        # bnf.y.rb:1437
        #|  Region.set_class( val[2].val, val[4] )
        self._unported(407)
        return result

    def _reduce_408(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_NAME : IDENTIFIER
        # bnf.y.rb:1441
        #|  result = Region.new( val[0].val )
        self._unported(408)
        return result

    def _reduce_417(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # region_cell : spec_L statement_specifier_list spec_R cell
        # bnf.y.rb:1461
        #|             obj = val[3]
        #|             if obj.kind_of?( Cell ) then
        #|             else
        #|           Generator.get_statement_specifier   # クリア
        #|           Generator.error( "G9999 unexpected specifier"  )
        #|             end
        self._unported(417)
        return result

    def _reduce_418(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_region_NAME : IDENTIFIER
        # bnf.y.rb:1483
        #|  result = [ val[0].val ]
        self._unported(418)
        return result

    def _reduce_419(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # spec_L : "["
        # bnf.y.rb:1488
        #|  set_in_specifier
        self.set_in_specifier()
        self._unported(419)
        return result

    def _reduce_420(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # spec_R : "]"
        # bnf.y.rb:1490
        #|  unset_in_specifier
        self.unset_in_specifier()
        self._unported(420)
        return result

    def _reduce_421(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # tool_info : TOOL_INFO "(" JSON_string ")" JSON_object
        # bnf.y.rb:1495
        #|  TOOL_INFO.new( val[2].to_sym, val[4] )
        self._unported(421)
        return result

    def _reduce_422(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_object : "{" JSON_property_list "}"
        # bnf.y.rb:1496
        #|   result = val[1]
        self._unported(422)
        return result

    def _reduce_423(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_property_list : JSON_string ":" JSON_value
        # bnf.y.rb:1497
        #|  result = { val[0].to_sym => val[2] }
        self._unported(423)
        return result

    def _reduce_424(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_property_list : JSON_property_list "," JSON_string ":" JSON_value
        # bnf.y.rb:1499
        #|  val[0][ val[2].to_sym ] = val[4]
        self._unported(424)
        return result

    def _reduce_429(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_value : TRUE
        # bnf.y.rb:1501
        #|  result=val[0].val
        self._unported(429)
        return result

    def _reduce_430(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_value : FALSE
        # bnf.y.rb:1501
        #|  result=val[0].val
        self._unported(430)
        return result

    def _reduce_431(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_array : "[" JSON_array_list "]"
        # bnf.y.rb:1502
        #|  result = val[1]
        self._unported(431)
        return result

    def _reduce_432(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_array : "[" "]"
        # bnf.y.rb:1503
        #|  result = []
        self._unported(432)
        return result

    def _reduce_433(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_array_list : JSON_value
        # bnf.y.rb:1504
        #|  result = [ val[0] ]
        self._unported(433)
        return result

    def _reduce_434(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_array_list : JSON_array_list "," JSON_value
        # bnf.y.rb:1505
        #|  val[0] << val[2]
        self._unported(434)
        return result

    def _reduce_435(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_string : STRING_LITERAL
        # bnf.y.rb:1506
        #|  result = val[0].val.gsub!( /\"(.*)\"/, "\\1" )
        self._unported(435)
        return result

    def _reduce_436(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_number : INTEGER_CONSTANT
        # bnf.y.rb:1507
        #|  result = val[0].val.to_i
        self._unported(436)
        return result

    def _reduce_437(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_number : FLOATING_CONSTANT
        # bnf.y.rb:1508
        #|  result = val[0].val.to_f
        self._unported(437)
        return result

    def _reduce_438(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_number : "-" INTEGER_CONSTANT
        # bnf.y.rb:1509
        #|  result = - val[0].val.to_i
        self._unported(438)
        return result

    def _reduce_439(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_number : "-" FLOATING_CONSTANT
        # bnf.y.rb:1510
        #|  result = - val[0].val.to_f
        self._unported(439)
        return result

    def _reduce_440(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_number : "+" INTEGER_CONSTANT
        # bnf.y.rb:1511
        #|  result = val[0].val.to_i
        self._unported(440)
        return result

    def _reduce_441(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # JSON_number : "+" FLOATING_CONSTANT
        # bnf.y.rb:1512
        #|  result = val[0].val.to_f
        self._unported(441)
        return result


# アクションを持つ規則の番号（移植漏れの検査に使う）
ACTION_RULES = frozenset(
    i
    for i, r in enumerate(REDUCE_TABLE)
    if r[2].startswith("_reduce_") and r[2] != "_reduce_none"
)
