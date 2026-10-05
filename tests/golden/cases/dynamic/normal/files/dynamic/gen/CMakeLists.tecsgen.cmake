# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "dynamic.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/utility.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialTaskBody_tecsgen.c"
    "${TECS_GEN_DIR}/tMain_tecsgen.c"
    "${TECS_GEN_DIR}/tTalkerSelector_tecsgen.c"
    "${TECS_GEN_DIR}/tTalker_tecsgen.c"
    "${TECS_GEN_DIR}/tMainForComp_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tSerialTaskBody.c"
    "tMain.c"
    "tTalkerSelector.c"
    "tTalker.c"
    "tMainForComp.c"
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

