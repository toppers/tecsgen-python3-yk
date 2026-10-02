"""配布物に標準 CDL ライブラリ（tecs/）が同梱されていることの確認。"""

from pathlib import Path

from tecsgen import cli


def test_bundled_tecs_library_exists() -> None:
    tecs = Path(cli.PACKAGE_DIR) / "tecs"
    assert (tecs / "sMalloc.cdl").is_file()
    assert (tecs / "tecs.h").is_file()
