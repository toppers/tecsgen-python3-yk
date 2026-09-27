"""P3: tecsgen の CLI（cli.run）を通しで動かす差分テストのうち、P3 の範囲で比べられるもの。

コード生成まで通しで比べる差分テストは tests/test_p4_gen.py。ここでは P4 の比較から外している
ケースを比べる。

- ErrorCase/attribute-err: Ruby 版は elements_eval_const の無限再帰で SystemStackError になる。
  Python 版は RecursionError を捕まえて、Ruby と同じく標準出力の内容と終了コード 1 を再現する
  （ユーザー決定 2026-09-27。標準エラー出力は例外名の行だけを合わせ、バックトレースは比べない）
"""

from __future__ import annotations

import pytest
from conftest import GOLDEN
from p3_oracle_data import RecordedHost, load_case, text

from tecsgen import cli
from tecsgen.context import TecsgenContext
from tecsgen.host import set_host


def test_attribute_err_stack_overflow_like_ruby(
    fresh_state: TecsgenContext, capsysbinary: pytest.CaptureFixture[bytes]
) -> None:
    case_id = "ErrorCase/attribute-err"
    rec = load_case(case_id)
    assert rec.exit_error == "SystemStackError"
    set_host(RecordedHost(rec))

    status = cli.run(rec.argv, rec.env, base_path=text(rec.globals["base"]))

    captured = capsysbinary.readouterr()
    assert status == 1
    assert captured.out == (GOLDEN / case_id / "stdout.txt").read_bytes()
    assert b"stack level too deep (SystemStackError)" in captured.err
