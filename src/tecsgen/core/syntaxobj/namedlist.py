"""namedlist.rb の移植。名前で引ける、定義順を保つ要素のリスト。

要素（item）は `get_name()` を持つこと。Ruby 版では戻り値が Symbol でなければならない。
Python 版は Symbol を str で表すので、str であることを確認する。
"""

from __future__ import annotations

import copy
from typing import Any

from tecsgen.context import dbg_print
from tecsgen.core.generator import Generator
from tecsgen.ruby_compat import inspect, rb_print, rb_puts, to_s, truthy


class NamedList:
    _names: dict[str, Any]
    _items: list[Any]
    _type: str

    def __init__(self, item: Any, type: str) -> None:  # Ruby と同名の引数
        self._names = {}
        self._items = []
        self._type = type  # エラーメッセージ用
        self.add_item(item)

    def add_item(self, item: Any) -> NamedList:
        """要素を加える。parse した時点で加えること（場所を記憶する）。"""
        if truthy(item):
            dbg_print(f"add_item: name={to_s(item.get_name())}   {item.locale_str()}\n")
            self.assert_name(item)
            name = item.get_name()
            prev = self._names.get(name)
            if prev is not None:  # 登録済みの要素は truthy なので nil 判定と同じ
                Generator.error("S2001 '$1' duplicate $2", name, self._type)
                prev_locale = prev.get_locale()
                rb_puts(
                    f"previous: {to_s(prev_locale[0])}: line {to_s(prev_locale[1])} "
                    f"'{to_s(name)}' defined here"
                )
                return self
            self._names[name] = item
            self._items.append(item)
        return self

    def change_item(self, item: Any) -> None:
        self.assert_name(item)
        name = item.get_name()
        prev_one = self._names.get(name)
        self._names[name] = item
        self._items = [i for i in self._items if i is not prev_one]
        self._items.append(item)

    def del_item(self, item: Any) -> None:
        self.assert_name(item)
        name = item.get_name()
        self._names.pop(name, None)
        self._items = [i for i in self._items if i is not item]

    def get_item(self, name: Any) -> Any:
        if not isinstance(name, str):
            rb_print(f"get_item: '{to_s(name)}', items are below\n")
            for nm in self._names:
                rb_print(inspect(nm) + "\n")
            raise TypeError(f"get_item: {to_s(name)}: not Symbol")
        return self._names.get(name)

    def get_items(self) -> list[Any]:
        return self._items

    def clone_for_composite(
        self, ct_name: Any, cell_name: Any, locale: Any
    ) -> NamedList:
        """composite cell を clone した時に要素（Join）を clone する。

        mikan このメソッドは Join に特化されているので NamedList から分離すべき
        """
        cl = copy.copy(self)
        cl.set_cloned(ct_name, cell_name, locale)
        return cl

    def set_cloned(self, ct_name: Any, cell_name: Any, locale: Any) -> None:
        """clone された NamedList インスタンスの参照するもの（item）を clone する。"""
        items: list[Any] = []
        names: dict[str, Any] = {}
        for i in self._items:
            dbg_print(
                f"NamedList clone {to_s(ct_name)}, {to_s(cell_name)}, {to_s(i.get_name())}\n"
            )
            cl = i.clone_for_composite(ct_name, cell_name, locale)
            names[cl.get_name()] = cl
            items.append(cl)
        self._items = items
        self._names = names

    def assert_name(self, item: Any) -> None:
        if not isinstance(item.get_name(), str):
            raise TypeError("Not symbol for NamedList item")

    def show_tree(self, indent: int) -> None:
        for i in self._items:
            i.show_tree(indent)
