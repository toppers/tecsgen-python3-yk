"""namespacepath.rb の移植。名前空間パス（`NamespacePath`）。"""

from __future__ import annotations

import copy
from typing import Any

from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import RubyRuntimeError, sym, to_s


class NamespacePath(Node):
    """@b_absolute::Bool / @path::[ Symbol,... ]
    @namespace::Namespace:  @b_absolute == false のとき、基点となる namespace
    """

    def __init__(self, ident: Any, b_absolute: Any, namespace: Any = None) -> None:
        """ident::Symbol 最初の名前, ただし "::" のみの場合は String。

        b_absolute:Bool "::" で始まっている場合 true
        namespace::Namespace b_absolute = false かつ、構文解釈段階以外で呼び出す場合は、必ず指定すること
        """
        from tecsgen.core.componentobj.namespace import Namespace

        super().__init__()

        # Ruby の ident == "::"（String との比較。Symbol :"::" とは一致しない）
        if type(ident) is str and ident == "::":  # RootNamespace
            self._path: list[Any] = []
            self._b_absolute = True
        else:
            self._path = [ident]
            self._b_absolute = b_absolute

        if namespace is not None and namespace is not False:
            self._namespace: Any = namespace
            if b_absolute is True:
                raise RubyRuntimeError(
                    "NamespacePath#initialize: naamespace specified for absolute path"
                )
        elif b_absolute is False:
            self._namespace = Namespace.get_current()
        else:
            self._namespace = None

    def append_bang(self, ident: Any) -> NamespacePath:  # Ruby: append!
        """append する（元の NamespacePath オブジェクトを変形して返す）。"""
        self._path.append(ident)
        return self

    def append(self, ident: Any) -> NamespacePath:
        """append する（元の NamespacePath オブジェクトを変形しない。複製を返す）。"""
        cl = copy.copy(self)
        cl.set_clone()
        cl.append_bang(ident)
        return cl

    def set_clone(self) -> None:
        self._path = list(self._path)

    def get_name(self) -> Any:
        return self._path[len(self._path) - 1] if self._path else None

    def change_name(self, name: Any) -> NamespacePath:
        """クローンを作成して名前を変更する。"""
        cl = copy.copy(self)
        cl.set_clone()
        cl.change_name_no_clone(name)
        return cl

    change_name_clone = change_name

    def change_name_no_clone(self, name: Any) -> None:
        """名前を変更する（このインスタンスを参照するすべてに影響を与えることに注意）。"""
        self._path[len(self._path) - 1] = name

    def to_s(self) -> str:
        """CDL 用の path 文字列を生成。"""
        return self.get_path_str()

    def get_path_str(self) -> str:
        first = True
        path = "::" if self._b_absolute else ""
        for n in self._path:
            if first:
                path = f"{path}{to_s(n)}"
                first = False
            else:
                path += f"::{to_s(n)}"
        return path

    def is_absolute(self) -> Any:  # Ruby: is_absolute?
        return self._b_absolute

    def is_name_only(self) -> bool:  # Ruby: is_name_only?
        return len(self._path) == 1 and self._b_absolute is False

    def get_path(self) -> list[Any]:
        """パスの配列を返す（ルート namespace の場合、長さ０の配列）。"""
        return self._path

    def get_full_path(self) -> list[Any]:
        """フルパスの配列を返す（返された配列を書き換えてはならない）。"""
        if self._b_absolute:
            return self._path
        return list(self._namespace.get_namespace_path().get_full_path()) + self._path

    def get_base_namespace(self) -> Any:
        """相対パスのベースとなる namespace（is_absolute? == false の時のみ有効）。"""
        return self._namespace

    def get_global_name(self) -> str:
        """C 言語グローバル名を得る。"""
        if self._b_absolute:
            global_name = ""
        else:
            global_name = to_s(self._namespace.get_global_name())

        for n in self._path:
            if global_name != "":
                global_name = f"{global_name}_{to_s(n)}"
            else:
                global_name = to_s(n)
        return global_name

    @classmethod
    def analyze(cls, path_str: str, b_force_absolute: bool = False) -> NamespacePath:
        """分解して NamespacePath インスタンスを生成する（オプションなどで指定される文字列用）。"""
        if path_str == "::":
            return cls("::", True)

        pa = _ruby_split(path_str, "::")
        if pa and pa[0] == "":
            pa.pop(0)
            b_absolute = True
        else:
            b_absolute = bool(b_force_absolute)

        if pa:
            nsp = cls(sym(pa[0]), b_absolute)
        else:
            nsp = cls("::", b_absolute)
        if pa:
            pa.pop(0)

        for a in pa:
            nsp.append_bang(sym(a))

        return nsp

    def print_cdl_decl_path_pre(self, file: Any) -> None:
        """CDL に出力する際の定義用のパスを出力する。"""
        for i in range(len(self._path)):
            file.print("  " * i)
            file.print(f"namespace {to_s(self._path[i])}{{\n")

    def print_cdl_decl_path_post(self, file: Any) -> None:
        length = len(self._path) - 1
        for i in range(length + 1):
            file.print("  " * (length - i))
            file.print("}\n")
        file.print("\n")


def _ruby_split(s: str, sep: str) -> list[str]:
    """Ruby の String#split(sep)（末尾の空文字列を取り除く）。"""
    parts = s.split(sep)
    while parts and parts[-1] == "":
        parts.pop()
    return parts
