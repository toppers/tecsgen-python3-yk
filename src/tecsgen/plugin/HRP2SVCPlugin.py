"""HRP2SVCPlugin.rb の移植（内部仕様9章）。拡張サービスコールを用いたドメイン間通信の through プラグイン。

HRP2 ドメインプラグインによって挿入される。Ruby 版は進行状況を `puts`／`p` で標準出力へ書く
（正解データの標準出力に含まれる）ので、同じ内容をそのまま書く。

mikan through plugin: namespace が考慮されていない

以下を仮定（制限事項）:
  呼び元、呼び先のエンディアン、char, short, int_t, long_t, intptr_t のサイズが同じ
  有符号、無符号でサイズが同じ
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.core.cdl_types import VoidType
from tecsgen.core.generate import AppFile
from tecsgen.core.plugin import CFile
from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import (
    Y,
    inspect,
    rb_puts,
    sym,
    to_s,
    truthy,
    utf8_literal,
)


class SVCManage:
    # TODO: デフォルトの拡張サービスコール分を予約しておく
    # デフォルトの拡張サービスコール（syslogなど）もコンポーネント化するまで
    _id: ClassVar[int] = 20
    _func_ids: ClassVar[dict[str, int]] = {}

    @classmethod
    def reset(cls) -> None:
        SVCManage._id = 20
        SVCManage._func_ids = {}

    @classmethod
    def get_func_id(cls, func_name: str) -> int | None:
        return SVCManage._func_ids.get(func_name)

    @classmethod
    def set_func_id(cls, func_name: str) -> None:
        SVCManage._func_ids[func_name] = cls.assign_id()
        rb_puts(SVCManage._func_ids[func_name])

    @classmethod
    def include_func_id(cls, func_name: str) -> bool:  # Ruby: include_func_id?
        return func_name in SVCManage._func_ids

    @classmethod
    def get_id(cls) -> int:
        return SVCManage._id

    @classmethod
    def set_id(cls, id_: int) -> None:
        SVCManage._id = id_

    @classmethod
    def assign_id(cls) -> int:
        SVCManage._id += 1
        return SVCManage._id


class HRP2SVCPlugin(ThroughPlugin):
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
        port = to_s(self._next_cell_port_name)
        self._ct_name_body = sym(
            f"{to_s(self._ct_name)}SVCBody_{to_s(self._next_cell.get_name())}_{port}"
        )
        self._ct_name = sym(
            f"{to_s(self._ct_name)}SVCCaller_{to_s(self._next_cell.get_name())}_{port}"
        )
        self._cell_name_body = sym(f"{to_s(self._cell_name)}SVCBody")
        self._cell_name = sym(f"{to_s(self._cell_name)}SVCCaller")
        rb_puts("%%%% ")
        rb_puts(inspect(self._next_cell.get_name()))
        rb_puts(inspect(self._caller_cell.get_name()))

    def get_cell_namespace_path(self) -> Any:
        """生成するセルの namespace path を生成する。"""
        nsp = self._start_region.get_namespace_path()
        return nsp.append(self._cell_name)

    def _is_kernel_object(self) -> bool:
        return HRP2KernelObjectPlugin.include_celltype(self._next_cell.get_celltype())

    def gen_plugin_decl_code(self, file: Any) -> None:
        gen = get_context().gen
        sig = to_s(self._signature.get_name())
        generated = ThroughPlugin._generated_celltype

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if not self._is_kernel_object():
            if generated.get(self._ct_name_body) is None:
                generated[self._ct_name_body] = [self]
                file2 = CFile.open(f"{gen}/{to_s(self._ct_name_body)}.cdl", "w")
                file2.print(
                    "[active]\n"
                    f"celltype {to_s(self._ct_name_body)} {{\n"
                    f"    call {sig} {to_s(self._call_port_name)};\n"
                    "};\n"
                )
                file2.close()
            else:
                generated[self._ct_name_body].append(self)
            file.print(f'import( "{gen}/{to_s(self._ct_name_body)}.cdl" );\n')

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if generated.get(self._ct_name) is None:
            generated[self._ct_name] = [self]
            file2 = CFile.open(f"{gen}/{to_s(self._ct_name)}.cdl", "w")
            if not self._is_kernel_object():
                file2.print(
                    f"celltype {to_s(self._ct_name)} {{\n"
                    f"    entry {sig} {to_s(self._entry_port_name)};\n"
                    "};\n"
                )
            else:
                # TODO inlineにした方が効率がよいが，tecsgenの生成したヘッダファイルの
                # 読込順のためにエラーとなる
                file2.print(
                    f"celltype {to_s(self._ct_name)} {{\n"
                    f"    //[inline] entry {sig} {to_s(self._entry_port_name)};\n"
                    f"    entry {sig} {to_s(self._entry_port_name)};\n"
                    f"    call {sig} {to_s(self._call_port_name)};\n"
                    "};\n"
                )
            file2.close()
        else:
            generated[self._ct_name].append(self)
        file.print(f'import( "{gen}/{to_s(self._ct_name)}.cdl" );\n')

    def _subscript(self) -> str:
        if truthy(self._next_cell_port_subscript):
            return "[" + to_s(self._next_cell_port_subscript) + "]"
        return ""

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        gen = get_context().gen
        self.gen_plugin_decl_code(file)

        if not self._is_kernel_object():
            ##### クライアント側のセルの生成 #####
            nest = self._start_region.gen_region_str_pre(file)
            nest_str = "  " * nest

            # クライアント側チャンネルの生成
            # 拡張サービスコール呼出し
            file.print(
                f"{nest_str}  //  Client Side Channel\n"
                f"{nest_str}  cell {to_s(self._ct_name)} {to_s(self._cell_name)}{{\n"
                f"{nest_str}  }};\n"
                "\n"
            )

            self._start_region.gen_region_str_post(file)
            file.print("\n\n")

            ##### サーバー側のセルの生成 #####
            nest = self._end_region.gen_region_str_pre(file)
            nest_str = "  " * nest
            subscript = self._subscript()

            # サーバー側チャンネルの生成
            # 拡張サービスコール本体
            file.print(
                "\n"
                f"{nest_str}  //  Server Side Channel\n"
                f"{nest_str}  cell {to_s(self._ct_name_body)} {to_s(self._cell_name_body)}{{\n"
                f"{nest_str}    {to_s(self._call_port_name)} = {self._next_cell.get_namespace_path().get_path_str()}.{to_s(self._next_cell_port_name)}{subscript};\n"
                f"{nest_str}  }};\n"
            )

            self._end_region.gen_region_str_post(file)

            file2 = AppFile.open(f"{gen}/tecsgen.cfg")
            file2.print("\n/* Generated by HRP2SVCPlugin */\n\n")
            file2.print(f'#include "{to_s(self._ct_name_body)}_factory.h"\n')
            file2.close()
        else:
            ##### クライアント側のセルの生成 #####
            nest = self._start_region.gen_region_str_pre(file)
            nest_str = "  " * nest
            subscript = self._subscript()

            # クライアント側チャンネルの生成
            # 拡張サービスコール呼出し
            file.print(
                f"{nest_str}  //  Client Side Channel\n"
                f"{nest_str}  cell {to_s(self._ct_name)} {to_s(self._cell_name)}{{\n"
                f"{nest_str}    {to_s(self._call_port_name)} = {self._next_cell.get_namespace_path().get_path_str()}.{to_s(self._next_cell_port_name)}{subscript};\n"
                f"{nest_str}  }};\n"
                "\n"
            )

            self._start_region.gen_region_str_post(file)
            file.print("\n\n")

    def gen_ep_func_body(
        self,
        file: Any,
        b_singleton: bool,
        ct_name: Any,
        global_ct_name: Any,
        sig_name: Any,
        ep_name: Any,
        func_name: Any,
        func_global_name: Any,
        func_type: Any,
        params: list[Any],
    ) -> None:
        """受け口関数の本体(C言語)を生成する。

        通常であれば、ジェネレータは受け口関数のテンプレートを生成する。
        プラグインの場合、変更する必要のないセルタイプコードを生成する。
        """
        rb_puts(f"generate ep_func for {to_s(ct_name)}")

        if self._is_kernel_object():
            # カーネルドメインのセルは特別なことは何もせず，普通に呼び出す
            super().gen_ep_func_body(
                file,
                b_singleton,
                ct_name,
                global_ct_name,
                sig_name,
                ep_name,
                func_name,
                func_global_name,
                func_type,
                params,
            )
            return

        gen = get_context().gen
        ret_type = func_type.get_type()
        b_void = isinstance(ret_type, VoidType)
        body = to_s(self._ct_name_body)
        call_port = to_s(self._call_port_name)
        fname = to_s(func_name)

        # 拡張サービスコール呼出し
        if not b_void:
            file.print(f"  {ret_type.get_type_str()}  retval;\n")

        if not b_singleton:
            file.print(
                f"  {to_s(ct_name)}_CB    *p_cellcb;\n"
                "  if( VALID_IDX( idx ) ){\n"
                f"    p_cellcb = {to_s(global_ct_name)}_GET_CELLCB(idx);\n"
                "  }else{\n"
                + utf8_literal("     /* エラー処理コードをここに記述 */\n")
                + "  }\n\n"
            )

        if not b_void:
            file.print(f"  retval = ({ret_type.get_type_str()})")
        else:
            file.print("  ")

        new_func = False
        if not SVCManage.include_func_id(f"{body}_{fname}"):
            new_func = True
            SVCManage.set_func_id(f"{body}_{fname}")
        svcid = SVCManage.get_func_id(f"{body}_{fname}")
        file.print(f"cal_svc( {to_s(svcid)}")

        i = 0
        for param in params:
            file.printf(f", {to_s(param.get_name())}")
            i += 1

        while i < 5:
            file.printf(", 0")
            i += 1

        file.print(" );\n")

        if not b_void:
            file.print("  return retval;\n")

        # 拡張サービスコール本体
        if new_func:
            file2 = AppFile.open(f"{gen}/{body}.c")

            if b_void:
                retval_assign = ""
                retval_return = ""
            else:
                retval_assign = "retval = (ER_UINT)"
                retval_return = "retval"

            file2.print(
                "ER_UINT\n"
                f"{body}_{fname}(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid)\n"
                "{\n"
                f"    {body}_CB    *p_cellcb;\n"
                "#if 0\n"
                "    if( VALID_IDX( idx ) ){\n"
                f"      p_cellcb = {body}_GET_CELLCB(idx);\n"
                "    }else{\n"
                + utf8_literal("       /* エラー処理コードをここに記述 */\n")
                + "    }\n"
                "#else\n"
                "    p_cellcb = NULL;\n"
                "#endif\n"
                "\n"
                "    ER_UINT retval = 0;\n"
                "\n"
            )

            num = 1
            for param in params:
                if param.get_declarator().get_ptr_level() > 0:
                    if param.get_direction() == Y.IN:
                        file2.print(
                            f"    if(prb_mem((void *)par{num}, sizeof({param.get_type().get_type_str()}), TSK_SELF, TPM_READ) != E_OK){{\n"
                            "        return E_MACV;\n"
                            "    }\n"
                        )
                    elif param.get_direction() == Y.OUT:
                        file2.print(
                            f"    if(prb_mem((void *)par{num}, sizeof({param.get_type().get_type_str()}), TSK_SELF, TPM_WRITE) != E_OK){{\n"
                            "        return E_MACV;\n"
                            "    }\n"
                        )
                num += 1

            file2.print(f"    {retval_assign}{call_port}_{fname}(")

            delim = ""
            num = 1
            for param in params:
                file2.print(delim)
                delim = ", "
                file2.print(f"({param.get_type().get_type_str()})")
                file2.print("par" + str(num))
                file2.print(param.get_type().get_type_str_post())
                num += 1

            file2.print(");\n")

            if not b_void:
                file2.print(f"\n    return {retval_return};\n")
            file2.print("}\n\n")

            file2.close()

            file2 = AppFile.open(f"{gen}/tecsgen.cfg")
            file2.print("\n/* Generated by HRP2SVCPlugin */\n\n")
            # TODO: スタックサイズは適当
            file2.print(
                "KERNEL_DOMAIN{\n"
                f"    DEF_SVC( {to_s(svcid)}, {{ TA_NULL, {body}_{fname}, 256 }} );\n"
                "}\n"
            )
            file2.close()

            file2 = AppFile.open(f"{gen}/{body}_factory.h")
            file2.print("\n/* Generated by HRP2SVCPlugin */\n\n")
            file2.print(
                f"extern ER_UINT {body}_{fname}(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);\n"
            )
            file2.close()
