# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "allocator.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/tRelayComponent_tecsgen.c"
    "${TECS_GEN_DIR}/tTargetComponent_tecsgen.c"
    "${TECS_GEN_DIR}/tTestClient_tecsgen.c"
    "${TECS_GEN_DIR}/tTestOptional_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tAlloc.c"
    "tRelayComponent.c"
    "tTargetComponent.c"
    "tTestClient.c"
    "tTestOptional.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../RUNTIME/tecs-runtime/target"
    "${ASP3_SRCDIR}/../RUNTIME/tecs-runtime/include"
    "${ASP3_SRCDIR}/gen"
    "${ASP3_SRCDIR}/src"
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

