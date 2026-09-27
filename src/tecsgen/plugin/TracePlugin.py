"""TracePlugin.rb の移植（内部仕様9章）。呼び口の呼び出しを syslog へトレース出力する through プラグイン。"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.core.cdl_types import (
    ArrayType,
    BoolType,
    DefinedType,
    EnumType,
    FloatType,
    FuncType,
    IntType,
    PtrType,
    StructType,
    VoidType,
)
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import Y, sym, to_s, truthy


class TracePlugin(ThroughPlugin):
    """@cellEntry_list:: [ "Cell.eEntry", "Cell2.eEntry2", ... ]
    @b_generate:: bool   true : TracePlugin を生成する必要がある
    """

    TRACE_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

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
        """説明は ThroughPlugin (plugin.rb) を参照。"""
        self._max_array_display = 16
        self._cell_entry_list: list[str] = []
        self._probe_name = ""
        self._b_generate = False
        self._b_display_time = False
        self._kernel_celltype = sym("tKernel")
        self._syslog_celltype = sym("tSysLog")

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
        self._plugin_arg_check_proc_tab = TracePlugin.TRACE_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

        if len(self._cell_entry_list) > 0:
            for ce in self._cell_entry_list:
                if f"{to_s(next_cell.get_name())}.{to_s(next_cell_port_name)}" == to_s(
                    ce
                ):
                    self._b_generate = True
        else:
            self._b_generate = True

        if self._b_generate is False:
            # 元々呼び出すセルに結合するものとする
            self._entry_port_name = next_cell_port_name
            self._cell_name = next_cell.get_name()

    def gen_plugin_decl_code(self, file: Any) -> None:
        """宣言コードの生成。typedef, signature, celltype など（cell 以外）のコードを生成する。

        重複して生成してはならない（すでに生成されている場合は出力しないこと）。
        """
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if TracePlugin._generated_celltype.get(self._ct_name) is None:
            TracePlugin._generated_celltype[self._ct_name] = [self]
        else:
            TracePlugin._generated_celltype[self._ct_name].append(self)
            return

        gen_dir = get_context().gen
        file2 = CFile.open(f"{gen_dir}/{to_s(self._ct_name)}.cdl", "w")

        send_receive: list[tuple[Any, Any, Any]] = []
        if self._signature is not None:

            def collect(fd: Any, param: Any) -> None:
                d = param.get_direction()
                if d in (Y.SEND, Y.RECEIVE):
                    send_receive.append((d, fd, param))

            self._signature.each_param(collect)

        file2.print(f"celltype {to_s(self._ct_name)} {{\n")

        if len(send_receive) > 0:
            file2.print("  [ allocator(\n")
            delim = ""
            for _d, fd, param in send_receive:
                file2.print(
                    f"{delim}\t{to_s(fd.get_name())}.{to_s(param.get_name())}<="
                    f"{to_s(self._call_port_name)}.{to_s(fd.get_name())}.{to_s(param.get_name())}"
                )
                delim = ",\n"
            file2.print("\n  )]\n")

        file2.print(
            f"  entry {to_s(self._signature.get_namespace_path())} {to_s(self._entry_port_name)};\n"
            f"  call  {to_s(self._signature.get_namespace_path())} {to_s(self._call_port_name)};\n"
            "  attr{\n"
            '    char_t   *probeName_str      = "";\n'
            '    char_t   *from_str           = "";\n'
            "  };\n"
            f"  require  {to_s(self._syslog_celltype)}.eSysLog;\n"
            f"  require  {to_s(self._kernel_celltype)}.eKernel;\n"
            "};\n"
        )
        file2.close()

        file.print(f'import( "{gen_dir}/{to_s(self._ct_name)}.cdl" );\n')

    def gen_through_cell_code(self, file: Any) -> None:
        self.gen_plugin_decl_code(file)

        if self._b_generate is not False:
            nest = self._region.gen_region_str_pre(file)
            indent_str = "  " * nest
            subscript = (
                f"[{to_s(self._next_cell_port_subscript)}]"
                if truthy(self._next_cell_port_subscript)
                else ""
            )

            probe_name_str = (
                f'{indent_str}  probeName_str = "{self._probe_name}: ";\n'
                if truthy(self._probe_name)
                else ""
            )
            caller_cell_str = (
                f'{indent_str}  from_str = "{to_s(self._caller_cell.get_name())}";\n'
                if truthy(self._caller_cell)
                else ""
            )

            file.print(
                f"{indent_str}cell {to_s(self._ct_name)} {to_s(self._cell_name)} {{\n"
                f"{indent_str}  {to_s(self._call_port_name)} = "
                f"{self._next_cell.get_namespace_path().get_path_str()}."
                f"{to_s(self._next_cell_port_name)}{subscript};\n"
                f"{probe_name_str}{caller_cell_str}{indent_str}}};\n"
            )
            self._region.gen_region_str_post(file)

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

        subscript = (
            f"[{to_s(self._next_cell_port_subscript)}]"
            if truthy(self._next_cell_port_subscript)
            else ""
        )

        file.print(
            "\tgetMicroTime( &utime );\n"
            f'\tsyslog( LOG_INFO, "Leave: %sTime=%d: {to_s(self._next_cell.get_name())}.'
            f'{to_s(self._next_cell_port_name)}{subscript}.{to_s(func_name)}", '
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

    def print_params(
        self, params: list[Any], file: Any, nest: int, direction: Any
    ) -> None:
        for param in params:
            dir_ = param.get_direction()
            if direction == Y.IN:
                if dir_ in (Y.IN, Y.INOUT, Y.SEND):
                    self.print_param(
                        param.get_name(),
                        param.get_type(),
                        file,
                        nest,
                        dir_,
                        param.get_type().get_type_str(),
                        None,
                        None,
                    )
            else:
                if dir_ in (Y.OUT, Y.INOUT):
                    self.print_param(
                        param.get_name(),
                        param.get_type(),
                        file,
                        nest,
                        dir_,
                        param.get_type().get_type_str(),
                        None,
                        None,
                    )
                elif dir_ == Y.RECEIVE:
                    referto = param.get_type().get_referto()
                    self.print_param(
                        param.get_name(),
                        referto,
                        file,
                        nest,
                        dir_,
                        referto.get_type_str(),
                        "*",
                        None,
                    )

    def print_param(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        direction: Any,
        type_str: str,
        outer: str | None,
        outer2: str | None,
        name_list: Any = None,
    ) -> None:
        indent = "    " * (nest + 1)
        o = outer or ""
        o2 = outer2 or ""

        if isinstance(type_, DefinedType):
            self.print_param(
                name,
                type_.get_type(),
                file,
                nest,
                direction,
                type_str,
                outer,
                outer2,
                name_list,
            )
        elif isinstance(type_, VoidType):
            pass
        elif isinstance(type_, BoolType):
            file.print(
                f'{indent}syslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                f'{o}{to_s(name)}{o2} = %d;", {o}{to_s(name)}{o2} );\n'
            )
        elif isinstance(type_, IntType):
            file.print(
                f"{indent}if( sizeof({o}{to_s(name)}{o2}) > sizeof(int_t) )\n"
                f'{indent}\tsyslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                f'{o}{to_s(name)}{o2} = %ld;", (long){o}{to_s(name)}{o2} );\n'
                f"{indent}else\n"
                f'{indent}\tsyslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                f'{o}{to_s(name)}{o2} = %d;", {o}{to_s(name)}{o2} );\n'
            )
        elif isinstance(type_, FloatType):
            file.print(
                f'{indent}syslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                f'{o}{to_s(name)}{o2} = %g;", (double){o}{to_s(name)}{o2} );\n'
            )
        elif isinstance(type_, EnumType):
            pass  # mikan EnumType
        elif isinstance(type_, StructType):
            members_decl = type_.get_members_decl()
            outer_m = (
                f"({o}{to_s(name)}{o2})." if (outer or outer2) else f"{to_s(name)}."
            )
            for m in members_decl.get_items():
                self.print_param(
                    m.get_name(),
                    m.get_type(),
                    file,
                    nest,
                    direction,
                    m.get_type().get_type_str(),
                    outer_m,
                    None,
                    members_decl,
                )
        elif isinstance(type_, FuncType):
            pass  # mikan FuncType
        elif isinstance(type_, ArrayType):
            pass  # mikan ArrayType
        elif isinstance(type_, PtrType):
            self._print_param_ptr(
                name, type_, file, nest, direction, outer, outer2, name_list, indent
            )

    def _print_param_ptr(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        direction: Any,
        outer: str | None,
        outer2: str | None,
        name_list: Any,
        indent: str,
    ) -> None:
        se = type_.get_size()
        ce = type_.get_count()
        max_loop = self._max_array_display
        loop_count = None
        size = None
        o = outer or ""
        o2 = outer2 or ""

        if truthy(se):
            se_str = se.to_str(name_list, outer, outer2)
            loop_count = f"((({se_str})>{max_loop}) ? {max_loop} : ({se_str}))"
            file.print(
                f'{indent}syslog( LOG_INFO, "{indent}size_is({se_str})=%d", {se_str} );\n'
            )
            size = se_str
        elif truthy(ce):
            ce_str = ce.to_str(name_list, outer, outer2)
            loop_count = f"((({ce_str})>{max_loop}) ? {max_loop} : ({ce_str})) "
            file.print(
                f'{indent}syslog( LOG_INFO, "{indent}count_is({ce_str})=%d", {ce_str} );\n'
            )
            size = ce_str

        # mikan PtrType: string
        referto = type_.get_referto()
        type0 = type_
        typ = referto
        type_str = typ.get_type_str()
        if isinstance(typ, DefinedType):
            typ = typ.get_original_type()

        indent0 = indent
        outer0 = outer
        outer20 = outer2
        if type0.is_nullable():
            nest += 1
            indent = indent + "    "
            file.print(f"{indent0}if( {o}{to_s(name)}{o2} ){{\n")

        if loop_count is None:
            if isinstance(typ, StructType):
                members = typ.get_members_decl()
                outer_s = (
                    f"({o}{to_s(name)}{o2})->"
                    if (outer or outer2)
                    else f"{to_s(name)}->"
                )
                for m in members.get_items():
                    self.print_param(
                        m.get_name(),
                        m.get_type(),
                        file,
                        nest,
                        direction,
                        m.get_type().get_type_str(),
                        outer_s,
                        None,
                        members,
                    )
            elif isinstance(typ, (FuncType, ArrayType)):
                pass  # mikan
            elif isinstance(typ, (BoolType, IntType, FloatType, EnumType, PtrType)):
                self.print_param(
                    name, typ, file, nest, direction, type_str, f"*{o}", o2, name_list
                )
        else:  # loop_count is not None
            num_per_loop = 1 if isinstance(typ, (PtrType, StructType)) else 4

            file.print(
                f"{indent}{{\n"
                f"{indent}\tint i__{nest}, loop_count__ = {loop_count};\n"
                f"{indent}\tfor( i__{nest} = 0; i__{nest} < loop_count__; i__{nest}+={num_per_loop} ){{\n"
            )

            if isinstance(typ, StructType):
                members = typ.get_members_decl()
                outer_s = (
                    f"({o}{to_s(name)}{o2})[i__{nest}]."
                    if (outer or outer2)
                    else f"{to_s(name)}[i__{nest}]."
                )
                for m in members.get_items():
                    self.print_param(
                        m.get_name(),
                        m.get_type(),
                        file,
                        nest + 1,
                        direction,
                        m.get_type().get_type_str(),
                        outer_s,
                        None,
                        members,
                    )
            elif isinstance(typ, (FuncType, ArrayType)):
                pass  # mikan
            elif isinstance(typ, (BoolType, FloatType)):
                oo, oo2 = (f"({o}", f"{o2})") if (outer or outer2) else (o, o2)
                file.print(
                    f'{indent}\t\tsyslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                    f'{to_s(name)}[%d]: %d %d %d %d",\n'
                    f"{indent}\t\t\t\ti__{nest}, {oo}{to_s(name)}{oo2}[i__{nest}], "
                    f"{oo}{to_s(name)}{oo2}[i__{nest}+1], {oo}{to_s(name)}{oo2}[i__{nest}+2], "
                    f"{oo}{to_s(name)}{oo2}[i__{nest}+3] );\n"
                )
            elif isinstance(typ, IntType):
                oo, oo2 = (f"({o}", f"{o2})") if (outer or outer2) else (o, o2)
                file.print(
                    f"{indent}\t\tif( sizeof({oo}{to_s(name)}{oo2}) > sizeof(int_t) )\n"
                    f'{indent}\t\t\tsyslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                    f'{to_s(name)}[%d]: %02x %02x %02x %02x",\n'
                    f"{indent}\t\t\t\t\ti__{nest}, {oo}{to_s(name)}{oo2}[i__{nest}], "
                    f"{oo}{to_s(name)}{oo2}[i__{nest}+1], {oo}{to_s(name)}{oo2}[i__{nest}+2], "
                    f"{oo}{to_s(name)}{oo2}[i__{nest}+3] );\n"
                    f"{indent}\t\telse\n"
                    f'{indent}\t\t\tsyslog( LOG_INFO, "{indent}[{to_s(direction)}]{type_str} '
                    f'{to_s(name)}[%d]: %02lx %02lx %02lx %02lx",\n'
                    f"{indent}\t\t\t\t\ti__{nest}, {oo}{to_s(name)}{oo2}[i__{nest}], "
                    f"{oo}{to_s(name)}{oo2}[i__{nest}+1], {oo}{to_s(name)}{oo2}[i__{nest}+2], "
                    f"{oo}{to_s(name)}{oo2}[i__{nest}+3] );\n"
                )
            elif isinstance(typ, PtrType):
                if outer or outer2:
                    outer_p = f"({o}"
                    outer2_p = f"{o2})[i__{nest}]"
                else:
                    outer_p, outer2_p = "", f"[i__{nest}]"
                self.print_param(
                    name, typ, file, nest + 1, direction, type_str, outer_p, outer2_p
                )

            file.print(
                f"{indent}\t}} /* for ( i__{nest} ) */\n"
                f"{indent}\tif( i__{nest} < {size} )\n"
                f'{indent}\t\tsyslog( LOG_INFO, "{indent}(%d elements are omitted)", {size} - i__{nest} );\n'
                f"{indent}\telse if( i__{nest} > {size} )\n"
                f'{indent}\t\tsyslog( LOG_INFO, "{indent}(last %d elements are void)", i__{nest} - {size} );\n'
                f"{indent}}}\n"
            )

        if type0.is_nullable():
            file.print(
                f"{indent0}}} else {{\n"
                f'{indent0}    syslog( LOG_INFO, "{indent0}[{to_s(direction)}]{outer0 or ""}'
                f'{to_s(name)}{outer20 or ""} = NULL" );\n'
                f"{indent0}}}\n"
            )

    # --- プラグイン引数 ---

    def set_maxArrayDisplay(self, rhs: Any) -> None:
        self._max_array_display = rhs

    def set_cellEntry(self, rhs: Any) -> None:
        ces = re.split(r"\s*,\s*", to_s(rhs))
        for ce in ces:
            if not re.match(r"^[A-Za-z_]\w*\.[A-Za-z_]\w*$", ce):
                self.cdl_error(f'{ce}: TracePlugin arg not in "symbol.symbol" form')
        self._cell_entry_list.extend(ces)

    def set_probeName(self, rhs: Any) -> None:
        self._probe_name = to_s(rhs)

    def set_displayTime(self, rhs: Any) -> None:
        if to_s(rhs) == "true":
            self._b_display_time = True
        elif to_s(rhs) == "false":
            self._b_display_time = False
        else:
            self.cdl_error(
                f"displayTime : {to_s(rhs)} unsuitable: specify true or false"
            )

    def set_kernelCelltype(self, rhs: Any) -> None:
        """プラグイン引数 tKernel のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._kernel_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._kernel_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(
                f"TracePlugin: kernelCelltype '{to_s(rhs)}' not celltype or not defined"
            )

    def set_syslogCelltype(self, rhs: Any) -> None:
        """プラグイン引数 tSyslog のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._syslog_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._syslog_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(
                f"TracePlugin: syslogCelltype '{to_s(rhs)}' not celltype or not defined"
            )


TracePlugin.TRACE_PLUGIN_ARG_PROC = {
    "maxArrayDisplay": lambda obj, rhs: obj.set_maxArrayDisplay(rhs),
    "cellEntry": lambda obj, rhs: obj.set_cellEntry(rhs),
    "probeName": lambda obj, rhs: obj.set_probeName(rhs),
    "displayTime": lambda obj, rhs: obj.set_displayTime(rhs),
    "kernelCelltype": lambda obj, rhs: obj.set_kernelCelltype(rhs),
    "syslogCelltype": lambda obj, rhs: obj.set_syslogCelltype(rhs),
}
