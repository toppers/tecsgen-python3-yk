# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "DataPumpHolderTest.cdl"
    "../cygwin3//cygwin_kernel.cdl"
    "../cygwin3//tSysLog.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/DataPumpHolder/DataPumpHolder.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/rpc.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sChannel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/TDR.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/RPCTask.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/PPAllocator.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/sRPCErrorHandler.cdl"
    "kernel.cdl"
    "gen/tPersonalData_signature.cdl"
    "gen/tPersonalData_celltype.cdl"
    "gen/tRPCPluginDPH_tTDR_sPersonalDataSetSignatureAsync.cdl"
    "gen/tMarshalerDPH_sPersonalDataSetSignatureAsync.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/rpc/tDataqueueOWChannel.cdl"
    "gen/tRPCPlugin_tTDR_sPersonalDataSetSignatureAsync.cdl"
    "gen/tMarshaler_sPersonalDataSetSignatureAsync.cdl"
    "gen/tRPCPlugin_tTDR_sPersonalDataSetSignature.cdl"
    "gen/tMarshaler_sPersonalDataSetSignature.cdl"
    "gen/tmp_DataPumpHolderPlugin_post_code.cdl"
    "gen/tmp_TransparentRPCSignaturePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueuePeer_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tPersonalDataSub_tecsgen.c"
    "${TECS_GEN_DIR}/tPersonalDataPub_tecsgen.c"
    "${TECS_GEN_DIR}/tTaskMain_tecsgen.c"
    "${TECS_GEN_DIR}/tMainMain_tecsgen.c"
    "${TECS_GEN_DIR}/tLoopMain_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTDR_tecsgen.c"
    "${TECS_GEN_DIR}/tRPCDedicatedTaskMain_tecsgen.c"
    "${TECS_GEN_DIR}/tPPAllocator_tecsgen.c"
    "${TECS_GEN_DIR}/tPumpMainConverter_tecsgen.c"
    "${TECS_GEN_DIR}/tPersonalDataDataPump_tecsgen.c"
    "${TECS_GEN_DIR}/tPersonalDataDataHolder_tecsgen.c"
    "${TECS_GEN_DIR}/tPersonalDataSyncAdaptor_tecsgen.c"
    "${TECS_GEN_DIR}/tPersonalDataAsyncAdaptor_tecsgen.c"
    "${TECS_GEN_DIR}/tMarshalerDPH_sPersonalDataSetSignatureAsync_tecsgen.c"
    "${TECS_GEN_DIR}/tUnmarshalerDPH_sPersonalDataSetSignatureAsync_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueueAdaptor_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tRPCDedicatedTaskMain.c"
    "tPPAllocator.c"
    "tPersonalDataDataPump.c"
    "tPersonalDataDataHolder.c"
    "tMarshalerDPH_sPersonalDataSetSignatureAsync.c"
    "tUnmarshalerDPH_sPersonalDataSetSignatureAsync.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tEventflag.c"
    "tSysLog.c"
    "tPersonalDataSub.c"
    "tPersonalDataPub.c"
    "tTaskMain.c"
    "tMainMain.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin3/"
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

