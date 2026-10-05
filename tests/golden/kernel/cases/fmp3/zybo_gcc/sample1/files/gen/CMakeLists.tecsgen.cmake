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
    "../target/zybo_gcc/target.cdl"
    "../target/zybo_gcc/target_class.cdl"
    "../target/zybo_gcc/class_def.cdf"
    "../target/zybo_gcc/tPutLogZYBO.cdl"
    "../target/zybo_gcc/tSIOPortZYBO.cdl"
    "../arch/arm_gcc/zynq7000/tXUartPs.cdl"
    "./gen/tmp_FMPPlugin_post_code.cdl"
    "./gen/tmp_FMPObjectPlugin_post_code.cdl"
    "./gen/tmp_NotifierPlugin_post_code.cdl"
    "./gen/tmp_FMPHandlerPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tInterruptRequest_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tTerminateRoutine_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialPortMain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialAdapter_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLogAdapter_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tLogTaskMain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tBannerMain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tPutLogZYBO_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tXUartPs_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSIOPortZYBOMain_rProcessor1Migratable_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tInterruptRequest.c"
    "tISR.c"
    "tInitializeRoutine.c"
    "tTerminateRoutine.c"
    "tSerialPortMain.c"
    "tSerialAdapter.c"
    "tSysLog.c"
    "tSysLogAdapter.c"
    "tLogTaskMain.c"
    "tBannerMain.c"
    "tPutLogZYBO.c"
    "tXUartPs.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../target/zybo_gcc"
    "${ASP3_SRCDIR}/../arch/arm_gcc/zynq7000"
    "${ASP3_SRCDIR}/../arch/arm_gcc/common"
    "${ASP3_SRCDIR}/../arch/gcc"
    "${ASP3_SRCDIR}/.."
    "${ASP3_SRCDIR}/../sample"
    "${ASP3_SRCDIR}/./gen"
    "${ASP3_SRCDIR}/../tecs_kernel"
    "${ASP3_SRCDIR}/../tecsgen/tecs"
    "${ASP3_SRCDIR}/../tecsgen/tecs/rpc"
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

