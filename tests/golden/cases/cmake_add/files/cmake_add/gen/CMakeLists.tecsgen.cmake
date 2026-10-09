# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "hello.cdl"
    "gen/tmp_MyCMakePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tHello_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tHello.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
    "plugin_a.c"
    "sym_b"
    "from_new_cell.c"
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_TECSGEN_DIR}/tecs"
    "${ASP3_TECSGEN_DIR}/tecs/mruby"
    "${ASP3_TECSGEN_DIR}/tecs/rpc"
    "${ASP3_TECSGEN_DIR}/tecs/TLSFMalloc"
    "${ASP3_TECSGEN_DIR}/tecs/DataPumpHolder"
    "${ASP3_TECSGEN_DIR}/tecs/posix"
    "${ASP3_TECSGEN_DIR}/tecs/TECSInfo"
    "${TECS_GEN_DIR}"
    "$(BASE_DIR)/inc"
    "/abs/path/win"
)

set(TECS_COMPILE_DEFINITIONS
    "FOO=1"
    "42"
)

set(TECS_LINK_OPTIONS
    "-Wl,--gc-sections"
)

set(TECS_CUSTOM_COMMANDS
    "add_custom_command(OUTPUT x COMMAND y)"
)

# plugin additional cmake lines
# line1
set(X 1)

