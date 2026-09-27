"""P4: tecsgen を通しで動かし、生成物（gen/）・標準出力・終了コードが Ruby 版と一致することの差分テスト。

プラグインを使わないケースが対象（プラグインを使うケースは P5）。比べ方は tests/p4_gen_check.py。
"""

from __future__ import annotations

from typing import Any

import pytest
from p3_oracle_data import case_ids, load_case
from p4_gen_check import run_case

from tecsgen.context import TecsgenContext


def _cases() -> list[Any]:
    params = []
    for cid in case_ids():
        rec = load_case(cid)
        marks = []
        if rec.uses_plugin:
            marks.append(pytest.mark.skip(reason="プラグインを使う（P5）"))
        elif rec.exit_error == "SystemStackError":
            marks.append(pytest.mark.skip(reason="test_p3_cli で確認する"))
        params.append(pytest.param(cid, marks=marks, id=cid))
    return params


@pytest.mark.parametrize("case_id", _cases())
def test_generated_files_match_ruby(
    case_id: str,
    fresh_state: TecsgenContext,
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    res = run_case(load_case(case_id))
    captured = capsysbinary.readouterr()
    assert captured.out == res.golden_stdout, "stdout"
    assert res.status == res.golden_status, "exit status"
    assert not res.missing, f"not generated: {res.missing}"
    assert not res.extra, f"unexpected files: {res.extra}"
    for name in res.differ:
        assert res.written[name] == res.golden[name], name
