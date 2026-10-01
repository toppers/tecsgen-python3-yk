"""HRPSVCThroughPlugin.rb の移植（内部仕様9章）。拡張サービスコールを用いたドメイン間通信の through プラグイン。

HRP ドメインプラグインによって挿入される。前提条件: 呼出し先がカーネルオブジェクトかどうかの判定は
HRP ドメインプラグインで実施されるため、ここでは判定しない。

mikan through plugin: namespace が考慮されていない

以下を仮定（制限事項）:
  呼び元、呼び先のエンディアン、char, short, int_t, long_t, intptr_t のサイズが同じ
  有符号、無符号でサイズが同じ

Ruby 版の private メソッド `gen_caller_check_code` は、どこからも呼ばれない（呼び出しは `=begin`〜`=end`
でコメントアウトされている）ので移植していない。
"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import Y, sym, to_s, truthy


class HRPSVCThroughPlugin(ThroughPlugin):
    # HRP3 の拡張サービスコールで扱うことのできる引数の最大個数
    NUM_SVC_ARG_MAX = 5

    def __init__(
        self,
        cell_name: Any,
        plugin_arg: Any,
        next_cell: Any,
        next_cell_port_name: Any,
        next_cell_port_subscript: Any,
        signature: Any,
        celltype: Any,
        caller_cell: Any,
    ) -> None:
        super().__init__(
            cell_name,
            plugin_arg,
            next_cell,
            next_cell_port_name,
            next_cell_port_subscript,
            signature,
            celltype,
            caller_cell,
        )

        caller_dt = caller_cell.get_region().get_domain_root().get_domain_type()
        if caller_dt is None:
            # 呼び元がドメイン指定のないリージョンに属する場合、エラーとしない (ローダブルモジュール対応)
            pass
        elif caller_dt.get_name() not in (Y.HRP, Y.HRMP):
            self.cdl_error(
                "HSV0011 domain of caller cell '$1' is '$1'. This plugin supports HRP or HRMP",
                caller_cell.get_name(),
                caller_dt.get_name(),
            )
        callee_dt = next_cell.get_region().get_domain_root().get_domain_type()
        if callee_dt is None:
            self.cdl_error(
                "HSV0012 callee cell '$1' is not in domain region.",
                next_cell.get_name(),
            )
        elif callee_dt.get_name() not in (Y.HRP, Y.HRMP):
            self.cdl_error(
                "HSV0013 domain of callee cell '$1' is '$2'. This plugin supports HRP or HRMP",
                next_cell.get_name(),
                callee_dt.get_name(),
            )

        # 受け口配列の場合、配列添数ごとに別のセルタイプとする
        # （Ruby 版でも subscript は使われない）
        sig_name = to_s(signature.get_global_name())
        self._ct_name_body = sym(f"tHRPSVCBody_{sig_name}")
        self._ct_name = sym(f"tHRPSVCCaller_{sig_name}")
        self._cell_name_body = sym(f"{to_s(self._cell_name)}SVCBody")
        self._cell_name = sym(f"{to_s(self._cell_name)}SVCCaller")
        self._entry_port_name = sym("eEntry")

        self._b_printed_include_stdint = False

    def get_cell_namespace_path(self) -> Any:
        """生成するセルの namespace path を生成する。"""
        nsp = self._start_region.get_namespace_path()
        return nsp.append(self._cell_name)

    def gen_plugin_decl_code(self, file: Any) -> None:
        subsc = (
            "[" + to_s(self._next_cell_port_subscript) + "]"
            if truthy(self._next_cell_port_subscript)
            else ""
        )
        file.print(
            "/*\n"
            " * generated automatically by HRPSVCThroughPlugin.\n"
            f" *   caller port={to_s(self._caller_cell.get_name())}.{to_s(self._join.get_name())}\n"
            f" *   callee port={to_s(self._next_cell.get_name())}.{to_s(self._next_cell_port_name)}{subsc}\n"
            " */\n"
            "\n"
            f"/* generate celltypes for extended service call for signature {to_s(self._signature.get_name())}  */\n"
            f'generate( HRPSVCSignaturePlugin, {to_s(self._signature.get_namespace_path())}, "" );\n'
            "\n"
        )

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        ##### クライアント側のセルの生成 #####
        tfn = f"TFN_SVCBody_{to_s(self._next_cell.get_name())}_{to_s(self._next_cell_port_name)}".upper()
        nest = self._start_region.gen_region_str_pre(file)
        nest_str = "  " * nest

        # クライアント側チャンネルの生成
        # 拡張サービスコール呼出し
        file.print(
            f"{nest_str}/* HRPSVCTHROUGH0003 */\n"
            f"{nest_str}//  Client Side Channel\n"
            f"{nest_str}cell {to_s(self._ct_name)} {to_s(self._cell_name)}{{\n"
            f'{nest_str}  tfn_base = C_EXP( "{tfn}" );\n'
            f"{nest_str}}};\n"
            "\n"
        )

        self._start_region.gen_region_str_post(file)
        file.print("\n\n")

        ##### サーバー側のセルの生成 #####
        file.print(
            "/* HRPSVCTHROUGH0004 : generate kernel side cell */\n"
            f"generate( HRPSVCBodyCellPlugin, {to_s(self._next_cell.get_namespace_path())}, "
            f'"exportEntryPort={to_s(self._next_cell_port_name)}:{to_s(self._start_region.get_name())}" );\n'
        )

    def get_callee_cell(self) -> Any:
        return self._callee_cell

    def get_caller_cell(self) -> Any:
        return self._caller_cell

    def get_callee_ep_name(self) -> Any:
        return self._join.get_port_name()
