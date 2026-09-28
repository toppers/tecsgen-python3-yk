"""CIfGenCelltypePlugin.rb の移植。非 TECS の C コードから受け口関数を呼ぶための `<ct>_cif.h` を生成する。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import Y, to_s


class CIfGenCelltypePlugin(CelltypePlugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        self._cell_list: list[Any] = []

    def new_cell(self, cell: Any) -> None:
        self._cell_list.append(cell)

    def gen_factory(self, file: Any) -> None:
        """tCelltype_factory.h の代わりに `<ct>_cif.h` を生成する（引数の file は使わない）。"""
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        ct = self._celltype
        gn = to_s(ct.get_global_name())
        f = CFile.open(f"{get_context().gen}/{gn}_cif.h", "w")

        f.print(
            f"#ifndef {gn.upper()}_H\n"
            f"#define {gn.upper()}_H\n"
            "\n"
            "/*\n"
            " * This header file is intedned to be included in non-TECS celltype code.\n"
            " * Don not include in celltype code.\n"
            " * Mutiple *_cif.h files can be included non-TECS celltype code.\n"
            " */\n"
            "\n"
            "/* include celltype definition header */\n"
            "#ifndef TOPPERS_CB_TYPE_ONLY\n"
            "#define TOPPERS_CB_TYPE_ONLY\n"
            f"#define TOPPERS_CB_TYPE_ONLY_defined_{gn}_CIF_H\n"
            "#endif\n"
            "\n"
            f'#include "{gn}_tecsgen.h"\n'
            "\n"
            f"#ifdef TOPPERS_CB_TYPE_ONLY_defined_{gn}_CIF_H\n"
            "#undef TOPPERS_CB_TYPE_ONLY\n"
            f"#undef TOPPERS_CB_TYPE_ONLY_defined_{gn}_CIF_H\n"
            "#endif\n"
            "\n"
            "/**/\n"
        )

        for cell in ct.get_cell_list():
            if not cell.is_generate():
                continue
            f.print(f"\n/*** cell: {to_s(cell.get_name())} ***/\n")
            name_array = ct.get_name_array(cell)
            for port in ct.get_port_list():
                if port.get_port_type() == Y.ENTRY:
                    if port.get_array_size() is not None:
                        subsc = "subscript"
                        delim_subsc = ", "
                    else:
                        subsc = ""
                        delim_subsc = ""
                    f.print(f"/** port: {to_s(port.get_name())} **/\n")
                    for fh in port.get_signature().get_function_head_array():
                        pn = to_s(port.get_name())
                        fn = to_s(fh.get_name())
                        f.print(f"/* funcition: {fn} */\n")
                        f.print(
                            f"#define {to_s(cell.get_global_name())}_{pn}_{fn}( {subsc}"
                        )
                        delim = delim_subsc
                        for param in fh.get_paramlist().get_items():
                            f.print(f"{delim}{to_s(param.get_name())}")
                            delim = ", "
                        f.print(" ) \\\n        ")
                        f.print(f"{gn}_{pn}_{fn}( ")
                        if ct.is_singleton():
                            delim = ""
                        else:
                            f.print(to_s(name_array[7]))  # cell_IDX
                            delim = ", "
                        f.print(f"{delim}{subsc}")
                        delim = delim_subsc
                        for param in fh.get_paramlist().get_items():
                            f.print(f"{delim}{to_s(param.get_name())}")
                            delim = ", "
                        f.print(" )\n")
                f.print("\n")
        f.print(f"#endif /* {gn.upper()}_H */\n")
        f.close()
