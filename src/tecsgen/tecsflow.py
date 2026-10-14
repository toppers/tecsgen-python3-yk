"""tecsflow コマンド（Ruby 版 tecsflow.rb の移植）。

tecsgen が書いたモデル（`<gen_dir>/tecsgen.pickle`、Ruby 版の `tecsgen.rbdmp`）と、
tcflow が書いた関数リスト（`<gen_dir>/tcflow.json`、Ruby 版の `tcflow.rbdmp`）を読み、
アクティブセルの呼び出し関数から始まる呼び出しフローと、参照されていない関数を表示する。

Ruby 版は `Namespace`・`Cell` を再オープンしてメソッドを足すが、Python 版はモデルクラスへ
足さず、このモジュールの関数にした（`Cell` の `@@printed_*` は `_State`）。

Ruby 版との違い:
- 保存形式。`tecsgen.rbdmp`・`tcflow.rbdmp`（Marshal）を `tecsgen.pickle`・`tcflow.json` に置き換えた。
- `tecsflow.rb:452` の `TCFlow::Function.load_funclist $tecsgen_dump_file_name` は再現しない。
  戻り値が捨てられ、直後に上書きされる無駄な呼び出しで、出力に影響しない
  （WSL で確認済み。vault の tecsflow・Marshal調査ノート参照）。
- `$unopt` は Marshal に保存されないので、Ruby 版 tecsflow では常に偽（最適化済みの結合を使う）。
  Python 版も同じで、`-U` は受け付けない（Makefile の `tecsflow_u` が渡す `-U` は警告になる）。
"""

from __future__ import annotations

import os
import pickle
import re
import sys
from typing import Any, ClassVar

from tecsgen import cli
from tecsgen.context import get_context, reset_context
from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
from tecsgen.core.componentobj.namespace import Namespace
from tecsgen.core.componentobj.port import Port
from tecsgen.core.unjoin_plugin import DUMP_FILE_NAME as TECSGEN_DUMP_NAME
from tecsgen.flowlib.c_parser import err, out, to_bstr
from tecsgen.flowlib.classes import Function, print_locale
from tecsgen.flowlib.ruby_errors import ruby_open_message
from tecsgen.host import get_host
from tecsgen.ruby_compat import Symbol, Y, sym, to_s
from tecsgen.ruby_optparse import (
    HelpRequested,
    OptionParser,
    OptionParserError,
    VersionRequested,
)

TITLE = "tecsflow"
TOOL_VERSION = "1.G.0"
TCFLOW_DUMP_NAME = "tcflow.json"
RECURSION_LIMIT = 20000  # Ruby のスタックは深い再帰に耐えるため

_CALL_PORT_FUNC = re.compile(r"->(?P<cp>\w+)(?P<subsc>(\[\])*)\.(?P<func>\w+)__T")


class _Exit(Exception):
    """Ruby の `exit`。"""

    def __init__(self, status: int) -> None:
        super().__init__("exit")
        self.status = status


class _State:
    """Cell の `@@printed_*` と、`$tcflow_funclist`。"""

    printed_func_nsp_list: ClassVar[dict[Symbol, bool]] = {}
    printed_cell_list: ClassVar[dict[Any, bool]] = {}
    funclist: ClassVar[dict[Symbol, Function | int]] = {}

    @classmethod
    def reset(cls) -> None:
        cls.printed_func_nsp_list = {}
        cls.printed_cell_list = {}
        cls.funclist = {}


def _b(value: Any) -> str:
    """モデルの値を、標準出力へ書くバイト列表現の文字列にする。"""
    return to_bstr(to_s(value))


def print_indent(level: int) -> int:
    if level > 0:
        out("    " * level)
        return level
    return -level


def _funclist_get(name: Any) -> Function | int | None:
    return _State.funclist.get(name)


