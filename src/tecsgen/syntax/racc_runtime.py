"""racc のパーサ駆動部の移植。

Ruby 版の Generator・C_parser は racc が生成した LALR 表で動く。Python 版は同じ表
（tools/port/gen_racc_tables.py が生成する cdl_tables・cdecl_tables）を使い、同じ手順で
shift・reduce・エラー回復を行う。構文エラーの位置と件数を Ruby 版と一致させるため、
エラー回復まで含めて racc の動作をそのまま写している（内部仕様5章）。

移植元は racc の **C 実装**（ext/racc/cparse/cparse.c の parse_main・reduce0、racc 1.8.1）。
racc は C 実装を読み込めるときはそちらを使い、Ruby 版 tecsgen の実行でも C 実装が使われる。
Ruby 実装（lib/racc/parser.rb の _racc_do_parse_rb）とは、エラー回復の挙動が違う。

- C 実装は、error トークンを shift しても先読みのトークンを捨てない。回復した状態で同じ
  トークンをもう一度見て、再びエラーになったとき（error_status が 3）に初めて読み捨てる。
  Ruby 実装は error トークンの shift で次のトークンを読む
- C 実装は、shift のたびに error_status を減らす（先読みが error トークンか EOF かを問わない）
- C 実装は `_reduce_none` を呼ばず、右辺の先頭の値をそのまま積む
- next_token が nil を返したとき（C_parser）、C 実装は EOF として扱い、値を "$" にする

デバッグ出力（yydebug）は移植していない。生成済みの表は Racc_debug_parser = false で、
Ruby 版でもデバッグ出力は無効になっている。
"""

from __future__ import annotations

from types import ModuleType
from typing import Any, ClassVar

FINAL_TOKEN = 0  # EOF
ERROR_TOKEN = 1


class ParseError(Exception):
    """racc の Racc::ParseError。on_error を上書きしない場合に送出する。"""


class _Jump(Exception):
    def __init__(self, code: int) -> None:
        super().__init__()
        self.code = code


