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
    "../target/ct11mpcore_gcc/target.cdl"
    "../target/ct11mpcore_gcc/tPutLogCT11MPCore.cdl"
    "../target/ct11mpcore_gcc/tSIOPortCT11MPCore.cdl"
    "../arch/arm_gcc/common/tUartPL011.cdl"
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
    "${TECS_GEN_DIR}/tTask_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tInterruptRequest_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tInitializeRoutine_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tTerminateRoutine_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialPortMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tLogTaskMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tBannerMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tPutLogCT11MPCore_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tUartPL011_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSIOPortCT11MPCoreMain_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tSerialAdapter_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLogAdapter_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tHRPSVCBody_sSysLog_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCBody_sSerialPort_rKernelDomain_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCCaller_sSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tHRPSVCCaller_sSerialPort_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tHRPSVCBody_sSysLog.c"
    "tHRPSVCBody_sSerialPort.c"
    "tHRPSVCCaller_sSysLog.c"
    "tHRPSVCCaller_sSerialPort.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tISR.c"
    "tInitializeRoutine.c"
    "tTerminateRoutine.c"
    "tSerialPortMain.c"
    "tSysLog.c"
    "tLogTaskMain.c"
    "tBannerMain.c"
    "tPutLogCT11MPCore.c"
    "tUartPL011.c"
    "tSerialAdapter.c"
    "tSysLogAdapter.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../target/ct11mpcore_gcc"
    "${ASP3_SRCDIR}/../arch/arm_gcc/mpcore"
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

