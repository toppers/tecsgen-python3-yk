"""bnf.y.rb のうち、`Generator` のエラー処理・位置情報と `Token` の移植（内部仕様11章）。

Ruby 版の `Generator` は racc が生成するパーサクラスで、構文解析とエラー報告の両方を担う。
Python 版では、構文解析（`parse`・`next_token` など）を `tecsgen.syntax.cdl_parser` へ移し、
このモジュールには全フェーズから呼ばれるエラー報告と、パーサの入れ子（import による再帰的な
パース）の状態だけを置く。

位置情報（locale）は `(ファイル名, 行番号, 桁)` のタプル。Ruby 版の `[file, lineno, col]` に当たる。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.core.messages import TECSMsg
from tecsgen.core.tecs_lang import Console
from tecsgen.ruby_compat import rb_print, sub_first, to_s
from tecsgen.syntax.tecsio import TECSIO

Locale = tuple[str, int, int]

_ARG_PATTERNS = [re.compile(r"\$" + str(i)) for i in range(1, 10)]


def _arg_pattern(count: int) -> re.Pattern[str]:
    if count <= len(_ARG_PATTERNS):
        return _ARG_PATTERNS[count - 1]
    return re.compile(r"\$" + str(count))


class Generator:
    # 再帰的なパーサのためのスタック
    _generator_nest: ClassVar[int] = -1
    _generator_stack: ClassVar[list[Any]] = []
    _current_locale: ClassVar[list[Locale | None]] = []

    # import_C 中である
    _import_C: ClassVar[bool] = False

    # すべての構文解析が完了した
    _b_end_all_parse: ClassVar[bool] = False

    _n_error: ClassVar[int] = 0
    _n_warning: ClassVar[int] = 0
    _n_info: ClassVar[int] = 0

    # statement_specifier は構文解釈途中で参照したいため
    _statement_specifier_stack: ClassVar[list[list[Any] | None]] = []

    @classmethod
    def reset(cls) -> None:
        """クラス変数を初期状態に戻す（Ruby 版には無い。1プロセスで複数回実行するテスト用）。"""
        cls._generator_nest = -1
        cls._generator_stack = []
        cls._current_locale = []
        cls._import_C = False
        cls._b_end_all_parse = False
        cls._n_error = 0
        cls._n_warning = 0
        cls._n_info = 0
        cls._statement_specifier_stack = []

    # --- パーサの入れ子 ------------------------------------------------------

    @classmethod
    def push_parser(cls, parser: Any) -> None:
        """Generator#parse の冒頭（`@@generator_nest += 1` と stack への登録）。"""
        cls._generator_nest += 1
        _set_at(cls._generator_stack, cls._generator_nest, parser)

    @classmethod
    def pop_parser(cls) -> None:
        """Generator#parse の ensure 節（`@@generator_nest -= 1`）。stack の要素は Ruby と同じく残す。"""
        cls._generator_nest -= 1

    @classmethod
    def current_parser(cls) -> Any:
        return _get_at(cls._generator_stack, cls._generator_nest)

    @classmethod
    def current_locale(cls) -> Locale | None:
        return _get_at(cls._current_locale, cls._generator_nest)

    @classmethod
    def set_current_locale(cls, locale: Locale) -> None:
        """next_token がトークンを取り出すたびに呼ぶ。"""
        _set_at(cls._current_locale, cls._generator_nest, locale)

    @classmethod
    def get_nest(cls) -> int:
        return cls._generator_nest

    @classmethod
    def set_import_C(cls, b: bool) -> None:
        """bnf.y.rb の文法アクションが `@@import_C` を切り替える箇所に相当。"""
        cls._import_C = b

    @classmethod
    def parsing_C(cls) -> bool:  # Ruby: parsing_C?
        return cls._import_C

    @classmethod
    def end_all_parse(cls) -> None:
        """すべての構文解析が完了したことを報告する。"""
        cls._b_end_all_parse = True

    # --- statement specifier ---------------------------------------------

    @classmethod
    def add_statement_specifier(cls, ss: Any) -> None:
        cur = _get_at(cls._statement_specifier_stack, cls._generator_nest)
        if cur is None:
            _set_at(cls._statement_specifier_stack, cls._generator_nest, [ss])
        else:
            cur.append(ss)

    @classmethod
    def get_statement_specifier(cls) -> list[Any] | None:
        spec_list = _get_at(cls._statement_specifier_stack, cls._generator_nest)
        _set_at(cls._statement_specifier_stack, cls._generator_nest, None)
        return spec_list

    # --- エラー・警告・情報 ----------------------------------------------

    @classmethod
    def error(cls, msg: str, *args: Any) -> None:
        """構文解析、意味解析からのみ呼出し可（コード生成でエラー発生は不適切）。"""
        cls.error2(None, msg, *args)

    @classmethod
    def error2(cls, locale: Locale | None, msg: str, *args: Any) -> None:
        cls._n_error += 1
        cls._report(locale, "error", TECSMsg.get_error_message(msg), args)

    @classmethod
    def warning(cls, msg: str, *args: Any) -> None:
        cls.warning2(None, msg, *args)

    @classmethod
    def warning2(cls, locale: Locale | None, msg: str, *args: Any) -> None:
        cls._n_warning += 1
        cls._report(locale, "warning", TECSMsg.get_warning_message(msg), args)

    @classmethod
    def info(cls, msg: str, *args: Any) -> None:
        cls.info2(None, msg, *args)

    @classmethod
    def info2(cls, locale: Locale | None, msg: str, *args: Any) -> None:
        cls._n_info += 1
        cls._report(locale, "info", TECSMsg.get_info_message(msg), args)

    @classmethod
    def _report(
        cls, locale: Locale | None, kind: str, msg: str, args: tuple[Any, ...]
    ) -> None:
        # $1, $2, ... を arg で置換（Ruby の String#sub! なので、置換文字列中の \1 等も解釈される）
        for count, a in enumerate(args, start=1):
            s = TECSIO.str_code_convert(msg, to_s(a))
            msg = sub_first(_arg_pattern(count), s, msg)

        if cls._import_C:
            # import_C の中でのエラー
            from tecsgen.syntax.cdecl_parser import CdeclParser

            locale = CdeclParser.current_locale()
        elif not cls._b_end_all_parse or locale is None:
            # 構文解析中は、Node が記憶する位置ではなく、解析中の位置を出力する
            locale = cls.current_locale()

        if locale is not None:  # Ruby では空配列も真
            Console.puts(
                f"{to_s(locale[0])}:{to_s(locale[1])}:{to_s(locale[2])}: {kind}: {msg}"
            )
        else:
            Console.puts(f"{kind}: {msg}")

    @classmethod
    def get_n_error(cls) -> int:
        return cls._n_error

    @classmethod
    def get_n_warning(cls) -> int:
        return cls._n_warning

    @classmethod
    def get_n_info(cls) -> int:
        return cls._n_info


