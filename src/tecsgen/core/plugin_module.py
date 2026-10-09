"""pluginModule.rb の移植。プラグインをロードする側のモジュール（`PluginModule`、内部仕様9章）。

@@loaded_plugin_list:: {Symbol=>Integer}
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import sys
from typing import TYPE_CHECKING, Any, ClassVar

from tecsgen.context import dbg_print, get_context, print_exception
from tecsgen.host import get_host
from tecsgen.ruby_compat import (
    RubyError,
    Symbol,
    class_name,
    rb_print,
    sym,
    to_s,
    truthy,
)

# 型検査のときだけ Node の子として扱う（mixin から cdl_error を呼ぶため。celltype_module.py と同じ手法）
if TYPE_CHECKING:
    from tecsgen.core.syntaxobj.node import Node

    class _Base(Node):
        pass
else:
    _Base = object


class PluginNotPorted(RubyError):
    """P5 でまだ移植していないプラグイン機構が必要になった。"""


def is_plugin_kind(obj: Any, plugin_class_name: str) -> bool:
    """`obj.kind_of?( ThroughPlugin )` など、プラグインの基底クラスとの比較。"""
    if obj is None:
        return False
    plugin_class = _import_plugin_class(plugin_class_name)
    if plugin_class is None:
        return False
    return isinstance(obj, plugin_class)


# `-L` で探した利用者プラグインのクラス（実行回ごと。ロードに失敗したものは None）。
# 同名で内容の違うプラグインが別ケースにあるので、`sys.modules` ではなくここに持つ。
_USER_PLUGIN_SUBDIRS = ("", "tecslib/plugin/")
_user_plugin_classes: dict[str, Any] = {}


def reset_user_plugins() -> None:
    _user_plugin_classes.clear()


def _import_plugin_class(name: str) -> Any:
    """`require_tecsgen_lib( "#{name}.rb", false )` + `Object.const_get(name)` に相当。

    組み込みの `tecsgen.plugin.<name>` を先に探し、無ければ `-L` のディレクトリを
    先頭から探す（組み込みと同名の利用者プラグインは上書きできない）。見つからなければ nil。
    """
    if name in _user_plugin_classes:
        return _user_plugin_classes[name]
    module_name = f"tecsgen.plugin.{name}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        if e.name != module_name:
            raise
        return _import_user_plugin_class(name)
    return getattr(module, name, None)


def _find_user_plugin_file(name: str) -> str | None:
    host = get_host()
    for directory in get_context().library_path:
        for subdir in _USER_PLUGIN_SUBDIRS:
            found = host.resolve_plugin_file(directory, f"{subdir}{name}.py")
            if found is not None:
                return found
    return None


def _import_user_plugin_class(name: str) -> Any:
    """`-L` のディレクトリにある `<name>.py` を読み、`<name>` クラスを返す。

    ファイルが無ければ nil。ロード中の例外は Ruby の `require` 失敗と同じく
    `print_exception` して再送出する（`load_plugin` が P2003 にする）。
    """
    path = _find_user_plugin_file(name)
    if path is None:
        return None
    module_name = "tecsgen_user_plugin_" + hashlib.sha1(path.encode()).hexdigest()[:12]
    _user_plugin_classes[name] = None  # 失敗しても読み直さない
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    except Exception as e:  # Ruby の rescue Exception
        sys.modules.pop(module_name, None)
        print_exception(e)
        raise
    plugin_class = getattr(module, name, None)
    if plugin_class is None:
        raise RubyError(f"uninitialized constant {name}")
    _user_plugin_classes[name] = plugin_class
    return plugin_class


def _register_plugin_class(plugin_class: Any) -> None:
    """`MultiPlugin#get_plugin` が返したクラスを、名前で引けるようにする。

    Ruby ではロード済みのクラスは定数になり、`Object.const_get(name)` で引ける。
    Python 版は名前からファイルを読み直すので、ファイル名と違う名前のクラス（利用者の
    `MultiPlugin` と同じファイルに書いたクラスなど）は、登録しないと post_code の生成などで
    見つからず、黙って飛ばされる。同名がすでにあれば何もしない。
    """
    if isinstance(plugin_class, type):
        _user_plugin_classes.setdefault(class_name(plugin_class), plugin_class)


def _lookup_loaded_plugin_class(name: str) -> Any:
    """`Object.const_get(name)`（require し直さない）に相当。

    `load_plugin` は2度目以降、require を試みず定数参照だけを行うので、
    ロード済みのクラス（組み込みは `sys.modules`、利用者プラグインはレジストリ）からだけ引く（無ければ nil）。
    """
    if name in _user_plugin_classes:
        return _user_plugin_classes[name]
    module = sys.modules.get(f"tecsgen.plugin.{name}")
    if module is None:
        return None
    return getattr(module, name, None)


def _resolve_super_class(super_class: Any) -> type:
    """load_plugin の `superClass` 引数（クラスまたはクラス名の文字列）を解決する。"""
    if isinstance(super_class, type):
        return super_class
    name = to_s(super_class)
    resolved = _import_plugin_class(name)
    if resolved is None:
        raise RubyError(f"unknown plugin base class '{name}'")
    return resolved


class PluginModule(_Base):
    _loaded_plugin_list: ClassVar[dict[Symbol, Any]] = {}

    # 後ろのコードの出力順の指定 (数字が少ないほどプライオリティは高い)
    MULTI_PLUGIN_POST_CODE_PRIORITY = 0
    DOMAIN_PLUGIN_POST_CODE_PRIORITY = 10000
    CLASS_PLUGIN_POST_CODE_PRIORITY = 10000
    THROUGH_PLUGIN_POST_CODE_PRIORITY = 20000
    CELLTYPE_PLUGIN_POST_CODE_PRIORITY = 30000
    COMPOSITE_PLUGIN_POST_CODE_PRIORITY = 40000
    CELL_PLUGIN_POST_CODE_PRIORITY = 50000
    SIGNATURE_PLUGIN_POST_CODE_PRIORITY = 60000

    @classmethod
    def reset(cls) -> None:
        PluginModule._loaded_plugin_list = {}
        reset_user_plugins()

    def load_plugin(self, plugin_name: Any, superClass: Any) -> Any:
        """プラグインをロードする。

        `#{plugin_name}.rb` をロードし、`plugin_name` クラスのオブジェクトを生成する。
        `plugin_name` が `MultiPlugin` の場合、`get_plugin` により `superClass` のプラグイン
        オブジェクトをロードする。すでにロードされているものは重複してロードしない。
        ロード時の例外はこのメソッドの中でキャッチされて None が返される。
        """
        dbg_print(f"PluginModule: load_plugin: {to_s(plugin_name)}\n")
        key = sym(plugin_name)
        try:
            if not truthy(PluginModule._loaded_plugin_list.get(key)):
                PluginModule._loaded_plugin_list[key] = 0
                if get_context().verbose:
                    rb_print(f"load '{to_s(plugin_name)}.rb'\n")
                pl_class = _import_plugin_class(to_s(plugin_name))
                if pl_class is None:
                    self.cdl_error("P2001 $1.rb : fail to load plugin", plugin_name)
                    return None
            else:
                # 2度目以降は require し直さず、定数参照だけを行う（失敗すれば例外 → P2003）
                pl_class = _lookup_loaded_plugin_class(to_s(plugin_name))
                if pl_class is None:
                    raise RubyError(f"uninitialized constant {to_s(plugin_name)}")

            super_cls = _resolve_super_class(superClass)
            if issubclass(pl_class, super_cls):  # plClass inherits superClass
                return pl_class

            multi_plugin = _import_plugin_class("MultiPlugin")
            if multi_plugin is not None and issubclass(pl_class, multi_plugin):
                dbg_print(f"pluginClass={class_name(pl_class)}\n")
                plugin_object = pl_class.get_plugin(super_cls)
                dbg_print(f"pluginClass={to_s(plugin_object)}\n")
                if plugin_object is None:
                    self.cdl_error(
                        "P9999 '$1': MultiPlugin not support '$2'",
                        plugin_name,
                        class_name(super_cls),
                    )
                _register_plugin_class(plugin_object)
                PluginModule._loaded_plugin_list[key] = sym("MultiPlugin")
                return plugin_object

            self.cdl_error(
                "P2002 $1: not kind of $2", plugin_name, class_name(super_cls)
            )
            return None
        except PluginNotPorted:
            raise
        except Exception:  # noqa: BLE001  Ruby の rescue Exception
            self.cdl_error("P2003 $1: load failed", plugin_name)
            return None

    def generate_and_parse(self, plugin_object: Any) -> None:
        """プラグインの gen_cdl_file を呼びして cdl ファイルを生成させ、解釈を行う。"""
        from tecsgen.context import get_context as _get_context
        from tecsgen.context import print_exception
        from tecsgen.core.componentobj.import_cdl import _host_reader
        from tecsgen.core.plugin import CFile
        from tecsgen.ruby_compat import class_name as _class_name
        from tecsgen.syntax.cdl_parser import CdlParser

        if plugin_object is None:  # プラグインのロードに失敗している（既にエラー）
            return
        plugin_name = sym(_class_name(type(plugin_object)))
        if PluginModule._loaded_plugin_list.get(plugin_name) == sym("MultiPlugin"):
            rb_print(f"{plugin_name}: MultiPlugin\n")
            return
        if PluginModule._loaded_plugin_list.get(plugin_name) is None:
            # プラグインのファイル名と、プラグインのクラス名が相違する場合
            # MultiPlugin の get_plugin で返されたケースでは None のままになっている
            PluginModule._loaded_plugin_list[plugin_name] = 0
        count = PluginModule._loaded_plugin_list[plugin_name]
        PluginModule._loaded_plugin_list[plugin_name] = count + 1
        tmp_file_name = f"{_get_context().gen}/tmp_{plugin_name}_{count}.cdl"

        tmp_file = None
        try:
            tmp_file = CFile.open(tmp_file_name, "w")
        except Exception as evar:  # noqa: BLE001
            self.cdl_error("P2004 $1: open error '$2'", plugin_name, tmp_file_name)
            print_exception(evar)
        dbg_print(
            f"generate_and_parse: {_class_name(type(plugin_object))}: gen_cdl_file\n"
        )
        try:
            plugin_object.gen_cdl_file(tmp_file)
        except Exception as evar:  # noqa: BLE001
            self.cdl_error(
                "P2005 $1: plugin error in gen_through_cell_code", plugin_name
            )
            print_exception(evar)
        try:
            if tmp_file is not None:
                tmp_file.close()
        except Exception as evar:  # noqa: BLE001
            self.cdl_error("P2006 $1: close error '$2'", plugin_name, tmp_file_name)
            print_exception(evar)

        # Import と同様、Host 経由で読み書きするパーサインスタンスを作る（別パーサで読み込む）
        parser = CdlParser(_host_reader)
        parser.set_plugin(plugin_object)
        parser.parse([tmp_file_name])
        parser.finalize()

    @classmethod
    def gen_plugin_post_code(cls) -> None:
        """プラグインが CDL の POST コードを生成（tmp_plugin_post_code.cdl への出力）。"""
        dbg_print("------------  gen_plugin_post_code  -------------\n")
        dbg_print(f"PluginModule {to_s(PluginModule._loaded_plugin_list)}\n")
        sorted_plugin_list = cls.sort_and_load(
            list(PluginModule._loaded_plugin_list.keys())
        )
        sorted_names = {sym(class_name(plugin)) for plugin in sorted_plugin_list}
        new_plugin_list = [
            plugin_name
            for plugin_name in PluginModule._loaded_plugin_list
            if plugin_name not in sorted_names
        ]
        cls.sort_and_load(new_plugin_list)

    @classmethod
    def sort_and_load(cls, plugin_list: list[Any]) -> list[Any]:
        """post_code priority 順のリストを作成し、その順に post code を生成する。"""
        from tecsgen.context import get_context as _get_context
        from tecsgen.core.componentobj.import_cdl import Import
        from tecsgen.core.plugin import CFile

        # ------ post_code priority 順のリストを作成 ------
        plugin_priority_list: dict[int, list[Any]] = {}
        for plugin_name in plugin_list:
            plClass = _import_plugin_class(to_s(plugin_name))
            if plClass is None:  # undefined PluginModule
                continue
            get_prio = getattr(plClass, "get_post_code_priority", None)
            prio = (
                get_prio()
                if callable(get_prio)
                else cls.get_post_code_priority(plClass)
            )
            plugin_priority_list.setdefault(prio, []).append(plClass)
            dbg_print(f"pluginModule: prio={prio} plugin={class_name(plClass)}\n")

        sorted_plugin_list: list[Any] = []
        for prio in sorted(plugin_priority_list):
            if prio != 0:  # exclude MultiPlugin
                sorted_plugin_list += plugin_priority_list[prio]

        # ----- post code priority 順に post code を生成 -------
        for plClass in sorted_plugin_list:
            tmp_file_name = (
                f"{_get_context().gen}/tmp_{class_name(plClass)}_post_code.cdl"
            )
            file = None
            try:
                file = CFile.open(tmp_file_name, "w")
            except Exception:  # noqa: BLE001
                from tecsgen.core.generator import Generator

                Generator.error(f"G9999 fail to create {tmp_file_name}")

            if file is not None:
                dbg_print(f"PluginModule: {class_name(plClass)}\n")
                if _get_context().verbose:
                    rb_print(
                        # Ruby 版は eval_str = "plClass.name}.gen_post_code( file )"
                        # （#{ が欠けている）をそのまま表示する
                        "gen_plugin_post_code: plClass.name}.gen_post_code( file )\n"
                    )
                try:
                    plClass.gen_post_code(file)
                except Exception as evar:  # noqa: BLE001
                    from tecsgen.context import print_exception
                    from tecsgen.core.generator import Generator

                    Generator.error(
                        "P2007 $1: fail to generate post code", class_name(plClass)
                    )
                    print_exception(evar)
                try:
                    file.close()
                except Exception:  # noqa: BLE001
                    from tecsgen.core.generator import Generator

                    Generator.error(f"G9999 fail to close {tmp_file_name}")
                dbg_print("## Import Post Code\n")
                Import(tmp_file_name)

        return sorted_plugin_list

    @classmethod
    def get_post_code_priority(cls, plClass: type) -> int:
        """プラグインの後ろの CDL コードの生成順を指定。"""
        multi_plugin = _import_plugin_class("MultiPlugin")
        domain_plugin = _import_plugin_class("DomainPlugin")
        class_plugin = _import_plugin_class("ClassPlugin")
        through_plugin = _import_plugin_class("ThroughPlugin")
        composite_plugin = _import_plugin_class("CompositePlugin")
        celltype_plugin = _import_plugin_class("CelltypePlugin")
        cell_plugin = _import_plugin_class("CellPlugin")
        signature_plugin = _import_plugin_class("SignaturePlugin")
        if multi_plugin is not None and issubclass(plClass, multi_plugin):
            return cls.MULTI_PLUGIN_POST_CODE_PRIORITY
        if domain_plugin is not None and issubclass(plClass, domain_plugin):
            return cls.DOMAIN_PLUGIN_POST_CODE_PRIORITY
        if class_plugin is not None and issubclass(plClass, class_plugin):
            return cls.CLASS_PLUGIN_POST_CODE_PRIORITY
        if through_plugin is not None and issubclass(plClass, through_plugin):
            return cls.THROUGH_PLUGIN_POST_CODE_PRIORITY
        if composite_plugin is not None and issubclass(plClass, composite_plugin):
            return cls.COMPOSITE_PLUGIN_POST_CODE_PRIORITY
        if celltype_plugin is not None and issubclass(plClass, celltype_plugin):
            return cls.CELLTYPE_PLUGIN_POST_CODE_PRIORITY
        if cell_plugin is not None and issubclass(plClass, cell_plugin):
            return cls.CELL_PLUGIN_POST_CODE_PRIORITY
        if signature_plugin is not None and issubclass(plClass, signature_plugin):
            return cls.SIGNATURE_PLUGIN_POST_CODE_PRIORITY
        raise RubyError(f"Unknown Plugin type '{class_name(plClass)}'")


def verbose_print(s: str) -> None:
    if get_context().verbose:
        rb_print(s)
