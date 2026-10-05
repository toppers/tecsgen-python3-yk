# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "multiplugin.cdl"
    "../cygwin//cygwin_kernel.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mruby.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mrubyInitializer.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mrubyPointers.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mrubyVMs.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/posix/posix.cdl"
    "gen/tmp_MrubyBridgeCelltypePluginModule_tSimpleServer_1.cdl"
    "gen/tmp_MrubyBridgeCelltypePluginModule_tSimpleServer_2.cdl"
    "gen/tmp_MrubyBridgeCelltypePluginModule_tCompSimpleServer_3.cdl"
    "gen/tmp_MrubyBridgeCelltypePlugin_post_code.cdl"
    "gen/tmp_MrubyBridgeCompositePlugin_post_code.cdl"
    "gen/tmp_MrubyBridgeCellPlugin_post_code.cdl"
    "gen/tmp_MrubyBridgeSignaturePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSimpleServer_tecsgen.c"
    "${TECS_GEN_DIR}/tSimpleClient_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/nMruby_tTECSInitializer_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tCharPointer_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tsSimple_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tsSimple_Initializer_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "nMruby_tTECSInitializer.c"
    "nMruby_tCharPointer.c"
    "nMruby_tsSimple.c"
    "nMruby_tsSimple_Initializer.c"
)

set(TECS_CELLTYPE_SOURCES
    "tSimpleServer.c"
    "tSimpleClient.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin/"
    "${ASP3_TECSGEN_DIR}/tecs"
    "${ASP3_TECSGEN_DIR}/tecs/mruby"
    "${ASP3_TECSGEN_DIR}/tecs/rpc"
    "${ASP3_TECSGEN_DIR}/tecs/TLSFMalloc"
    "${ASP3_TECSGEN_DIR}/tecs/DataPumpHolder"
    "${ASP3_TECSGEN_DIR}/tecs/posix"
    "${ASP3_TECSGEN_DIR}/tecs/TECSInfo"
    "$(MRUBYPATH)/include"
    "${TECS_GEN_DIR}"
)

set(TECS_COMPILE_DEFINITIONS
)

