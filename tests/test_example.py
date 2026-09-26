import os

import pytest
from tree_sitter import Parser

from tecsgen.example import DEFAULT_CDL_DLL, SAMPLE_CDL, load_cdl_language

DLL = os.environ.get("TECSGEN_CDL_DLL", DEFAULT_CDL_DLL)


@pytest.mark.skipif(not os.path.exists(DLL), reason="CDL parser DLL not found")
def test_parse_sample_cdl_without_errors() -> None:
    tree = Parser(load_cdl_language(DLL)).parse(SAMPLE_CDL)

    assert tree.root_node.type == "source_file"
    assert not tree.root_node.has_error
