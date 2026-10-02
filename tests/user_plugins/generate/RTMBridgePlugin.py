"""test/generate/RTMBridgePlugin.rb の Python 版。"""

from __future__ import annotations

from typing import Any

from tecsgen.context import get_context
from tecsgen.core.cdl_types import VoidType
from tecsgen.core.generator import Generator
from tecsgen.core.plugin import CFile
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import rb_print, to_s


class RTMBridgePlugin(SignaturePlugin):
    def __init__(self, signature: Any, option: Any) -> None:
        super().__init__(signature, option)
        # Ruby 版は each_param のブロックの中で何もしない（呼び出すだけ）
        signature.each_param(lambda func_decl, param_decl: None)

    def gen_cdl_file(self, file: Any) -> None:
        """CDL ファイルの生成。typedef, signature, celltype, cell コードを生成。"""
        # ブリッジセルタイプの生成
        file.print(
            "/// RTM ⇒ TECS ブリッジセルタイプ ///\n"
            f"celltype tRTM{to_s(self._signature.get_name())}Bridge {{\n"
            f"    call {to_s(self._signature.get_name())} cTECS;\n"
            "};\n"
        )

        # RTM 用の IDL ファイルの生成。これは tecsgen.idl に出力する
        fname = f"{get_context().gen}/tecsgen.idl"

        try:
            file2 = CFile.open(fname, "w")
        except Exception:  # noqa: BLE001  Ruby の rescue
            Generator.error(f"{fname}: file open error")
            return

        try:
            file2.print(f"interface TECS{to_s(self._signature.get_name())} {{\n")
            for fh in self._signature.get_function_head_array():  # fh: FuncHead
                fd = fh.get_declarator()  # fd: Decl
                if fd.is_function():  # エラー検出済み
                    ft = fd.get_type()  # ft: FuncType
                    file2.print(f"\t{ft.get_type_str()} {to_s(fd.get_name())}( ")
                    for p in ft.get_paramlist().get_items():  # p: ParamDecl
                        # size_is, count_is, string, send, receive には対応しない
                        pd = p.get_declarator()  # pd: Decl
                        file2.print(
                            f"{to_s(p.get_direction()).lower()} "
                            f"{pd.get_type().get_type_str()} {to_s(pd.get_name())}"
                            f"{pd.get_type().get_type_str_post()}"
                        )
                        # Ruby 版は引数ごとに閉じ括弧を出す（引数が無ければ出さない）
                        file2.print(" );\n")
            file2.print("};\n")
        except Exception as evar:  # noqa: BLE001  Ruby の rescue Exception
            Generator.error(f"{fname}: file writing")
            rb_print(f"{evar}\n")
        finally:
            file2.close()

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """受け口関数の postamble (C言語)を生成する。"""
        for fh in self._signature.get_function_head_array():  # fh: FuncHead
            fd = fh.get_declarator()  # fd: Decl
            ft = fd.get_type()  # ft: FuncType
            ret_type = ft.get_type()
            file.print(f"{ft.get_type_str()}\nRTM_{to_s(fd.get_name())}( ")
            delim = ""
            for p in ft.get_paramlist().get_items():  # p: ParamDecl
                # size_is, count_is, string, send, receive には対応しない
                pd = p.get_declarator()  # pd: Decl
                file.print(
                    f"{delim}{pd.get_type().get_type_str()} {to_s(pd.get_name())}"
                    f"{pd.get_type().get_type_str_post()}"
                )
                delim = ", "
            file.print(" );\n{\n")

            if isinstance(ret_type.get_original_type(), VoidType):
                retval = ""
            else:
                file.print(
                    f"\t{ft.get_type().get_type_str()}\tretval"
                    f"{ft.get_type().get_type_str_post()};\n"
                )
                retval = "retval = "
            file.print(f"\t{retval}cTECS_{to_s(fd.get_name())}( ")
            delim = ""
            for p in ft.get_paramlist().get_items():
                pd = p.get_declarator()
                file.print(f"{delim}{to_s(pd.get_name())}")
                delim = ", "
            file.print(" );\n")
            if not isinstance(ret_type.get_original_type(), VoidType):
                file.print("\treturn\tretval;\n")
            file.print("}\n\n")
