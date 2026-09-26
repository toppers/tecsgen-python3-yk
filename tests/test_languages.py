from tree_sitter import Parser

from tecsgen.syntax.languages import cdecl_language, cdl_language


def test_cdl_language_metadata() -> None:
    language = cdl_language()

    assert language.name == "cdl"
    assert language.abi_version == 15


def test_cdecl_language_metadata() -> None:
    language = cdecl_language()

    assert language.name == "tecs_cdecl"
    assert language.abi_version == 15


def test_languages_are_cached() -> None:
    assert cdl_language() is cdl_language()
    assert cdecl_language() is cdecl_language()


def test_parse_cdl_without_errors() -> None:
    source = b"""
    signature sTask { void main(void); };
    celltype tTask {
        entry sTask eTask;
        attr { int32_t priority = 1; };
    };
    cell tTask Task { priority = 3; };
    """

    tree = Parser(cdl_language()).parse(source)

    assert tree.root_node.type == "source_file"
    assert not tree.root_node.has_error


def test_parse_cdl_reports_syntax_error() -> None:
    tree = Parser(cdl_language()).parse(b"celltype tTask { entry sTask ; };")

    assert tree.root_node.has_error


def test_parse_c_header_without_errors() -> None:
    source = b"""
    typedef int int_t;
    struct point { int_t x; int_t y; };
    typedef struct point point_t;
    """

    tree = Parser(cdecl_language()).parse(source)

    assert not tree.root_node.has_error
