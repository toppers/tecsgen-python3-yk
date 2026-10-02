"""test/SWIGBridge/SWIGBridgePlugin.rb の Python 版（SWIG を使って Ruby ⇒ TECS コンポーネントを生成するシグニチャプラグイン）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.core.cdl_types import VoidType
from tecsgen.core.componentobj.namespace import Namespace
from tecsgen.core.generator import Generator
from tecsgen.core.plugin import CFile
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import Y, sym, to_s


class SWIGBridgePlugin(SignaturePlugin):
    # クラス変数（このファイルは実行回ごとに読み直すので、実行ごとに空から始まる）
    _instances: ClassVar[
        dict[Any, list[Any]]
    ] = {}  # @signature => [ インスタンスの配列 ]
    _b_written = False  # ファイル .i, .cxx, .hxx 出力済み

    def __init__(self, signature: Any, option: Any) -> None:
        super().__init__(signature, option)

        def check(func_decl: Any, param_decl: Any) -> None:
            if param_decl.get_direction() in (Y.INOUT, Y.OUT, Y.SEND, Y.RECEIVE):
                Generator.error(
                    f"{to_s(param_decl.get_direction()).lower()} parameter cannot be used in Ruby Bridge"
                )

        signature.each_param(check)
        self._celltype_name = f"tSWIG{to_s(self._signature.get_name())}Bridge"
        self._class_name = f"C{to_s(self._signature.get_name())}"
        instances = SWIGBridgePlugin._instances
        if instances.get(signature):
            instances[signature].append(self)
        else:
            instances[signature] = [self]

    def gen_cdl_file(self, file: Any) -> None:
        """ブリッジセルタイプの生成。"""
        file.print(
            "/// Ruby ⇒ TECS ブリッジセルタイプ ///\n"
            "[idx_is_id]\n"
            f"celltype {self._celltype_name} {{\n"
            f"    call {to_s(self._signature.get_name())} cTECS;\n"
            "};\n"
        )

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """受け口関数の postamble (C言語)を生成する。"""
        cls = SWIGBridgePlugin
        # mikan namespace
        ct = Namespace.find(["::", ct_name])
        self.gen_cxx(ct)
        self.gen_hxx(ct)
        if not cls._b_written:
            cls._b_written = True
            for instances in cls._instances.values():
                ct = Namespace.find(["::", sym(instances[0].get_celltype_name())])
                instances[0].gen_i(ct)

    def gen_cxx(self, ct: Any) -> None:
        file = CFile.open(f"{get_context().gen}/{self._class_name}.cxx", "w")
        cn = self._class_name

        file.print(
            "#include  <stdlib.h>\n"
            "#include  <memory.h>\n"
            "#include  <stdio.h>\n"
            f'#include  "{self._celltype_name}_tecsgen.h"\n'
            f'#include  "{cn}.hxx"\n'
            "\n"
        )

        for cell in ct.get_cell_list():
            if cell.is_generate():
                file.print(
                    f'char    CELL_{to_s(cell.get_name())}[] = "{to_s(cell.get_name())}";\n'
                )

        file.print("struct tagName2ID { char *name; ID id; } Name2ID[] = {\n")
        for cell in ct.get_cell_list():
            if cell.is_generate():
                file.print(
                    f"    {{ CELL_{to_s(cell.get_name())}, {to_s(cell.get_id())} }},\n"
                )

        file.print(
            "    { (char*)0, 0 }\n"
            "};\n"
            "\n"
            f"{cn} *\n"
            f"{cn}::join( const char *CellName )\n"
            "{\n"
            f"\t{cn} *cell = new {cn}( CellName );\n"
            "\treturn cell;\n"
            "}\n"
            "\n"
            f"{cn}::{cn}( const char *CellName )\n"
            "{\n"
            "    m_CellName = (char *)malloc( strlen( CellName ) + 1 );\n"
            "    if( m_CellName )\n"
            "       strcpy( m_CellName, CellName );\n"
            "    else\n"
            "       m_CellName = 0;\n"
            "\n"
            "    int   i;\n"
            "    for( i = 0; Name2ID[i].name; i++ )\n"
            "        if( strcmp( CellName, Name2ID[i].name ) == 0 )\n"
            "             break;\n"
            "\n"
            "    if( Name2ID[i].name )\n"
            "         m_id = Name2ID[i].id;\n"
            "    else\n"
            "         m_id = 0;\n"
            "}\n"
            "\t\n"
            f"{cn}::~{cn}()\n"
            "{\n"
            "    if( m_CellName )\n"
            "        free( m_CellName );\n"
            "    m_CellName = 0;\n"
            "    m_id = 0;\n"
            "}\n"
            "\n"
        )

        for fh in self._signature.get_function_head_array():  # fh: FuncHead
            fd = fh.get_declarator()  # fd: Decl (ここで fd が関数以外のことはない)
            ft = fd.get_type()  # ft: FuncType
            ret_type = ft.get_type()

            # 関数頭部の出力
            file.print(f"{ft.get_type_str()}\n{cn}::{to_s(fd.get_name())}(")
            delim = ""
            for p in ft.get_paramlist().get_items():  # p: ParamDecl
                # size_is, count_is, string, send, receive には対応しない
                pd = p.get_declarator()  # pd: Decl
                file.print(
                    f"{delim} {pd.get_type().get_type_str()} {to_s(pd.get_name())}"
                    f"{pd.get_type().get_type_str_post()}"
                )
                delim = ", "
            file.print(" )\n{\n")

            # 戻り値を記憶する変数の定義を出力
            if isinstance(ret_type.get_original_type(), VoidType):
                retval = ""
                retnul = ""
            else:
                file.print(
                    f"\t{ft.get_type().get_type_str()}\tretval{ft.get_type().get_type_str_post()};\n"
                )
                retval = "retval = "
                retnul = "0"

            file.print(
                "    if( ! VALID_IDX( m_id ) )\n"
                f"         return {retnul};\n"
                "    CELLCB *p_cellcb = (CELLCB*)GET_CELLCB( m_id );\n"
            )

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

        file.close()

    def gen_hxx(self, ct: Any) -> None:
        file = CFile.open(f"{get_context().gen}/{self._class_name}.hxx", "w")
        self.gen_class(file)
        file.close()

    def gen_i(self, ct: Any) -> None:
        file = CFile.open(f"{get_context().gen}/SWIGBridge.i", "w")
        instances = SWIGBridgePlugin._instances

        file.print(
            '%module SWIGBridge\n%{\n#include <stdint.h>\n#include "global_tecsgen.h"\n'
        )

        # Ruby 版は、ループの中でも self の @class_name を使う（インスタンスごとの名前ではない）
        for _signature in instances:
            file.print(f'#include "{self._class_name}.hxx"\n')

        file.print(
            "%}\n"
            "\n"
            "typedef  int int_t;\n"
            "typedef  char char_t;\n"
            "%import stdint.h\n"
            "%import global_tecsgen.h\n"
        )

        for plugins in instances.values():
            plugins[0].gen_class(file)
        file.close()

    def gen_class(self, file: Any) -> None:
        cn = self._class_name
        file.print(
            f"class {cn} {{\npublic:\n    static {cn} *join( const char *CellName );\n"
        )

        for fh in self._signature.get_function_head_array():  # fh: FuncHead
            fd = fh.get_declarator()
            ft = fd.get_type()

            # 関数頭部の出力
            file.print(f"    {ft.get_type_str()} {to_s(fd.get_name())}(")
            delim = ""
            for p in ft.get_paramlist().get_items():
                pd = p.get_declarator()
                file.print(
                    f"{delim} {pd.get_type().get_type_str()} {to_s(pd.get_name())}"
                    f"{pd.get_type().get_type_str_post()}"
                )
                delim = ", "
            file.print(" );\n")

        file.print(
            "\n"
            "private:\n"
            f"    {cn}( const char *CellName );\n"
            f"    {cn}();\n"
            f"    ~{cn}();\n"
            "\n"
            "    ID    m_id;\n"
            "    char  *m_CellName;\n"
            "};\n"
            "\n"
        )

    def get_celltype_name(self) -> Any:
        return self._celltype_name