def _entry_function(name: Any) -> Function | None:
    """entry 関数の `Function`。未登録なら None。

    Ruby 版は `if $tcflow_funclist[name]` で調べる。呼ばれたが定義が無い関数の値 0 は真なので、
    そのあとの `0.get_call_funcs` は NoMethodError で落ちる。Python 版も AttributeError で落とす。
    """
    function = _funclist_get(name)
    if function is None or isinstance(function, Function):
        return function
    raise AttributeError(f"undefined method for {function}:Integer ({name})")


# --- Namespace#print_all_cells ----------------------------------------------


def print_all_cells(ns: Any) -> None:
    """アクティブセルの呼び出しポート関数から始まる呼び出しフローをすべて表示する。"""
    for cell in ns.get_cell_list():
        celltype = cell.get_celltype()
        if not (celltype.is_active() and not isinstance(celltype, CompositeCelltype)):
            continue
        call_funcs: dict[Symbol, bool] = {}
        out(f"[active cell] {_b(cell.get_namespace_path())}")
        print_locale(cell.get_locale())
        out("\n")
        for j in cell.get_join_list().get_items():
            if isinstance(j.get_definition(), Port):
                port = j.get_definition()
                for f in port.get_signature().get_function_head_array():
                    func_name = sym(f"->{_b(port.get_name())}.{_b(f.get_name())}__T")
                    call_funcs[func_name] = False
        # 呼び出しポート関数が entry ポート関数から呼ばれていれば、実際にはアクティブではない
        # （タスク本体・ハンドラ本体は entry 関数から呼ばれない）
        for ep in celltype.get_port_list():
            if ep.get_port_type() != Y.ENTRY:
                continue
            for f in ep.get_signature().get_function_head_array():
                ep_func = sym(
                    f"{_b(celltype.get_global_name())}_{_b(ep.get_name())}_{_b(f.get_name())}"
                )
                function = _entry_function(ep_func)
                if function is not None:
                    for cf in function.get_call_funcs():
                        if call_funcs.get(cf) is False:
                            call_funcs[cf] = True
                else:
                    out(f"ep_func {ep_func} not found. why not defined ?\n")
        for call_func_name, called in call_funcs.items():
            if called is False:  # entry ポート関数から呼ばれていない
                print_call_func_flow(cell, True, call_func_name, 1, [])
    for child in ns.get_namespace_list():
        print_all_cells(child)


# --- Cell ---------------------------------------------------------------------


def print_unused_func() -> None:
    parent_cell: list[Any] = []
    indent_level = 1
    for cell in list(_State.printed_cell_list):
        ct = cell.get_celltype()
        if cell.is_in_composite():
            continue
        for port in ct.get_port_list():
            if port.get_port_type() == Y.CALL:
                continue
            entry_port_name = port.get_name()
            for head in port.get_signature().get_function_head_array():
                func_name = head.get_name()
                ep_func = sym(
                    f"{_b(ct.get_global_name())}_{_b(entry_port_name)}_{_b(func_name)}"
                )
                func = _funclist_get(ep_func)
                if isinstance(func, Function) and not func.is_printed():
                    out(
                        f"[unreferenced entry function] {_b(cell.get_namespace_path())}"
                        f".{_b(entry_port_name)}.{_b(func_name)}"
                    )
                    print_entry_func_flow(
                        cell, entry_port_name, func_name, indent_level, parent_cell
                    )


def get_function_nsp(
    cell: Any, port_name: Any, func_name: Any, parent_cell: list[Any]
) -> Symbol:
    if cell.is_in_composite() is False:
        nsp = re.sub(r"^::", "", _b(cell.get_namespace_path()), count=1)
        return sym(f"{nsp}.{_b(port_name)}.{_b(func_name)}")
    n_parent = len(parent_cell)
    if not parent_cell:
        # Bug trap
        out(
            f"\nname={_b(cell.get_name())}, len={n_parent}"
            f" nsp={_b(cell.get_namespace_path())}\n"
        )
        nsp = "__" + _b(cell.get_name())
    else:
        nsp = _b(parent_cell[0].get_namespace_path())
    for i in range(1, n_parent):
        nsp = nsp + "_" + _b(parent_cell[i].get_name())
    return sym(f"{nsp}_{_b(cell.get_name())}.{_b(port_name)}.{_b(func_name)}")


