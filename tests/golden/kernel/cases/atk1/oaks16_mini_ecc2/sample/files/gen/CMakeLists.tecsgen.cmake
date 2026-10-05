# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "sample.cdl"
    "syslib_inst.cdl"
    "../../../include/kernel.cdl"
    "target_syslib_decl.cdl"
    "../../../syslib/m16c-renesas/oaks16_mini/tHwSerial.cdl"
    "../../../syslib/m16c-renesas/oaks16_mini/tHwSysTimer.cdl"
    "../../../syslib/tString.cdl"
    "../../../syslib/tSerial.cdl"
    "../../../syslib/tSysTimer.cdl"
    "target_syslib_inst.cdl"
    "gen/tmp_ATK1KernelPlugin_post_code.cdl"
    "gen/tmp_ATK1TaskPlugin_post_code.cdl"
    "gen/tmp_ATK1ISRPlugin_post_code.cdl"
    "gen/tmp_ATK1AlarmPlugin_post_code.cdl"
    "gen/tmp_ATK1EventPlugin_post_code.cdl"
    "gen/tmp_ATK1ResourcePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tCPU_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tApplicationMode_tecsgen.c"
    "${TECS_GEN_DIR}/tTask_tecsgen.c"
    "${TECS_GEN_DIR}/tISR_tecsgen.c"
    "${TECS_GEN_DIR}/tCounter_tecsgen.c"
    "${TECS_GEN_DIR}/tAlarm_tecsgen.c"
    "${TECS_GEN_DIR}/tHwSerial_tecsgen.c"
    "${TECS_GEN_DIR}/tHwSysTimer_tecsgen.c"
    "${TECS_GEN_DIR}/tString_tecsgen.c"
    "${TECS_GEN_DIR}/tSerial_tecsgen.c"
    "${TECS_GEN_DIR}/tSysTimer_tecsgen.c"
    "${TECS_GEN_DIR}/tSample_tecsgen.c"
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
    "tHwSerial.c"
    "tHwSysTimer.c"
    "tString.c"
    "tSerial.c"
    "tSysTimer.c"
    "tSample.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/../../../config/m16c-renesas"
    "${ASP3_SRCDIR}/../../../config/m16c-renesas/oaks16_mini"
    "${ASP3_SRCDIR}/../../../include"
    "${ASP3_SRCDIR}/../../.."
    "${ASP3_SRCDIR}/../../../syslib"
    "${ASP3_SRCDIR}/../../../syslib/m16c-renesas/oaks16_mini"
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
)

