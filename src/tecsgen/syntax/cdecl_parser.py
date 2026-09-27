"""import_C 用の C ヘッダのパーサ（C_parser.y.rb の `C_parser`。内部仕様5章）。

`import_C` は C プリプロセッサの出力を読み、`typedef` と `struct` の宣言だけを取り出す。
`next_token` が、それ以外の文のトークンを読み飛ばす。パーサの入れ子の状態
（`@@generator_nest` など）は、CDL の `Generator` とは別に持つ。

TYPE_NAME の判定は `CdlParser` と同じく `typename_resolver` を差し替えて使う（P3 まで）。
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.core.generator import Generator, Locale, Token, _get_at, _set_at
from tecsgen.ruby_compat import rb_print, to_s
from tecsgen.syntax import cdecl_tables
from tecsgen.syntax.cdecl_actions import CdeclActions
from tecsgen.syntax.cdecl_lexer import lex_files
from tecsgen.syntax.cdl_lexer import Reader, _read_file
from tecsgen.syntax.racc_runtime import RaccParser

# next_token で見る記号。Ruby 版は Token の値（String）と比べている
_RESET_NO_TYPE_NAME = frozenset({";", ":", ",", "(", ")", "{", "}"})
_SET_NO_TYPE_NAME = frozenset({".", "->"})


def _namespace_is_typename(name: Any) -> bool:
    """Namespace.is_typename?（TYPE_NAME の判定）。"""
    from tecsgen.core.componentobj.namespace import Namespace

    return Namespace.is_typename(name)


class CdeclParser(CdeclActions, RaccParser):
    TABLES = cdecl_tables

    # Namespace.is_typename? に当たる関数（テストで差し替えられるようにクラス属性にしている）
    typename_resolver: ClassVar[Callable[[Any], bool]] = staticmethod(
        _namespace_is_typename
    )

    _generator_nest: ClassVar[int] = -1
    _generator_stack: ClassVar[list[Any]] = []
    _current_locale: ClassVar[list[Locale | None]] = []

    def __init__(self, reader: Reader = _read_file) -> None:
        super().__init__()
        self._plugin: Any = None
        self._b_no_type_name = False
        self._q: deque[tuple[Any, Token] | None] = deque()
        self._in = False
        self._count = 0
        self._prev_block_end = True
        self._reader = reader

    @classmethod
    def reset(cls) -> None:
        """クラス変数を初期状態に戻す（Ruby 版には無い。1プロセスで複数回実行するテスト用）。"""
        cls._generator_nest = -1
        cls._generator_stack = []
        cls._current_locale = []

    def finalize(self) -> None:
        self._pop_model_stacks()

    def set_plugin(self, plugin: Any) -> None:
        self._plugin = plugin

    def get_plugin(self) -> Any:
        return self._plugin

    @classmethod
    def current_plugin(cls) -> Any:
        """Ruby の `C_parser.get_plugin`。"""
        return _get_at(cls._generator_stack, cls._generator_nest).get_plugin()

    @classmethod
    def current_locale(cls) -> Locale | None:
        return _get_at(cls._current_locale, cls._generator_nest)

    @classmethod
    def get_nest(cls) -> int:
        return cls._generator_nest

    # --- 構文解析 ------------------------------------------------------------

    def parse(self, files: list[str]) -> Any:
        self._push_model_stacks()
        cls = type(self)
        cls._generator_nest += 1
        _set_at(cls._generator_stack, cls._generator_nest, self)
        self._b_no_type_name = False
        try:
            q: list[Any] = []
            # typedef, struct のみ
            self._in = False  # typedef, struct の途中
            self._count = 0
            self._prev_block_end = True
            lex_files(files, q, self._reader)
            # 終了の印
            q.append(None)
            self._q = deque(q)
            return self.do_parse()
        finally:
            cls._generator_nest -= 1

    def _shift(self) -> tuple[Any, Token] | None:
        return self._q.popleft() if self._q else None

    def next_token(self) -> tuple[Any, Any] | None:
        token = self._shift()
        # typedef, struct の宣言文のみ評価する
        if self._in:
            assert (
                token is not None
            )  # Ruby 版は nil で NoMethodError（入力の途中で終わるとき）
            self._prev_block_end = False
            # ';' で 文の終わり
            if token[0] == "{":
                self._count += 1
            elif token[0] == "}":
                self._count -= 1
            elif token[0] == ";" and self._count == 0:
                self._in = False
                self._prev_block_end = True
        else:
            while token:
                if token[0] in ("TYPEDEF", "STRUCT") and self._prev_block_end:
                    self._in = True
                    self._prev_block_end = False
                    break
                self._prev_block_end = token[0] in (";", "}")
                token = self._shift()

        if token:
            kind, tok = token
            cls = type(self)
            _set_at(cls._current_locale, cls._generator_nest, tok.locale())

            if isinstance(tok.val, str):
                if tok.val in _RESET_NO_TYPE_NAME:
                    self.set_no_type_name(False)
                elif tok.val in _SET_NO_TYPE_NAME:
                    self.set_no_type_name(True)

            # TYPE_NAME トークンへ置き換え
            if (
                not self._b_no_type_name
                and kind == "IDENTIFIER"
                and cls.typename_resolver(tok.val)
            ):
                kind = "TYPE_NAME"

            if get_context().debug:
                locale = cls.current_locale()
                assert locale is not None
                rb_print(f"{locale[0]}: line {locale[1]} : {kind} '{to_s(tok.val)}'\n")
            return (kind, tok)
        return None

    def on_error(self, t: int, val: Any, vstack: list[Any]) -> None:
        if val == "$":
            Generator.error("B1003 Unexpected EOF")
        else:
            Generator.error("B1004 syntax error near '$1'", val.val)

    def set_no_type_name(self, b_no_type_name: bool) -> None:
        self._b_no_type_name = b_no_type_name

    # --- モデルのスタック ------------------------------------------------------

    def _push_model_stacks(self) -> None:
        """Celltype・Cell・CompositeCelltype・Region の push（mikan Namespace.push）。"""
        from tecsgen.syntax import _model as m

        m.Celltype.push()
        m.Cell.push()
        m.CompositeCelltype.push()
        m.Region.push()

    def _pop_model_stacks(self) -> None:
        """finalize の中身。Celltype・Cell・CompositeCelltype・Region の pop。"""
        from tecsgen.syntax import _model as m

        m.Celltype.pop()
        m.Cell.pop()
        m.CompositeCelltype.pop()
        m.Region.pop()
