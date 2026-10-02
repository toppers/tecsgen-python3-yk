"""P6: tecsmerge を Ruby 版の実行結果（tests/golden/tecsmerge/、tools/golden/collect_tecsmerge.py で採取）と比べる。

標準出力・終了コード・実行後のファイル一式（バックアップ `_1` を含む）がバイト単位で一致すること。
標準エラー出力も一致させる。ただし Ruby 版が例外（バックトレース付き）で終わるケースは、
バックトレースより前の行だけが先頭から一致すること。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tecsgen import tecsmerge

DATA = Path(__file__).parent / "golden" / "tecsmerge"
CASES = sorted(p.stem for p in DATA.glob("*.json"))
ENC = "latin-1"


def _snapshot(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)).replace("\\", "/"): p.read_bytes().decode(ENC)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


@pytest.mark.parametrize("case", CASES)
def test_tecsmerge_matches_ruby(
    case: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    data = json.loads((DATA / f"{case}.json").read_text(encoding="utf-8"))
    for rel, content in data["input"].items():
        f = tmp_path / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(content.encode(ENC))
    # Ruby 版は src/・dst/ を空にしないので、空のディレクトリは作らない（入力にあるファイルだけ）
    monkeypatch.chdir(tmp_path)

    status = tecsmerge.run(data["argv"])

    captured = capsysbinary.readouterr()
    assert status == data["returncode"]
    assert captured.out.decode(ENC) == data["stdout"]
    assert _snapshot(tmp_path) == data["tree"]
    if data["crash_ok"] and data["returncode"] != 0:
        # Ruby 版の標準エラー出力は、例外のとき末尾にバックトレースが付く。先頭の行だけを比べる
        ours = [
            ln
            for ln in captured.err.decode(ENC).splitlines()
            if not ln.startswith("tecsmerge:")
        ]
        assert ours == data["stderr"].splitlines()[: len(ours)]
    else:
        assert captured.err.decode(ENC) == data["stderr"]
