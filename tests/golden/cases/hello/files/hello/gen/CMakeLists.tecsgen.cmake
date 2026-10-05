# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "hello.cdl"
    "../cygwin/tSysLog.cdl"
    "../cygwin/cygwin_kernel.cdl"
    "gen/tTracePlugin_sPrint.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tTECSMain_tecsgen.c"
    "${TECS_GEN_DIR}/tOutput_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTracePlugin_sPrint_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tTracePlugin_sPrint.c"
)

set(TECS_CELLTYPE_SOURCES
    "tSysLog.c"
    "tTECSMain.c"
    "tOutput.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin"
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

