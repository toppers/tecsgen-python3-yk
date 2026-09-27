"""P3 の差分テストが使う、Ruby 版オラクルの記録（tests/golden/p3/）の読み込みと再生。

記録は tools/port/run_p3_oracle.sh が tests/ruby/p3_oracle.rb を使って採る。1ケースにつき
1ファイルで、起動時の引数と環境、ファイルシステムへの問い合わせとその結果、読んだファイルの
中身、cpp の出力、プラグインの読み込み、チェックポイントごとのモデルのダンプが入っている。

`RecordedHost` は、記録された問い合わせに記録された結果を返す `Host`。記録に無い問い合わせは
`HostMiss` にする（Python 版が Ruby 版と違うファイルを見に行ったことを意味する）。
"""

from __future__ import annotations

import gzip
import json
import posixpath
from dataclasses import dataclass, field
from typing import Any

from conftest import GOLDEN

from tecsgen.host import Host

P3_GOLDEN = GOLDEN.parent / "p3"


def raw(s: str) -> bytes:
    """オラクルが latin-1 で JSON にした文字列を、元のバイト列に戻す。"""
    return s.encode("latin-1")


def text(s: str) -> str:
    """オラクルの文字列を Python 版で使う文字列（パス・引数）にする。

    パスや引数は ASCII のものしか無い前提（非 ASCII なら surrogateescape で保つ）。
    """
    return raw(s).decode("utf-8", "surrogateescape")


@dataclass
class Checkpoint:
    at: str  # "parse" | "sem1" | "sem2"
    out: int  # それまでに標準出力へ書いたバイト数
    n_error: int
    n_warning: int
    dump: dict[str, Any]


@dataclass
class CaseRecord:
    case_id: str
    cwd: str = ""
    argv: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    globals: dict[str, Any] = field(default_factory=dict)
    fs: dict[tuple[str, str, str], bool] = field(default_factory=dict)
    dirs: dict[tuple[str, str], list[str] | None] = field(default_factory=dict)
    reads: dict[tuple[str, str], bytes | None] = field(default_factory=dict)
    # 同じコマンド（import_C の cpp は毎回 gen/tmp_C_src.c を読む）が何度も実行されるので、
    # 出現順に並べておき、順に使う
    popens: dict[tuple[str, str], list[bytes | None]] = field(default_factory=dict)
    plugins: list[tuple[str, str]] = field(default_factory=list)
    checkpoints: list[Checkpoint] = field(default_factory=list)
    exit_out: int = 0
    exit_error: str | None = None
    exit_status: int | None = None

    @property
    def uses_plugin(self) -> bool:
        return bool(self.plugins)

    def checkpoint(self, at: str) -> Checkpoint | None:
        for c in self.checkpoints:
            if c.at == at:
                return c
        return None


def case_ids() -> list[str]:
    return sorted(
        p.relative_to(P3_GOLDEN).as_posix().removesuffix(".jsonl.gz")
        for p in P3_GOLDEN.rglob("*.jsonl.gz")
    )


def load_case(case_id: str) -> CaseRecord:
    rec = CaseRecord(case_id)
    with gzip.open(P3_GOLDEN / f"{case_id}.jsonl.gz", "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            ev = json.loads(line)
            kind = ev["ev"]
            if kind == "env":
                rec.cwd = text(ev["cwd"])
                rec.argv = [text(a) for a in ev["argv"]]
                rec.env = {k: text(v) for k, v in ev["env"].items()}
            elif kind == "globals":
                rec.globals = ev
            elif kind == "fs":
                rec.fs[(ev["op"], text(ev["cwd"]), text(ev["path"]))] = ev["r"]
            elif kind == "dir":
                r = ev["r"]
                rec.dirs[(text(ev["cwd"]), text(ev["path"]))] = (
                    None if r is None else [text(n) for n in r]
                )
            elif kind == "read":
                d = ev["data"]
                rec.reads[(text(ev["cwd"]), text(ev["path"]))] = (
                    None if d is None else raw(d)
                )
            elif kind == "popen":
                d = ev["data"]
                rec.popens.setdefault((text(ev["cwd"]), text(ev["cmd"])), []).append(
                    None if d is None else raw(d)
                )
            elif kind == "plugin":
                rec.plugins.append((text(ev["name"]), ev["super"]))
            elif kind == "model":
                rec.checkpoints.append(
                    Checkpoint(
                        ev["at"], ev["out"], ev["n_error"], ev["n_warning"], ev["dump"]
                    )
                )
            elif kind == "exit":
                rec.exit_out = ev["out"]
                rec.exit_error = ev["error"]
                rec.exit_status = ev.get("status")
    return rec


class HostMiss(AssertionError):
    """記録に無い問い合わせ（Ruby 版はしなかった問い合わせ）。"""


class RecordedHost(Host):
    """記録を再生する Host。書き込んだファイルは覚えておき、後の読み込みで返す。"""

    def __init__(self, rec: CaseRecord) -> None:
        super().__init__(rec.cwd)
        self._rec = rec
        self._written: dict[str, bytes] = {}
        self._made_dirs: set[str] = set()
        self._popen_count: dict[tuple[str, str], int] = {}

    def isabs(self, path: str) -> bool:
        # 記録ではパスの先頭の作業ディレクトリ・ソースが @WORK@・@SOURCE@ に置き換わっている
        return path.startswith(("/", "@WORK@", "@SOURCE@"))

    def _is_directory(self, abs_path: str) -> bool:
        # chdir 先の存在は記録から分からないので、あるものとして扱う
        return True

    def _lookup_fs(self, op: str, path: str) -> bool:
        key = (op, self._cwd, path)
        if key in self._rec.fs:
            return self._rec.fs[key]
        if self._abs(path) in self._written:
            return op != "directory?"
        if op == "directory?" and self.expand_path(path) in self._made_dirs:
            return True
        raise HostMiss(f"File.{op}({path!r}) in {self._cwd!r}")

    def exists(self, path: str) -> bool:
        return self._lookup_fs("exist?", path)

    def is_directory(self, path: str) -> bool:
        return self._lookup_fs("directory?", path)

    def listdir(self, path: str) -> list[str]:
        key = (self._cwd, path)
        if key not in self._rec.dirs:
            raise HostMiss(f"Dir.foreach({path!r}) in {self._cwd!r}")
        names = self._rec.dirs[key]
        if names is None:
            raise FileNotFoundError(2, "No such file or directory", path)
        return names

    def read_bytes(self, path: str) -> bytes:
        abs_path = self._abs(path)
        if abs_path in self._written:
            return self._written[abs_path]
        key = (self._cwd, path)
        if key not in self._rec.reads:
            raise HostMiss(f"read {path!r} in {self._cwd!r}")
        data = self._rec.reads[key]
        if data is None:
            raise FileNotFoundError(2, "No such file or directory", path)
        return data

    def write_bytes(self, path: str, data: bytes) -> None:
        self._written[self._abs(path)] = data

    def mkdir(self, path: str) -> None:
        self._made_dirs.add(self.expand_path(path))

    def popen_read(self, cmd: str) -> bytes:
        key = (self._cwd, cmd)
        outputs = self._rec.popens.get(key, [])
        n = self._popen_count.get(key, 0)
        if n >= len(outputs):
            raise HostMiss(f"popen #{n + 1} {cmd!r} in {self._cwd!r}")
        self._popen_count[key] = n + 1
        data = outputs[n]
        if data is None:
            raise FileNotFoundError(2, "No such file or directory", cmd)
        return data

    def written(self, path: str) -> bytes | None:
        return self._written.get(posixpath.normpath(self._abs(path)))
