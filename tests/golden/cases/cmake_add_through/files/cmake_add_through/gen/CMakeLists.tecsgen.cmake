# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "through.cdl"
    "../cygwin/tSysLog.cdl"
    "../cygwin/cygwin_kernel.cdl"
    "gen/tThroughPlugin_sSignature.cdl"
    "gen/tTracePlugin_sSignature.cdl"
    "gen/tPlugin2_sSignature.cdl"
    "gen/tPlugin1_sSignature.cdl"
    "gen/tmp_ThroughPlugin_post_code.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
    "gen/tmp_Plugin2_post_code.cdl"
    "gen/tmp_Plugin1_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/tClient_tecsgen.c"
    "${TECS_GEN_DIR}/tServer_tecsgen.c"
    "${TECS_GEN_DIR}/tMain_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tThroughPlugin_sSignature_tecsgen.c"
    "${TECS_GEN_DIR}/tTracePlugin_sSignature_tecsgen.c"
    "${TECS_GEN_DIR}/tPlugin2_sSignature_tecsgen.c"
    "${TECS_GEN_DIR}/tPlugin1_sSignature_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tTracePlugin_sSignature.c"
)

set(TECS_CELLTYPE_SOURCES
    "tSysLog.c"
    "tAlloc.c"
    "tClient.c"
    "tServer.c"
    "tMain.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
    "through_plugin.c"
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin"
    "${ASP3_SRCDIR}/../../tecs"
    "${ASP3_SRCDIR}/src"
    "${ASP3_TECSGEN_DIR}/tecs"
    "${ASP3_TECSGEN_DIR}/tecs/mruby"
    "${ASP3_TECSGEN_DIR}/tecs/rpc"
    "${ASP3_TECSGEN_DIR}/tecs/TLSFMalloc"
    "${ASP3_TECSGEN_DIR}/tecs/DataPumpHolder"
    "${ASP3_TECSGEN_DIR}/tecs/posix"
    "${ASP3_TECSGEN_DIR}/tecs/TECSInfo"
    "${TECS_GEN_DIR}"
    "inc_through"
)

set(TECS_COMPILE_DEFINITIONS
    "K_THROUGH=1"
)

# plugin additional cmake lines
# from through

