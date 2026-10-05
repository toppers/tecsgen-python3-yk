# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "info.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "HelloWorld.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/TECSInfo/TECSInfoAccessor.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/TECSInfo/TECSInfo.cdl"
    "./gen-raminitializer/tmp_rTEMP_TECSInfoSub.cdl"
    "./gen-raminitializer/tmp_TECSInfoCompoPlugin_post_code.cdl"
    "./gen-raminitializer/tmp_TECSInfoPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tPutStringStdio_tecsgen.c"
    "${TECS_GEN_DIR}/tHelloWorld_tecsgen.c"
    "${TECS_GEN_DIR}/tTaskMain_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tTECSInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tTECSInfoSub_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tNamespaceInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tSignatureInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tFunctionInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tParamInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tCelltypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tCallInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tEntryInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tVarDeclInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tRegionInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tCellInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tRawEntryDescriptorInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tVoidTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tBoolTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tIntTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tStructTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tPtrTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tDefinedTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tDescriptorTypeInfo_tecsgen.c"
    "${TECS_GEN_DIR}/nTECSInfo_tTECSInfoAccessor_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tPutStringStdio.c"
    "tHelloWorld.c"
    "tTaskMain.c"
    "nTECSInfo_tTECSInfoSub.c"
    "nTECSInfo_tNamespaceInfo.c"
    "nTECSInfo_tSignatureInfo.c"
    "nTECSInfo_tFunctionInfo.c"
    "nTECSInfo_tParamInfo.c"
    "nTECSInfo_tCelltypeInfo.c"
    "nTECSInfo_tCallInfo.c"
    "nTECSInfo_tEntryInfo.c"
    "nTECSInfo_tVarDeclInfo.c"
    "nTECSInfo_tRegionInfo.c"
    "nTECSInfo_tCellInfo.c"
    "nTECSInfo_tRawEntryDescriptorInfo.c"
    "nTECSInfo_tVoidTypeInfo.c"
    "nTECSInfo_tBoolTypeInfo.c"
    "nTECSInfo_tIntTypeInfo.c"
    "nTECSInfo_tStructTypeInfo.c"
    "nTECSInfo_tPtrTypeInfo.c"
    "nTECSInfo_tDefinedTypeInfo.c"
    "nTECSInfo_tDescriptorTypeInfo.c"
    "nTECSInfo_tTECSInfoAccessor.c"
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

