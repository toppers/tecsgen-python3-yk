"""MrubyBridgeCellPlugin.rb の移植。セルの受け口ごとに mruby ブリッジセルを生成する。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.CellPlugin import CellPlugin
from tecsgen.ruby_compat import Y, rb_print, sym, to_s


class MrubyBridgeCellPlugin(CellPlugin):
    # プラグイン引数名 => 処理（ファイル末尾で設定する）
    MRUBY_BRIDGE_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}
    _cell_list: ClassVar[
        dict[Any, Any]
    ] = {}  # gen_cdl_file 済みのセル（重複生成を避ける）
    _signature_list: ClassVar[dict[Any, bool]] = {}

    @classmethod
    def reset(cls) -> None:
        """Ruby のクラス変数に当たる状態を初期化する（1プロセスで何度も実行するテスト用）。"""
        MrubyBridgeCellPlugin._cell_list = {}
        MrubyBridgeCellPlugin._signature_list = {}

    def __init__(self, cell: Any, option: Any) -> None:
        """このメソッドは、セルの構文解析が終わったところで呼び出される（意味解析は終わっていない）。

        @exclude_port:: [str(port_name)]
        @exclude_port_func:: {str(port_name) => [str(func_name)]}
        @port_list:: {Port => str(include/exclude=func_name)}  すべての対象 port とオプション文字列
        """
        from tecsgen.core.syntaxobj.cdlstring import CDLString
        from tecsgen.plugin.MrubyBridgeSignaturePlugin import MrubyBridgeSignaturePlugin

        # Ruby 版はクラス定義の中で MrubyBridgeSignaturePlugin.rb を require する
        MrubyBridgeSignaturePlugin.on_load()
        super().__init__(cell, option)
        self._cell = cell

        # option
        self._b_ignoreUnsigned = False
        self._exclude_port: list[str] = []
        self._exclude_port_func: dict[str, list[str]] = {}
        self._b_auto_exclude = True  # auto_exclude = true by default

        self._plugin_arg_str = CDLString.remove_dquote(option)
        self._plugin_arg_list = {}
        self._plugin_arg_check_proc_tab = (
            MrubyBridgeCellPlugin.MRUBY_BRIDGE_PLUGIN_ARG_PROC
        )
        self.parse_plugin_arg()

        self._port_list: dict[Any, str] = {}  # return する前に設定しておく
        ct = self._cell.get_celltype()
        if ct is None:  # error case
            return

        port_list = ct.get_port_list()
        if len(self._exclude_port) > 0:
            # この実装では、存在しない port を指定されてもチェックできない
            for port in port_list:
                if to_s(port.get_name()) not in self._exclude_port:
                    self._port_list[port] = ""
        else:
            for port in port_list:
                self._port_list[port] = ""

        if len(self._exclude_port_func) > 0:
            for port, opt_str in list(self._port_list.items()):
                delim = ""
                pn = to_s(port.get_name())
                if pn in self._exclude_port_func:
                    for func_name in self._exclude_port_func[pn]:
                        opt_str += delim + "exclude=" + func_name
                        delim = ","
                self._port_list[port] = opt_str

    def gen_cdl_file(self, file: Any) -> None:
        cell_name = to_s(self._cell.get_name())
        file.print(f"/* MrubyBridgeCellPlugin: generate for cell={cell_name} */\n")

        if MrubyBridgeCellPlugin._cell_list.get(self._cell) is not None:
            file.print(
                "\n"
                "/*\n"
                f" * generate for {cell_name} duplicate and ignored.\n"
                " * This might comes from generate for celltype.\n"
                " */\n"
            )
            self.cdl_info(
                "MrubyBridgeCellPlugin: generate duplicate for cell '$1'",
                self._cell.get_name(),
            )
            return
        MrubyBridgeCellPlugin._cell_list[self._cell] = self._cell

        for port, opt_str in self._port_list.items():
            sig = port.get_signature()
            if sig is None:
                continue
            if sig.get_context() not in ("task", "any"):
                continue
            if port.get_port_type() != Y.ENTRY:
                continue

            pn = to_s(port.get_name())
            sgn = to_s(sig.get_global_name())
            rb_print(
                f"  MrubyBridgeCellPlugin: [cell.port] {cell_name}.{pn} => [mruby instance] "
                f"TECS::T{sgn}.new( '{cell_name}{pn}Bridge' ) \n"
            )
            if MrubyBridgeCellPlugin._signature_list.get(sig) is None:
                opt_str = (
                    f"ignoreUnsigned={to_s(self._b_ignoreUnsigned)}, "
                    f"auto_exclude={to_s(self._b_auto_exclude)}, " + opt_str
                )
                file.print(
                    "\n"
                    f"/* cell.port={cell_name}.{pn} */\n"
                    f'generate( MrubyBridgePlugin, {to_s(sig.get_namespace_path())}, "{opt_str}" );\n'
                )
                MrubyBridgeCellPlugin._signature_list[sig] = True

            # mikan option
            nest = self._cell.get_region().gen_region_str_pre(file)
            nest_str = "  " * nest
            file.print(
                f"{nest_str}/* BridgeCell */\n"
                f"{nest_str}cell nMruby::t{sgn} {cell_name}{pn}Bridge {{\n"
                f"{nest_str}    cTECS = {to_s(self._cell.get_namespace_path())}.{pn};\n"
                f"{nest_str}}};\n"
            )
            self._cell.get_region().gen_region_str_post(file)

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        cls.gen_post_code_body(file)

    @classmethod
    def gen_post_code_body(cls, file: Any) -> None:
        pass  # Ruby 版も何もしない（MrubyBridgeSignaturePlugin.gen_post_code_body の呼び出しはコメントアウト）

    def set_ignoreUnsigned(self, rhs: Any) -> None:
        """プラグイン引数 ignoreUnsigned。"""
        if rhs == "true" or rhs is None:
            self._b_ignoreUnsigned = True

    def set_exclude_port(self, rhs: Any) -> None:
        """プラグイン引数 exclude_port。"""
        from tecsgen.core.componentobj.port import Port

        ct = self._cell.get_celltype()
        if ct is None:  # error case
            return
        for rhs_port in to_s(rhs).split(","):
            obj = ct.find(sym(rhs_port))
            if type(obj) is not Port or obj.get_port_type() != Y.ENTRY:
                self.cdl_error(
                    "MRB9999 exclude_port '$1' not found or not entry in celltype '$2'",
                    rhs_port,
                    ct.get_name(),
                )
            else:
                self._exclude_port.append(rhs_port)

    def set_exclude_port_func(self, rhs: Any) -> None:
        """プラグイン引数 exclude_port_func。"""
        from tecsgen.core.componentobj.port import Port

        ct = self._cell.get_celltype()
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
                # Ruby 版は未定義の変数 rhs_port を参照して NameError になる（そのまま再現する）
                raise NameError(
                    "undefined local variable or method `rhs_port' for MrubyBridgeCellPlugin"
                )
            signature = obj.get_signature()
            if signature is None:  # error case
                continue
            if signature.get_function_head(sym(port_func[1])) is not None:
                self._exclude_port_func.setdefault(port_func[0], []).append(
                    port_func[1]
                )
            else:
                self.cdl_error(
                    "MRB9999 exclude_port_func: func '$1' not found in port '$2' celltype $3",
                    port_func[1],
                    port_func[0],
                    ct.get_name(),
                )

    def set_auto_exclude(self, rhs: Any) -> None:
        """プラグイン引数 auto_exclude。"""
        if rhs == "false":
            self._b_auto_exclude = False
        elif rhs == "true":
            self._b_auto_exclude = True  # auto_exclude = true by default
        else:
            self.cdl_warning(
                "MRB9999 auto_exclude: unknown rhs value ignored. specify true or false"
            )


MrubyBridgeCellPlugin.MRUBY_BRIDGE_PLUGIN_ARG_PROC = {
    "ignoreUnsigned": lambda obj, rhs: obj.set_ignoreUnsigned(rhs),
    "exclude_port": lambda obj, rhs: obj.set_exclude_port(rhs),
    "exclude_port_func": lambda obj, rhs: obj.set_exclude_port_func(rhs),
    "auto_exclude": lambda obj, rhs: obj.set_auto_exclude(rhs),
}
