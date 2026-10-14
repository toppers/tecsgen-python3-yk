"""tecsgen_rcov コマンド（Ruby 版 tecsgen_rcov.rb の移植）。

カバレッジを取るための tecsgen コマンド。Ruby 版は SimpleCov を起動してから `tecsgen` を読み込む
だけの薄いラッパーで、Python 版は coverage.py を起動してから `tecsgen` の CLI を実行する。

    Usage: tecsgen_rcov [options] CDL-file.cdl

引数は `tecsgen` にそのまま渡す。coverage.py は必須の依存ではない（`uv sync --group dev`、または
`pip install coverage` で入れる）。無ければ Ruby 版の `require 'simplecov'` 失敗と同じく、
エラーを出して終了コード 1 で終わる。

カバレッジの記録は、実行ごとに追記する（Ruby 版の `--aggregate` / SimpleCov のマージに当たる）。
データは作業ディレクトリの `.coverage`、HTML は `coverage/` に書く。計測の対象は `tecsgen`
パッケージ。Ruby 版は `require 'tecsgen'` の時点から計測するので、Python 版も `tecsgen.cli` を
読み込む前に計測を始める。
"""

from __future__ import annotations

import sys
from pathlib import Path

DATA_FILE = ".coverage"
HTML_DIR = "coverage"


def run(argv: list[str]) -> int:
    """計測を始めて tecsgen を実行し、終了後に記録を保存する。終了コードは tecsgen のもの。"""
    try:
        import coverage
    except ImportError as e:
        sys.stderr.write(f"tecsgen_rcov: cannot load such file -- coverage ({e})\n")
        return 1

    package_dir = str(Path(__file__).resolve().parent)
    cov = coverage.Coverage(data_file=DATA_FILE, source=[package_dir])
    if Path(DATA_FILE).exists():
        cov.load()
    cov.start()
    print("simplecov begin")
    status = 0
    try:
        # 計測を始めた後で読み込む（モジュールの先頭の文も計測の対象にする）
        from tecsgen import cli

        status = cli.run(argv)
        print("simplecov end")
    finally:
        cov.stop()
        cov.save()
        try:
            cov.html_report(directory=HTML_DIR)
        except coverage.exceptions.CoverageException as e:
            # 対象を1つも実行しなかったとき（`--help` だけなど）。記録の保存は済んでいる
            sys.stderr.write(f"tecsgen_rcov: no coverage report: {e}\n")
    return status


def main() -> None:
    sys.exit(run(sys.argv[1:]))
