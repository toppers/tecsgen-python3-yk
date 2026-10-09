# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "class.cdl"
    "class_def.cdf"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/tSysLog.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/rpc.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sChannel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/TDR.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/RPCTask.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/PPAllocator.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sRPCErrorHandler.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/tDataqueueOWChannel.cdl"
    "gen/tTracePlugin_sSimple.cdl"
    "gen/tRPCPlugin_tTDR_sTaskBody.cdl"
    "gen/tMarshaler_sTaskBody.cdl"
    "gen/tmp_MyClassPlugin_post_code.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
    "gen/tmp_RPCPlugin_post_code.cdl"
    "gen/tmp_TransparentRPCSignaturePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_rClass1_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_rClass1_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueuePeer_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tTDR_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tRPCDedicatedTaskMain_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueueAdaptor_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTracePlugin_sSimple_rClass1_tecsgen.c"
    "${TECS_GEN_DIR}/tMarshaler_sTaskBody_rClass2e_tecsgen.c"
    "${TECS_GEN_DIR}/tUnmarshaler_sTaskBody_rClass2e_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tTracePlugin_sSimple.c"
    "tMarshaler_sTaskBody.c"
    "tUnmarshaler_sTaskBody.c"
)

set(TECS_CELLTYPE_SOURCES
    "tEventflag.c"
    "tRPCDedicatedTaskMain.c"
    "tTask.c"
    "tSysLog.c"
    "tSimple.c"
    "tSample.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
    "class_plugin.c"
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
    "inc_class"
)

set(TECS_COMPILE_DEFINITIONS
    "K_CLASS=1"
)

# plugin additional cmake lines
# from class

