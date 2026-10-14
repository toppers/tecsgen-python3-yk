"""P8 tecsflow: Ruby 版 tecsflow との差分テスト。

tests/golden/tecsflow/<id>.json.gz は、Ruby 版で `make tecsflow`（tecsgen → tcflow → tecsflow）を
実行して採った記録（tools/port/collect_tecsflow_oracle.py）。

Python 版では、入力（inputs/、TECS の test/ の一部）に Python 版の tecsgen を実行して
`tecsgen.pickle` を作り、tcflow の関数リストは Ruby 版が書いたものを JSON にした記録を置いて、
tecsflow を実行する。tcflow は別に P7 で検証しているので、ここでは tecsflow の処理
（モデルの pickle 受け渡しを含む）だけを比べる。標準出力・標準エラー出力・終了コードが一致すること。

違いを許すのは、Ruby 版の保存ファイル名（`tecsgen.rbdmp`・`tcflow.rbdmp`）と
Python 版（`tecsgen.pickle`・`tcflow.json`）だけで、メッセージ中の名前を置き換えてから比べる。
"""

from __future__ import annotations

import gzip
import json
import os
import shutil
import sys
import tomllib
from pathlib import Path
from typing import Any

import pytest

from tecsgen import cli
from tecsgen.context import reset_context
from tecsgen.tecsflow import run as run_tecsflow

GOLDEN = Path(__file__).parent / "golden" / "tecsflow"
INPUTS = GOLDEN / "inputs"
CASES = {
    c["id"]: c
    for c in tomllib.loads((GOLDEN / "cases.toml").read_text(encoding="utf-8"))["case"]
}


def _load(case_id: str) -> dict[str, Any]:
    with gzip.open(GOLDEN / f"{case_id}.json.gz", "rb") as f:
        return json.loads(f.read().decode("ascii"))


def _b(s: str) -> bytes:
    return s.encode("latin-1")


def _py_name(text: str) -> str:
    """Ruby 版のメッセージ中の保存ファイル名を、Python 版の名前にそろえる。"""
    return text.replace("tecsgen.rbdmp", "tecsgen.pickle").replace(
        "tcflow.rbdmp", "tcflow.json"
    )


def _generate(case: dict[str, Any], work: Path) -> None:
    """Python 版の tecsgen を実行して、gen/ に tecsgen.pickle を作る。"""
    tecspath = f"{cli.PACKAGE_DIR}/tecs"
    args = [a.replace("{TECSPATH}", tecspath) for a in case["args"]]
    reset_context()
    rc = cli.run(args, {"LANG": "C"})
    assert rc == 0, f"tecsgen failed: {args}"


@pytest.mark.skipif(
    sys.platform != "linux" or shutil.which("gcc") is None,
    reason="tecsgen の import_C が Linux の gcc -E を使う（正解データは Linux で採取）",
)
@pytest.mark.parametrize("case_id", sorted(CASES))
def test_tecsflow_matches_ruby(
    case_id: str,
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = CASES[case_id]
    record = _load(case_id)
    shutil.copytree(INPUTS, tmp_path / "test")
    work = tmp_path / "test" / case["cwd"]
    monkeypatch.chdir(work)

    _generate(case, work)
    capfdbinary.readouterr()  # tecsgen の出力は比べない

    gen = work / record["gen_dir"]
    assert (gen / "tecsgen.pickle").is_file()
    (gen / "tcflow.json").write_text(
        json.dumps(record["funclist"], ensure_ascii=True, indent=1) + "\n",
        encoding="ascii",
    )

    flow = record["tecsflow"]
    rc = run_tecsflow(flow["args"])
    captured = capfdbinary.readouterr()
    assert rc == flow["returncode"]
    assert captured.out == _b(_py_name(flow["stdout"]))
    assert captured.err == _b(_py_name(flow["stderr"]))


# --- エラー系・オプション（Ruby 版 tecsflow.rb で確認した挙動） -----------------------------


def _run_in_empty_dir(
    argv: list[str],
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[int, str, str]:
    monkeypatch.chdir(tmp_path)
    rc = run_tecsflow(argv)
    captured = capfdbinary.readouterr()
    return rc, captured.out.decode("latin-1"), captured.err.decode("latin-1")


def test_missing_model_file(
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "gen").mkdir()
    rc, out, err = _run_in_empty_dir([], tmp_path, capfdbinary, monkeypatch)
    assert rc == 1
    assert out == (
        "reading 'gen/tecsgen.pickle'\n"
        "#<Errno::ENOENT: No such file or directory @ rb_sysopen - gen/tecsgen.pickle>\n"
        "fatal: fail to load 'gen/tecsgen.pickle' in file reading\n"
    )
    assert err.startswith("tecsflow version 1.G.0 (tecsgen version ")


def test_help(
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rc, out, err = _run_in_empty_dir(["-h"], tmp_path, capfdbinary, monkeypatch)
    assert rc == 1
    assert err.startswith("tecsflow version 1.G.0")
    assert out.startswith("Usage: tecsflow [options]\n")
    assert "-g, --gen=dir" in out


def test_invalid_option_is_warned(
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Makefile の tecsflow_u が渡す -U は未定義で、警告のあと処理が続く。"""
    rc, _, err = _run_in_empty_dir(["-U"], tmp_path, capfdbinary, monkeypatch)
    assert rc == 1  # モデルが無いので失敗する
    assert "tecsflow: invalid option: -U\n" in err
    assert os.path.exists(tmp_path) is True