def print_entry_func_flow(
    cell: Any,
    entry_port_name: Any,
    func_name: Any,
    indent_level: int,
    parent_cell: list[Any],
) -> None:
    func_nsp = get_function_nsp(cell, entry_port_name, func_name, parent_cell)
    _State.printed_cell_list[cell] = True
    if _State.printed_func_nsp_list.get(func_nsp):
        out(": printed\n")
        return
    _State.printed_func_nsp_list[func_nsp] = True
    celltype = cell.get_celltype()
    if not isinstance(celltype, CompositeCelltype):
        ep_func = sym(
            f"{_b(celltype.get_global_name())}_{_b(entry_port_name)}_{_b(func_name)}"
        )
        function = _entry_function(ep_func)
        if function is not None:
            print_locale(function.get_locale())
            out("\n")
            function.set_printed()
            for call_func_name in list(function.get_call_funcs()):
                print_call_func_flow(
                    cell, True, call_func_name, indent_level, parent_cell
                )
        else:
            out("\n")
            indent_level = print_indent(indent_level)
            out(f"not found '{ep_func}' !!!\n")
    else:
        cj = celltype.find_export(entry_port_name)
        inner_cell = cj.get_cell()
        ep_name = cj.get_cell_elem_name()
        out(f" == [inner]{_b(inner_cell.get_name())}.{_b(ep_name)}")
        parent_cell = [*parent_cell, cell]
        print_entry_func_flow(inner_cell, ep_name, func_name, indent_level, parent_cell)


def analyze_call_port_func_name(fname: Any) -> list[Any] | None:
    """`->call_port[].function__T` を [call_port, function, subsc] に分ける。"""
    m = _CALL_PORT_FUNC.search(str(fname))
    if m is None:
        return None
    subsc = m.group("subsc")
    return [sym(m.group("cp")), sym(m.group("func")), subsc if subsc != "" else None]


def print_call_func_flow(
    cell: Any,
    no_caller_cell: bool,
    call_func_name: Any,
    indent_level: int,
    parent_cell: list[Any],
) -> None:
    m = analyze_call_port_func_name(call_func_name)
    if m is not None:
        call_port, function, call_subsc = m
        join_list = cell.get_join_list()
        if call_subsc is None:
            join = join_list.get_item(call_port)
            print_call_func_flow_sub(
                cell,
                indent_level,
                no_caller_cell,
                call_port,
                call_subsc,
                function,
                join,
                parent_cell,
            )
            return
        join_0 = join_list.get_item(call_port)
        if join_0 is not None:
            call_subsc = 0
            for join in join_0.get_array_member2():
                print_call_func_flow_sub(
                    cell,
                    indent_level,
                    no_caller_cell,
                    call_port,
                    call_subsc,
                    function,
                    join,
                    parent_cell,
                )
                call_subsc += 1
        else:
            print_call_func_flow_sub(
                cell,
                indent_level,
                no_caller_cell,
                call_port,
                call_subsc,
                function,
                join_0,
                parent_cell,
            )
        return

    # TECS 以外の関数
    func = _funclist_get(call_func_name)
    if isinstance(func, Function):
        if func.is_printed():
            indent_level = print_indent(indent_level)
            out(f"{func.get_name()}: printed\n")
        else:
            indent_level = print_indent(indent_level)
            out(f"{call_func_name}")
            print_locale(func.get_locale())
            out(" [Function Out of TECS]\n")
            func.set_printed()
            for cf in list(func.get_call_funcs()):
                print_call_func_flow(cell, False, cf, indent_level + 1, parent_cell)
    else:
        indent_level = print_indent(indent_level)
        out(f"{call_func_name}: [Function Out of TECS, not defined]\n")


