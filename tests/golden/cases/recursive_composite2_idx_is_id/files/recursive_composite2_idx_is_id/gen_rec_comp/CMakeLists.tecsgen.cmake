# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "recursive_composite.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tCell1_tecsgen.c"
    "${TECS_GEN_DIR}/tCell2_tecsgen.c"
    "${TECS_GEN_DIR}/tCell3_tecsgen.c"
    "${TECS_GEN_DIR}/tCell4_tecsgen.c"
    "${TECS_GEN_DIR}/tCell_serv_tecsgen.c"
    "${TECS_GEN_DIR}/tCell_clnt_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tCell1.c"
    "tCell2.c"
    "tCell3.c"
    "tCell4.c"
    "tCell_serv.c"
    "tCell_clnt.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../RUNTIME/runtime/test"
    "${ASP3_SRCDIR}/../RUNTIME/runtime/include"
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

