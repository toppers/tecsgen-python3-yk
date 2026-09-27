"""pluginModule.rb の移植。プラグインをロードする側のモジュール（`PluginModule`、内部仕様9章）。

プラグイン機構（`Plugin` とサブクラス、標準プラグイン）は P5 で移植する。それまでは
`load_plugin` が `PluginNotPorted` を送出し、プラグインを使う CDL の処理を止める
（差分テストでは、Ruby 版がプラグインを読んだケースを P5 まで比較対象から外している）。

@@loaded_plugin_list:: {Symbol=>Integer}
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.ruby_compat import RubyError, class_name, rb_print, sym, to_s


class PluginNotPorted(RubyError):
    """P5 まで移植しないプラグイン機構が必要になった。"""


def is_plugin_kind(obj: Any, plugin_class_name: str) -> bool:
    """`obj.kind_of?( ThroughPlugin )` など、プラグインの基底クラスとの比較（P5 で移植）。

    nil は常に偽。プラグインのオブジェクトは P5 まで現れないので、現れたら止める。
    """
    if obj is None:
        return False
    raise PluginNotPorted(f"kind_of?( {plugin_class_name} ) is ported in P5")


class PluginModule:
    _loaded_plugin_list: ClassVar[dict[Any, Any]] = {}

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

    def load_plugin(self, plugin_name: Any, superClass: Any) -> Any:
        """プラグインをロードする（P5 で移植）。

        Ruby 版は #{plugin_name}.rb をロードし、plugin_name クラスを返す。
        """
        dbg_print(f"PluginModule: load_plugin: {to_s(plugin_name)}\n")
        raise PluginNotPorted(
            f"plugin '{to_s(plugin_name)}' ({class_name(superClass) if isinstance(superClass, type) else to_s(superClass)}) is not ported yet (P5)"
        )

    def generate_and_parse(self, plugin_object: Any) -> None:
        """プラグインの gen_cdl_file を呼びして cdl ファイルを生成させ、解釈を行う（P5 で移植）。"""
        if plugin_object is None:  # プラグインのロードに失敗している（既にエラー）
            return
        raise PluginNotPorted("generate_and_parse is ported in P5")

    @classmethod
    def gen_plugin_post_code(cls) -> None:
        """プラグインが CDL の POST コードを生成（tmp_plugin_post_code.cdl への出力）。"""
        dbg_print("------------  gen_plugin_post_code  -------------\n")
        dbg_print(f"PluginModule {to_s(PluginModule._loaded_plugin_list)}\n")
        sorted_plugin_list = cls.sort_and_load(
            list(PluginModule._loaded_plugin_list.keys())
        )
        new_plugin_list = []
        for plugin_name in list(PluginModule._loaded_plugin_list.keys()):
            b_found = any(
                sym(class_name(plugin)) == plugin_name for plugin in sorted_plugin_list
            )
            if not b_found:
                new_plugin_list.append(plugin_name)
        cls.sort_and_load(new_plugin_list)

    @classmethod
    def sort_and_load(cls, plugin_list: list[Any]) -> list[Any]:
        """post_code priority 順のリストを作成し、その順に post code を生成する（P5 で移植）。"""
        if not plugin_list:
            return []
        raise PluginNotPorted("sort_and_load is ported in P5")

    @classmethod
    def get_post_code_priority(cls, plClass: Any) -> int:
        """プラグインの後ろの CDL コードの生成順を指定（P5 で移植）。"""
        raise PluginNotPorted("get_post_code_priority is ported in P5")


def verbose_print(s: str) -> None:
    if get_context().verbose:
        rb_print(s)
