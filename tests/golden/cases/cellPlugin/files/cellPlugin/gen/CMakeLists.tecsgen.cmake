# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "cellPlugin.cdl"
    "gen/tmp_RepeatJoinPlugin_post_code.cdl"
    "gen/tmp_RepeatCellPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tCelltype_tecsgen.c"
    "${TECS_GEN_DIR}/tCelltype2_tecsgen.c"
    "${TECS_GEN_DIR}/tCelltype3_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tCelltype.c"
    "tCelltype2.c"
    "tCelltype3.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin/"
    "${ASP3_SRCDIR}/../../tecsgen/tecs"
    "${ASP3_TECSGEN_DIR}/tecs"
    "${ASP3_TECSGEN_DIR}/tecs/mruby"
    "${ASP3_TECSGEN_DIR}/tecs/rpc"
    "${ASP3_TECSGEN_DIR}/tecs/TLSFMalloc"
    "${ASP3_TECSGEN_DIR}/tecs/DataPumpHolder"
    "${ASP3_TECSGEN_DIR}/tecs/posix"
    "${ASP3_TECSGEN_DIR}/tecs/TECSInfo"
    "${TECS_GEN_DIR}"
)

set(TECS_COMPILE_DEFINITIONS
)

