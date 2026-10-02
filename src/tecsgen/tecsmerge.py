"""tecsmerge: TECS が生成したテンプレートと保守中のセルタイプコードのマージ（tecsmerge.rb の移植）。

Ruby 版と同じく、ファイルは ASCII-8BIT（バイト列）として行単位に読み書きする。ここでは
latin-1 で文字列に対応づけ、改行は `\\n` だけを行の区切りとする。標準出力・標準エラー出力の
書き方（メッセージ・順序）も Ruby 版と同じにする。Ruby 版の癖（`-f` を `-p` より前に書いたときの
例外、`-o` なしでの前キーワード違反時の例外など）は、例外として終了コード 1 になるところまで再現する。
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field

from tecsgen.ruby_optparse import HelpRequested, OptionParser, OptionParserError

ENC = "latin-1"

# 状態 → (開始キーワードの原文, 直前に許される状態)。順序は Ruby 版の Hash の挿入順
_DELIMITERS: dict[str, tuple[str, list[str]]] = {
    "HEAD": ("#[<BeginingOfFile>]#", []),
    "PREAMBLE_COMMENT": ("/* #[<PREAMBLE>]#", ["HEAD"]),
    "PREAMBLE_BODY": (" * #[</PREAMBLE>]#", ["PREAMBLE_COMMENT"]),
    "ENTRY_COMMENT": (
        "/* #[<ENTRY_PORT>]# PORT_NAME",
        ["PREAMBLE_BODY", "ENTRY_FUNC_BODY", "ENTRY_FUNC_BODY2"],
    ),
    "ENTRY_BODY": (" * #[</ENTRY_PORT>]#", ["ENTRY_COMMENT"]),
    "ENTRY_FUNC_COMMENT": (
        "/* #[<ENTRY_FUNC>]# FUNC_NAME",
        ["ENTRY_BODY", "ENTRY_FUNC_BODY", "ENTRY_FUNC_BODY2"],
    ),
    "POSTAMBLE_COMMENT": (
        "/* #[<POSTAMBLE>]#",
        ["ENTRY_FUNC_BODY", "ENTRY_FUNC_BODY2", "PREAMBLE_BODY"],
    ),
    "POSTAMBLE_BODY": (" * #[</POSTAMBLE>]#", ["POSTAMBLE_COMMENT"]),
    "EOF": (
        "#[</EndOfFile>]#",
        ["POSTAMBLE_BODY", "ENTRY_FUNC_BODY", "ENTRY_FUNC_BODY2", "PREAMBLE_BODY"],
    ),
}
_FUNC_BY_COMMENT: dict[str, tuple[str, list[str]]] = {
    "ENTRY_FUNC_BODY": (" * #[</ENTRY_FUNC>]#", ["ENTRY_FUNC_COMMENT"]),
    "ENTRY_FUNC_BODY2": (
        " * #[/ENTRY_FUNC>]#",
        ["ENTRY_FUNC_COMMENT"],
    ),  # Bug compatibility
}
_FUNC_BY_BRACKET: dict[str, tuple[str, list[str]]] = {
    "ENTRY_FUNC_BODY": ("\\{", ["ENTRY_FUNC_COMMENT"]),
}


def _compile(original: str) -> re.Pattern[str]:
    """Ruby 版 rewrite_DELIMITERS: `*`・`[`・`]` をエスケープし、`..._NAME` を `(\\w*)` にする。"""
    s = re.sub(r"([\*\[\]])", r"\\\1", original)
    s = re.sub(r"\s*\w*_NAME", r"\\s*(\\w*)", s)
    return re.compile("^" + s, re.ASCII)


class MergeError(Exception):
    """Ruby 版では例外（バックトレース付き）で終了コード 1 になる場面。"""


@dataclass
class _State:
    n_err: int = 0
    b_show: bool = False
    b_exist: bool = False
    old_mode: bool = False
    delimiters: dict[str, tuple[str, list[str]]] = field(default_factory=dict)
    regexps: dict[str, re.Pattern[str]] = field(default_factory=dict)
    port_renamers: dict[str, PortRenamer] = field(default_factory=dict)
    port_renamer_current: PortRenamer | None = None


class _Exit(Exception):
    def __init__(self, code: int) -> None:
        super().__init__(code)
        self.code = code


def _err(msg: str) -> None:
    sys.stderr.write(msg + "\n")


def _out(msg: str) -> None:
    sys.stdout.write(msg)


class PortRenamer:
    def __init__(
        self, st: _State, old_port_name: str, new_port_name: str | None
    ) -> None:
        self.st = st
        st.port_renamers[old_port_name] = self
        st.port_renamer_current = self
        self.old_port_name = old_port_name
        self.new_port_name = new_port_name
        self.func_renamer_list: dict[str, str] = {}

    @staticmethod
    def add_func_to_current(st: _State, old_name: str, new_name: str | None) -> None:
        if st.port_renamer_current is None:
            _err(f"error: {old_name}: specify -p before -f")
            # Ruby 版は `n_err += 1`（局所変数）で NoMethodError になる
            raise MergeError("undefined method '+' for nil")
        st.port_renamer_current.add_func(old_name, new_name)

    def add_func(self, old_name: str, new_name: str | None) -> None:
        if new_name is None:
            raise MergeError("undefined method 'to_sym' for nil")
        if old_name in self.func_renamer_list:
            _err(f"error: {old_name}: duplicate in port {self.old_port_name}")
            self.st.n_err += 1
        elif old_name == new_name:
            _err(f"error: {old_name}: old and new are the same name")
            self.st.n_err += 1
        self.func_renamer_list[old_name] = new_name

    def show(self) -> None:
        line = f"port: {self.old_port_name}"
        if self.new_port_name:
            line += f" => {self.new_port_name}"
        _out(line + "\n")
        for old, new in self.func_renamer_list.items():
            _out(f"  func: {old} => {new}\n")


class CDLEntryPort:
    def __init__(self) -> None:
        self.entry_comment: list[str | None] = []
        self.entry_body: list[str | None] = []
        self.entry_func_comment: dict[str, list[str | None]] = {}
        self.entry_func_body: dict[str, list[str | None]] = {}
        self.entry_func_array: list[str] = []

    def write(self, out: list[str]) -> None:
        _write_array(out, self.entry_comment)
        _write_array(out, self.entry_body)
        for fnm in self.entry_func_array:
            _write_array(out, self.entry_func_comment[fnm])
            _write_array(out, self.entry_func_body[fnm])


def _write_array(out: list[str], array: list[str | None]) -> None:
    for line in array:
        if line is not None:  # Ruby の file.write nil は何も書かない
            out.append(line)


def _need(name: str | None) -> str:
    if name is None:
        raise MergeError("undefined method for nil")
    return name


_COMMENT_STATES = (
    "PREAMBLE_COMMENT",
    "ENTRY_COMMENT",
    "ENTRY_FUNC_COMMENT",
    "POSTAMBLE_COMMENT",
)


class CDLContents:
    def __init__(self, st: _State, all_contents: list[str]) -> None:
        self.st = st
        self.entry_port: dict[str, CDLEntryPort] = {}
        self.entry_port_array: list[str] = []
        self.head: list[str | None] = []
        self.preamble_comment: list[str | None] = []
        self.preamble_body: list[str | None] = []
        self.postamble_comment: list[str | None] = []
        self.postamble_body: list[str | None] = []
        self._parse(all_contents)

    def _store(
        self,
        stat: str,
        part: list[str | None],
        arg: str | None,
        names: dict[str, str | None],
    ) -> None:
        if stat == "HEAD":
            self.head = part
        elif stat == "PREAMBLE_COMMENT":
            self.preamble_comment = part
        elif stat == "PREAMBLE_BODY":
            self.preamble_body = part
        elif stat == "ENTRY_COMMENT":
            port_name = arg
            if port_name is None:
                raise MergeError("undefined method 'to_sym' for nil")
            self.entry_port[port_name] = CDLEntryPort()
            self.entry_port_array.append(port_name)
            self.entry_port[port_name].entry_comment = part
            names["port"] = port_name
        elif stat == "ENTRY_BODY":
            self.entry_port[_need(names["port"])].entry_body = part
        elif stat == "ENTRY_FUNC_COMMENT":
            func_name = arg
            if func_name is None:
                raise MergeError("undefined method 'to_sym' for nil")
            names["func"] = func_name
            ep = self.entry_port.get(names["port"] or "")
            if ep is not None:  # None なら既にエラー
                ep.entry_func_comment[func_name] = part
                ep.entry_func_array.append(func_name)
        elif stat in ("ENTRY_FUNC_BODY", "ENTRY_FUNC_BODY2"):
            ep = self.entry_port.get(names["port"] or "")
            if ep is not None:
                ep.entry_func_body[_need(names["func"])] = part
        elif stat == "POSTAMBLE_COMMENT":
            self.postamble_comment = part
        elif stat == "POSTAMBLE_BODY":
            self.postamble_body = part
        else:
            raise MergeError(f"Unknown state {stat}")

    def _parse(self, all_contents: list[str]) -> None:
        st = self.st
        part: list[str | None] = []
        stat = "HEAD"
        arg: str | None = None
        names: dict[str, str | None] = {"port": None, "func": None}
        lines: list[str | None] = [*all_contents, None]  # None: EOF
        for line_no, line in enumerate(lines, start=1):
            b_delim = False
            for next_stat, (_orig, prevs) in st.delimiters.items():
                if next_stat == "HEAD" or (next_stat == "EOF" and line is not None):
                    continue
                # #1002 非受け口関数（PREAMBLE/POSTAMBLE部）の行頭の '{'
                if (
                    not st.old_mode
                    and line is not None
                    and line.startswith("{")
                    and stat in ("PREAMBLE_BODY", "POSTAMBLE_BODY")
                ):
                    continue
                m = st.regexps[next_stat].match(line) if line is not None else None
                if m is None and not (line is None and next_stat == "EOF"):
                    continue
                b_delim = True
                if stat not in prevs:
                    _err(f"error {line_no}: unsuitable previous keyword")
                    _err(f'error {line_no}:   previous:  "{st.delimiters[stat][0]}"')
                    _err(
                        f'error {line_no}:   current:   "{st.delimiters[next_stat][0]}"'
                    )
                    expect = ", ".join(
                        f'"{st.delimiters[p][0]}"' for p in prevs if p in st.delimiters
                    )
                    if any(p not in st.delimiters for p in prevs):
                        # Ruby 版は @@DELIMITERS[prev][0] が nil[0] になり NoMethodError
                        raise MergeError("undefined method '[]' for nil")
                    _err(f"error {line_no}:   suitable previous: {expect}")
                    st.n_err += 1
                if stat in _COMMENT_STATES:
                    part.append(line)
                self._store(stat, part, arg, names)
                part = [line] if next_stat in _COMMENT_STATES else []
                stat = next_stat
                arg = m.group(1) if m is not None and m.re.groups else None
                break
            if not b_delim:
                part.append(line)

    def check(self, template: CDLContents) -> None:
        for port_name, entry_port in self.entry_port.items():
            temp = template.entry_port.get(port_name)
            if temp is None:
                _err(f"info: {port_name} is deleted port")
                continue
            for func_name in entry_port.entry_func_body:
                if func_name not in temp.entry_func_body:
                    _err(f"info: {func_name} is deleted function")

    def rename(self) -> None:
        renamed_entry_port: dict[str, CDLEntryPort] = {}
        for pon, pr in self.st.port_renamers.items():
            ep = self.entry_port.get(pon)
            if ep is None:
                _err(f"warning: {pon}: renaming port not found")
                continue
            pnn = pr.new_port_name
            if pnn:
                renamed_entry_port[pnn] = self.entry_port[pon]
                del self.entry_port[pon]

            renamed_comment: dict[str, list[str | None]] = {}
            renamed_body: dict[str, list[str | None]] = {}
            for old, new in pr.func_renamer_list.items():
                ofn = f"{pon}_{old}"
                nfn = f"{pon}_{new}"
                if ofn not in ep.entry_func_comment:
                    _err(f"warning: {old}: renaming function not found")
                    continue
                ep.entry_func_array = [
                    nfn if fn == ofn else fn for fn in ep.entry_func_array
                ]
                renamed_comment[nfn] = ep.entry_func_comment[ofn]
                renamed_body[nfn] = ep.entry_func_body.get(ofn, [])
                del ep.entry_func_comment[ofn]
                ep.entry_func_body.pop(ofn, None)
            ep.entry_func_comment.update(renamed_comment)
            ep.entry_func_body.update(renamed_body)

            renamed_comment = {}
            renamed_body = {}
            if pnn:
                new_array: list[str] = []
                for ofn in ep.entry_func_array:
                    nfn = re.sub(re.escape(pon), lambda _m, r=pnn: r, ofn, count=1)
                    if nfn != ofn:
                        renamed_comment[nfn] = ep.entry_func_comment[ofn]
                        renamed_body[nfn] = ep.entry_func_body.get(ofn, [])
                        del ep.entry_func_comment[ofn]
                        ep.entry_func_body.pop(ofn, None)
                        new_array.append(nfn)
                    else:
                        new_array.append(ofn)
                ep.entry_func_array = new_array
                ep.entry_func_comment.update(renamed_comment)
                ep.entry_func_body.update(renamed_body)
        self.entry_port.update(renamed_entry_port)

    def merge(self, src: CDLContents) -> None:
        self.head = src.head
        self.preamble_body = src.preamble_body
        self.postamble_body = src.postamble_body
        for port_name in self.entry_port_array:
            entry_port = self.entry_port[port_name]
            src_entry_port = src.entry_port.get(port_name)
            if src_entry_port is None:
                _out(f"port merged:   {port_name}\n")
                continue
            entry_port.entry_body = src_entry_port.entry_body
            for func_name in entry_port.entry_func_array:
                if func_name not in src_entry_port.entry_func_body:
                    _out(f"func merged:   {func_name}\n")
                    continue
                _out(f"func remained: {func_name}\n")
                entry_port.entry_func_body[func_name] = src_entry_port.entry_func_body[
                    func_name
                ]

    def to_text(self) -> str:
        out: list[str] = []
        _write_array(out, self.head)
        _write_array(out, self.preamble_comment)
        _write_array(out, self.preamble_body)
        for port_name in self.entry_port_array:
            self.entry_port[port_name].write(out)
        _write_array(out, self.postamble_comment)
        _write_array(out, self.postamble_body)
        return "".join(out)


def _read_lines(path: str) -> list[str]:
    with open(path, "rb") as f:
        data = f.read().decode(ENC)
    return data.splitlines(keepends=True) if "\r" not in data else _split_lf(data)


def _split_lf(data: str) -> list[str]:
    """Ruby の readlines と同じく `\\n` だけで区切る（`\\r` では区切らない）。"""
    lines = data.split("\n")
    out = [ln + "\n" for ln in lines[:-1]]
    if lines[-1] != "":
        out.append(lines[-1])
    return out


def _write_text(path: str, text: str) -> None:
    with open(path, "wb") as f:
        f.write(text.encode(ENC))


def _error_check(st: _State, dst_file: str, level: int) -> None:
    if st.n_err > 0:
        _err(f"=== {dst_file} not generated because of error ===")
        raise _Exit(level)


def _rename_dst(dst_file: str) -> str | None:
    if not os.path.exists(dst_file):
        _err(f"info: backup not generated for {dst_file}")
        return None
    i = 0
    while True:
        i += 1
        bkup_file = f"{dst_file}_{i}"
        if not os.path.exists(bkup_file):
            break
    try:
        os.rename(dst_file, bkup_file)
    except OSError:
        _err(f"error: fail to rename backup file: {bkup_file}")
        raise _Exit(1) from None
    _err(f"info: backup generated for {dst_file} to {bkup_file}")
    return bkup_file


def merge(st: _State, src_file: str, dst_dir: str) -> None:
    m = re.search(r"(.*)_templ(.[ch])$", src_file)
    if m is None:
        _err(f"error: {src_file}: not end with _templ.c/h")
        raise _Exit(1)
    fname = f"{m.group(1)}{m.group(2)}"
    dst_file = f"{dst_dir}/{os.path.basename(fname)}"
    if os.path.isfile(dst_file):
        _out(f"merging {src_file} to {dst_file}\n")
        try:
            old_contents = _read_lines(dst_file)
        except OSError:
            _err(f"error: cannot open {dst_file}")
            st.n_err += 1
            raise _Exit(1) from None
        old = CDLContents(st, old_contents)
        try:
            new_contents = _read_lines(src_file)
        except OSError:
            _err(f"error: cannot open {src_file}")
            st.n_err += 1
            raise _Exit(1) from None
        templ = CDLContents(st, new_contents)

        old.rename()
        _error_check(st, dst_file, 1)
        old.check(templ)
        _error_check(st, dst_file, 2)
        templ.merge(old)
        _error_check(st, dst_file, 3)

        _rename_dst(dst_file)
        _write_text(dst_file, templ.to_text())
    elif not st.b_exist:
        try:
            contents = _read_lines(src_file)
        except OSError:
            _out(f"{src_file}: fail to read\n")
            return
        try:
            _write_text(dst_file, "".join(contents))
        except OSError:
            _out(f"{dst_file}: fail to write\n")
    else:
        _out(f"info: {dst_file} skipped\n")


def _make_parser(st: _State) -> OptionParser:
    parser = OptionParser()
    parser.banner = "Usage: tecsmerge [options] files_templ.c   src_dir\n       tecsmerge [options] gen_dir         src_dir"

    def exist_only() -> None:
        st.b_exist = True

    def port(ps: str) -> None:
        p = ps.split(":")
        PortRenamer(st, p[0], p[1] if len(p) > 1 and p[1] != "" else None)

    def func(fs: str) -> None:
        f = fs.split(":")
        PortRenamer.add_func_to_current(
            st, f[0], f[1] if len(f) > 1 and f[1] != "" else None
        )

    def show() -> None:
        st.b_show = True

    def old_mode() -> None:
        st.old_mode = True

    parser.on(
        "-e",
        "--exist-only",
        "merge if exist in destination directory",
        handler=exist_only,
    )
    parser.on(
        "-p", "--port=old_name:new_name", "specify entry port name change", handler=port
    )
    parser.on(
        "-f",
        "--func=old_name:new_name",
        "specify entry function name change",
        handler=func,
    )
    parser.on(
        "-s", "--show_change_set", "show change set. all substitute", handler=show
    )
    parser.on(
        "-o", "--old-mode", "old mode (function head not substituted)", handler=old_mode
    )
    return parser


def run(argv: list[str]) -> int:
    st = _State()
    parser = _make_parser(st)
    try:
        try:
            args = parser.parse(argv)
        except HelpRequested:
            _out(parser.help())
            return 0
        except OptionParserError as e:
            _err(f"tecsmerge: {e}")
            return 1
        if len(args) < 2:
            _out(parser.help())
            return 1

        if st.b_show:
            for pr in st.port_renamers.values():
                pr.show()

        table = {
            **_DELIMITERS,
            **(_FUNC_BY_COMMENT if st.old_mode else _FUNC_BY_BRACKET),
        }
        st.delimiters = table
        st.regexps = {s: _compile(info[0]) for s, info in table.items()}

        if st.n_err > 0:
            _err(f"{st.n_err} errors")
            return 1

        src, dst = args[:-1], args[-1]
        if not os.path.exists(dst):
            _err(f"error: {dst}: not found")
            return 1
        if not os.path.isdir(dst):
            _err(f"error: {dst}: not directory")
            return 1

        for s in src:
            if not os.path.exists(s):
                _err(f"error: {s}: not found or cannot access")
                return 1
            if os.path.isdir(s):
                for f in os.listdir(s):
                    if re.search(r"_templ.[ch]$", f):
                        merge(st, f"{s}/{f}", dst)
            elif os.path.isfile(s):
                merge(st, s, dst)
    except _Exit as e:
        return e.code
    except MergeError as e:
        _err(f"tecsmerge: {e}")
        return 1
    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:]))
