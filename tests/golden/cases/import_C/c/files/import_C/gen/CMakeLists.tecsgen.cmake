# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "myappl.cdl"
    "include/toppers_jsp.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tTaskEx_tecsgen.c"
    "${TECS_GEN_DIR}/tSem_tecsgen.c"
    "${TECS_GEN_DIR}/tFlg_tecsgen.c"
    "${TECS_GEN_DIR}/tDtq_tecsgen.c"
    "${TECS_GEN_DIR}/tMbx_tecsgen.c"
    "${TECS_GEN_DIR}/tCyc_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tMyMain_tecsgen.c"
    "${TECS_GEN_DIR}/tMyMainEx_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tTaskEx.c"
    "tSem.c"
    "tFlg.c"
    "tDtq.c"
    "tMbx.c"
    "tCyc.c"
    "tKernel.c"
    "tMyMain.c"
    "tMyMainEx.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/include"
    "${ASP3_SRCDIR}/config_win"
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

