# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "opaqueMarshaler.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/tSysLog.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/rpc.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sChannel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/TDR.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/RPCTask.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/PPAllocator.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sRPCErrorHandler.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/tSocketChannel.cdl"
    "gen/tOpaqueMarshaler_sSig.cdl"
    "gen/tmp_OpaqueMarshalerPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tNBOTDR_tecsgen.c"
    "${TECS_GEN_DIR}/tRPCDedicatedTaskMainWithOpener_tecsgen.c"
    "${TECS_GEN_DIR}/tPPAllocator_tecsgen.c"
    "${TECS_GEN_DIR}/tSocketServer_tecsgen.c"
    "${TECS_GEN_DIR}/tServer_tecsgen.c"
    "${TECS_GEN_DIR}/tServerErrorHandler_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tOpaqueUnmarshaler_sSig_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tOpaqueUnmarshaler_sSig.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tSysLog.c"
    "tRPCDedicatedTaskMainWithOpener.c"
    "tPPAllocator.c"
    "tSocketServer.c"
    "tServer.c"
    "tServerErrorHandler.c"
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

