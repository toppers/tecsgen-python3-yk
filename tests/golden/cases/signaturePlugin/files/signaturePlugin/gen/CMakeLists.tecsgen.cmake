# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "generate.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "gen/tmp_C2TECSBridgePlugin_post_code.cdl"
    "gen/tmp_SignaturePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tTECSTest_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSignaturePlugin_sTest_tecsgen.c"
    "${TECS_GEN_DIR}/nC2TECS_tsTest_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "nC2TECS_tsTest.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tTECSTest.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin3"
    "${ASP3_SRCDIR}/../../tecs"
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

