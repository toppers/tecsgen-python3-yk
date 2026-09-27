"""C_parser.y.rb の文法アクション（racc の _reduce_N）。

tools/port/gen_action_stubs.py で骨格を生成し、本体は手で移植する。各メソッドの
コメントは、規則（左辺 : 右辺）と移植元のアクション（行番号付き）。
`self._unported(N)` が残っているメソッドは、まだ移植していない。
"""

from __future__ import annotations

from typing import Any

from tecsgen.syntax.cdecl_tables import REDUCE_TABLE


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

    def _reduce_2(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : namespace_identifier
        # C_parser.y.rb:53
        #|  result = [ :IDENTIFIER, val[0] ]
        self._unported(2)
        return result

    def _reduce_3(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : INTEGER_CONSTANT
        # C_parser.y.rb:61
        #|  result = [ :INTEGER_CONSTANT, val[0] ]
        self._unported(3)
        return result

    def _reduce_4(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : FLOATING_CONSTANT
        # C_parser.y.rb:63
        #|  result = [ :FLOATING_CONSTANT, val[0] ]
        self._unported(4)
        return result

    def _reduce_5(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : OCTAL_CONSTANT
        # C_parser.y.rb:65
        #|  result = [ :OCTAL_CONSTANT, val[0] ]
        self._unported(5)
        return result

    def _reduce_6(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : HEX_CONSTANT
        # C_parser.y.rb:67
        #|  result = [ :HEX_CONSTANT, val[0] ]
        self._unported(6)
        return result

    def _reduce_7(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : CHARACTER_LITERAL
        # C_parser.y.rb:69
        #|  result = [ :CHARACTER_LITERAL, val[0] ]
        self._unported(7)
        return result

    def _reduce_8(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : string_literal_list
        # C_parser.y.rb:71
        #|  result = [ :STRING_LITERAL_LIST, val[0] ]
        self._unported(8)
        return result

    def _reduce_9(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : "(" expression ")"
        # C_parser.y.rb:73
        #|  result = [ :PARENTHESES, val[1].get_elements ]
        self._unported(9)
        return result

    def _reduce_10(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # string_literal_list : STRING_LITERAL
        # C_parser.y.rb:77
        #|  result = [val[0]]
        self._unported(10)
        return result

    def _reduce_11(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # string_literal_list : string_literal_list STRING_LITERAL
        # C_parser.y.rb:79
        #|  result << val[1]
        self._unported(11)
        return result

    def _reduce_13(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "[" expression "]"
        # C_parser.y.rb:85
        #|  result = [ :OP_SUBSC, val[0], val[2] ]
        self._unported(13)
        return result

    def _reduce_17(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "." IDENTIFIER
        # C_parser.y.rb:90
        #|  result = [ :OP_DOT, val[0], val[2] ]
        self._unported(17)
        return result

    def _reduce_18(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "->" IDENTIFIER
        # C_parser.y.rb:92
        #|  result = [ :OP_REF, val[0], val[2] ]
        self._unported(18)
        return result

    def _reduce_19(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "++"
        # C_parser.y.rb:93
        #|  result = val[0]
        self._unported(19)
        return result

    def _reduce_20(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression "--"
        # C_parser.y.rb:94
        #|  result = val[0]
        self._unported(20)
        return result

    def _reduce_26(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : unary_operator cast_expression
        # C_parser.y.rb:107
        #|  result = [ val[0], val[1] ]
        self._unported(26)
        return result

    def _reduce_27(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : SIZEOF unary_expression
        # C_parser.y.rb:109
        #|  result = [ :OP_SIZEOF_EXPR, val[1] ]
        self._unported(27)
        return result

    def _reduce_28(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : SIZEOF "(" type_name ")"
        # C_parser.y.rb:111
        #|  result = [ :OP_SIZEOF_TYPE, val[1] ]
        self._unported(28)
        return result

    def _reduce_29(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : "++" unary_expression
        # C_parser.y.rb:112
        #|  result = val[1]
        self._unported(29)
        return result

    def _reduce_30(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : "--" unary_expression
        # C_parser.y.rb:113
        #|  result = val[1]
        self._unported(30)
        return result

    def _reduce_31(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "&"
        # C_parser.y.rb:116
        #|  result = :OP_U_AMP
        self._unported(31)
        return result

    def _reduce_32(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "*"
        # C_parser.y.rb:117
        #|  result = :OP_U_ASTER
        self._unported(32)
        return result

    def _reduce_33(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "+"
        # C_parser.y.rb:118
        #|  result = :OP_U_PLUS
        self._unported(33)
        return result

    def _reduce_34(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "-"
        # C_parser.y.rb:119
        #|  result = :OP_U_MINUS
        self._unported(34)
        return result

    def _reduce_35(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "~"
        # C_parser.y.rb:120
        #|  result = :OP_U_TILDE
        self._unported(35)
        return result

    def _reduce_36(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_operator : "!"
        # C_parser.y.rb:121
        #|  result = :OP_U_EXCLAM
        self._unported(36)
        return result

    def _reduce_38(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cast_expression : "(" type_name ")" cast_expression
        # C_parser.y.rb:126
        #|   result = [ :CAST, val[1], val[3] ]
        self._unported(38)
        return result

    def _reduce_40(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # multiplicative_expression : multiplicative_expression "*" cast_expression
        # C_parser.y.rb:131
        #|  result = [ :OP_MULT, val[0], val[2] ]
        self._unported(40)
        return result

    def _reduce_41(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # multiplicative_expression : multiplicative_expression "/" cast_expression
        # C_parser.y.rb:133
        #|  result = [ :OP_DIV, val[0], val[2] ]
        self._unported(41)
        return result

    def _reduce_42(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # multiplicative_expression : multiplicative_expression "%" cast_expression
        # C_parser.y.rb:135
        #|  result = [ :OP_REMAIN, val[0], val[2] ]
        self._unported(42)
        return result

    def _reduce_44(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # additive_expression : additive_expression "+" multiplicative_expression
        # C_parser.y.rb:140
        #|  result = [ :OP_ADD, val[0], val[2] ]
        self._unported(44)
        return result

    def _reduce_45(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # additive_expression : additive_expression "-" multiplicative_expression
        # C_parser.y.rb:142
        #|  result = [ :OP_SUB, val[0], val[2] ]
        self._unported(45)
        return result

    def _reduce_47(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # shift_expression : shift_expression "<<" additive_expression
        # C_parser.y.rb:147
        #|  result = [ :OP_LSFT, val[0], val[2] ]
        self._unported(47)
        return result

    def _reduce_48(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # shift_expression : shift_expression ">>" additive_expression
        # C_parser.y.rb:149
        #|  result = [ :OP_RSFT, val[0], val[2] ]
        self._unported(48)
        return result

    def _reduce_50(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression "<" shift_expression
        # C_parser.y.rb:154
        #|  result = [ :OP_LT, val[0], val[2] ]
        self._unported(50)
        return result

    def _reduce_51(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression ">" shift_expression
        # C_parser.y.rb:156
        #|  result = [ :OP_GT, val[0], val[2] ]
        self._unported(51)
        return result

    def _reduce_52(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression "<=" shift_expression
        # C_parser.y.rb:158
        #|  result = [ :OP_LE, val[0], val[2] ]
        self._unported(52)
        return result

    def _reduce_53(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # relational_expression : relational_expression ">=" shift_expression
        # C_parser.y.rb:160
        #|  result = [ :OP_GE, val[0], val[2] ]
        self._unported(53)
        return result

    def _reduce_55(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # equality_expression : equality_expression "==" relational_expression
        # C_parser.y.rb:165
        #|  result = [ :OP_EQ, val[0], val[2] ]
        self._unported(55)
        return result

    def _reduce_56(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # equality_expression : equality_expression "!=" relational_expression
        # C_parser.y.rb:167
        #|  result = [ :OP_NE, val[0], val[2] ]
        self._unported(56)
        return result

    def _reduce_58(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # and_expression : and_expression "&" equality_expression
        # C_parser.y.rb:172
        #|  result = [ :OP_AND, val[0], val[2] ]
        self._unported(58)
        return result

    def _reduce_60(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # exclusive_or_expression : exclusive_or_expression "^" and_expression
        # C_parser.y.rb:177
        #|  result = [ :OP_EOR, val[0], val[2] ]
        self._unported(60)
        return result

    def _reduce_62(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # inclusive_or_expression : inclusive_or_expression "|" exclusive_or_expression
        # C_parser.y.rb:182
        #|  result = [ :OP_OR, val[0], val[2] ]
        self._unported(62)
        return result

    def _reduce_64(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # logical_and_expression : logical_and_expression "&&" inclusive_or_expression
        # C_parser.y.rb:187
        #|  result = [ :OP_LAND, val[0], val[2] ]
        self._unported(64)
        return result

    def _reduce_66(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # logical_or_expression : logical_or_expression "||" logical_and_expression
        # C_parser.y.rb:192
        #|  result = [ :OP_LOR, val[0], val[2] ]
        self._unported(66)
        return result

    def _reduce_68(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # conditional_expression : logical_or_expression "?" expression ":" conditional_expression
        # C_parser.y.rb:197
        #|  result = [ :OP_CEX, val[0], val[2].get_elements, val[4] ]
        self._unported(68)
        return result

    def _reduce_82(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # expression : assignment_expression
        # C_parser.y.rb:218
        #| 			result = Expression.new( val[0] )
        #| 			# result.print
        self._unported(82)
        return result

    def _reduce_83(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # expression : expression "," assignment_expression
        # C_parser.y.rb:223
        #| 			result = Expression.new( val[2] )    # ',' の後ろを採用
        self._unported(83)
        return result

    def _reduce_84(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # constant_expression : conditional_expression
        # C_parser.y.rb:229
        #| 			result = Expression.new( val[0] )
        #| 			# result.print
        #| #			res = result.eval_const( nil )
        #|
        #| 			# if res then
        #| 			#   puts "val: #{res}"
        #| 			# else
        #| 			#   puts "val: nil"
        #| 			# end
        self._unported(84)
        return result

    def _reduce_86(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : storage_class
        # C_parser.y.rb:258
        #| 			result = CIntType.new( -3 )    # storage class は無視
        self._unported(86)
        return result

    def _reduce_88(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_qualifier
        # C_parser.y.rb:263
        #| 			result = CIntType.new( -3 )
        #| 			result.set_qualifier val[0]
        self._unported(88)
        return result

    def _reduce_89(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : storage_class declaration_specifiers
        # C_parser.y.rb:268
        #| 			result = val[1]                # storage class は無視
        self._unported(89)
        return result

    def _reduce_90(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_specifier declaration_specifiers
        # C_parser.y.rb:272
        #| 			result = val[1].merge val[0]
        self._unported(90)
        return result

    def _reduce_91(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration_specifiers : type_qualifier declaration_specifiers
        # C_parser.y.rb:276
        #| 			val[1].set_qualifier val[0]
        #|                         result = val[1]
        self._unported(91)
        return result

    def _reduce_94(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator
        # C_parser.y.rb:286
        #|  result = [val[0]]
        self._unported(94)
        return result

    def _reduce_95(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator_list "," init_declarator
        # C_parser.y.rb:288
        #|  result << val[2]
        self._unported(95)
        return result

    def _reduce_97(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator : declarator "=" initializer
        # C_parser.y.rb:293
        #|  val[0].set_initializer( val[2] )
        self._unported(97)
        return result

    def _reduce_102(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : VOID
        # C_parser.y.rb:304
        #|  set_no_type_name true; result = CVoidType.new
        self.set_no_type_name(True)
        self._unported(102)
        return result

    def _reduce_103(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : CHAR
        # C_parser.y.rb:306
        #|  set_no_type_name true; result = CIntType.new(-11 )
        self.set_no_type_name(True)
        self._unported(103)
        return result

    def _reduce_104(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : SHORT
        # C_parser.y.rb:308
        #|  set_no_type_name true; result = CIntType.new( -2 )
        self.set_no_type_name(True)
        self._unported(104)
        return result

    def _reduce_105(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : INT
        # C_parser.y.rb:310
        #|  set_no_type_name true; result = CIntType.new( -3 )
        self.set_no_type_name(True)
        self._unported(105)
        return result

    def _reduce_106(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : INT64
        # C_parser.y.rb:312
        #|  set_no_type_name true; result = CIntType.new( 64 )
        self.set_no_type_name(True)
        self._unported(106)
        return result

    def _reduce_107(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : BOOL
        # C_parser.y.rb:314
        #|  set_no_type_name true; result = CIntType.new( -3 )
        self.set_no_type_name(True)
        self._unported(107)
        return result

    def _reduce_108(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : LONG
        # C_parser.y.rb:316
        #|  set_no_type_name true; result = CIntType.new( -4 )
        self.set_no_type_name(True)
        self._unported(108)
        return result

    def _reduce_109(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : SIGNED
        # C_parser.y.rb:318
        #|           set_no_type_name true
        #|          	result = CIntType.new( -3 )
        #|           result.set_sign :SIGNED
        self.set_no_type_name(True)
        self._unported(109)
        return result

    def _reduce_110(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : UNSIGNED
        # C_parser.y.rb:324
        #|           set_no_type_name true
        #|           result = CIntType.new( -3 )
        #|           result.set_sign :UNSIGNED
        self.set_no_type_name(True)
        self._unported(110)
        return result

    def _reduce_111(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : FLOAT
        # C_parser.y.rb:330
        #|  set_no_type_name true; result = CFloatType.new(-32)
        self.set_no_type_name(True)
        self._unported(111)
        return result

    def _reduce_112(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : DOUBLE
        # C_parser.y.rb:332
        #|  set_no_type_name true; result = CFloatType.new(-64)
        self.set_no_type_name(True)
        self._unported(112)
        return result

    def _reduce_113(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : BOOL
        # C_parser.y.rb:334
        #|  set_no_type_name true; result = CBoolType.new
        self.set_no_type_name(True)
        self._unported(113)
        return result

    def _reduce_114(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : struct_specifier
        # C_parser.y.rb:336
        #|  set_no_type_name true; result = val[0]
        self.set_no_type_name(True)
        self._unported(114)
        return result

    def _reduce_115(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : union_specifier
        # C_parser.y.rb:338
        #|  set_no_type_name true; result = CVoidType.new
        self.set_no_type_name(True)
        self._unported(115)
        return result

    def _reduce_116(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : enum_specifier
        # C_parser.y.rb:340
        #|  set_no_type_name true; result = CVoidType.new
        self.set_no_type_name(True)
        self._unported(116)
        return result

    def _reduce_117(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : TYPEOF
        # C_parser.y.rb:341
        #|             token = next_token
        #|             if token && token[1].val == '(' then
        #|               depth = 1
        #|               while depth > 0
        #|                 token = next_token
        #|                 break if token.nil?
        #|                 case token[1].val
        #|                 when '(' then depth += 1
        #|                 when ')' then depth -= 1
        #|                 end
        #|               end
        #|             end
        #|             set_no_type_name true
        #|             result = CVoidType.new
        # P2 で移植: typeof( ... ) の括弧の中を読み飛ばす（パーサを通さずにトークンを消費する）
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
        self._unported(117)  # result = CVoidType.new
        return result

    def _reduce_118(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : TYPE_NAME
        # C_parser.y.rb:358
        #|  set_no_type_name true; result = CDefinedType.new( val[0].val )
        self.set_no_type_name(True)
        self._unported(118)
        return result

    def _reduce_119(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @1 : /* empty */
        # C_parser.y.rb:364
        #|  StructType.set_define( true )
        self._unported(119)
        return result

    def _reduce_120(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : struct_term struct_tag "{" @1 struct_declaration_list "}"
        # C_parser.y.rb:366
        #| 			StructType.end_of_parse
        #|       set_no_type_name true
        #| 			result = val[1]
        self.set_no_type_name(True)
        self._unported(120)
        return result

    def _reduce_121(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # @2 : /* empty */
        # C_parser.y.rb:373
        #| 			result = CStructType.new()
        #| 			StructType.set_define( true )
        self._unported(121)
        return result

    def _reduce_122(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : struct_term @2 "{" struct_declaration_list "}"
        # C_parser.y.rb:378
        #| 			StructType.end_of_parse
        #|       set_no_type_name true
        #| 			result = val[1]
        self.set_no_type_name(True)
        self._unported(122)
        return result

    def _reduce_123(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_specifier : struct_term struct_tag
        # C_parser.y.rb:384
        #| 			StructType.set_define( false )
        #| 			StructType.end_of_parse
        #|       set_no_type_name true
        #| 			result = val[1]
        self.set_no_type_name(True)
        self._unported(123)
        return result

    def _reduce_124(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_term : STRUCT
        # C_parser.y.rb:392
        #|  set_no_type_name true
        self.set_no_type_name(True)
        self._unported(124)
        return result

    def _reduce_127(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_tag : IDENTIFIER
        # C_parser.y.rb:400
        #| 			result = CStructType.new( val[0].val )
        #| 			set_no_type_name true
        self.set_no_type_name(True)
        self._unported(127)
        return result

    def _reduce_128(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declaration : declaration_specifiers struct_declarator_list ";"
        # C_parser.y.rb:409
        #| 			val[1].each { |i|	# i: Decl
        #| 				i.set_type( val[0] )
        #| 				i.set_kind( :MEMBER )
        #| 				i.check
        #| 				CStructType.new_member( i )
        #| 			}
        #| 			result = val[1]
        self._unported(128)
        return result

    def _reduce_132(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier_qualifier_list : type_specifier type_specifier_qualifier_list
        # C_parser.y.rb:428
        #| 			result = val[1].merge val[0]
        self._unported(132)
        return result

    def _reduce_133(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier_qualifier_list : type_qualifier
        # C_parser.y.rb:432
        #| 			result = CIntType.new( -3 )
        #| 			result.set_qualifier val[0]
        self._unported(133)
        return result

    def _reduce_134(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier_qualifier_list : type_qualifier type_specifier_qualifier_list
        # C_parser.y.rb:437
        #| 			val[1].set_qualifier val[0]
        #|                         result = val[1]
        self._unported(134)
        return result

    def _reduce_135(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declarator_list : struct_declarator
        # C_parser.y.rb:444
        #|  result = [ val[0] ]
        self._unported(135)
        return result

    def _reduce_136(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # struct_declarator_list : struct_declarator_list "," struct_declarator
        # C_parser.y.rb:446
        #|  result << val[2]
        self._unported(136)
        return result

    def _reduce_139(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # union_specifier : union_term union_tag "{" union_declaration_list "}"
        # C_parser.y.rb:456
        #|  set_no_type_name true
        self.set_no_type_name(True)
        self._unported(139)
        return result

    def _reduce_140(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # union_specifier : union_term "{" union_declaration_list "}"
        # C_parser.y.rb:457
        #|  set_no_type_name true
        self.set_no_type_name(True)
        self._unported(140)
        return result

    def _reduce_141(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # union_specifier : union_term union_tag
        # C_parser.y.rb:458
        #|  set_no_type_name true
        self.set_no_type_name(True)
        self._unported(141)
        return result

    def _reduce_142(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # union_term : UNION
        # C_parser.y.rb:461
        #|  set_no_type_name true
        self.set_no_type_name(True)
        self._unported(142)
        return result

    def _reduce_164(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_qualifier : CONST
        # C_parser.y.rb:504
        #|  result = :CONST
        self._unported(164)
        return result

    def _reduce_165(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_qualifier : VOLATILE
        # C_parser.y.rb:505
        #|  result = :VOLATILE
        self._unported(165)
        return result

    def _reduce_170(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer direct_declarator
        # C_parser.y.rb:515
        #| 			val[1].set_type( val[0] )
        #| 			result = val[1]
        self._unported(170)
        return result

    def _reduce_172(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer TYPE_NAME
        # C_parser.y.rb:521
        #| 			result = Decl.new( val[1].val )
        #| 			result.set_type( val[0] )
        self._unported(172)
        return result

    def _reduce_173(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : IDENTIFIER
        # C_parser.y.rb:528
        #|  result = Decl.new( val[0].val )
        self._unported(173)
        return result

    def _reduce_174(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : "(" declarator ")"
        # C_parser.y.rb:530
        #|  result = val[1]
        self._unported(174)
        return result

    def _reduce_175(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "[" constant_expression "]"
        # C_parser.y.rb:532
        #| 			val[0].set_type( CArrayType.new( val[2] ) )
        #| 			result = val[0]
        self._unported(175)
        return result

    def _reduce_176(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "[" "]"
        # C_parser.y.rb:537
        #| 			val[0].set_type( CArrayType.new )
        #| 			result = val[0]
        self._unported(176)
        return result

    def _reduce_177(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" parameter_type_list ")"
        # C_parser.y.rb:542
        #| 		# 	Generator.warning( "W6001 need 'void' for no parameter"  )
        #| 			val[0].set_type( CFuncType.new )
        #| 			result = val[0]
        self._unported(177)
        return result

    def _reduce_178(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator "(" ")"
        # C_parser.y.rb:550
        #| 		# 	Generator.warning( "W6002 need 'void' for no parameter"  )
        #| 			val[0].set_type( CFuncType.new )
        #| 			result = val[0]
        self._unported(178)
        return result

    def _reduce_179(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*"
        # C_parser.y.rb:558
        #|  result = CPtrType.new
        self._unported(179)
        return result

    def _reduce_180(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*" type_qualifier
        # C_parser.y.rb:560
        #| 			result = CPtrType.new
        #| 			result.set_qualifier( val[1] )
        self._unported(180)
        return result

    def _reduce_181(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*" pointer
        # C_parser.y.rb:565
        #| 			val[1].set_type(CPtrType.new)
        #| 			result = val[1]
        self._unported(181)
        return result

    def _reduce_182(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # pointer : "*" type_qualifier pointer
        # C_parser.y.rb:570
        #| 			ptrtype = CPtrType.new
        #| 			ptrtype.set_qualifier( val[1] )
        #| 			val[2].set_type( ptrtype )
        #| 			result = val[2]
        self._unported(182)
        return result

    def _reduce_200(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : "(" ")"
        # C_parser.y.rb:634
        #| 			Generator.warning( "W6003 need 'void' for no parameter"  )
        self._unported(200)
        return result

    def _reduce_202(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_abstract_declarator : direct_abstract_declarator "(" ")"
        # C_parser.y.rb:639
        #| 			Generator.warning( "W6004 need 'void' for no parameter"  )
        self._unported(202)
        return result

    def _reduce_204(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : assignment_expression
        # C_parser.y.rb:647
        #|  result = val[0]
        self._unported(204)
        return result

    def _reduce_205(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : "{" initializer_list "}"
        # C_parser.y.rb:649
        #|  result = val[1]
        self._unported(205)
        return result

    def _reduce_206(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : "{" initializer_list "," "}"
        # C_parser.y.rb:651
        #|  result = val[1]
        self._unported(206)
        return result

    def _reduce_207(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer : C_EXP "(" STRING_LITERAL ")"
        # C_parser.y.rb:653
        #|  result = C_EXP.new( val[2] )
        self._unported(207)
        return result

    def _reduce_208(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer_list : initializer
        # C_parser.y.rb:657
        #| 			result = [ val[0] ]
        self._unported(208)
        return result

    def _reduce_209(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # initializer_list : initializer_list "," initializer
        # C_parser.y.rb:661
        #| 			val[0] << val[2]
        #| 			result = val[0]
        self._unported(209)
        return result

    def _reduce_212(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # extension_statement : statement
        # C_parser.y.rb:675
        #|  set_no_type_name false
        self.set_no_type_name(False)
        self._unported(212)
        return result

    def _reduce_221(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF type_specifier_qualifier_list declarator_list ";"
        # C_parser.y.rb:689
        #| 			val[2].each{ |i|
        #| 			   i.set_kind( :TYPEDEF )
        #| 			}
        #| 			Typedef.new_decl_list( val[1], val[2] )
        #|                         # val[1].show_tree 0
        self._unported(221)
        return result

    def _reduce_222(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator_list : declarator
        # C_parser.y.rb:699
        #|  result = [ val[0] ]
        self._unported(222)
        return result

    def _reduce_223(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator_list : declarator_list "," declarator
        # C_parser.y.rb:701
        #|  result << val[2]
        self._unported(223)
        return result

    def _reduce_258(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_identifier : IDENTIFIER
        # C_parser.y.rb:764
        #|  result = NamespacePath.new( val[0].val, false )
        self._unported(258)
        return result

    def _reduce_259(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_identifier : "::" IDENTIFIER
        # C_parser.y.rb:765
        #|  result = NamespacePath.new( val[1].val, true )
        self._unported(259)
        return result

    def _reduce_260(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # namespace_identifier : namespace_identifier "::" IDENTIFIER
        # C_parser.y.rb:767
        #|  result = val[0].append!( val[2].val )
        self._unported(260)
        return result

    def _reduce_261(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # asm_statement : _ASM
        # C_parser.y.rb:770
        #|         while true
        #|           # ';' が表れるまで、トークンを読み飛ばす。
        #|           # gcc の構文拡張に対応すべきだが、単純な実装として、';' まで読み飛ばす。
        #|           # トークン単位で読み飛ばしているので、文字列やコメント内の ';' は対象にならない。
        #|           token = next_token
        #|           if token[1].val == ";"
        #|             break
        #|           end
        #| 		      # p "skip: #{token[1].val}"
        #|         end
        self._unported(261)
        return result


# アクションを持つ規則の番号（移植漏れの検査に使う）
ACTION_RULES = frozenset(
    i
    for i, r in enumerate(REDUCE_TABLE)
    if r[2].startswith("_reduce_") and r[2] != "_reduce_none"
)
