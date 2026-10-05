# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "namespace.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tAppl_tecsgen.c"
    "${TECS_GEN_DIR}/tOSEKAppl_tecsgen.c"
    "${TECS_GEN_DIR}/nAlloc_tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/TOPPERS_tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/TOPPERS_tAppl_tecsgen.c"
    "${TECS_GEN_DIR}/OSEK_tKernel_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tKernel.c"
    "tAppl.c"
    "tOSEKAppl.c"
    "nAlloc_tAlloc.c"
    "TOPPERS_tKernel.c"
    "TOPPERS_tAppl.c"
    "OSEK_tKernel.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin"
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

