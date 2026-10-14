"""flowlib/C_parser.y.rb の文法アクション（racc の _reduce_N）。

tools/port/gen_action_stubs.py で骨格を生成し、本体を手で移植した。racc と同じく、
アクションが result に代入しない規則では、右辺の先頭の値（val[0]）が結果になる
（引数 result の初期値）。メソッド名の N は規則番号。コメントは規則と移植元の行番号。

値の表し方は Ruby と同じ。識別子の名前は Symbol、式の結果で連結した名前は str、
値の無いものは None。Ruby の `"#{x}"` は `to_s` で書く（`None` は空文字列になる）。
"""

from __future__ import annotations

from typing import Any

from tecsgen.flowlib.classes import Function
from tecsgen.ruby_compat import sym, to_s


class TcflowActions:
    """アクションの mixin。パーサ本体のクラスが継承する。"""

    # パーサ本体のクラスが持つ状態とメソッド
    _current_function: Function | None
    _type_name_list: dict[Any, Any]

    def set_no_type_name(self, b_no_type_name: bool) -> None:
        raise NotImplementedError

    def next_token(self) -> Any:
        raise NotImplementedError

    def error(self, msg: Any) -> None:
        raise NotImplementedError

    # --- 式 --------------------------------------------------------------------

    def _reduce_2(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : IDENTIFIER                       (C_parser.y.rb:50)
        return val[0].val

    def _reduce_3(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # primary_expression : INTEGER_CONSTANT | FLOATING_CONSTANT | OCTAL_CONSTANT
        #   | HEX_CONSTANT | CHARACTER_LITERAL | string_literal_list | '(' expression ')'
        #                                                       (C_parser.y.rb:51-59)
        return None

    _reduce_4 = _reduce_5 = _reduce_6 = _reduce_7 = _reduce_8 = _reduce_9 = _reduce_3

    def _reduce_12(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : primary_expression                         (C_parser.y.rb:68)
        return val[0]

    def _reduce_13(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression '(' argument_list ')'   (C_parser.y.rb:70)
        if val[0] is not None:
            if self._current_function is not None:
                self._current_function.ref_func(sym(val[0]))
            result = sym(f"{to_s(val[0])}()")
        return result

    def _reduce_14(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression '[' expression ']'      (C_parser.y.rb:80)
        return f"{to_s(val[0])}[]"

    def _reduce_15(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression '.' IDENTIFIER          (C_parser.y.rb:81)
        return f"{to_s(val[0])}.{to_s(val[2])}"

    def _reduce_16(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression '->' IDENTIFIER        (C_parser.y.rb:82)
        return f"{to_s(val[0])}->{to_s(val[2])}"

    def _reduce_17(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # postfix_expression : postfix_expression '++' | '--'            (C_parser.y.rb:83-84)
        return val[0]

    _reduce_18 = _reduce_17

    def _reduce_22(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : postfix_expression                           (C_parser.y.rb:96)
        # 式の値を「読み取り」として記録する。() で終わるものは関数として報告済み
        if (
            val[0] is not None
            and not to_s(val[0]).endswith("()")
            and self._current_function is not None
        ):
            self._current_function.ref_var(sym(val[0]))
            result = sym(val[0])
        return result

    def _reduce_23(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : '++' unary_expression | '--' unary_expression
        #   | SIZEOF unary_expression | SIZEOF '(' type_name ')'   (C_parser.y.rb:110-114)
        return None

    _reduce_24 = _reduce_26 = _reduce_27 = _reduce_23

    def _reduce_25(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # unary_expression : unary_operator cast_expression               (C_parser.y.rb:112)
        return val[1]

    def _reduce_35(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # cast_expression : '(' type_name ')' cast_expression             (C_parser.y.rb:126)
        return val[3]

    def _reduce_230(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # assignment_expression : unary_expression assignment_operator assignment_expression
        # 左辺を「書き込み」として記録する                               (C_parser.y.rb:548)
        if (
            val[0] is not None
            and not to_s(val[0]).endswith("()")
            and self._current_function is not None
        ):
            self._current_function.ref_var(sym(val[0]), True)
            result = sym(val[0])
        return result

    # --- 宣言 ------------------------------------------------------------------

    def _reduce_69(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration : declaration_specifiers init_declarator_list ';'   (C_parser.y.rb:220)
        return val[1]

    def _reduce_70(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declaration : declaration_specifiers ';'                        (C_parser.y.rb:221)
        return None

    def _reduce_77(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator                          (C_parser.y.rb:232)
        return [val[0]]

    def _reduce_78(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator_list : init_declarator_list ',' init_declarator (C_parser.y.rb:234)
        result.append(val[2])
        return result

    def _reduce_79(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # init_declarator : declarator | declarator '=' initializer      (C_parser.y.rb:239-240)
        return val[0]

    _reduce_80 = _reduce_79

    def _type_specifier(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # type_specifier : VOID | FLOAT | ... | __BOOL, struct_or_union : STRUCT | UNION
        # 構造体のメンバ名などが TYPE_NAME に置き換わらないよう字句解析の状態を変える
        #                                                       (C_parser.y.rb:243-259, 270-271)
        self.set_no_type_name(True)
        return result

    _reduce_81 = _reduce_82 = _reduce_83 = _reduce_85 = _type_specifier
    _reduce_86 = _reduce_87 = _reduce_88 = _reduce_89 = _reduce_90 = _type_specifier
    _reduce_91 = _reduce_92 = _reduce_93 = _reduce_94 = _reduce_95 = _type_specifier
    _reduce_96 = _reduce_97 = _reduce_103 = _reduce_104 = _type_specifier

    def _reduce_129(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : pointer direct_declarator                          (C_parser.y.rb:324)
        return val[1]

    def _reduce_130(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator : direct_declarator                                  (C_parser.y.rb:325)
        return val[0]

    def _reduce_131(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : IDENTIFIER                                  (C_parser.y.rb:328)
        return val[0].val

    def _reduce_132(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : '(' declarator ')'                          (C_parser.y.rb:329)
        return val[1]

    def _reduce_133(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # direct_declarator : direct_declarator '[' ... | '(' ... ')'    (C_parser.y.rb:330-334)
        return val[0]

    _reduce_134 = _reduce_135 = _reduce_136 = _reduce_137 = _reduce_133

    def _reduce_148(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_type_list : parameter_list [',' ] ['...']
        # 引数リストは関数が new される前に解釈されるので、先に渡しておく  (C_parser.y.rb:352-354)
        Function.param_list(val[0])
        return result

    _reduce_149 = _reduce_150 = _reduce_148

    def _reduce_151(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_list : parameter_declaration                          (C_parser.y.rb:358)
        return [val[0]] if val[0] is not None else None

    def _reduce_152(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_list : parameter_list ',' parameter_declaration       (C_parser.y.rb:365)
        if val[0] is not None and val[2] is not None:
            result.append(val[2])
        elif val[2] is not None:
            result = [val[2]]  # 文法エラー時しかありえない
        return result

    def _reduce_153(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : declaration_specifiers declarator       (C_parser.y.rb:377)
        return val[1]

    def _reduce_154(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # parameter_declaration : declaration_specifiers abstract_declarator | declaration_specifiers
        # 仮引数名なし                                               (C_parser.y.rb:379-382)
        return None

    _reduce_155 = _reduce_154

    # --- トップレベルの構文要素 --------------------------------------------------

    def _reduce_184(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF type_specifier_qualifier_list declarator_list ';'  (C_parser.y.rb:438)
        for t in val[2]:
            self._type_name_list[sym(t)] = t
        return result

    def _reduce_185(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # typedef : TYPEDEF type_specifier_qualifier_list ';'             (C_parser.y.rb:445)
        self.error("maybe typedef duplicate, ignored")
        return result

    def _reduce_186(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # func_def の途中のアクション（declaration_specifiers declarator @1 ...） (C_parser.y.rb:451)
        self._current_function = Function(self._current_locale_ref())
        return result

    def _reduce_187(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # func_def : declaration_specifiers declarator @1 kr_param_list compoundstatement
        #                                                                 (C_parser.y.rb:455)
        assert self._current_function is not None
        self._current_function.set_name(val[1])
        self._current_function = None
        return result

    def _reduce_188(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # func_def の途中のアクション（declarator @2 ...）                (C_parser.y.rb:461)
        self._current_function = Function(self._current_locale_ref())
        return result

    def _reduce_189(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # func_def : declarator @2 kr_param_list compoundstatement        (C_parser.y.rb:465)
        assert self._current_function is not None
        self._current_function.set_name(val[0])
        self._current_function = None
        return result

    def _reduce_193(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator_list : declarator                                    (C_parser.y.rb:478)
        return [val[0]]

    def _reduce_194(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # declarator_list : declarator_list ',' declarator                (C_parser.y.rb:479)
        result.append(val[2])
        return result

    def _reduce_250(self, val: list[Any], _values: list[Any], result: Any) -> Any:
        # asm_statement : _ASM
        # ';' が現れるまでトークンを読み飛ばす（文字列やコメント内の ';' は対象にならない）
        #                                                                 (C_parser.y.rb:587)
        while True:
            token = self.next_token()
            if token is None:
                # Ruby 版は nil[1] で NoMethodError になる
                raise AttributeError("undefined method '[]' for nil")
            if token[1].val == ";":
                break
        return result

    def _current_locale_ref(self) -> list[Any]:
        raise NotImplementedError
