# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "../sample/sample1.cdl"
    "../tecs_kernel/kernel.cdl"
    "../syssvc/tSerialPort.cdl"
    "../syssvc/tSerialAdapter.cdl"
    "../syssvc/tSysLog.cdl"
    "../syssvc/tSysLogAdapter.cdl"
    "../syssvc/tLogTask.cdl"
    "../syssvc/tBanner.cdl"
    "../target/linux_gcc/target.cdl"
    "../arch/posix_gcc/posix.cdl"
    "../arch/posix_gcc/tPutLogPosix.cdl"
    "../arch/posix_gcc/tSIOPortPosix.cdl"
    "./gen/tmp_NotifierPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_tecsgen.c"
    "${TECS_GEN_DIR}/tInterruptRequest_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_tecsgen.c"
    "${TECS_GEN_DIR}/tTerminateRoutine_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialPortMain_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialAdapter_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLogAdapter_tecsgen.c"
    "${TECS_GEN_DIR}/tLogTaskMain_tecsgen.c"
    "${TECS_GEN_DIR}/tBannerMain_tecsgen.c"
    "${TECS_GEN_DIR}/tPutLogPosix_tecsgen.c"
    "${TECS_GEN_DIR}/tSIOPortPosixMain_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tISR.c"
    "tInitializeRoutine.c"
    "tTerminateRoutine.c"
    "tSerialPortMain.c"
    "tSerialAdapter.c"
    "tSysLog.c"
    "tSysLogAdapter.c"
    "tLogTaskMain.c"
    "tBannerMain.c"
    "tPutLogPosix.c"
    "tSIOPortPosixMain.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../target/linux_gcc"
    "${ASP3_SRCDIR}/../arch/posix_gcc"
    "${ASP3_SRCDIR}/../arch/gcc"
    "${ASP3_SRCDIR}/.."
    "${ASP3_SRCDIR}/../sample"
    "${ASP3_SRCDIR}/./gen"
    "${ASP3_SRCDIR}/../tecs_kernel"
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

