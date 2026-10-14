"""unjoin_plugin.rb の移植：モデルを pickle で保存する（tecsflow に渡す）。

Ruby 版は `Marshal.dump(Namespace.get_root)` の前に、生きたオブジェクトを破壊的に書き換えて
プラグインへの参照を外す（`Namespace#unjoin_plugin`）。Python 版は元のオブジェクトを壊さず、
保存用の状態だけを差し替える `pickle.Pickler` のサブクラス（`UnjoinPickler`）で同じことをする。
そのため呼び出し順の制約（コード生成のあとでなければならない）は無い。

| Ruby                                                          | Python                              |
|---------------------------------------------------------------|-------------------------------------|
| Signature/Celltype/CompositeCelltype/Cell/DomainType の参照消去 | `UNJOIN_RESET`（属性名 → 置換値）   |
| Join/Region の through プラグイン → `ThroughPluginProxy`      | `_proxy_list`・`_proxy_dict`        |
| `Proc#_dump_data` を nil にする                                | lambda・ローカル関数を None にする  |
| 残存プラグイン                                                 | None にする（Ruby は Marshal のまま） |

`Namespace#unjoin_plugin` の再帰と `Join#unjoin_plugin2` は要らない（pickle が到達した
オブジェクトごとに差し替えるため）。
"""

from __future__ import annotations

import io
import pickle
import types
from dataclasses import dataclass
from typing import Any

PICKLE_PROTOCOL = 4
DUMP_FILE_NAME = "tecsgen.pickle"


@dataclass(frozen=True)
class ThroughPluginProxy:
    """through プラグインオブジェクトの代わりに保存する、tecsflow が参照する3値だけの代理。

    Ruby 版の `Join::ThroughPluginProxy`。pickle から参照できるようモジュール直下に置く。
    """

    namespace_path: Any
    entry_port_name: Any
    entry_port_subscript: Any

    def get_cell_namespace_path(self) -> Any:
        return self.namespace_path

    def get_through_entry_port_name(self) -> Any:
        return self.entry_port_name

    def get_through_entry_port_subscript(self) -> Any:
        return self.entry_port_subscript


def _to_proxy(po: Any) -> Any:
    if isinstance(po, ThroughPluginProxy) or po is None:
        return po
    return ThroughPluginProxy(
        po.get_cell_namespace_path(),
        po.get_through_entry_port_name(),
        po.get_through_entry_port_subscript(),
    )


def _proxy_list(items: list[Any]) -> list[Any]:
    return [_to_proxy(po) for po in items]


def _proxy_dict(items: dict[Any, Any]) -> dict[Any, Any]:
    return {key: _to_proxy(po) for key, po in items.items()}


# クラス名 → { 属性名: 置換値を作る関数 }（unjoin_plugin.rb の各 unjoin_plugin）
UNJOIN_RESET: dict[str, dict[str, Any]] = {
    "Signature": {"_generate": lambda v: None},
    "Celltype": {
        "_generate": lambda v: None,
        "_generate_list": lambda v: [],
        "_plugin": lambda v: None,
    },
    "CompositeCelltype": {
        "_generate": lambda v: None,
        "_generate_list": lambda v: [],
    },
    "Cell": {"_generate": lambda v: None, "_plugin": lambda v: None},
    # Ruby 版は @plugin だけ消す。_pluginClass はクラスへの参照で、読む側が
    # プラグインを import できるとは限らないため、Python 版では併せて消す
    "DomainType": {"_plugin": lambda v: None, "_pluginClass": lambda v: None},
    "Join": {
        "_through_generated_list": _proxy_list,
        "_region_through_generated_list": _proxy_list,
    },
    "Region": {"_cell_port_throug_plugin_list": _proxy_dict},
}


def _is_unpicklable_function(obj: Any) -> bool:
    if not isinstance(obj, types.FunctionType):
        return False
    return "<lambda>" in obj.__qualname__ or "<locals>" in obj.__qualname__


class UnjoinPickler(pickle.Pickler):
    """プラグインへの参照を外してモデルを pickle する。"""

    def __init__(self, file: io.BufferedIOBase) -> None:
        super().__init__(file, protocol=PICKLE_PROTOCOL)
        from tecsgen.core.plugin import Plugin

        self._plugin_class = Plugin

    def reducer_override(self, obj: Any) -> Any:
        # Proc は Marshal.dump できないので nil を返す定義が入る（Proc#_dump_data）
        if _is_unpicklable_function(obj):
            return (_none, ())
        if isinstance(obj, self._plugin_class):
            return (_none, ())

        # サブクラス（Region の派生など）にも適用する
        resets: dict[str, Any] = {}
        for klass in reversed(type(obj).__mro__):
            resets.update(UNJOIN_RESET.get(klass.__name__, {}))
        if not resets or not hasattr(obj, "__dict__"):
            return NotImplemented
        reduced = obj.__reduce_ex__(PICKLE_PROTOCOL)
        state = dict(reduced[2])
        for attr, make in resets.items():
            if attr in state:
                state[attr] = make(state[attr])
        return (reduced[0], reduced[1], state, *reduced[3:])


def _none() -> None:
    return None


def dumps(root: Any) -> bytes:
    """`root`（Namespace のルート）をプラグインへの参照を外して pickle したバイト列。"""
    buf = io.BytesIO()
    UnjoinPickler(buf).dump(root)
    return buf.getvalue()
