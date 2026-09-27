"""CDL のパーサ（bnf.y.rb の `Generator` のうち、構文解析を行う部分。内部仕様5章）。

Ruby 版の `Generator` は racc が生成したパーサクラスで、次の3つを兼ねる。

1. 構文解析（`parse`・`next_token`・`on_error`）→ このモジュールの `CdlParser`
2. 文法アクション（`_reduce_N`）→ `cdl_actions.CdlActions`（本体は P3 で移植）
3. エラー報告とパーサの入れ子の状態 → `tecsgen.core.generator.Generator`（P1）

`parse` は、ファイルを字句解析してトークン列を作り（`cdl_lexer`）、racc の表で駆動する
（`racc_runtime`）。`import` のアクションは、パースの途中で別の `CdlParser` を作って
同期的にパースする（入れ子）。

TYPE_NAME の判定は `Namespace.is_typename?`（`typename_resolver`。差分テストでは差し替える）。
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.core.generator import Generator, Token
from tecsgen.ruby_compat import rb_print, to_s
from tecsgen.syntax import cdl_tables
from tecsgen.syntax.cdl_actions import CdlActions
from tecsgen.syntax.cdl_lexer import Reader, _read_file, lex_files
from tecsgen.syntax.racc_runtime import RaccParser

# 指定子 '[ ]' 内でのみ使用できるキーワード（bnf.y.rb の RESERVED2）
RESERVED2: dict[str, str] = {
    # specifier
    "id": "ID",
    # signature
    "callback": "CALLBACK",
    "context": "CONTEXT",
    "deviate": "DEVIATE",
    # celltype
    "singleton": "SINGLETON",
    "idx_is_id": "IDX_IS_ID",
    "active": "ACTIVE",
    "pseudo_active": "PSEUDO_ACTIVE",
    # port (entry)
    "inline": "INLINE",
    "ref_desc": "REF_DESC",  # call も可
    # port (call)
    "optional": "OPTIONAL",
    "dynamic": "DYNAMIC",
    # port (call), attribute
    "omit": "OMIT",
    # attribute
    "choice": "CHOICE",
    # cell
    "allocator": "ALLOCATOR",
    "prototype": "PROTOTYPE",
    "restrict": "RESTRICT",
    # FuncType
    "oneway": "ONEWAY",
    # parameter (basic)
    "in": "IN",
    "out": "OUT",
    "inout": "INOUT",
    "send": "SEND",
    "receive": "RECEIVE",
    # parameter
    "size_is": "SIZE_IS",
    "count_is": "COUNT_IS",
    "string": "STRING",
    "nullable": "NULLABLE",
    "through": "THROUGH",
    "in_through": "IN_THROUGH",
    "out_through": "OUT_THROUGH",
    "to_through": "TO_THROUGH",
    "from_through": "FROM_THROUGH",
    "node": "NODE",
    "linkunit": "LINKUNIT",
    "domain": "DOMAIN",
    "class": "CLASS",
}


def _namespace_is_typename(name: Any) -> bool:
    """Namespace.is_typename?（TYPE_NAME の判定）。"""
    from tecsgen.core.componentobj.namespace import Namespace

    return Namespace.is_typename(name)


class CdlParser(CdlActions, RaccParser):
    TABLES = cdl_tables

    # Namespace.is_typename? に当たる関数（テストで差し替えられるようにクラス属性にしている）
    typename_resolver: ClassVar[Callable[[Any], bool]] = staticmethod(
        _namespace_is_typename
    )

    def __init__(self, reader: Reader = _read_file) -> None:
        super().__init__()
        self._plugin: Any = None
        self._b_reuse = False
        self._in_specifier = False
        self._q: deque[tuple[Any, Token] | None] = deque()
        self._reader = reader

    # --- Generator.parse とその周辺 -------------------------------------------

    @classmethod
    def parse_file(
        cls, file_name: str, plugin: Any = None, b_reuse: bool = False
    ) -> None:
        """Ruby の `Generator.parse`。別のパーサインスタンスで file_name を読み込む。"""
        parser = cls()
        # plugin から import されている場合の plugin 設定
        parser.set_plugin(plugin)
        # reuse フラグを設定
        parser.set_reuse(b_reuse)
        # cdl をパース
        parser.parse([file_name])
        # 終期化　パーサスタックを戻す
        parser.finalize()

    def finalize(self) -> None:
        self._pop_model_stacks()

    def set_plugin(self, plugin: Any) -> None:
        self._plugin = plugin

    def get_plugin(self) -> Any:
        return self._plugin

    @classmethod
    def current_plugin(cls) -> Any:
        """Ruby の `Generator.get_plugin`。tecsgen 引数の cdl が import される場合は nil。"""
        parser = Generator.current_parser()
        return parser.get_plugin() if parser is not None else None

    def set_reuse(self, b_reuse: bool) -> None:
        self._b_reuse = b_reuse

    def is_reuse(self) -> bool:
        return self._b_reuse

    @classmethod
    def current_is_reuse(cls) -> bool:
        """Ruby の `Generator.is_reuse?`。"""
        parser = Generator.current_parser()
        return parser.is_reuse() if parser is not None else False

    # --- 構文解析 ------------------------------------------------------------

    def parse(self, files: list[str]) -> Any:
        self._push_model_stacks()
        Generator.push_parser(self)
        self._in_specifier = False
        try:
            q: list[Any] = []
            lex_files(files, q, self._reader)
            # 終了の印
            q.append(None)
            self._q = deque(q)
            return self.do_parse()
        finally:
            Generator.pop_parser()

    def next_token(self) -> tuple[Any, Any]:
        token = self._q.popleft() if self._q else None
        if token is None:
            return (False, False)

        kind, tok = token
        Generator.set_current_locale(tok.locale())
        if kind == "IDENTIFIER":
            # TYPE_NAME トークンへ置換え
            if type(self).typename_resolver(tok.val):
                kind = "TYPE_NAME"
            elif self._in_specifier and to_s(tok.val) in RESERVED2:
                # 指定子キーワード（ '[', ']' 内でのみ有効)
                kind = RESERVED2[to_s(tok.val)]

        if get_context().debug:
            locale = Generator.current_locale()
            assert locale is not None
            rb_print(f"{locale[0]}: line {locale[1]} : {kind} '{to_s(tok.val)}'\n")
        return (kind, tok)

    def on_error(self, t: int, val: Any, vstack: list[Any]) -> None:
        if self.token_to_str(t) == "$end":
            Generator.error("G1015 Unexpected EOF")
        else:
            Generator.error("G1016 syntax error near '$1'", val.val)

    # '[' specifier 始め
    def set_in_specifier(self) -> None:
        self._in_specifier = True

    # ']' specifier 終わり
    def unset_in_specifier(self) -> None:
        self._in_specifier = False

    # --- モデルのスタック ------------------------------------------------------

    def _push_model_stacks(self) -> None:
        """Namespace・Signature・Celltype・Cell・CompositeCelltype の push。"""
        from tecsgen.syntax import _model as m

        m.Namespace.push()
        m.Signature.push()
        m.Celltype.push()
        m.Cell.push()
        m.CompositeCelltype.push()

    def _pop_model_stacks(self) -> None:
        """finalize の中身。Namespace・Signature・Celltype・Cell・CompositeCelltype の pop。"""
        from tecsgen.syntax import _model as m

        m.Namespace.pop()
        m.Signature.pop()
        m.Celltype.pop()
        m.Cell.pop()
        m.CompositeCelltype.pop()