def _callee(join: Any) -> tuple[Any, Any, Any]:
    """結合の右辺（cell, port 名, 添数）。`$unopt` は常に偽。"""
    return join.get_rhs_cell(), join.get_rhs_port().get_name(), join.get_rhs_subscript()


def print_call_func_flow_sub(
    cell: Any,
    indent_level: int,
    no_caller_cell: bool,
    call_port: Any,
    call_subsc: Any,
    function: Any,
    join: Any,
    parent_cell: list[Any],
) -> None:
    if join is not None:
        callee_cell, callee_port, callee_subsc = _callee(join)
        print_flow(
            cell,
            indent_level,
            no_caller_cell,
            call_port,
            call_subsc,
            callee_cell,
            callee_port,
            callee_subsc,
            function,
        )
        print_entry_func_flow(
            callee_cell, callee_port, function, indent_level + 1, parent_cell
        )
        return

    if not parent_cell:
        indent_level = print_indent(indent_level)
        out(f"{_b(cell.get_name())}.{_b(call_port)} not joined\n")
        return

    composite = parent_cell[-1].get_celltype()
    # 外部に出しているポートから、内側のセルの呼び口に対応するものを探す
    compjoin = None
    for cj in composite.get_port_list():
        if (
            cj.get_cell().get_name() == cell.get_name()
            and cj.get_cell_elem_name() == call_port
        ):
            compjoin = cj
            break
    if compjoin is None:
        out("\n")
        indent_level = print_indent(indent_level)
        out(
            f"{_b(cell.get_name())}.{_b(call_port)} not found in composite"
            f" {_b(parent_cell[-1].get_name())}\n"
        )
        return

    indent_level = print_indent(indent_level)
    if no_caller_cell is False:
        out(f"[inner]{_b(cell.get_name())}.")
    out(f"{_b(call_port)} == ")
    j = parent_cell[-1].get_join_list().get_item(compjoin.get_name())
    if j is not None:
        callee_cell, callee_port, callee_subsc = _callee(j)
        print_flow(
            parent_cell[-1],
            -indent_level,
            False,
            call_port,
            call_subsc,
            callee_cell,
            callee_port,
            callee_subsc,
            function,
        )
        print_entry_func_flow(
            callee_cell, callee_port, function, indent_level + 1, parent_cell[:-1]
        )
    else:
        # 親の呼び口が、さらに親の外部ポートに結合されている場合
        cf_name = sym(f"->{_b(compjoin.get_name())}.{_b(function)}__T")
        tmp_indent_level = -indent_level if indent_level > 0 else indent_level
        print_call_func_flow(
            parent_cell[-1], False, cf_name, tmp_indent_level, parent_cell[:-1]
        )


def print_name(
    cell: Any, no_cell_name: bool, port_name: Any, subsc: Any, func_name: Any
) -> None:
    if not no_cell_name:
        nsp = re.sub(r"^::", "", _b(cell.get_namespace_path()), count=1)
        if nsp != "":
            out(f"{nsp}.")
        else:
            out(f"{_b(cell.get_name())}.")
    out(_b(port_name))
    if subsc is not None:
        out(f"[{_b(subsc)}]")
    out(f".{_b(func_name)}")


def print_flow(
    cell: Any,
    indent_level: int,
    no_caller_cell: bool,
    call_port_name: Any,
    call_subsc: Any,
    callee_cell: Any,
    entry_port_name: Any,
    callee_subsc: Any,
    func_name: Any,
) -> None:
    print_indent(indent_level)
    print_name(cell, no_caller_cell, call_port_name, call_subsc, func_name)
    out(" => ")
    print_name(callee_cell, False, entry_port_name, callee_subsc, func_name)


# --- TECSFlow.main -------------------------------------------------------------


def print_unref_function() -> None:
    out("--- unreferenced entry functions ---\n")
    print_unused_func()
    out("--- unreferenced C functions ---\n")
    Function.update()
    for func in list(_State.funclist.values()):
        if isinstance(func, Function) and not func.is_printed() and func.is_top():
            out(f"[Function Out of TECS, unreferenced] {func.get_name()}")
            print_locale(func.get_locale())
            out("\n")
            func.print_all_functions(0)


