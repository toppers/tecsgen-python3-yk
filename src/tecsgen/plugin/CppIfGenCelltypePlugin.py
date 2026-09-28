"""CppIfGenCelltypePlugin.rb の移植。C++ から受け口関数を呼ぶための `<ct>_cppif.hpp`・`<sig>_cppif.hpp` を生成する。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import Y, to_s


class CppIfGenCelltypePlugin(CelltypePlugin):
    CLASS_NAME_SUFFIX = ""
    _b_signature_header_generated: ClassVar[bool] = False

    @classmethod
    def reset(cls) -> None:
        """`@@b_signature_header_generated` を初期化する（1プロセスで何度も実行するテスト用）。"""
        CppIfGenCelltypePlugin._b_signature_header_generated = False

    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        self._cell_list: list[Any] = []

    def new_cell(self, cell: Any) -> None:
        self._cell_list.append(cell)

    def gen_factory(self, file: Any) -> None:
        """tCelltype_factory.h の代わりに `<ct>_cppif.hpp` を生成する（引数の file は使わない）。"""
        from tecsgen.context import get_context
        from tecsgen.core.cdl_types import VoidType
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.plugin import CFile

        ct = self._celltype
        gn = to_s(ct.get_global_name())
        ct_name = to_s(ct.get_name())

        if not ct.is_singleton():
            idx_def = f"CPP_{gn}_IDX idx_"
            idx_ini = ":cpp_idx( idx_ )"
            cpp_idx = "cpp_idx"
            idx2 = "cpp_idx.idx"
            idx_ = "idx_"
            delim_ini = ", "
        else:
            idx_def = ""
            idx_ini = ""
            cpp_idx = ""
            idx2 = ""
            idx_ = ""
            delim_ini = ""

        # シグニチャヘッダを生成する（最初に呼び出されたときに、一度だけ、すべて生成する）
        if CppIfGenCelltypePlugin._b_signature_header_generated is not True:
            CppIfGenCelltypePlugin._b_signature_header_generated = True
            self.gen_namespace_signature_header(Namespace.get_root())

        f = CFile.open(f"{get_context().gen}/{gn}_cppif.hpp", "w")
        f.print(
            f"#ifndef {gn.upper()}_CPPIF_HPP\n"
            f"#define {gn.upper()}_CPPIF_HPP\n"
            "\n"
            "/*\n"
            " * This file is intended to be included in non-TECS celltype code and in C++ code.\n"
            " */\n"
        )
        # Ruby 版は TOPPERS_CB_TYPE_ONLY の定義・解除部分を dummy 変数に入れて出力していない
        f.print(f'#include "{gn}_tecsgen.h"\n')

        # signature ヘッダをインクルード
        b_gen = False
        for port in ct.get_port_list():
            if port.get_port_type() == Y.ENTRY:
                f.print(
                    f'#include "{to_s(port.get_signature().get_global_name())}_cppif.hpp"\n'
                )
                b_gen = True
        if b_gen:
            f.print("\n")

        if not ct.is_singleton():
            # シングルトンの場合 IDX は不要
            f.print(
                "/*\n"
                " * Cell IDX type for Cpp\n"
                " */\n"
                "typedef struct  {\n"
                f"    {gn}_IDX idx;\n"
                f"}} CPP_{gn}_IDX;\n"
                "\n"
                "/*\n"
                f" * Cell IDX macros in celltype '{ct_name}'\n"
                f" *   type of the macro value is {ct_name}_IDX.\n"
                ' *   macro name is (cell name) + "_IDX"\n'
                " */\n"
            )
            for cell in ct.get_cell_list():
                if cell.is_generate():
                    name_array = ct.get_name_array(cell)
                    idx_real = to_s(name_array[7]) if not ct.is_singleton() else ""
                    cgn = to_s(cell.get_global_name())
                    f.print(
                        f"inline CPP_{gn}_IDX CPP_{cgn}_IDX__()\n"
                        "{\n"
                        f"    CPP_{gn}_IDX cpp_idx = {{ {idx_real} }};\n"
                        "    return cpp_idx;\n"
                        "}\n"
                        f"#define {cgn}_IDX  CPP_{cgn}_IDX__()\n"
                    )

        cell_sample = None
        for cell in ct.get_cell_list():
            if cell.is_generate():
                cell_sample = cell
                break
        cell_sample_name = (
            to_s(cell_sample.get_name()) if cell_sample is not None else "Cell"
        )

        for port in ct.get_port_list():
            if port.get_port_type() == Y.ENTRY:
                fhs = port.get_signature().get_function_head_array()
                if len(fhs) > 0:
                    func_1st = fhs[0]
                    if not ct.is_singleton():
                        cell_idx = "( Cell_IDX );"
                        cell_idx2 = (
                            f"({to_s(ct.get_cell_list()[0].get_global_name())}_IDX);"
                        )
                    else:
                        cell_idx = ";     // don't put empty parenthesis for singleton"
                        cell_idx2 = ";"
                    f.print(
                        "\n"
                        "/*-------------- begin: use sample ------------\n"
                        " * Define variable for Cell with Cnstructor\n"
                        f" *   tCelltypeName    CellNameInCpp{cell_idx}\n"
                        f" *   ex) {gn}     {cell_sample_name}{cell_idx2}\n"
                        " *\n"
                        " * Call member function\n"
                        " *   CellNameInCpp.eEntryName.FunctionName( parameters... );\n"
                        f" *   ex) {cell_sample_name}.{to_s(port.get_name())}.{to_s(func_1st.get_name())}( parameters... );\n"
                        " *-------------- end:   use sample ------------*/\n"
                        "\n"
                    )
                    break

        f.print(
            "/*\n"
            " * C++ interface code\n"
            f" *   This class comes from celltype '{ct_name}'.\n"
            " */\n"
            f"class {gn} {{\n"
        )

        for port in ct.get_port_list():
            pn = to_s(port.get_name())
            if port.get_port_type() == Y.ENTRY:
                sig = port.get_signature()
                sgn = to_s(sig.get_global_name())
                if port.get_array_size() is not None:
                    subsc_def = "int_t subscript_"
                    delim = delim_ini
                else:
                    subsc_def = ""
                    delim = ""
                f.print(
                    f"    /* class for entry {sgn} {pn} */\n"
                    f"    class {pn}_ : public {sgn}{{\n"
                    "        public : \n"
                    "        /* constructor: internal use only */\n"
                    f"        {pn}_({idx_def}{delim}{subsc_def});\n"
                    "        /* destructor */\n"
                    f"        // ~{pn}_();   unnecessary\n"
                    "    \n"
                    f"        /* {to_s(sig.get_name())} functions */\n"
                )
                for fh in sig.get_function_head_array():
                    f.print(
                        f"        {fh.get_return_type().get_type_str()} {to_s(fh.get_name())}( "
                    )
                    delim = ""
                    for param in fh.get_paramlist().get_items():
                        f.print(
                            f"{delim}{param.get_type().get_type_str()} {to_s(param.get_name())}"
                            f"{param.get_type().get_type_str_post()}"
                        )
                        delim = ", "
                    f.print(" );\n")
                f.print("\n")
                if not ct.is_singleton():
                    f.print(f"        private:\n        CPP_{gn}_IDX cpp_idx;\n")
                # entry port array
                if port.get_array_size() is not None:
                    f.print("        private:\n        int_t  subscript;\n")
                f.print("    };\n")
            # entry port array
            if port.get_array_size() is not None:
                f.print(
                    f"    class {pn}_EA{{\n"
                    "        public : \n"
                    "        /* constructor: internal use only */\n"
                    f"        {pn}_EA({idx_def});\n"
                    "        /* destructor */\n"
                    f"        // ~{pn}_();   unnecessary\n"
                    "\n"
                    f"        {pn}_ operator[]( int_t subscript ) const; \n"
                )
                if not ct.is_singleton():
                    f.print(f"        private:\n        CPP_{gn}_IDX cpp_idx;\n")
                f.print("    };\n")

        f.print(
            "\n"
            "    /*--------  begin public ----------*/\n"
            "    public:\n"
            "    /* constructor */\n"
            f"    {ct_name}( {idx_def} );\n"
            "    /* destructor */\n"
            f"    // ~{ct_name}();   unnecessary\n"
            "\n"
        )
        for port in ct.get_port_list():
            entry_array = "EA" if port.get_array_size() is not None else ""
            pn = to_s(port.get_name())
            f.print(
                f"    /* entry {to_s(port.get_signature().get_global_name())} {pn} */\n"
                f"    {pn}_{entry_array} {pn}; \n"
            )
        f.print("    /*--------  end public ----------*/\n};\n")

        f.print(
            "\n"
            "/*-------------- begin: implementation (I/F code only) ----------------*/\n"
            "/* constructor  */\n"
        )
        f.print(f"inline    {gn}::{gn}({idx_def}) : ")
        delim = ""
        for port in ct.get_port_list():
            if port.get_port_type() == Y.ENTRY:
                f.print(f"{delim}{to_s(port.get_name())}({idx_})")
                delim = ", "
        f.print("{}\n\n")

        for port in ct.get_port_list():
            pn = to_s(port.get_name())
            if port.get_array_size() is not None:
                subsc_def = "int_t subscript_"
                subsc_ini = "subscript(subscript_)"
                if idx_ini == "":
                    subsc_ini = ":" + subsc_ini
                delim = delim_ini
            else:
                subsc_def = ""
                subsc_ini = ""
                delim = ""
            f.print(
                f"/* ------------- entry port: {pn} ------------------*/\n"
                "/* constructor: internal use only */\n"
                f"inline    {gn}::{pn}_::{pn}_( {idx_def}{delim}{subsc_def} ) {idx_ini}{delim}{subsc_ini}{{}}\n"
                "\n"
                f"/* entry {pn} functions */\n"
            )
            for fh in port.get_signature().get_function_head_array():
                fn = to_s(fh.get_name())
                cr = "\n" if len(f"{gn}::{pn}_::{fn}") >= 32 else ""
                f.print(
                    f"inline {fh.get_return_type().get_type_str()} {gn}::{pn}_::{fn}( "
                )
                delim = ""
                for param in fh.get_paramlist().get_items():
                    f.print(
                        f"{delim}{param.get_type().get_type_str()} {to_s(param.get_name())}"
                        f"{param.get_type().get_type_str_post()}"
                    )
                    delim = ", "
                f.print(f" ){cr}{{ ")
                if not isinstance(fh.get_return_type(), VoidType):
                    f.print("return ")
                delim = delim_ini
                f.print(f"{gn}_{pn}_{fn}( {idx2}")
                if port.get_array_size() is not None:
                    f.print(f"{delim}subscript")
                    delim = ", "
                for param in fh.get_paramlist().get_items():
                    f.print(f"{delim}{to_s(param.get_name())}")
                    delim = ", "
                f.print(f" ); }}\n{cr}")
            if port.get_array_size() is not None:
                f.print(
                    "/* constructor for entry array (internal use only)*/\n"
                    f"inline  {gn}::{pn}_EA::{pn}_EA( {idx_def} ){idx_ini}{{}}\n"
                    "/* operator[] */\n"
                    f"inline  {gn}::{pn}_ {gn}::{pn}_EA::operator[]( int_t subscript ) const\n"
                    "{\n"
                    "    /*\n"
                    "     * subscript is not checked here. No way to return error.\n"
                    "     */\n"
                    f"    return {gn}::{pn}_({cpp_idx}{delim_ini}subscript);\n"
                    "};\n"
                    "\n"
                )
        # undef macros
        ct.gen_ph_undef(f)
        f.print(
            "/*-------------- end: implementation (I/F code only) ----------------*/\n"
            "\n"
            f"#endif /* {gn.upper()}_CPPIF_HPP */\n"
        )
        f.close()

    def gen_namespace_signature_header(self, ns: Any) -> None:
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        suffix = CppIfGenCelltypePlugin.CLASS_NAME_SUFFIX
        for sig in ns.get_signature_list():
            sgn = to_s(sig.get_global_name())
            f = CFile.open(f"{get_context().gen}/{sgn}_cppif.hpp", "w")
            f.print(
                f"#ifndef {sgn.upper()}_CPPIF_HPP\n"
                f"#define {sgn.upper()}_CPPIF_HPP\n"
                "/*\n"
                " * C++ interface code\n"
                f" *   This class comes from signature '{to_s(sig.get_name())}{suffix}'.\n"
                " *   All functions are pure virtual. These are defined in celltype class.\n"
                " */\n"
                " \n"
                " /* */\n"
                f" class {sgn}{suffix} {{\n"
                "    public:\n"
            )
            for fh in sig.get_function_head_array():
                f.print(
                    f"    virtual {fh.get_return_type().get_type_str()} {to_s(fh.get_name())}( "
                )
                delim = ""
                for param in fh.get_paramlist().get_items():
                    f.print(
                        f"{delim}{param.get_type().get_type_str()} {to_s(param.get_name())}"
                        f"{param.get_type().get_type_str_post()}"
                    )
                    delim = ", "
                f.print(" ) = 0;\n")
            f.print(f"}};\n\n#endif /* {sgn.upper()}_CPPIF_HPP */\n")
            f.close()

        # 子ネームスペース
        for subns in ns.get_namespace_list():
            self.gen_namespace_signature_header(subns)
