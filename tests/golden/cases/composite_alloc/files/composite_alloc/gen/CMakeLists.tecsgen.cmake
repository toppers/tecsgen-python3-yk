# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "composite_alloc.cdl"
    "../cygwin3/cygwin_kernel.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/tTestComponent_tecsgen.c"
    "${TECS_GEN_DIR}/tTestServ_tecsgen.c"
    "${TECS_GEN_DIR}/tTestClient_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tAlloc.c"
    "tTestComponent.c"
    "tTestServ.c"
    "tTestClient.c"
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

