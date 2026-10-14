"""P8 tecsgen_rcov: カバレッジを取りながら tecsgen を動かす。

Ruby 版（SimpleCov）と違い coverage.py を使うので、レポートの中身は比べない。比べるのは、
tecsgen の標準出力・終了コードをそのまま通すことと、標準出力の前後に出す
`simplecov begin` / `simplecov end`、記録が実行ごとに追記されること、coverage.py が無いときの終了。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tecsgen import tecsgen_rcov


def test_without_coverage_py_fails_like_load_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setitem(sys.modules, "coverage", None)

    assert tecsgen_rcov.run(["--version"]) == 1
    assert "cannot load such file -- coverage" in capsys.readouterr().err


def test_runs_tecsgen_and_records_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    pytest.importorskip("coverage")
    monkeypatch.chdir(tmp_path)

    status = tecsgen_rcov.run(["--version"])

    captured = capsys.readouterr()
    assert status == 0
    assert captured.out.startswith("simplecov begin\n")
    assert captured.out.endswith("simplecov end\n")
    assert (tmp_path / tecsgen_rcov.DATA_FILE).is_file()
    assert (tmp_path / tecsgen_rcov.HTML_DIR / "index.html").is_file()
