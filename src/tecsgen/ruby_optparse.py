"""Ruby の `optparse`（`OptionParser#parse!`）のうち、tecsgen が使う部分の再現。

tecsgen の CLI は Ruby 版と完全互換にする（[[tecsgen-python3 P0基本方針決定]]）。
Python の argparse とは、次の点で挙動が違うので自前で書く。

- 長いオプション名は、一意に決まる前方一致で省略できる（`--gen-r` など）。完全一致が優先
- 引数を取る短いオプションは、引数を続けて書ける（`-Igen`）。引数を取らない短いオプションは
  まとめて書ける（`-Rv`）
- 引数を取る長いオプションは `--gen=dir` と `--gen dir` の両方を受け付ける
- オプションでない引数は、オプションの間に置いてもよい（残りの引数として順序を保って返す）
- `--` 以降はすべてオプションでない引数
- `-h`・`--help` は組み込み（ヘルプを表示して終了）

エラーは `OptionParserError` で、メッセージは Ruby の例外の to_s と同じ書式にする。
ヘルプの書式（`summary_width` 32、字下げ4）は Ruby 3.2 の optparse に合わせた（TBC: 実物と未比較）。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

SUMMARY_WIDTH = 32
SUMMARY_INDENT = "    "


class OptionParserError(Exception):
    """OptionParser::ParseError の子（InvalidOption・MissingArgument・AmbiguousOption）。"""

    def __init__(self, reason: str, arg: str) -> None:
        super().__init__(f"{reason}: {arg}")
        self.reason = reason
        self.arg = arg


class HelpRequested(Exception):
    """-h・--help。Ruby はヘルプを表示して exit する。"""


@dataclass
class _Switch:
    short: str | None  # "-D"
    long: str | None  # "--define"
    arg_name: str | None  # "def"（引数を取らなければ None）
    desc: str
    handler: Callable[..., Any]

    def summary_left(self) -> str:
        if self.short and self.long:
            left = f"{self.short}, {self.long}"
        elif self.short:
            left = self.short
        else:
            left = f"    {self.long}"
        if self.arg_name is not None:
            left += f"={self.arg_name}" if self.long else f" {self.arg_name}"
        return left


class OptionParser:
    def __init__(self) -> None:
        self.banner = ""
        self.version: str | None = None
        self.release: str | None = None
        self._switches: list[_Switch] = []
        # 解析エラーのとき、エラーになった引数より後ろに残っていた引数（Ruby の ARGV の残り）
        self.remaining: list[str] = []

    def on(self, *specs: str, handler: Callable[..., Any]) -> None:
        """`parser.on('-D', '--define=def', '説明') { |v| ... }` に当たる。"""
        short = long = arg_name = None
        desc = ""
        for s in specs:
            if s.startswith("--"):
                name, sep, arg = s.partition("=")
                long = name
                if sep:
                    arg_name = arg
            elif s.startswith("-"):
                short = s[:2]
                if len(s) > 2:
                    arg_name = s[2:].strip()
            else:
                desc = s
        self._switches.append(_Switch(short, long, arg_name, desc, handler))

    # --- ヘルプ ---------------------------------------------------------------

    def help(self) -> str:
        lines = [self.banner]
        for sw in [*self._switches]:
            left = sw.summary_left()
            if len(left) <= SUMMARY_WIDTH:
                lines.append(f"{SUMMARY_INDENT}{left.ljust(SUMMARY_WIDTH)} {sw.desc}")
            else:
                lines.append(f"{SUMMARY_INDENT}{left}")
                lines.append(f"{SUMMARY_INDENT}{' ' * SUMMARY_WIDTH} {sw.desc}")
        return "\n".join(lines) + "\n"

    # --- 解析 -----------------------------------------------------------------

    def _find_long(self, name: str) -> _Switch:
        exact = [sw for sw in self._switches if sw.long == name]
        if exact:
            return exact[0]
        if name == "--help":
            raise HelpRequested
        cands = [sw for sw in self._switches if sw.long and sw.long.startswith(name)]
        if "--help".startswith(name) and len(name) > 2 and not cands:
            raise HelpRequested
        if not cands:
            raise OptionParserError("invalid option", name)
        if len(cands) > 1:
            raise OptionParserError("ambiguous option", name)
        return cands[0]

    def _find_short(self, ch: str, arg: str) -> _Switch:
        for sw in self._switches:
            if sw.short == f"-{ch}":
                return sw
        if ch == "h":
            raise HelpRequested
        raise OptionParserError("invalid option", arg)

    def parse(self, argv: list[str]) -> list[str]:
        """`parse!` と同じく、オプションを取り除いた残りの引数を返す。"""
        self._argv = argv
        self._i = 0
        try:
            return self._parse()
        except OptionParserError:
            self.remaining = self._argv[self._i :]
            raise

    def _next_arg(self) -> str | None:
        if self._i >= len(self._argv):
            return None
        a = self._argv[self._i]
        self._i += 1
        return a

    def _parse(self) -> list[str]:
        argv = self._argv
        rest: list[str] = []
        while self._i < len(argv):
            arg = argv[self._i]
            self._i += 1
            if arg == "--":
                rest.extend(argv[self._i :])
                break
            if arg.startswith("--"):
                name, sep, value = arg.partition("=")
                sw = self._find_long(name)
                if sw.arg_name is not None:
                    if not sep:
                        nxt = self._next_arg()
                        if nxt is None:
                            raise OptionParserError("missing argument", arg)
                        value = nxt
                    sw.handler(value)
                else:
                    if sep:
                        raise OptionParserError("needless argument", arg)
                    sw.handler()
                continue
            if arg.startswith("-") and arg != "-":
                j = 1
                while j < len(arg):
                    sw = self._find_short(arg[j], "-" + arg[j:] if j > 1 else arg)
                    if sw.arg_name is not None:
                        value = arg[j + 1 :]
                        if value == "":
                            nxt = self._next_arg()
                            if nxt is None:
                                raise OptionParserError("missing argument", arg)
                            value = nxt
                        sw.handler(value)
                        break
                    sw.handler()
                    j += 1
                continue
            rest.append(arg)
        return rest
