# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "domainPlugin.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/tSysLog.cdl"
    "gen/tTracePlugin_sSimple.cdl"
    "gen/tmp_MyDomainPlugin_post_code.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_rSimple_rSimple0_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_rSimple_rSimple0_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_rSample_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_rSample_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_rTEST2_rSimple2_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_rTEST2_rSimple2_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_rSample_rSample1_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_rTEST2_rSample2_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTracePlugin_sSimple_rSimple_rSimple0_tecsgen.c"
    "${TECS_GEN_DIR}/tTracePlugin_sSimple_rTEST2_rSimple2_tecsgen.c"
    "${TECS_GEN_DIR}/tTracePlugin_sSimple_tecsgen.c"
    "${TECS_GEN_DIR}/tTracePlugin_sSimple_rSample_rSample1_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tTracePlugin_sSimple.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tSysLog.c"
    "tSimple.c"
    "tSample.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin3"
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

