"""`tecsgen-path`（tecs/ を含むディレクトリを返すコマンド）のテスト。"""

from pathlib import Path

import pytest

from tecsgen import libpath


def test_prints_directory_containing_tecs(capsys: pytest.CaptureFixture[str]) -> None:
    assert libpath.main() == 0
    out = capsys.readouterr().out
    assert out.endswith("\n")
    path = out.strip()
    assert "\\" not in path  # 区切りは / にそろえる
    assert (Path(path) / "tecs" / "sMalloc.cdl").is_file()


def test_fails_when_tecs_is_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(libpath, "PACKAGE_DIR", tmp_path.as_posix())
    assert libpath.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "tecs/ not found" in captured.err
