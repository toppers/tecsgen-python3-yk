"""Mruby2CBridgePlugin.rb の移植（内部仕様9章）。mruby から C の関数を呼び出すブリッジ。

`MrubyBridgePlugin`・`TECS2CBridgePlugin`・`C2TECSBridgePlugin` を `generate` する CDL を生成する。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import sym, to_s


class Mruby2CBridgePlugin(SignaturePlugin):
    # シグニチャのグローバル名 → プラグインインスタンスのリスト（@@signature_list）
    _signature_list: ClassVar[dict[Any, list[Any]]] = {}

    @classmethod
    def reset(cls) -> None:
        """`@@signature_list` を初期化する（1プロセスで何度も実行するテスト用）。"""
        Mruby2CBridgePlugin._signature_list = {}

    def __init__(self, signature: Any, option: Any) -> None:
        super().__init__(signature, option)

        gname = to_s(self._signature.get_global_name())
        self._celltype_name = sym(f"t{gname}")
        self._class_name = sym(f"T{gname}")

        self.parse_plugin_arg()

    def gen_cdl_file(self, file: Any) -> None:
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        lst = Mruby2CBridgePlugin._signature_list
        # Ruby 版の c2tecs は、最初のシグニチャ以外では代入されず nil（文字列にすると空）
        c2tecs = ""
        if len(lst) == 0:
            self.print_msg(
                "  Mruby2CBridgePlugin: [initialize function] 'void initializeBridge( mrb_state *mrb )' must be called from VM.\n"
            )
            c2tecs = 'generate( C2TECSBridgePlugin, nMruby::sInitializeBridge, "silent=true" );\n'

        gname = self._signature.get_global_name()
        if lst.get(gname) is not None:
            lst[gname].append(self)
            self.cdl_warning(
                "MRCW001 signature '$1' duplicate. ignored current one",
                self._signature.get_namespace_path(),
            )
            return

        lst[gname] = [self]
        self.print_msg(
            f"  Mruby2CBridgePlugin: [object creattion]    object = TECS::{to_s(self._class_name)}.new( 'C{to_s(gname)}' )\n"
        )
        self.print_msg(
            "  Mruby2CBridgePlugin: [function call]       result = object.function( params )  # substitute 'function' and params \n"
        )

        cf = CFile.open(f"{get_context().gen}/Mruby2C_tsInitializerBridge.cdl", "w")
        cf.print(
            "cell nC2TECS::tnMruby_sInitializeBridge C2TECS_tsInitializeBridge{\n"
            "    cCall = VM_TECSInitializer.eInitialize;\n"
            "};\n"
        )
        cf.close()

        path = to_s(self._signature.get_namespace_path())
        name = to_s(self._signature.get_name())
        file.print(
            f'generate( MrubyBridgePlugin, {path}, "silent=true" );\n'
            f'generate( TECS2CBridgePlugin, {path}, "silent=true" );\n'
            f"{c2tecs}\n"
            f"cell nMruby::t{name} C{name}{{\n"
            f"    cTECS = TECS2C_{name}.eEnt;\n"
            "};\n"
            f"cell nTECS2C::t{name} TECS2C_{name}{{}};\n"
            "\n"
            'import( "Mruby2C_tsInitializerBridge.cdl" );\n'
        )
