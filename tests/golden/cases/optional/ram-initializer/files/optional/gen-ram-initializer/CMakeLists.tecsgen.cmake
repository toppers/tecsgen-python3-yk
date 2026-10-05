# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "optional.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/allocator.cdl"
    "../cygwin3/utility.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tAlloc_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialTaskBody_tecsgen.c"
    "${TECS_GEN_DIR}/tSingleCellOptimizeCaller_tecsgen.c"
    "${TECS_GEN_DIR}/tSingleCellOptimizeCallee_tecsgen.c"
    "${TECS_GEN_DIR}/tVMTUselessOptimizeCaller_tecsgen.c"
    "${TECS_GEN_DIR}/tVMTUselessOptimizeCallee_tecsgen.c"
    "${TECS_GEN_DIR}/tSkeltonUselessOptimizeCaller_tecsgen.c"
    "${TECS_GEN_DIR}/tSkeltonUselessOptimizeCallee_tecsgen.c"
    "${TECS_GEN_DIR}/tMain_tecsgen.c"
    "${TECS_GEN_DIR}/tCPArray_tecsgen.c"
    "${TECS_GEN_DIR}/tNCPArray_tecsgen.c"
    "${TECS_GEN_DIR}/tSendRecvClnt_tecsgen.c"
    "${TECS_GEN_DIR}/tSendRecvServ_tecsgen.c"
    "${TECS_GEN_DIR}/tSendRecvClntOmit_tecsgen.c"
    "${TECS_GEN_DIR}/tCCP5Caller_tecsgen.c"
    "${TECS_GEN_DIR}/tCCP5Callee_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tAlloc.c"
    "tSerialTaskBody.c"
    "tSingleCellOptimizeCaller.c"
    "tSingleCellOptimizeCallee.c"
    "tVMTUselessOptimizeCaller.c"
    "tVMTUselessOptimizeCallee.c"
    "tSkeltonUselessOptimizeCaller.c"
    "tSkeltonUselessOptimizeCallee.c"
    "tMain.c"
    "tCPArray.c"
    "tNCPArray.c"
    "tSendRecvClnt.c"
    "tSendRecvServ.c"
    "tSendRecvClntOmit.c"
    "tCCP5Caller.c"
    "tCCP5Callee.c"
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

