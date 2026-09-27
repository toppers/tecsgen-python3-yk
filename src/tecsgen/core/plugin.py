"""plugin.rb の移植（内部仕様9章）。

`Plugin` 基底クラスは `ThroughPlugin`・`SignaturePlugin`・`CelltypePlugin`・`CellPlugin`
（`tecsgen.plugin` パッケージ、P5）に include される。
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any, ClassVar

from tecsgen.context import KCONV_BINARY, KCONV_CODECS, get_context
from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import RubyIO, rb_print, sub_first, truthy


class Plugin(Node):
    """`ThroughPlugin`・`SignaturePlugin`・`CelltypePlugin`・`CellPlugin` の共通の親クラス。

    @plugin_arg_str:: str  プラグイン引数の生文字列（サブクラスの `__init__` が設定する）
    @plugin_arg_list:: dict[str, str]  `parse_plugin_arg` の結果
    @plugin_arg_check_proc_tab:: dict[str, Callable] | None  サブクラスが `check_plugin_arg` で使う
    """

    #: `"key1=val1, key2=val2"` の共通引数（`silent`）
    PLUGIN_ARG_PROC: ClassVar[dict[str, Callable[[Plugin, str], None]]] = {
        "silent": lambda obj, rhs: obj.set_silent(rhs),
    }

    _plugin_arg_str: str
    _plugin_arg_list: dict[str, str]
    _plugin_arg_check_proc_tab: dict[str, Callable[[Any, str], None]] | None

    def __init__(self) -> None:
        super().__init__()
        # Plugin は parse とは異なるタイミングで new されるため、set_locale が
        # 呼び出されるまで locale は未設定（Node.__init__ が設定したものを上書きする）
        self._locale = None
        self._b_silent = False
        self._error_backlog: list[tuple[str, tuple[Any, ...]]] = []
        self._plugin_arg_check_proc_tab = None

    def cdl_error(self, message: str, *args: Any) -> None:
        """set_locale が呼び出されるまで backlog に保存し保留する。"""
        if self._locale is not None:
            super().cdl_error(message, *args)
        else:
            self._error_backlog.append((message, args))

    def set_locale(self, locale: Any) -> None:
        """locale を設定する。2度呼び出すと backlog のエラーが2度出力されるので注意。"""
        self._locale = locale
        for message, args in self._error_backlog:
            super().cdl_error(message, *args)

    ### 構文解釈または意味解析段階で呼び出されるメソッド ###

    def gen_cdl_file(self, file: Any) -> None:
        """typedef・signature・celltype・cell のコードを生成する（サブクラスが実装）。"""

    ### コード生成段階で呼び出されるメソッド ###

    def gen_ep_func(self) -> bool:  # Ruby: gen_ep_func?
        """`gen_ep_func_body` を提供するか（提供する場合、テンプレートではなくセルタイプコードを生成する）。"""
        return hasattr(type(self), "gen_ep_func_body")

    def gen_preamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """受け口関数の preamble (C言語)を生成する。デフォルトでは何も出力しない。"""

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """受け口関数の postamble (C言語)を生成する。デフォルトでは何も出力しない。"""

    def new_cell(self, cell: Any) -> None:
        """gen_cdl_file の中で生成されたセルタイプに新しいセルが生成された。デフォルトでは何もしない。"""

    ### プラグイン引数の解釈 ###

    def parse_plugin_arg(self) -> None:
        """`@plugin_arg_str`（`"key1=val1, key2=val2"` 形式）をパースし `@plugin_arg_list` へ入れる。"""
        arg = self._plugin_arg_str

        # 改行を消す
        arg = re.sub(r"\\\n", "", arg)

        while arg != "":
            # 前の空白読み飛ばす
            arg = sub_first(r"\A\s*(?:\\\n)*\s*(.*)", r"\1", arg)

            # 識別子取得
            m = re.match(r"\A[a-zA-Z_]\w*", arg, re.DOTALL)
            if m:
                ident = m.group(0)
                arg = arg[m.end() :]
            else:
                self.cdl_error("P1001 plugin arg: cannot find identifier in $1", arg)
                return

            # 前の空白読み飛ばす
            arg = sub_first(r"\A\s*(?:\\\n)*\s*(.*)", r"\1", arg)

            m = re.search("=", arg)
            if m:
                arg = arg[m.end() :]
            else:
                self.cdl_error("P1002 plugin arg: expecting '=' not '$1'", arg)
                return

            # 前の空白読み飛ばす
            arg = sub_first(r"\A\s*(?:\\\n)*\s*(.*)", r"\1", arg)

            # 右辺文字列
            rhs, remain = _match_plugin_rhs(arg)
            if rhs is None:
                self.cdl_error("P1003 plugin arg: unexpected $1", arg)
                return

            # 0文字の文字列を to_sym すると例外発生するので空白文字とする
            if rhs == "":
                rhs = " "

            arg = remain
            arg = sub_first(r"\A\s*(?:\\\n)*\s*(.*)", r"\1", arg)  # 前の空白読み飛ばす

            # \ を外す
            rhs = re.sub(r"\\(.)", r"\1", rhs)
            self._plugin_arg_list[ident] = rhs

            self.check_plugin_arg(ident, rhs)

    def check_plugin_arg(self, ident: str, rhs: str) -> None:
        """`@plugin_arg_check_proc_tab` に従ってプラグイン引数をチェックする。"""
        proc = None
        if self._plugin_arg_check_proc_tab:
            proc = self._plugin_arg_check_proc_tab.get(ident)
        if proc is None:
            proc = Plugin.PLUGIN_ARG_PROC.get(ident)
        if callable(proc):
            proc(self, rhs)
        else:
            params = ", ".join((self._plugin_arg_check_proc_tab or {}).keys())
            self.cdl_error(
                "P1004 $1: unknown plugin argument's identifier\n"
                "  $2 are acceptible for RPCPlugin.",
                ident,
                params,
            )

    def print_msg(self, msg: str) -> None:
        """プラグインのメッセージ出力。"""
        if self._b_silent is True:
            return
        rb_print(msg)

    def set_silent(self, rhs: Any) -> None:
        """プラグイン引数 silent。"""
        if rhs == "true" or not truthy(rhs):
            self._b_silent = True


def _match_plugin_rhs(arg: str) -> tuple[str | None, str]:
    """`parse_plugin_arg` の右辺文字列の取り出し（Ruby の分岐と同じ順で試す）。"""
    for pattern in (
        r'\A\\"(.*?)\\"\s*,',
        r"\A%(.*?)%\s*,",
        r"\A!(.*?)!\s*,",
        r"\A'(.*?)'\s*,",
        r'\A\\"(.*?)\\"\s*\Z',
        r"\A%(.*?)%\s*\Z",
        r"\A!(.*?)!\s*\Z",
        r"\A'(.*?)'\s*\Z",
        r"\A(.*?),",
        r"\A(.*?)\s*\Z",
    ):
        m = re.match(pattern, arg, re.DOTALL)
        if m:
            rhs = m.group(1)
            remain = arg[m.end() :]
            if pattern == r"\A(.*?),":
                rhs = sub_first(r"\A\s*(.*)\s*\Z", r"\1", rhs)
            return rhs, remain
    return None, arg


class CFile:
    """出力文字列を utf-8 から出力ファイルの文字コードに変換して書く。

    tecsgen のソースコードは utf-8 で記述されている。これを出力ファイルの文字コードに変換して出力する。
    mikan: CFile で出力したものに factory で追記できない（cdl ファイルの場合、追記できても意味がない）
    """

    @staticmethod
    def open(path: str, mode: str) -> CFile:
        return CFile(path, mode)

    def __init__(self, path: str, mode: str) -> None:
        self._file = RubyIO(path, mode, _cfile_codec())

    def print(self, s: Any) -> None:
        self._file.print(s)

    def puts(self, s: Any) -> None:
        # Ruby 版は str を print してから "\n" を書く（末尾が改行でも改行を足す）
        self._file.print(s)
        self._file.write("\n")

    def printf(self, fmt: str, *args: Any) -> None:
        self._file.printf(fmt, *args)

    def close(self) -> None:
        self._file.close()


def _cfile_codec() -> str:
    """CFile が書くときのコーデック。

    Ruby 版は `$KCONV_CONSOLE`（コンソールの文字コード）が BINARY でなければ `$KCONV_CDL` へ kconv し、
    BINARY なら変換せずに書く。判定に使う変数がコンソール側なのは Ruby 版のとおり（移植元の挙動を保つ）。
    ファイルを Shift_JIS で開いた場合は、Ruby の IO が書き込み時に Shift_JIS へ変換するので、常に cp932。
    """
    ctx = get_context()
    if ctx.ruby19_file_encode == "Shift_JIS":
        return "cp932"
    if ctx.kconv_console == KCONV_BINARY:
        return "utf-8"
    return KCONV_CODECS[ctx.kconv_cdl]
