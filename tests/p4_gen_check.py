"""P4 の差分テストの本体。tecsgen を通しで動かし、生成物・標準出力・終了コードを正解データと比べる。

tests/test_p4_gen.py（pytest）と tools/port/p4_progress.py（ケースごとの一致状況の一覧）が使う。

Ruby 版の外界とのやりとりは P3 のオラクル記録から再生する（RecordedHost）。記録は run 全体で
採っているので、コード生成中の `File.readable?` なども入っている。生成物の正解は
tests/golden/cases/<id>/files/ にある（採取時の作業ツリー `@WORK@/test` からの相対パス）。
Ruby 版が書き、正解データに保存していないもの（`*.rbdmp`・`tmp_*.h`）は比べない。
"""

from __future__ import annotations

import io
import json
import posixpath
import re
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from conftest import GOLDEN
from p3_oracle_data import CaseRecord, RecordedHost, load_case, text

from tecsgen import cli
from tecsgen.host import set_host

WORK_ROOT = "@WORK@/test/"
KERNEL_PREFIX = "kernel/"
PACKAGES_PREFIX = "packages/"
# tecs.timestamp は make のレシピ（touch）が作るもので、tecsgen は書かない
EXCLUDED = ("*.rbdmp", "*.pickle", "tmp_*.h", "tecs.timestamp")


def _excluded(path: str) -> bool:
    name = posixpath.basename(path)
    return any(fnmatch(name, pat) for pat in EXCLUDED)


def golden_dir(case_id: str) -> Path:
    """ケースの正解データのディレクトリ。カーネルのケースは tests/golden/kernel/cases/ にある。"""
    if case_id.startswith(KERNEL_PREFIX):
        return GOLDEN.parent / "kernel" / "cases" / case_id.removeprefix(KERNEL_PREFIX)
    if case_id.startswith(PACKAGES_PREFIX):
        return (
            GOLDEN.parent / "packages" / "cases" / case_id.removeprefix(PACKAGES_PREFIX)
        )
    return GOLDEN / case_id


def work_root(rec: CaseRecord) -> str:
    """生成物のパスの基準。通常は作業ツリーの test/、カーネル・パッケージは tecsgen を起動した作業ディレクトリ。"""
    if rec.case_id.startswith((KERNEL_PREFIX, PACKAGES_PREFIX)):
        return rec.cwd.rstrip("/") + "/"
    return WORK_ROOT


def golden_files(case_id: str) -> dict[str, bytes]:
    root = golden_dir(case_id) / "files"
    if not root.is_dir():
        return {}
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def golden_stdout(case_id: str) -> bytes:
    """正解の標準出力。カーネル・パッケージのケースは make 経由で採ったので、make が表示した行を除く。

    先頭の tecsgen の呼び出し行（"ruby ../tecsgen/tecsgen.rb …"。行末が "\\" なら次の行へ続く）と、
    末尾のレシピ（"touch tecs.timestamp" など）。tecsgen 自身はこれらを出力しない。
    """
    data = (golden_dir(case_id) / "stdout.txt").read_bytes()
    if not case_id.startswith((KERNEL_PREFIX, PACKAGES_PREFIX)):
        return data
    lines = data.split(b"\n")
    if lines[0].startswith((b"ruby ", b"/usr/bin/ruby ")):
        while lines[0].endswith(b"\\"):
            lines.pop(0)
        lines.pop(0)
    if len(lines) > 1 and lines[-1] == b"" and lines[-2].startswith(b"touch "):
        lines.pop(-2)
    return b"\n".join(lines)


def golden_meta(case_id: str) -> dict[str, Any]:
    return json.loads((golden_dir(case_id) / "meta.json").read_text(encoding="utf-8"))


_MAKE_ERROR_RE = re.compile(rb"^make: \*\*\* \[[^\]]*\] Error (\d+)$", re.MULTILINE)


def golden_exit_code(case_id: str, meta: dict[str, Any]) -> int:
    """正解の終了コード。カーネルのケースは make 経由で採ったので、make が失敗したときの終了コード（2）は
    tecsgen 自身の終了コードではない。make が標準エラー出力に書く "Error N" が tecsgen の終了コード。
    """
    code = meta["exit_code"]
    if case_id.startswith(KERNEL_PREFIX) and code == 2:
        stderr = (golden_dir(case_id) / "stderr.txt").read_bytes()
        m = _MAKE_ERROR_RE.search(stderr)
        if m is not None:
            return int(m.group(1))
    return code  # type: ignore[no-any-return]


@dataclass
class GenResult:
    case_id: str
    status: int
    stdout: bytes
    stderr: bytes
    written: dict[str, bytes]  # 作業ツリーからの相対パス → 中身
    golden: dict[str, bytes]
    golden_stdout: bytes
    golden_stderr: bytes
    golden_status: int
    missing: list[str] = field(default_factory=list)  # 正解にあって書かなかった
    extra: list[str] = field(default_factory=list)  # 書いたが正解に無い
    differ: list[str] = field(default_factory=list)  # 中身が違う
    same: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return (
            self.status == self.golden_status
            and self.stdout == self.golden_stdout
            and not self.missing
            and not self.extra
            and not self.differ
        )


def run_case(rec: CaseRecord, stdout: Any = None, stderr: Any = None) -> GenResult:
    """記録を再生しながら tecsgen を通しで実行する。

    stdout・stderr はバイト列を受け取れる出力先（pytest の capsysbinary を使うときは None）。
    """
    host = RecordedHost(rec)
    set_host(host)
    try:
        status = cli.run(rec.argv, rec.env, base_path=text(rec.globals["base"]))
    finally:
        set_host(None)
    written: dict[str, bytes] = {}
    for path, data in host.written_files().items():
        root = work_root(rec)
        if not path.startswith(root):
            raise AssertionError(f"wrote outside the work tree: {path}")
        rel = path[len(root) :]
        if not _excluded(rel):
            written[rel] = data
    meta = golden_meta(rec.case_id)
    golden = {k: v for k, v in golden_files(rec.case_id).items() if not _excluded(k)}
    res = GenResult(
        rec.case_id,
        status,
        b"",
        b"",
        written,
        golden,
        golden_stdout(rec.case_id),
        (golden_dir(rec.case_id) / "stderr.txt").read_bytes(),
        golden_exit_code(rec.case_id, meta),
    )
    for k in sorted(set(golden) | set(written)):
        if k not in written:
            res.missing.append(k)
        elif k not in golden:
            res.extra.append(k)
        elif written[k] != golden[k]:
            res.differ.append(k)
        else:
            res.same.append(k)
    return res


def run_case_captured(case_id: str) -> GenResult:
    """標準出力・標準エラー出力を取り込んで実行する（pytest の外で使う）。"""
    from tecsgen.context import reset_context
    from tecsgen.core.tecs_lang import TECS_LANG
    from tecsgen.state import reset_model_state

    ctx = reset_context()
    reset_model_state()
    TECS_LANG.setup(ctx, {"LANG": "C"})
    rec = load_case(case_id)
    out = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", write_through=True)
    err = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", write_through=True)
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, 20000))
    try:
        with redirect_stdout(out), redirect_stderr(err):
            res = run_case(rec)
    finally:
        sys.setrecursionlimit(old_limit)
    res.stdout = out.buffer.getvalue()  # type: ignore[attr-defined]
    res.stderr = err.buffer.getvalue()  # type: ignore[attr-defined]
    return res
