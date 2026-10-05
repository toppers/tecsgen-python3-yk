# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "composite.cdl"
    "../cygwin/cygwin_kernel.cdl"
    "../cygwin/tSysLog.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tCell1_tecsgen.c"
    "${TECS_GEN_DIR}/tCell2_tecsgen.c"
    "${TECS_GEN_DIR}/tCell_serv_tecsgen.c"
    "${TECS_GEN_DIR}/tCell_clnt_tecsgen.c"
    "${TECS_GEN_DIR}/tCell2_active_single_tecsgen.c"
    "${TECS_GEN_DIR}/tPtrAttr_tecsgen.c"
    "${TECS_GEN_DIR}/tSizeArray_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tSysLog.c"
    "tCell1.c"
    "tCell2.c"
    "tCell_serv.c"
    "tCell_clnt.c"
    "tCell2_active_single.c"
    "tPtrAttr.c"
    "tSizeArray.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../cygwin"
    "${ASP3_TECSGEN_DIR}/tecs"
    "${ASP3_SRCDIR}/../RUNTIME/runtime/include"
    "${ASP3_SRCDIR}/../RUNTIME/runtime/test"
    "${ASP3_SRCDIR}/src"
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

