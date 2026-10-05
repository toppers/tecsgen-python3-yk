# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "../sample/tSample2.cdl"
    "../tecs_kernel/kernel.cdl"
    "../syssvc/tSerialPort.cdl"
    "../syssvc/tSysLog.cdl"
    "../syssvc/tSysLogAdapter.cdl"
    "../syssvc/tLogTask.cdl"
    "../syssvc/tBanner.cdl"
    "../target/blueninja_gcc/target.cdl"
    "../target/blueninja_gcc/tPutLogTarget.cdl"
    "../target/blueninja_gcc/tSIOPortTarget.cdl"
    "./gen/tmp_HRPPlugin_post_code.cdl"
    "./gen/tmp_HRPSVCThroughPlugin_post_code.cdl"
    "./gen/tmp_HRPTaskPlugin_post_code.cdl"
    "./gen/tmp_HRPObjectPlugin_post_code.cdl"
    "./gen/tmp_NotifierPlugin_post_code.cdl"
    "./gen/tmp_HRPHandlerPlugin_post_code.cdl"
    "./gen/tmp_HRPSVCBodyCellPlugin_post_code.cdl"
    "./gen/tmp_HRPSVCSignaturePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLogAdapter_tecsgen.c"
    "${TECS_GEN_DIR}/tSample2_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_rDomain1_tecsgen.c"
    "${TECS_GEN_DIR}/tAlarmNotifier_rDomain1_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_rDomain2_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tTimeEventHandler_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tCyclicNotifier_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tInterruptRequest_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tCpuExceptionHandler_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tTerminateRoutine_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialPortMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tLogTaskMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tBannerMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tPutLogTarget_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSIOPortTargetMain_rKernelDomain_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tHRPSVCCaller_sSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCCaller_sSerialPort_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCBody_sSysLog_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCBody_sSerialPort_rKernelDomain_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tHRPSVCCaller_sSysLog.c"
    "tHRPSVCCaller_sSerialPort.c"
    "tHRPSVCBody_sSysLog.c"
    "tHRPSVCBody_sSerialPort.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tSysLogAdapter.c"
    "tSample2.c"
    "tAlarmNotifier.c"
    "tTimeEventHandler.c"
    "tCyclicNotifier.c"
    "tISR.c"
    "tCpuExceptionHandler.c"
    "tInitializeRoutine.c"
    "tTerminateRoutine.c"
    "tSerialPortMain.c"
    "tSysLog.c"
    "tLogTaskMain.c"
    "tBannerMain.c"
    "tPutLogTarget.c"
    "tSIOPortTargetMain.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../target/blueninja_gcc"
    "${ASP3_SRCDIR}/../arch"
    "${ASP3_SRCDIR}/../target/blueninja_gcc/device/RTE"
    "${ASP3_SRCDIR}/../target/blueninja_gcc/device/RTE/Device/TZ1001MBG"
    "${ASP3_SRCDIR}/../target/blueninja_gcc/device/TOSHIBA.TZ10xx_DFP/Device/Include"
    "${ASP3_SRCDIR}/../target/blueninja_gcc/device/TOSHIBA.TZ10xx_DFP/RTE_Driver"
    "${ASP3_SRCDIR}/../target/blueninja_gcc/device/ARM.CMSIS/CMSIS/Include"
    "${ASP3_SRCDIR}/../target/blueninja_gcc/device/ARM.CMSIS/CMSIS/Driver/Include"
    "${ASP3_SRCDIR}/../arch/arm_m_gcc/common"
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

