"""import.rb の移植（`import` は Python の予約語なので import_cdl と改名）。CDL の import（`Import`）。

import はパースの途中で別のパーサを作って同期的にパースする（入れ子）。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.core.componentobj.importable import Importable
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.syntaxobj.node import Node
from tecsgen.host import get_host
from tecsgen.ruby_compat import RubyRuntimeError, gsub, rb_or, to_s, truthy


class Import(Importable, Node):
    """@b_reuse::bool: 再利用．セルタイプの template 生成不要 / @b_reuse_real::bool:  実際に再利用
    @cdl:: string: import する CDL / @cdl_path:: string: CDL のパス
    @b_imported:: bool: import された(コマンドライン指定されていない)
    """

    # ヘッダの名前文字列のリスト  添字：expand したパス、値：Import
    _import_list: ClassVar[dict[str, Any]] = {}

    _nest_stack_index: ClassVar[int] = -1
    _nest_stack: ClassVar[list[Any]] = []
    _current_object: ClassVar[Any] = None
    _current_import: ClassVar[Any] = None

    _cdl_path: Any  # 見つかるまで None

    @classmethod
    def reset(cls) -> None:
        Import._import_list = {}
        Import._nest_stack_index = -1
        Import._nest_stack = []
        Import._current_object = None
        Import._current_import = None

    @classmethod
    def push(cls, obj: Any) -> None:
        Import._nest_stack_index += 1
        _set_at(Import._nest_stack, Import._nest_stack_index, Import._current_object)
        Import._current_object = obj

    @classmethod
    def pop(cls) -> None:
        Import._current_object = _get_at(Import._nest_stack, Import._nest_stack_index)
        Import._nest_stack_index -= 1
        if Import._nest_stack_index < -1:
            raise RubyRuntimeError("TooManyRestore")

    def __init__(self, cdl: Any, b_reuse: Any = False, b_imported: Any = True) -> None:
        """import を行う。cdl:: string cdl へのパス．"" で囲まれていることを仮定 / b_reuse:: true: template を生成しない"""
        from tecsgen.core.generator import Generator
        from tecsgen.syntax.cdl_parser import CdlParser

        Import.push(self)
        self._b_imported = b_imported
        super().__init__()
        Import._current_import = self
        # ヘッダファイル名文字列から前後の "", <> を取り除く
        self._cdl = gsub(r'\A["<](.*)[">]\Z', "\\1", to_s(cdl))

        # サーチパスから探す
        found = False
        self._cdl_path = ""

        self._b_reuse = b_reuse
        self._b_reuse_real = rb_or(self._b_reuse, Generator.is_reuse())
        host = get_host()
        ctx = get_context()

        if truthy(Generator.get_plugin()) and host.exists(f"{ctx.gen}/{self._cdl}"):
            self._cdl_path = f"{ctx.gen}/{self._cdl}"
            found = True
        else:
            path: Any = self.find_file(self._cdl)
            if truthy(path):
                found = True
                self._cdl_path = path

        if found is False:
            self.cdl_error("S1148 $1 not found in search path", self._cdl)
            return

        # 読込み済みなら、読込まない
        prev: Any = Import._import_list.get(host.expand_path(self._cdl_path))
        if truthy(prev):
            if prev.is_reuse_real() != self._b_reuse_real:
                self.cdl_warning(
                    "W1008 $1: reuse designation mismatch with previous import",
                    self._cdl,
                )
            return

        # import リストを記録
        Import._import_list[host.expand_path(self._cdl_path)] = self

        # plugin から import されている場合
        plugin = Generator.get_plugin()

        # パーサインスタンスを生成(別パーサで読み込む)
        parser = CdlParser(_host_reader)

        # plugin から import されている場合の plugin 設定
        parser.set_plugin(plugin)

        # reuse フラグを設定
        parser.set_reuse(self._b_reuse_real)

        # cdl をパース
        parser.parse([self._cdl_path])

        # 終期化　パーサスタックを戻す
        parser.finalize()
        Import.pop()

    @classmethod
    def get_list(cls) -> dict[str, Any]:
        return Import._import_list

    def get_cdl_path(self) -> Any:
        return self._cdl_path

    def is_reuse_real(self) -> Any:  # Ruby: is_reuse_real?
        return self._b_reuse_real

    @classmethod
    def get_current(cls) -> Any:
        return Import._current_object

    def is_imported(self) -> Any:  # Ruby: is_imported?
        return self._b_imported

    def get_cdl_name(self) -> Any:
        """cdl の名前を返す（引数で指定されている cdl 名。一部パスを含む可能性がある）。"""
        return self._cdl


def _host_reader(file: str) -> bytes:
    return get_host().read_bytes(file)