def _get_at(lst: list[Any], idx: int) -> Any:
    """Ruby の Array#[]。範囲外は nil、負の添字は末尾から数える。"""
    if -len(lst) <= idx < len(lst):
        return lst[idx]
    return None


def _set_at(lst: list[Any], idx: int, value: Any) -> None:
    """Ruby の Array#[]=。範囲外に書くと間を nil で埋める。"""
    if idx < 0:
        if idx < -len(lst):
            raise IndexError(f"index {idx} too small for array; minimum: -{len(lst)}")
        lst[idx] = value
        return
    if idx >= len(lst):
        lst.extend([None] * (idx + 1 - len(lst)))
    lst[idx] = value


def print_report() -> None:
    """tecsgen.rb の print_report。エラーおよび警告の件数を出力する。"""
    msg = None
    n_error = Generator.get_n_error()
    n_warning = Generator.get_n_warning()
    if n_error != 0:
        msg = f"{n_error} error"
        if n_error >= 2:
            msg += "s"
    if n_warning != 0:
        msg = f"{msg}  " if msg else ""
        msg += f"{n_warning} warning"
        if n_warning >= 2:
            msg += "s"
    if msg:
        rb_print(msg + "\n")


class Token:
    """字句解析器が作るトークン。値と位置を持つ。"""

    __slots__ = ("col", "file", "lineno", "val")

    def __init__(self, val: Any, file: str, lineno: int, col: int) -> None:
        self.val = val
        self.file = file
        self.lineno = lineno
        self.col = col

    def to_s(self) -> str:
        return to_s(self.val)

    def __str__(self) -> str:
        return self.to_s()

    def to_sym(self) -> str:
        return to_s(self.val)

    def get_name(self) -> Any:
        return self.val

    def locale(self) -> Locale:
        return (self.file, self.lineno, self.col)

    def __eq__(self, other: object) -> bool:
        # Ruby 版の eql?（== の別名）。Symbol も String も Python では str
        if isinstance(other, Token):
            return self.val == other.val
        if isinstance(other, str):
            return to_s(self.val) == other
        raise TypeError(f"cannot compare Token with {type(other).__name__}")

    __hash__ = object.__hash__

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent + f"{to_s(self.val)}\n")
