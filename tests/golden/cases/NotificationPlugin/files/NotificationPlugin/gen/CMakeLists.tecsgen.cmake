# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "test.cdl"
    "gen/tmp_NotifierPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTestNotifier_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueue_tecsgen.c"
    "${TECS_GEN_DIR}/tUserCelltypeA_tecsgen.c"
    "${TECS_GEN_DIR}/tUserCelltypeB_tecsgen.c"
    "${TECS_GEN_DIR}/tTimeEventHandler_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTestNotifier.c"
    "tTask.c"
    "tSemaphore.c"
    "tEventflag.c"
    "tDataqueue.c"
    "tUserCelltypeA.c"
    "tUserCelltypeB.c"
    "tTimeEventHandler.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/./src"
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

