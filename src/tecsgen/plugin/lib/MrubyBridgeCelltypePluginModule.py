"""MrubyBridgeCelltypePluginModule.rb の移植。

`MrubyBridgeCelltypePlugin`・`MrubyBridgeCompositePlugin` に mix-in され、セルタイプのセルごとに
`generate( MrubyBridgeCellPlugin, ... )` を生成して import する。Ruby 版のモジュールのクラス変数
（`@@plugin_list` など）は include したクラスで共有されるので、ここでも1か所に持つ。
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, ClassVar

from tecsgen.ruby_compat import Y, sym, to_s

# 型検査のときだけ Plugin の子として扱う（mixin から cdl_error などを呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.plugin import Plugin

    class _Base(Plugin):
        pass
else:
    _Base = object


class MrubyBridgeCelltypePluginModule(_Base):
    MRUBY_BRIDGE_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}
    _plugin_list: ClassVar[list[Any]] = []
    _count: ClassVar[int] = 1
    _b_gen_post_code_called: ClassVar[bool] = False

    _celltype: Any
    _cell: Any

    @classmethod
    def reset_module(cls) -> None:
        """モジュールのクラス変数を初期化する（1プロセスで何度も実行するテスト用）。"""
        M = MrubyBridgeCelltypePluginModule
        M._plugin_list = []
        M._count = 1
        M._b_gen_post_code_called = False

    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: Celltype（CompositeCelltype）  セルタイプ（インスタンス）"""
        from tecsgen.core.syntaxobj.cdlstring import CDLString
        from tecsgen.plugin.MrubyBridgeSignaturePlugin import MrubyBridgeSignaturePlugin

        # Ruby 版はモジュール定義の中で MrubyBridgeCellPlugin.rb（→ MrubyBridgeSignaturePlugin.rb）を require する
        MrubyBridgeSignaturePlugin.on_load()
        super().__init__(celltype, option)  # ty: ignore[too-many-positional-arguments]
        self._celltype = celltype
        self._cell_list: list[Any] = []
        self._include_inner_cell = False
        self._exclude_cells: list[Any] = []
        self._exclude_port: list[str] = []
        self._exclude_port_func: dict[str, list[str]] = {}
        self._b_ignoreUnsigned = False
        self._b_auto_exclude = True  # auto_exclude = true by default
        MrubyBridgeCelltypePluginModule._plugin_list.append(self)

        self._plugin_arg_check_proc_tab = (
            MrubyBridgeCelltypePluginModule.MRUBY_BRIDGE_PLUGIN_ARG_PROC
        )
        self._plugin_arg_str = CDLString.remove_dquote(option)
        self.parse_plugin_arg()

    def new_cell(self, cell: Any) -> None:
        """セルタイププラグインに対する新しいセルの報告。

        generate 文により呼び出された場合、それまでに定義された cell については、initialize の
        タイミングで呼び出される。
        """
        from tecsgen.context import get_context
        from tecsgen.core.componentobj.import_cdl import Import
        from tecsgen.core.plugin import CFile
        from tecsgen.core.tecsgen import TECSGEN

        if cell in self._cell_list:  # この行は、本来不要のはず
            return
        if TECSGEN.is_post_coded():  # post_code 以降のセルは対象から外す
            self.cdl_info(
                "I9999 MrubyBridgeCelltypePlugin: $1 is excluded because cell generated after post_coded",
                cell.get_name(),
            )
            return

        # include_inner_cell option
        if cell.is_cloned() and self._include_inner_cell is False:
            self.cdl_info(
                "I9999 MrubyBridgeCelltypePlugin: inner cell $1 is excluded",
                cell.get_name(),
            )
            return

        # exclude_cell option
        if cell.get_name() in self._exclude_cells:
            return

        opt_str = (
            f"ignoreUnsigned={to_s(self._b_ignoreUnsigned)}, "
            f"auto_exclude={to_s(self._b_auto_exclude)}"
        )
        for port in self._exclude_port:
            opt_str += f",exclude_port={port}"
        for port, funcs in self._exclude_port_func.items():
            for func in funcs:
                opt_str += f",exclude_port_func={port}.{func}"

        M = MrubyBridgeCelltypePluginModule
        ct_name = to_s(self._celltype.get_name())
        fn2 = f"{get_context().gen}/tmp_MrubyBridgeCelltypePluginModule_{ct_name}_{M._count}.cdl"
        f2 = CFile.open(fn2, "w")
        f2.print(
            f"/* MrubyBridgeCelltypePluginModule: celltype={ct_name} */\n"
            f'generate( MrubyBridgeCellPlugin, {to_s(cell.get_namespace_path())}, "{opt_str}" );\n'
        )
        f2.close()
        Import(fn2)
        M._count += 1

    ### 意味解析段階で呼び出されるメソッド ###

    def gen_cdl_file(self, file: Any) -> None:
        """この段階で呼び出すと generate 文が呼び出される前のセルのみの出力となるので、何もしない。"""

    def gen_factory(self, file: Any) -> None:
        pass

    def get_celltype(self) -> Any:
        return self._celltype

    @classmethod
    def gen_post_code_module(cls, file: Any) -> None:
        """Ruby の `MrubyBridgeCelltypePluginModule.gen_post_code`（モジュールメソッド）。"""
        M = MrubyBridgeCelltypePluginModule
        if M._b_gen_post_code_called is False:
            M._b_gen_post_code_called = True

    def set_ignoreUnsigned(self, rhs: Any) -> None:
        if rhs == "true" or rhs is None:
            self._b_ignoreUnsigned = True

    def set_include_inner_cell(self, rhs: Any) -> None:
        if rhs == "true" or rhs is None:
            self._include_inner_cell = True

    def set_exclude_cell(self, rhs: Any) -> None:
        for rhs_cell in to_s(rhs).split(","):
            self._exclude_cells.append(sym(re.sub(r"\s", "", rhs_cell)))

    def set_exclude_port(self, rhs: Any) -> None:
        # Ruby 版は未定義の @cell（nil）に get_celltype を呼んで NoMethodError になる（そのまま再現する）
        raise AttributeError("undefined method `get_celltype' for nil:NilClass")

    def set_exclude_port_func(self, rhs: Any) -> None:
        from tecsgen.core.componentobj.port import Port

        ct = self._celltype
        if ct is None:  # error case
            return
        for rhs_port_func in to_s(rhs).split(","):
            port_func = rhs_port_func.split(".")
            if len(port_func) != 2:
                self.cdl_error(
                    "MRB9999 exclude_port_func: '$1' not in 'port.func' form",
                    rhs_port_func,
                )
            obj = ct.find(sym(port_func[0]))
            if type(obj) is not Port or obj.get_port_type() != Y.ENTRY:
                self.cdl_error(
                    "MRB9999 exclude_port_func: port '$1' not found in celltype '$2'",
                    rhs_port_func,
                    ct.get_name(),
                )
                continue
            signature = obj.get_signature()
            if signature is None:  # error case
                continue
            if signature.get_function_head(sym(port_func[1])) is not None:
                self._exclude_port_func.setdefault(port_func[0], []).append(
                    port_func[1]
                )
            else:
                self.cdl_error(
                    "MRB9999 include_port_func: func '$1' not found in port '$2' celltype $3",
                    port_func[1],
                    port_func[0],
                    ct.get_name(),
                )

    def set_auto_exclude(self, rhs: Any) -> None:
        if rhs == "false":
            self._b_auto_exclude = False
        elif rhs == "true":
            self._b_auto_exclude = True  # auto_exclude = true by default
        else:
            self.cdl_warning(
                "MRB9999 auto_exclude: unknown rhs value ignored. specify true or false"
            )


MrubyBridgeCelltypePluginModule.MRUBY_BRIDGE_PLUGIN_ARG_PROC = {
    "ignoreUnsigned": lambda obj, rhs: obj.set_ignoreUnsigned(rhs),
    "include_inner_cell": lambda obj, rhs: obj.set_include_inner_cell(rhs),
    "exclude_cell": lambda obj, rhs: obj.set_exclude_cell(rhs),
    "exclude_port": lambda obj, rhs: obj.set_exclude_port(rhs),
    "exclude_port_func": lambda obj, rhs: obj.set_exclude_port_func(rhs),
    "auto_exclude": lambda obj, rhs: obj.set_auto_exclude(rhs),
}
