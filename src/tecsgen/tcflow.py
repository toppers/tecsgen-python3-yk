"""tcflow コマンド（Ruby 版 tcflow.rb の移植）。

C のソースファイルを読み、関数ごとの呼び出し関数・参照グローバル変数を
`<gen_dir>/tcflow.json` に保存する。Ruby 版の `tcflow.rbdmp`（Marshal 形式）に当たる。

Ruby 版は、処理全体を `rescue Exception` で囲んでいるので、`exit 1` も `--help` も例外として
捕まえ、`fatal error: ...` を標準エラー出力へ書いて、**終了コード 0** で終わる。Python 版も同じ。
"""

from __future__ import annotations

import re
import sys

from tecsgen.flowlib.c_parser import (
    LATIN1,
    TcflowCparser,
    err,
    from_bstr,
    out,
    to_bstr,
)
from tecsgen.flowlib.classes import Function
from tecsgen.host import get_host
from tecsgen.ruby_optparse import (
    HelpRequested,
    OptionParser,
    OptionParserError,
    VersionRequested,
)

EXE_NAME = "tcflow"
VERSION = "V1.0.0.1"
DUMP_FILE_NAME = "tcflow.json"

_LIST_FILE = re.compile(r"@(.*)")
_COMMENT_LINE = re.compile(r"^\s*#", re.ASCII)
_STRIP_CHARS = " \t\n\v\f\r\0"


class _Exit(Exception):
    """Ruby の `exit`（SystemExit）。Ruby では message が "exit"。"""

    def __init__(self) -> None:
        super().__init__("exit")


def _read_list_file(path: str) -> list[str] | None:
    """`@listfile` の中身（`#` 行を除き、前後の空白を除いた空でない行）。開けなければ None。"""
    try:
        data = get_host().read_bytes(path)
    except OSError:
        return None
    files = []
    for line in data.decode(LATIN1).split("\n"):
        if _COMMENT_LINE.match(line):
            continue
        line = line.strip(_STRIP_CHARS)
        if line != "":
            files.append(from_bstr(line))
    return files


def _run(argv: list[str]) -> None:
    cpp_cmd: str | None = None
    gen_dir = "gen"
    read_dump = False
    print_all_token = False

    def set_cpp(arg: str) -> None:
        nonlocal cpp_cmd
        cpp_cmd = arg

    def set_gen(arg: str) -> None:
        nonlocal gen_dir
        gen_dir = arg

    def set_read_dump() -> None:
        nonlocal read_dump
        read_dump = True

    def set_print_all_token() -> None:
        nonlocal print_all_token
        print_all_token = True

    parser = OptionParser()
    parser.banner = "Usage: tcflow [options] files"
    parser.on(
        "-c",
        "--cpp=cpp_cmd",
        'C pre-processor command, if not specified cpp not invoked,  ex) "-cpp_cmd=cl /E -I include_path"',
        handler=set_cpp,
    )
    # -l（一覧表示）と -s（要約）は Ruby 版でも設定されるだけで、使われない
    parser.on("-l", "--list", "list all functions", handler=lambda: None)
    parser.on("-s", "--summarize", "summarize for top functions", handler=lambda: None)
    parser.on("-g", "--gen=dir", "generate dir", handler=set_gen)
    parser.on("-r", "--read-rbdmp", "read ruby dump", handler=set_read_dump)
    parser.on("-t", "--print-all-token", "print all token", handler=set_print_all_token)
    parser.version = VERSION
    parser.release = None
    try:
        files = parser.parse(argv)
    except HelpRequested:
        out(parser.help())
        raise _Exit from None
    except VersionRequested:
        out(f"{EXE_NAME} {VERSION}\n")
        raise _Exit from None
    except OptionParserError as e:
        # ARGV.options { ... } は解析エラーを捕まえて警告を出し、処理を続ける。
        # ARGV に残るのは、エラーになった引数より後ろの引数だけ
        err(to_bstr(f"{EXE_NAME}: {e}\n"))
        files = parser.remaining

    if not files and not read_dump:
        out(f"{EXE_NAME} : {VERSION}\n")
        out(parser.help())
        raise _Exit

    dump_file = f"{gen_dir}/{DUMP_FILE_NAME}"
    if read_dump:
        Function.load_funclist(dump_file)
        return

    err(f"{EXE_NAME} : {VERSION}\n")
    for file in files:
        m = _LIST_FILE.search(file)
        if m:
            file_list = _read_list_file(m.group(1))
            if file_list is None:
                err(to_bstr(f"faile to open {file}"))
                raise _Exit
        else:
            file_list = [file]
        for f in file_list:
            c_parser = TcflowCparser(gen_dir, print_all_token)
            c_parser.parse([f], cpp_cmd)
            c_parser.finalize()
    Function.dump_funclist(dump_file)


def run(argv: list[str]) -> int:
    """tcflow を実行する。終了コードは常に 0（上の説明参照）。"""
    Function.reset()
    TcflowCparser.reset()
    try:
        _run(argv)
    except Exception as e:  # noqa: BLE001  Ruby の rescue Exception
        err(to_bstr(f"fatal error: {e}\n"))
    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:]))
