"""P7 tcflow: Ruby 版 tcflow との差分テスト。

tests/golden/tcflow/<id>.json.gz は、Ruby 版 tcflow を実行して採った記録
（tools/port/collect_tcflow_oracle.py）。同じ入力を Python 版で処理し、各実行の標準出力・
標準エラー出力・終了コードと、作業ディレクトリに書かれたファイル、関数リストが一致することを確かめる。

違いを許すのは、Ruby 版の保存形式（`tcflow.rbdmp`、Marshal）と Python 版（`tcflow.json`）の
ファイル名だけで、メッセージ中の名前を置き換えてから比べる。
cpp（`-c`）は、記録した出力を返す Host で再生するので、gcc が無い環境でも動く。
"""

from __future__ import annotations

import gzip
import json
import os
import shutil
from pathlib import Path
from typing import Any

import pytest

from tecsgen.host import Host, set_host
from tecsgen.tcflow import run

GOLDEN = Path(__file__).parent / "golden" / "tcflow"
INPUTS = GOLDEN / "inputs"
CASE_IDS = sorted(p.name.removesuffix(".json.gz") for p in GOLDEN.glob("*.json.gz"))


def _load(case_id: str) -> dict[str, Any]:
    with gzip.open(GOLDEN / f"{case_id}.json.gz", "rb") as f:
        return json.loads(f.read().decode("ascii"))


def _b(s: str) -> bytes:
    return s.encode("latin-1")


class ReplayHost(Host):
    """cpp の実行を、記録した出力の再生に置き換える。ほかは実際のファイルシステムを使う。"""

    def __init__(self, cwd: str, cpp_outputs: dict[str, str]) -> None:
        super().__init__(cwd)
        self._cpp_outputs = cpp_outputs

    def popen_read(self, cmd: str) -> bytes:
        # 記録は "gcc -E gen/tmp_X.c" の出力を gen/tmp_X.c_2.c に残している
        tmp = cmd.split()[-1]
        return _b(self._cpp_outputs[f"{tmp}_2.c"])


def _rb_name(text: str) -> str:
    """Ruby 版のメッセージ中の保存ファイル名を、Python 版の名前にそろえる。"""
    return text.replace("tcflow.rbdmp", "tcflow.json")


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_tcflow_matches_ruby(
    case_id: str,
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    record = _load(case_id)
    cases = {c["id"]: c for c in _cases()}
    case = cases[case_id]

    for name in case.get("dirs", ["gen"]):
        (tmp_path / name).mkdir()
    for name in case["inputs"]:
        shutil.copy(INPUTS / name, tmp_path / name)

    cpp_outputs = {k: v for k, v in record["files"].items() if k.endswith("_2.c")}
    monkeypatch.chdir(tmp_path)
    set_host(ReplayHost(str(tmp_path).replace(os.sep, "/"), cpp_outputs))
    try:
        for step in record["steps"]:
            rc = run(step["args"])
            captured = capfdbinary.readouterr()
            where = f"{case_id} {step['args']}"
            assert rc == step["returncode"], where
            assert captured.out == _b(_rb_name(step["stdout"])), where
            assert captured.err == _b(_rb_name(step["stderr"])), where
    finally:
        set_host(None)

    # cpp の一時ファイルなど（tcflow.json 以外）
    for rel, expected in record["files"].items():
        if rel.endswith("_2.c"):
            continue  # cpp の出力。再生した内容をそのまま書くので比べる意味が無い
        assert (tmp_path / rel).read_bytes() == _b(expected), f"{case_id} {rel}"

    dumps = sorted(tmp_path.rglob("tcflow.json"))
    if record["funclist"] is None:
        assert dumps == [], case_id
    else:
        assert len(dumps) == 1, case_id
        actual = json.loads(dumps[0].read_text(encoding="ascii"))
        assert actual == record["funclist"], case_id
        # 関数の並び（Hash の挿入順）も同じ
        assert list(actual) == list(record["funclist"]), case_id


def _cases() -> list[dict[str, Any]]:
    import tomllib

    return tomllib.loads((GOLDEN / "cases.toml").read_text(encoding="utf-8"))["case"]
