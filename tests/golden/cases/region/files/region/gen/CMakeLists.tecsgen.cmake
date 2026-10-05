# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "region.cdl"
    "../cygwin/tSysLog.cdl"
    "../cygwin/cygwin_kernel.cdl"
    "region-body.cdl"
    "gen/tTracePlugin_sSig3.cdl"
    "gen/tPlugin2_sSig2.cdl"
    "gen/tPlugin2_sSig3.cdl"
    "gen/tPlugin1_sSig3.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
    "gen/tmp_Plugin2_post_code.cdl"
    "gen/tmp_Plugin1_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tCtR1_tecsgen.c"
    "${TECS_GEN_DIR}/tCtR2_tecsgen.c"
    "${TECS_GEN_DIR}/tCtOuter_tecsgen.c"
    "${TECS_GEN_DIR}/tMain_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTracePlugin_sSig3_tecsgen.c"
    "${TECS_GEN_DIR}/tPlugin2_sSig2_tecsgen.c"
    "${TECS_GEN_DIR}/tPlugin2_sSig3_tecsgen.c"
    "${TECS_GEN_DIR}/tPlugin1_sSig3_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tTracePlugin_sSig3.c"
)

set(TECS_CELLTYPE_SOURCES
    "tSysLog.c"
    "tCtR1.c"
    "tCtR2.c"
    "tCtOuter.c"
    "tMain.c"
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

