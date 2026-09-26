"""plugin.rb の移植（内部仕様9章）。

P1 では、プラグインがファイルを書くときに使う `CFile` だけを置く。
`Plugin` 基底クラスとサブクラスは P5 で移植する。
"""

from __future__ import annotations

from typing import Any

from tecsgen.context import KCONV_BINARY, KCONV_CODECS, get_context
from tecsgen.ruby_compat import RubyIO


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
