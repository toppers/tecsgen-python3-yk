"""cdlstring.rb の移植。CDL の文字列リテラルを扱うためのクラス（リテラルそのものではない）。"""

from __future__ import annotations

import re

from tecsgen.ruby_compat import gsub, sub_first


class CDLString:
    @staticmethod
    def escape(s: str) -> str:
        """エスケープ文字を変換する。

        Ruby 版の誤り（`\\t` を 0x08 にする、未定義のエスケープシーケンスも変換してしまう）も
        そのまま再現する。
        """
        s = gsub(r"\\a", "\x07", s)
        s = gsub(r"\\b", "\x08", s)
        s = gsub(r"\\f", "\x0c", s)
        s = gsub(r"\\n", "\x0a", s)
        s = gsub(r"\\r", "\x0d", s)
        s = gsub(r"\\t", "\x08", s)
        s = gsub(r"\\v", "\x0b", s)
        s = gsub(r"(\\[Xx][0-9A-Fa-f]{1,2})", '{printf \\"\\1\\"}', s)
        s = gsub(r"(\\[0-7]{1,3})", '{printf \\"\\1\\"}', s)
        s = gsub(re.compile(r"\\(.)"), "\\1", s)
        return s

    @staticmethod
    def remove_dquote(s: str) -> str:
        """前後の " を取り除く。"""
        s = sub_first(r'\A"', "", s)
        return sub_first(r'"\Z', "", s)
