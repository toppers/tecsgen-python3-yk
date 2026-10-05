# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "bool.cdl"
    "../cygwin/cygwin_kernel.cdl"
    "../cygwin/tSysLog.cdl"
    "gen/tTracePlugin_sSigBool_T.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tCTBool_T_tecsgen.c"
    "${TECS_GEN_DIR}/tCTBool_TClient_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTracePlugin_sSigBool_T_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tTracePlugin_sSigBool_T.c"
)

set(TECS_CELLTYPE_SOURCES
    "tSysLog.c"
    "tCTBool_T.c"
    "tCTBool_TClient.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin"
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

