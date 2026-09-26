"""P1（Node・エラー処理・入出力）の単体テスト。期待値は Ruby 版のソースから読み取った挙動。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from tecsgen.context import TecsgenContext, dbg_print
from tecsgen.core.generate import AppFile, MemFile
from tecsgen.core.generator import Generator, Token, print_report
from tecsgen.core.messages import TECSMsg
from tecsgen.core.plugin import CFile
from tecsgen.core.syntaxobj import node as node_mod
from tecsgen.core.syntaxobj.namedlist import NamedList
from tecsgen.core.syntaxobj.node import BDNode, Node
from tecsgen.core.tecs_lang import TECS_LANG, Console
from tecsgen.syntax.tecsio import TECSIO


def stdout_bytes(capfdbinary: pytest.CaptureFixture[bytes]) -> bytes:
    return capfdbinary.readouterr().out


# --- Generator: エラー・警告・情報 --------------------------------------------


def test_error_without_locale(capfdbinary: pytest.CaptureFixture[bytes]) -> None:
    Generator.error("S2001 '$1' duplicate $2", "foo", "celltype")
    assert stdout_bytes(capfdbinary) == b"error: S2001 'foo' duplicate celltype\n"
    assert Generator.get_n_error() == 1


def test_parse_time_uses_current_locale_not_node_locale(
    capfdbinary: pytest.CaptureFixture[bytes],
) -> None:
    """構文解析中（end_all_parse 前）は、渡した locale ではなく解析中の位置を出す。"""
    Generator.push_parser(object())
    Generator.set_current_locale(("a.cdl", 3, 5))
    Generator.warning2(("b.cdl", 9, 1), "W1002 $1: msg", "x")
    assert stdout_bytes(capfdbinary).startswith(b"a.cdl:3:5: warning: W1002 x: ")
    assert Generator.get_n_warning() == 1


def test_after_parse_uses_given_locale(
    capfdbinary: pytest.CaptureFixture[bytes],
) -> None:
    Generator.push_parser(object())
    Generator.set_current_locale(("a.cdl", 3, 5))
    Generator.pop_parser()
    Generator.end_all_parse()
    Generator.info2(("b.cdl", 9, 1), "I9999 hello $1", 7)
    Generator.error2(None, "S9999 no locale")
    # locale が nil のときは、nest = -1 なので Ruby の配列の末尾（最後に解析した位置）を使う
    assert stdout_bytes(capfdbinary) == (
        b"b.cdl:9:1: info: I9999 hello 7\na.cdl:3:5: error: S9999 no locale\n"
    )
    assert (Generator.get_n_error(), Generator.get_n_info()) == (1, 1)


def test_args_use_ruby_to_s(capfdbinary: pytest.CaptureFixture[bytes]) -> None:
    Generator.error("S9999 [$1] [$2] [$3] [$4]", None, True, 1.0, ["a", 1])
    assert stdout_bytes(capfdbinary) == b'error: S9999 [] [true] [1.0] [["a", 1]]\n'


def test_warning_without_number_raises() -> None:
    """Ruby 版は番号の無い警告で nil.to_sym の NoMethodError になる。"""
    with pytest.raises(TypeError):
        Generator.warning("no number")


def test_localized_message_ja(
    fresh_state: TecsgenContext, capfdbinary: pytest.CaptureFixture[bytes]
) -> None:
    TECS_LANG.setup(fresh_state, {"LANG": "ja_JP.eucJP"})
    Generator.error("B1003 Unexpected EOF")
    assert stdout_bytes(capfdbinary) == "error: B1003 予期しない EOF です\n".encode(
        "euc_jp"
    )


@pytest.mark.parametrize(
    ("errors", "warnings", "expected"),
    [
        (0, 0, b""),
        (1, 0, b"1 error\n"),
        (2, 0, b"2 errors\n"),
        (0, 1, b"1 warning\n"),
        (3, 2, b"3 errors  2 warnings\n"),
    ],
)
def test_print_report(
    errors: int,
    warnings: int,
    expected: bytes,
    capfdbinary: pytest.CaptureFixture[bytes],
) -> None:
    for _ in range(errors):
        Generator.error("S9999 e")
    for _ in range(warnings):
        Generator.warning("W9999 w")
    capfdbinary.readouterr()
    print_report()
    assert stdout_bytes(capfdbinary) == expected


def test_parser_nesting() -> None:
    a, b = object(), object()
    Generator.push_parser(a)
    Generator.push_parser(b)
    assert (Generator.get_nest(), Generator.current_parser()) == (1, b)
    Generator.pop_parser()
    assert (Generator.get_nest(), Generator.current_parser()) == (0, a)


def test_statement_specifier_stack() -> None:
    Generator.push_parser(object())
    Generator.add_statement_specifier("s1")
    Generator.add_statement_specifier("s2")
    assert Generator.get_statement_specifier() == ["s1", "s2"]
    assert Generator.get_statement_specifier() is None


# --- Token --------------------------------------------------------------------


def test_token() -> None:
    t = Token("tTask", "a.cdl", 2, 7)
    assert (t.to_s(), t.get_name(), t.locale()) == ("tTask", "tTask", ("a.cdl", 2, 7))
    assert t == "tTask"
    assert t == Token("tTask", "b.cdl", 1, 1)
    with pytest.raises(TypeError):
        _ = t == 1


# --- Node ---------------------------------------------------------------------


def test_node_records_current_locale(capfdbinary: pytest.CaptureFixture[bytes]) -> None:
    Generator.push_parser(object())
    Generator.set_current_locale(("n.cdl", 4, 2))
    n = Node()
    assert n.get_locale() == ("n.cdl", 4, 2)
    assert n.locale_str() == "locale=(n.cdl, 4)"
    Generator.end_all_parse()
    Generator.set_current_locale(("other.cdl", 1, 1))
    n.cdl_error("S9999 bad $1", "x")
    n.cdl_warning("W9999 careful")
    n.cdl_error3(("c.cdl", 8, 1), "S9998 see below")
    assert stdout_bytes(capfdbinary) == (
        b"n.cdl:4:2: error: S9999 bad x\n"
        b"n.cdl:4:2: warning: W9999 careful\n"
        b"other.cdl:1:1: error: S9998 see below\n"
        b"check: c.cdl: line 8 for above error\n"
    )


def test_node_without_locale() -> None:
    n = Node()
    assert n.get_locale() is None
    assert n.locale_str() == "locale=(?)"


def test_bdnode_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(node_mod, "_current_import", lambda: None)

    class Named(BDNode):
        def get_name(self) -> str:
            return "cell1"

    n = Named()
    with pytest.raises(RuntimeError, match="Node have no owner Named cell1"):
        n.get_owner()
    owner = object()
    n.set_owner(owner)
    assert n.get_owner() is owner


# --- NamedList ----------------------------------------------------------------


class Item(Node):
    def __init__(self, name: Any) -> None:
        super().__init__()
        self._name = name
        self.cloned_with: tuple[Any, ...] | None = None

    def get_name(self) -> Any:
        return self._name

    def clone_for_composite(self, ct_name: Any, cell_name: Any, locale: Any) -> Item:
        c = Item(f"{self._name}_c")
        c.cloned_with = (ct_name, cell_name, locale)
        return c


def test_namedlist_keeps_order_and_reports_duplicates(
    capfdbinary: pytest.CaptureFixture[bytes],
) -> None:
    Generator.push_parser(object())
    Generator.set_current_locale(("d.cdl", 1, 1))
    a = Item("a")
    Generator.set_current_locale(("d.cdl", 5, 3))
    nl = NamedList(a, "attribute")
    nl.add_item(Item("b"))
    nl.add_item(Item("a"))
    assert [i.get_name() for i in nl.get_items()] == ["a", "b"]
    assert nl.get_item("a") is a
    assert nl.get_item("zz") is None
    assert stdout_bytes(capfdbinary) == (
        b"d.cdl:5:3: error: S2001 'a' duplicate attribute\nprevious: d.cdl: line 1 'a' defined here\n"
    )


def test_namedlist_accepts_nil_first_item() -> None:
    nl = NamedList(None, "x")
    assert nl.get_items() == []


def test_namedlist_change_and_delete() -> None:
    a1, b, a2 = Item("a"), Item("b"), Item("a")
    nl = NamedList(a1, "x")
    nl.add_item(b)
    nl.change_item(a2)
    assert nl.get_items() == [b, a2]
    assert nl.get_item("a") is a2
    nl.del_item(b)
    assert nl.get_items() == [a2]
    assert nl.get_item("b") is None


def test_namedlist_rejects_non_symbol() -> None:
    with pytest.raises(TypeError):
        NamedList(Item(1), "x")
    nl = NamedList(None, "x")
    with pytest.raises(TypeError):
        nl.get_item(1)


def test_namedlist_clone_for_composite() -> None:
    nl = NamedList(Item("j1"), "join")
    cl = nl.clone_for_composite("tComp", "cell", ("f", 1, 1))
    assert [i.get_name() for i in cl.get_items()] == ["j1_c"]
    assert cl.get_item("j1_c").cloned_with == ("tComp", "cell", ("f", 1, 1))
    # 元のリストは変わらない
    assert [i.get_name() for i in nl.get_items()] == ["j1"]


# --- TECSIO -------------------------------------------------------------------


def test_tecsio_splits_only_on_lf(tmp_path: Path) -> None:
    f = tmp_path / "a.cdl"
    f.write_bytes(b"a\r\nb\rc\nlast")
    assert list(TECSIO.foreach(f)) == ["a\r\n", "b\rc\n", "last"]


@pytest.mark.parametrize(
    ("kcode", "codec", "text"),
    [
        ("euc", "euc_jp", "日本語"),
        ("sjis", "cp932", "表示"),
        ("utf8", "utf-8", "日本語"),
    ],
)
def test_tecsio_decodes_with_file_charset(
    fresh_state: TecsgenContext, tmp_path: Path, kcode: str, codec: str, text: str
) -> None:
    fresh_state.kcode = kcode
    TECS_LANG.setup(fresh_state, {"LANG": "C"})
    f = tmp_path / "a.cdl"
    f.write_bytes(f"/* {text} */\n".encode(codec))
    assert list(TECSIO.foreach(f)) == [f"/* {text} */\n"]


def test_tecsio_round_trips_invalid_bytes(tmp_path: Path) -> None:
    """文字コードとして不正なバイト列も、読んで書けば元に戻る（Ruby の ASCII-8BIT と同じ）。"""
    raw = b"/* \xff\xfe \xe3 */\n"
    src = tmp_path / "a.cdl"
    src.write_bytes(raw)
    out = tmp_path / "out.h"
    f = AppFile.open(str(out))
    for line in TECSIO.foreach(src):
        f.print(line)
    f.close()
    AppFile.update()
    assert out.read_bytes() == raw


# --- AppFile ------------------------------------------------------------------


def test_appfile_writes_tmp_then_renames(tmp_path: Path) -> None:
    name = str(tmp_path / "x.h")
    f = AppFile.open(name)
    f.print("line1\n")
    f.close()
    assert Path(name + ".tmp").exists()
    # 2回目は追記
    f = AppFile.open(name)
    f.puts("line2")
    f.close()
    AppFile.update()
    assert Path(name).read_bytes() == b"line1\nline2\n"
    assert not Path(name + ".tmp").exists()


def test_appfile_keeps_unchanged_file(
    fresh_state: TecsgenContext,
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
) -> None:
    fresh_state.verbose = True
    target = tmp_path / "x.h"
    target.write_bytes(b"same\n")
    mtime_before = target.stat().st_mtime_ns
    f = AppFile.open(str(target))
    f.print("same\n")
    f.close()
    AppFile.update()
    assert target.stat().st_mtime_ns == mtime_before
    assert not Path(str(target) + ".tmp").exists()
    assert stdout_bytes(capfdbinary) == f"{target} not changed\n".encode()


def test_appfile_replaces_changed_file(
    fresh_state: TecsgenContext,
    tmp_path: Path,
    capfdbinary: pytest.CaptureFixture[bytes],
) -> None:
    fresh_state.verbose = True
    target = tmp_path / "x.h"
    target.write_bytes(b"old\n")
    f = AppFile.open(str(target))
    f.print("new\n")
    f.close()
    AppFile.update()
    assert target.read_bytes() == b"new\n"
    assert stdout_bytes(capfdbinary) == (
        f"{target} changed\nrenaming '{target}.tmp' => '{target}'\n".encode()
    )


def test_appfile_force_overwrite(fresh_state: TecsgenContext, tmp_path: Path) -> None:
    fresh_state.force_overwrite = True
    target = tmp_path / "x.h"
    f = AppFile.open(str(target))
    f.print("direct\n")
    f.close()
    assert target.read_bytes() == b"direct\n"
    AppFile.update()
    assert not Path(str(target) + ".tmp").exists()


def test_appfile_writes_messages_in_file_charset(
    fresh_state: TecsgenContext, tmp_path: Path
) -> None:
    fresh_state.kcode = "euc"
    TECS_LANG.setup(fresh_state, {"LANG": "C"})
    target = tmp_path / "x.h"
    f = AppFile.open(str(target))
    f.print(TECSMsg.get("note"))
    f.close()
    AppFile.update()
    assert target.read_bytes() == TECSMsg.get("note").encode("euc_jp")
    assert "tecsgen" in TECSMsg.get("note")


def test_memfile() -> None:
    m = MemFile()
    m.print("a")
    m.print(1)
    assert m.get_string() == "a1"


# --- CFile・Console -----------------------------------------------------------


def test_cfile_puts_always_appends_newline(tmp_path: Path) -> None:
    p = tmp_path / "gen.cdl"
    f = CFile.open(str(p), "w")
    f.puts("a\n")
    f.printf("%s=%d\n", "x", 3)
    f.close()
    assert p.read_bytes() == b"a\n\nx=3\n"


@pytest.mark.parametrize(
    ("env", "kcode", "expected_codec"),
    [
        ({"LANG": "C"}, None, "utf-8"),  # コンソールが BINARY なら変換しない
        (
            {"LANG": "ja_JP.UTF-8"},
            "euc",
            "euc_jp",
        ),  # コンソールが BINARY でなければ CDL の文字コード
        ({"LANG": "C"}, "euc", "utf-8"),  # 判定はコンソール側の変数（Ruby 版のとおり）
        ({"LANG": "C"}, "sjis", "cp932"),  # Shift_JIS で開いたファイルは IO が変換する
    ],
)
def test_cfile_codec(
    fresh_state: TecsgenContext,
    tmp_path: Path,
    env: dict[str, str],
    kcode: str | None,
    expected_codec: str,
) -> None:
    fresh_state.kcode = kcode
    TECS_LANG.setup(fresh_state, env)
    p = tmp_path / "gen.cdl"
    f = CFile.open(str(p), "w")
    f.print("/* 日本語 */")
    f.close()
    assert p.read_bytes() == "/* 日本語 */".encode(expected_codec)


def test_console_encodes_with_console_charset(
    fresh_state: TecsgenContext, capfdbinary: pytest.CaptureFixture[bytes]
) -> None:
    TECS_LANG.setup(fresh_state, {"LANG": "ja_JP.SJIS"})
    Console.puts("表示")
    Console.print("x\n")
    assert stdout_bytes(capfdbinary) == "表示\nx\n".encode("cp932")


def test_dbg_print_only_in_debug(
    fresh_state: TecsgenContext, capfdbinary: pytest.CaptureFixture[bytes]
) -> None:
    dbg_print("hidden\n")
    fresh_state.debug = True
    dbg_print("shown\n")
    assert stdout_bytes(capfdbinary) == b"shown\n"
