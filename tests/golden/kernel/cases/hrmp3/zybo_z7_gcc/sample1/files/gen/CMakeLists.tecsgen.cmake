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
    "../target/zybo_z7_gcc/target.cdl"
    "../target/zybo_z7_gcc/target_class.cdf"
    "../syssvc/tPutLogSIOPort.cdl"
    "../target/zybo_z7_gcc/tSIOPortZYBO.cdl"
    "../arch/arm_gcc/zynq7000/tXUartPs.cdl"
    "./gen/tmp_HRPSVCThroughPlugin_post_code.cdl"
    "./gen/tmp_HRMPKernelObjectPlugin_post_code.cdl"
    "./gen/tmp_NotifierPlugin_post_code.cdl"
    "./gen/tmp_HRPSVCBodyCellPlugin_post_code.cdl"
    "./gen/tmp_HRPSVCSignaturePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tInterruptRequest_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tTerminateRoutine_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialPortMain_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tLogTaskMain_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tPutLogSIOPort_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tXUartPs_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSIOPortZYBOMain_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_rKernelDomain_rProcessor2Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tBannerMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialAdapter_rOutOfDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLogAdapter_rOutOfDomain_rProcessor1Migratable_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tHRPSVCBody_sSysLog_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCBody_sSerialPort_rKernelDomain_rProcessor1Migratable_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCCaller_sSysLog_rOutOfDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCCaller_sSerialPort_rOutOfDomain_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tHRPSVCBody_sSysLog.c"
    "tHRPSVCBody_sSerialPort.c"
    "tHRPSVCCaller_sSysLog.c"
    "tHRPSVCCaller_sSerialPort.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tInterruptRequest.c"
    "tISR.c"
    "tTerminateRoutine.c"
    "tSerialPortMain.c"
    "tSysLog.c"
    "tLogTaskMain.c"
    "tPutLogSIOPort.c"
    "tXUartPs.c"
    "tBannerMain.c"
    "tInitializeRoutine.c"
    "tSerialAdapter.c"
    "tSysLogAdapter.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../target/zybo_z7_gcc"
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

