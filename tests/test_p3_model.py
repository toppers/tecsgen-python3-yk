"""P3: 構文解析・意味解析の後のモデルとエラー・警告が Ruby 版と一致することの差分テスト。

Ruby 版オラクル（tests/ruby/p3_oracle.rb）が記録した3つのチェックポイント
（parse: 構文解析の直後、sem1: semantics_analisys_1 の後、sem2: semantics_analisys_2 の後）で、
次のものを比べる。

- それまでに標準出力へ出た内容（エラー・警告の行）が、正解データの stdout の先頭と一致する
- エラー・警告の件数
- モデルのダンプ（tests/p3_model_dump.py）

ファイルシステムと cpp は記録から再生する（RecordedHost）。プラグインを読むケースは、
プラグイン機構を移植する P5 まで比較しない。
"""

from __future__ import annotations

import sys
from typing import Any

import pytest
from conftest import GOLDEN
from p3_model_dump import compare, dump_model
from p3_oracle_data import CaseRecord, RecordedHost, case_ids, load_case, text

from tecsgen import cli
from tecsgen.context import TecsgenContext
from tecsgen.core.generator import Generator
from tecsgen.core.tecsgen import TECSGEN
from tecsgen.host import set_host

# P4 以降で移植するファイル（tool_info.rb）とプラグインのクラス変数は比べない
SKIP_CV = {
    "TOOL_INFO",
    "TECSGEN::Join_location",
    "TECSGEN::Cell_location",
    # プラグインの基底クラス（P5）
    "ThroughPlugin",
}

CHECKPOINTS = ("parse", "sem1", "sem2")


def _cases() -> list[Any]:
    params = []
    for cid in case_ids():
        rec = load_case(cid)
        marks = []
        if rec.uses_plugin:
            marks.append(pytest.mark.skip(reason="プラグインを使う（P5）"))
        params.append(pytest.param(cid, marks=marks, id=cid))
    return params


def _strip_cv(dump: dict[str, Any]) -> dict[str, Any]:
    return {
        "root": dump["root"],
        "cv": {k: v for k, v in dump["cv"].items() if k not in SKIP_CV},
    }


def _run(
    rec: CaseRecord, ctx: TecsgenContext, capsysbinary: Any
) -> list[tuple[Any, ...]]:
    """Python 版を記録と同じ入力で動かし、チェックポイントごとの (名前, 標準出力, 件数, ダンプ) を返す。"""
    set_host(RecordedHost(rec))
    ctx.argv = list(rec.argv)
    ctx.tecsgen_base_path = text(rec.globals["base"])
    cli.init(ctx, rec.env)
    capsysbinary.readouterr()  # init までの出力（バナーは標準エラー出力）は捨てない
    out = b""
    results: list[tuple[Any, ...]] = []
    tecsgen = TECSGEN()
    TECSGEN._current_tecsgen = tecsgen
    steps = (
        ("parse", lambda: tecsgen.syntax_analisys(ctx.argv)),
        ("sem1", tecsgen.semantics_analisys_1),
        ("sem2", tecsgen.semantics_analisys_2),
    )
    old_limit = sys.getrecursionlimit()
    for name, step in steps:
        step()
        out += capsysbinary.readouterr().out
        sys.setrecursionlimit(max(old_limit, 20000))
        try:
            dump = dump_model(tecsgen.get_root_namespace())
        finally:
            sys.setrecursionlimit(old_limit)
        counts = (Generator.get_n_error(), Generator.get_n_warning())
        results.append((name, out, counts, dump))
    return results


@pytest.mark.parametrize("case_id", _cases())
def test_model_matches_ruby(
    case_id: str,
    fresh_state: TecsgenContext,
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    rec = load_case(case_id)
    golden_out = (GOLDEN / case_id / "stdout.txt").read_bytes()
    if rec.exit_error == "SystemStackError":
        pytest.skip("Ruby 版は SystemStackError で止まる（test_p3_cli で確認する）")

    results = _run(rec, fresh_state, capsysbinary)
    for (name, out, counts, dump), cp in zip(results, rec.checkpoints, strict=True):
        assert name == cp.at
        assert out == golden_out[: cp.out], f"{name}: stdout"
        assert counts == (cp.n_error, cp.n_warning), f"{name}: error/warning count"
        diffs = compare(_strip_cv(cp.dump), _strip_cv(dump))
        assert not diffs, f"{name}: model differs\n" + "\n".join(diffs)