def _pp_exception(e: BaseException) -> None:
    """Ruby の `pp e`（`#<クラス名: メッセージ>`）。"""
    cls = "Errno::ENOENT" if isinstance(e, OSError) else type(e).__name__
    out(to_bstr(f"#<{cls}: {e}>\n"))


def _load_model(dump_file: str) -> Any:
    doing = "file reading"
    try:
        out(f"reading '{to_bstr(dump_file)}'\n")
        try:
            data = get_host().read_bytes(dump_file)
        except OSError as e:
            raise OSError(ruby_open_message(e, dump_file)) from e
        doing = "pickle.load"
        return pickle.loads(data)
    except Exception as e:  # noqa: BLE001  Ruby の rescue => e
        _pp_exception(e)
        out(f"fatal: fail to load '{to_bstr(dump_file)}' in {doing}\n")
        raise _Exit(1) from None


def _load_funclist(dump_file: str) -> None:
    doing = "nothing"
    try:
        out(f"reading '{to_bstr(dump_file)}'\n")
        _State.funclist = Function.load_funclist(dump_file)
    except Exception:  # noqa: BLE001  Ruby の bare rescue
        out(f"fatal: fail to load '{to_bstr(dump_file)}' in {doing}\n")
        raise _Exit(1) from None


def _make_parser() -> OptionParser:
    ctx = get_context()
    parser = OptionParser()
    parser.banner = "Usage: tecsflow [options]"

    def set_gen(arg: str) -> None:
        ctx.gen_base = arg
        ctx.gen = arg

    def set_version() -> None:
        ctx.print_version = True

    def show_help() -> None:
        text = parser.help()
        out(text if text.endswith("\n") else text + "\n")
        raise _Exit(1)

    parser.on("-g", "--gen=dir", "generate dir", handler=set_gen)
    parser.on("-h", "--help", "help", handler=show_help)
    parser.on("--version", "print version", handler=set_version)
    parser.version = cli.VERSION
    parser.release = None
    return parser


def _init(argv: list[str]) -> None:
    """TECSGEN.init(nil, true) と analyze_option。"""
    ctx = get_context()
    ctx.argv = list(argv)
    ctx.tecsgen_base_path = cli.PACKAGE_DIR
    ctx.title = TITLE
    ctx.tool_version = TOOL_VERSION
    ctx.tecsflow = True
    cli.initialize_global_var(ctx, os.environ)
    cli.print_banner(ctx)
    parser = _make_parser()
    try:
        ctx.argv = parser.parse(ctx.argv)
    except HelpRequested:
        text = parser.help()
        out(text if text.endswith("\n") else text + "\n")
        raise _Exit(1) from None
    except VersionRequested:
        out(f"{TITLE} {cli.VERSION}\n")
        raise _Exit(0) from None
    except OptionParserError as e:
        err(to_bstr(f"{TITLE}: {e}\n"))
        ctx.argv = parser.remaining
    cli.load_modules(ctx, os.environ)


def _run(argv: list[str]) -> None:
    _init(argv)
    ctx = get_context()
    tecsgen_dump = f"{ctx.gen}/{TECSGEN_DUMP_NAME}"
    tcflow_dump = f"{ctx.gen}/{TCFLOW_DUMP_NAME}"

    root = _load_model(tecsgen_dump)
    _load_funclist(tcflow_dump)
    Namespace._root_namespace = root  # Namespace.set_root
    print_all_cells(root)
    print_unref_function()


def run(argv: list[str]) -> int:
    """tecsflow を実行して終了コードを返す。"""
    reset_context()
    _State.reset()
    Function.reset()
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, RECURSION_LIMIT))
    try:
        _run(argv)
    except _Exit as e:
        return e.status
    finally:
        sys.setrecursionlimit(old_limit)
        sys.stdout.flush()
    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:]))
