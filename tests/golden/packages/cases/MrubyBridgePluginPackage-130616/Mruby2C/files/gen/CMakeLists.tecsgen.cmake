# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "test.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mruby.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mrubyInitializer.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mrubyPointers.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/mruby/mrubyVMs.cdl"
    "${ASP3_TECSGEN_DIR}/tecs/posix/posix.cdl"
    "gen/Mruby2C_tsInitializerBridge.cdl"
    "gen/tmp_Mruby2CBridgePlugin_post_code.cdl"
    "gen/tmp_MrubyBridgeSignaturePlugin_post_code.cdl"
    "gen/tmp_TECS2CBridgePlugin_post_code.cdl"
    "gen/tmp_C2TECSBridgePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/nMruby_tTECSInitializer_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tsTest_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tsTest_Initializer_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tsTest2_tecsgen.c"
    "${TECS_GEN_DIR}/nMruby_tsTest2_Initializer_tecsgen.c"
    "${TECS_GEN_DIR}/nTECS2C_tsTest_tecsgen.c"
    "${TECS_GEN_DIR}/nTECS2C_tsTest2_tecsgen.c"
    "${TECS_GEN_DIR}/nC2TECS_tnMruby_sInitializeBridge_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "nMruby_tTECSInitializer.c"
    "nMruby_tsTest.c"
    "nMruby_tsTest_Initializer.c"
    "nMruby_tsTest2.c"
    "nMruby_tsTest2_Initializer.c"
    "nC2TECS_tnMruby_sInitializeBridge.c"
)

set(TECS_CELLTYPE_SOURCES
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../../tecsgen/test/cygwin"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../../tecsgen/tecsgen/tecs"
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