class RaccParser:
    """racc が生成するパーサクラスの基底。サブクラスは TABLES と _reduce_N を定義する。

    next_token は (トークン種別, 値) を返す。種別は表の TOKEN_TABLE のキー（str）で、
    入力の終わりは種別に False を返す（Generator）か、None そのものを返す（C_parser）。
    表に無い種別は error トークン（1番）になる。
    """

    TABLES: ClassVar[ModuleType]

    def __init__(self) -> None:
        self._racc_error_status = 0

    # --- 利用者が上書きするメソッド -----------------------------------------

    def next_token(self) -> tuple[Any, Any] | None:
        raise NotImplementedError(f"{type(self).__name__}#next_token is not defined")

    def on_error(self, t: int, val: Any, vstack: list[Any]) -> None:
        raise ParseError(
            f"parse error on value {val!r} ({self.token_to_str(t) or '?'})"
        )

    # --- 利用者が呼ぶメソッド -----------------------------------------------

    def yyerror(self) -> None:
        """エラー回復モードに入る（on_error は呼ばない）。"""
        raise _Jump(1)

    def yyaccept(self) -> None:
        """構文解析を終える。戻り値は値スタックの先頭。"""
        raise _Jump(2)

    def yyerrok(self) -> None:
        """エラー回復モードを抜ける。"""
        self._racc_error_status = 0

    def token_to_str(self, t: int) -> str | None:
        table = self.TABLES.TOKEN_TO_S_TABLE
        return table[t] if 0 <= t < len(table) else None

    # --- 駆動部（cparse.c の parse_main） -------------------------------------

    def do_parse(self) -> Any:
        tb = self.TABLES
        action_table = tb.ACTION_TABLE
        action_check = tb.ACTION_CHECK
        action_default = tb.ACTION_DEFAULT
        action_pointer = tb.ACTION_POINTER
        token_table = tb.TOKEN_TABLE
        shift_n = tb.SHIFT_N
        reduce_n = tb.REDUCE_N

        self._racc_state: list[int] = [0]
        self._racc_vstack: list[Any] = []
        self._racc_error_status = 0
        t = FINAL_TOKEN + 1  # まだ何も読んでいない
        val: Any = None
        read_next = True

        while True:
            state = self._racc_state[-1]
            i = action_pointer[state]
            if i is None:
                act = action_default[state]
            else:
                if read_next and t != FINAL_TOKEN:
                    tok, val = self._extract_user_token(self.next_token())
                    t = token_table.get(tok, ERROR_TOKEN) if tok is not False else 0
                read_next = False
                i += t
                act = action_table[i] if 0 <= i < len(action_table) else None
                if act is None or action_check[i] != state:
                    act = action_default[state]
            assert act is not None

            if 0 < act < shift_n:
                # shift
                if self._racc_error_status > 0:
                    self._racc_error_status -= 1
                self._racc_vstack.append(val)
                self._racc_state.append(act)
                read_next = True
                continue
            if -reduce_n < act < 0:
                code = self._reduce(act)
                if code == 0:
                    continue
                if code == 2:  # yyaccept
                    return self._accept()
                # yyerror: on_error を呼ばずにエラー回復へ
                user_yyerror = True
            elif act == -reduce_n:
                user_yyerror = False
            elif act == shift_n:
                return self._accept()
            else:
                raise RuntimeError(f"[Racc Bug] unknown act value {act}")

            # error
            if not user_yyerror and self._racc_error_status == 0:
                self.on_error(t, val, self._racc_vstack)
            if self._racc_error_status == 3:
                if t == FINAL_TOKEN:
                    return None
                read_next = True
            self._racc_error_status = 3

            # error トークンを shift・reduce できる状態まで戻る
            while True:
                state = self._racc_state[-1]
                i = action_pointer[state]
                if i is not None:
                    i += ERROR_TOKEN
                    if 0 <= i < len(action_table):
                        found = action_table[i]
                        if found is not None and action_check[i] == state:
                            act = found
                            break
                if len(self._racc_state) <= 1:
                    return None
                self._racc_state.pop()
                self._racc_vstack.pop()

            if 0 < act < shift_n:
                # 先読みのトークンは捨てない（read_next はそのまま）
                self._racc_vstack.append(val)
                self._racc_state.append(act)
            elif -reduce_n < act < 0:
                code = self._reduce(act)
                if code == 2:
                    return self._accept()
                if code == 1:
                    # C 実装はここからエラー処理の先頭（user_yyerror）へ戻る。文法アクションは
                    # yyerror を使わないので移植していない
                    raise NotImplementedError("yyerror during error recovery")
            elif act == shift_n:
                return self._accept()
            else:
                raise RuntimeError(f"[Racc Bug] unknown act value {act}")

    @staticmethod
    def _extract_user_token(block_args: tuple[Any, Any] | None) -> tuple[Any, Any]:
        if block_args is None:
            return False, "$"  # EOF（cparse.c の extract_user_token）
        tok, val = block_args
        if tok is None:
            tok = False
        return tok, val

    def _accept(self) -> Any:
        return self._racc_vstack[0] if self._racc_vstack else None

    def _reduce(self, act: int) -> int:
        """cparse.c の reduce・reduce0。戻り値は 0: 通常、1: yyerror、2: yyaccept。"""
        tb = self.TABLES
        state = self._racc_state
        vstack = self._racc_vstack

        length, reduce_to, method_id = tb.REDUCE_TABLE[-act]
        start = len(vstack) - length
        try:
            if method_id == "_reduce_none":
                result = vstack[start] if length > 0 else None
                del vstack[start:]
                del state[len(state) - length :]
            else:
                tmp_v = vstack[start:]
                del vstack[start:]
                del state[len(state) - length :]
                method = getattr(self, method_id)
                if tb.USE_RESULT:
                    result = method(tmp_v, vstack, tmp_v[0] if tmp_v else None)
                else:
                    result = method(tmp_v, vstack)
        except _Jump as jump:
            return jump.code
        vstack.append(result)

        k1 = reduce_to - tb.NT_BASE
        goto_state: int | None = None
        i = tb.GOTO_POINTER[k1]
        if i is not None:
            i += state[-1]
            if 0 <= i < len(tb.GOTO_TABLE):
                candidate = tb.GOTO_TABLE[i]
                if candidate is not None and tb.GOTO_CHECK[i] == k1:
                    goto_state = candidate
        if goto_state is None:
            goto_state = tb.GOTO_DEFAULT[k1]
        assert goto_state is not None
        state.append(goto_state)
        return 0
