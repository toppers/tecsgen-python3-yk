"""test/restrict/MyTracePlugin.rb の Python 版。

Ruby 版は TracePlugin.rb の複製で、`gen_ep_func_body` だけが異なる（restrict の検査結果を
`callable from … = true/false` として標準出力に出す。Enter/Leave の syslog にも添字を付けない）。
複製ではなく TracePlugin の子クラスにする。クラス名が違うので、生成するセルタイプは
`tMyTracePlugin_…` になる。
"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.TracePlugin import TracePlugin
from tecsgen.ruby_compat import Y, rb_print, to_s


class MyTracePlugin(TracePlugin):
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
        ret_type = func_type.get_type()
        b_ret_void = ret_type.is_void()

        if not b_ret_void:
            file.print(f"\t{ret_type.get_type_str()}\tretval;\n")

        file.print("\tSYSUTM\tutime;\n")

        if not b_singleton:
            file.print(
                f"\t{to_s(ct_name)}_CB *p_cellcb;\n"
                "\tif( VALID_IDX( idx ) ){\n"
                f"\t\tp_cellcb = {to_s(global_ct_name)}_GET_CELLCB(idx);\n"
                "\t}else{\n"
                "\t\t/* put code here for error */\n"
                "\t}\n\n"
            )

        # ------------- check restrict ---------#
        rb_print(
            f"callable from {to_s(self._caller_cell.get_namespace_path())} "
            f"to {to_s(self._callee_cell.get_namespace_path())}."
            f"{to_s(self._join.get_port_name())}.{to_s(func_name)} "
            f"= {to_s(self._caller_cell.callable(self._callee_cell, self._join.get_port_name(), func_name))}\n"
        )

        file.print(
            "\tgetMicroTime( &utime );\n"
            f'\tsyslog( LOG_INFO, "Enter: %sTime=%d: {to_s(self._next_cell.get_name())}.'
            f'{to_s(self._next_cell_port_name)}.{to_s(func_name)} calledFrom: %s", '
            "ATTR_probeName_str, utime, ATTR_from_str );\n"
        )

        self.print_params(params, file, 0, Y.IN)

        delim = ""
        if not b_ret_void:
            file.print("\tretval = ")
        else:
            file.print("\t")

        file.print(f"{to_s(self._call_port_name)}_{to_s(func_name)}(")

        for param in params:
            file.printf(f"{delim} {to_s(param.get_name())}")
            delim = ","
        file.print(" );\n")

        file.print(
            "\tgetMicroTime( &utime );\n"
            f'\tsyslog( LOG_INFO, "Leave: %sTime=%d: {to_s(self._next_cell.get_name())}.'
            f'{to_s(self._next_cell_port_name)}.{to_s(func_name)}", '
            "ATTR_probeName_str, utime );\n"
        )

        self.print_params(params, file, 0, Y.OUT)

        if not b_ret_void:
            self.print_param(
                "retval",
                ret_type,
                file,
                0,
                Y.RETURN,
                ret_type.get_type_str(),
                None,
                None,
            )
            file.print("\treturn retval;\n")
