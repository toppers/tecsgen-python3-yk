# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "opaqueRPC.cdl"
    "../cygwin3/tSysLog.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/rpc.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sChannel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/TDR.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/RPCTask.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/PPAllocator.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sRPCErrorHandler.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/tSocketChannel.cdl"
    "tAlloc.cdl"
    "sSimple.cdl"
    "sSample.cdl"
    "gen/tOpaqueMarshaler_sSample.cdl"
    "gen/tSharedOpaqueRPCPluginChannel_tTDR.cdl"
    "gen/tTracePlugin_sSimple.cdl"
    "gen/tOpaqueMarshaler_sSimple.cdl"
    "gen/tTracePlugin_sTask.cdl"
    "gen/tTracePlugin_sSocketClientOpener.cdl"
    "gen/tTracePlugin_sAlloc.cdl"
    "gen/tmp_SharedOpaqueRPCPlugin_post_code.cdl"
    "gen/tmp_TracePlugin_post_code.cdl"
    "gen/tTracePlugin_sSysLog.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tTDR_tecsgen.c"
    "${TECS_GEN_DIR}/tRPCSharedTaskMainWithOpener_tecsgen.c"
    "${TECS_GEN_DIR}/tPPAllocator_tecsgen.c"
    "${TECS_GEN_DIR}/tSocketServer_tecsgen.c"
    "${TECS_GEN_DIR}/tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/tSimpleServer_tecsgen.c"
    "${TECS_GEN_DIR}/tSampleServer_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tOpaqueUnmarshaler_sSample_tecsgen.c"
    "${TECS_GEN_DIR}/tTracePlugin_sSimple_tecsgen.c"
    "${TECS_GEN_DIR}/tOpaqueUnmarshaler_sSimple_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tOpaqueUnmarshaler_sSample.c"
    "tTracePlugin_sSimple.c"
    "tOpaqueUnmarshaler_sSimple.c"
)

set(TECS_CELLTYPE_SOURCES
    "tSysLog.c"
    "tTask.c"
    "tRPCSharedTaskMainWithOpener.c"
    "tPPAllocator.c"
    "tSocketServer.c"
    "tAlloc.c"
    "tSimpleServer.c"
    "tSampleServer.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/.."
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
    "__extension__="
)

