# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "rpc_test.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/tSysLog.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/rpc.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sChannel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/TDR.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/RPCTask.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/PPAllocator.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sRPCErrorHandler.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/tDataqueueOWChannel.cdl"
    "SimpleSample.cdl"
    "gen/tSharedRPCPlugin_tTDR_tDataqueueOWChannel_sSample.cdl"
    "gen/tMarshaler_sSample.cdl"
    "gen/tSharedRPCPlugin_tDataqueueOWChannel.cdl"
    "gen/tmp_SharedRPCPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueuePeer_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tTDR_tecsgen.c"
    "${TECS_GEN_DIR}/tRPCSharedChannelMan_tecsgen.c"
    "${TECS_GEN_DIR}/tRPCSharedTaskMain_tecsgen.c"
    "${TECS_GEN_DIR}/tPPAllocator_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueueAdaptor_tecsgen.c"
    "${TECS_GEN_DIR}/tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_tecsgen.c"
    "${TECS_GEN_DIR}/tSimple_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tMarshaler_sSample_tecsgen.c"
    "${TECS_GEN_DIR}/tUnmarshaler_sSample_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tMarshaler_sSample.c"
    "tUnmarshaler_sSample.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tEventflag.c"
    "tSysLog.c"
    "tRPCSharedChannelMan.c"
    "tRPCSharedTaskMain.c"
    "tPPAllocator.c"
    "tAlloc.c"
    "tSample.c"
    "tSimple.c"
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

