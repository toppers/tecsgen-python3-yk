"""generate.rb の移植（内部仕様8章・10章）。

P1 では、コード生成が使うファイル出力の仕組み（`AppFile`・`MemFile`）だけを置く。
生成処理そのもの（各モデルクラスの `gen_*` を足す mixin）は P4 で移植する。
"""

from __future__ import annotations

import os
from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.ruby_compat import RubyIO, rb_print, to_s


class AppFile:
    """Appendable File（追記可能ファイル）。

    同じ名前で2回目以降に開くと追記モードになる。`--force-overwrite` でなければ `<name>.tmp` に
    書き、`update()` で既存ファイルと比べて、内容が変わったときだけ置き換える
    （make の依存関係で不要な再コンパイルが起きないようにするため）。
    """

    # 開いたファイルのリスト（挿入順を保つ。Ruby の Hash と同じ）
    _file_name_list: ClassVar[dict[str, bool]] = {}

    @classmethod
    def reset(cls) -> None:
        """開いたファイルのリストを空にする（Ruby 版には無い。テスト用）。"""
        cls._file_name_list = {}

    @classmethod
    def open(cls, name: str) -> RubyIO:
        ctx = get_context()
        real_name = name if ctx.force_overwrite else name + ".tmp"

        if cls._file_name_list.get(name):
            # 既に開いている: 追記モードで開く
            return RubyIO(real_name, "a", ctx.file_codec)
        # 新規モードで開く（既にあれば、サイズを０にする）
        f = RubyIO(real_name, "w", ctx.file_codec)
        cls._file_name_list[name] = True
        return f

    @classmethod
    def update(cls) -> None:
        ctx = get_context()
        if ctx.force_overwrite:
            return

        for name in cls._file_name_list:
            tmp = name + ".tmp"
            b_identical = False
            if os.access(name, os.R_OK):
                with open(name, "rb") as f:
                    old_lines = f.readlines()
                with open(tmp, "rb") as f:
                    new_lines = f.readlines()
                b_identical = old_lines == new_lines
            if not b_identical:
                if ctx.verbose:
                    rb_print(f"{name} changed\n")
                    rb_print(f"renaming '{name}.tmp' => '{name}'\n")
                os.replace(tmp, name)
            else:
                if ctx.verbose:
                    rb_print(f"{name} not changed\n")
                os.remove(tmp)


class MemFile:
    """文字列に書き溜める出力先（File と同じ print を持つ）。"""

    def __init__(self) -> None:
        self._string = ""

    def print(self, s: Any) -> None:
        self._string += to_s(s)

    def get_string(self) -> str:
        return self._string
