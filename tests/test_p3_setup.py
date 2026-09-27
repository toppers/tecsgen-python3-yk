"""P3: 起動時の処理（オプション解析・言語設定・setup）が Ruby 版と同じ状態を作ることの差分テスト。

Ruby 版オラクルが run1 の直前に記録した $import_path・$target などと比べる。
ファイルシステムへの問い合わせ（TECSPATH の下のディレクトリの一覧など）は記録から再生する。
"""

from __future__ import annotations

import pytest
from p3_oracle_data import RecordedHost, case_ids, load_case, text

from tecsgen import cli
from tecsgen.context import TecsgenContext
from tecsgen.host import set_host


@pytest.mark.parametrize("case_id", case_ids())
def test_setup_matches_ruby(case_id: str, fresh_state: TecsgenContext) -> None:
    rec = load_case(case_id)
    g = rec.globals
    set_host(RecordedHost(rec))
    ctx = fresh_state
    ctx.argv = list(rec.argv)
    ctx.tecsgen_base_path = text(g["base"])
    cli.init(ctx, rec.env)

    assert ctx.argv == [text(a) for a in g["argv"]]
    assert ctx.tecspath == text(g["tecspath"])
    assert ctx.import_path == [text(p) for p in g["import_path"]]
    assert ctx.run_dir == text(g["run_dir"])
    assert ctx.gen == text(g["gen"])
    assert ctx.target == text(g["target"])
    assert ctx.define == [text(d) for d in g["define"]]
    assert ctx.cpp == text(g["cpp"])


def test_option_parser_ruby_behaviour(fresh_state: TecsgenContext) -> None:
    ctx = fresh_state
    parser = cli.make_option_parser(ctx)
    rest = parser.parse(
        ["a.cdl", "-Igen", "-I", "x", "--gen=g2", "-Rv", "--no-b", "b.cdl"]
    )
    assert rest == ["a.cdl", "b.cdl"]
    assert ctx.import_path[-2:] == ["gen", "x"]
    assert ctx.gen == ctx.gen_base == "g2"
    assert ctx.ram_initializer and ctx.verbose and ctx.no_banner


def test_option_parser_errors(fresh_state: TecsgenContext) -> None:
    from tecsgen.ruby_optparse import OptionParserError

    parser = cli.make_option_parser(fresh_state)
    with pytest.raises(OptionParserError, match="invalid option: -x"):
        parser.parse(["a.cdl", "-x", "b.cdl"])
    assert parser.remaining == ["b.cdl"]
    with pytest.raises(OptionParserError, match="ambiguous option: --generate"):
        parser.parse(["--generate", "d"])
    # 完全一致は前方一致より優先する（--gen は --generate-* にも前方一致する）
    assert parser.parse(["--gen", "d"]) == []
