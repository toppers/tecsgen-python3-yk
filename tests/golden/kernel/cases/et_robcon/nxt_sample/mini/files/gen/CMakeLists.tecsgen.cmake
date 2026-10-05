# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "tSample.cdl"
    "../../include/kernel.cdl"
    "../../tecs_lib/mindstorms_nxt/target_lib_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tAVR_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tTWI_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tMotor_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tSensor_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tDisplay_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tLCD_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tSPI_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tButton_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tBattery_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tSound_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tBluetooth_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tFlash_decl.cdl"
    "../../tecs_lib/mindstorms_nxt/tBalancer_decl.cdl"
    "../../config/at91sam7s-gnu/lego_nxt/target_systim_decl.cdl"
    "../../config/at91sam7s-gnu/lego_nxt/target_systim_inst.cdl"
    "../../tecs_lib/mindstorms_nxt/target_lib_inst.cdl"
    "../../tecs_lib/mindstorms_nxt/ram_only.cdl"
    "gen/tmp_ATK1KernelPlugin_post_code.cdl"
    "gen/tmp_ATK1TaskPlugin_post_code.cdl"
    "gen/tmp_ATK1ISRPlugin_post_code.cdl"
    "gen/tmp_ATK1AlarmPlugin_post_code.cdl"
    "gen/tmp_ATK1ResourcePlugin_post_code.cdl"
    "gen/tmp_ATK1DelayTaskPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tCPU_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tApplicationMode_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_tecsgen.c"
    "${TECS_GEN_DIR}/tCounter_tecsgen.c"
    "${TECS_GEN_DIR}/tAlarm_tecsgen.c"
    "${TECS_GEN_DIR}/tResource_tecsgen.c"
    "${TECS_GEN_DIR}/tConfigInterrupt_tecsgen.c"
    "${TECS_GEN_DIR}/tTWIBody_tecsgen.c"
    "${TECS_GEN_DIR}/tAVRBody_tecsgen.c"
    "${TECS_GEN_DIR}/tSPIBody_tecsgen.c"
    "${TECS_GEN_DIR}/tLCD_tecsgen.c"
    "${TECS_GEN_DIR}/tDisplayBody_tecsgen.c"
    "${TECS_GEN_DIR}/tButtonBody_tecsgen.c"
    "${TECS_GEN_DIR}/tBattery_tecsgen.c"
    "${TECS_GEN_DIR}/tCheckNXTButtonBody_tecsgen.c"
    "${TECS_GEN_DIR}/tSystemTimer_tecsgen.c"
    "${TECS_GEN_DIR}/tSampleTaskBody_tecsgen.c"
    "${TECS_GEN_DIR}/tSampleAlarmBody_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
)

set(TECS_CELLTYPE_SOURCES
    "tCPU.c"
    "tApplicationMode.c"
    "tTask.c"
    "tISR.c"
    "tAlarm.c"
    "tConfigInterrupt.c"
    "tTWIBody.c"
    "tAVRBody.c"
    "tSPIBody.c"
    "tLCD.c"
    "tDisplayBody.c"
    "tButtonBody.c"
    "tCheckNXTButtonBody.c"
    "tSystemTimer.c"
    "tSampleTaskBody.c"
    "tSampleAlarmBody.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/./gen"
    "${ASP3_SRCDIR}/../../tecs_kernel_atk1"
    "${ASP3_SRCDIR}/../../tecs_kernel"
    "${ASP3_SRCDIR}/../../include"
    "${ASP3_SRCDIR}/../../config"
    "${ASP3_SRCDIR}/../.."
    "${ASP3_SRCDIR}/../../kernel"
    "${ASP3_SRCDIR}/../../config/at91sam7s-gnu/lego_nxt"
    "${ASP3_SRCDIR}/../../tecs_lib/mindstorms_nxt"
    "${ASP3_SRCDIR}/../../syslib/at91sam7s-gnu/lego_nxt"
    "${ASP3_SRCDIR}/../../config/at91sam7s-gnu"
    "${ASP3_SRCDIR}/../../kernel/ecc2"
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
    "TECS"
    "TECS_CPP"
)

