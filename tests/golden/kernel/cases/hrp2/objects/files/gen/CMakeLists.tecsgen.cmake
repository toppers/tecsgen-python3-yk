# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "hrp2_objects.cdl"
    "../include/kernel.cdl"
    "gen/tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee.cdl"
    "gen/tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee.cdl"
    "gen/tmp_HRP2Plugin_post_code.cdl"
    "gen/tmp_HRP2SVCPlugin_post_code.cdl"
    "gen/tmp_HRP2TaskPlugin_post_code.cdl"
    "gen/tmp_HRP2CyclicHandlerPlugin_post_code.cdl"
    "gen/tmp_HRP2AlarmHandlerPlugin_post_code.cdl"
    "gen/tmp_HRP2SemaphorePlugin_post_code.cdl"
    "gen/tmp_HRP2EventflagPlugin_post_code.cdl"
    "gen/tmp_HRP2DataqueuePlugin_post_code.cdl"
    "gen/tmp_HRP2PriorityDataqueuePlugin_post_code.cdl"
    "gen/tmp_HRP2FixedSizeMemoryPoolPlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tSemaphore_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueue_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tPriorityDataqueue_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tFixedSizeMemoryPool_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tService_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_rUser_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_rUser_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueue_rUser_tecsgen.c"
    "${TECS_GEN_DIR}/tPriorityDataqueue_rUser_tecsgen.c"
    "${TECS_GEN_DIR}/tFixedSizeMemoryPool_rUser_tecsgen.c"
    "${TECS_GEN_DIR}/tUser_rUser_tecsgen.c"
    "${TECS_GEN_DIR}/tSemaphore_tecsgen.c"
    "${TECS_GEN_DIR}/tEventflag_tecsgen.c"
    "${TECS_GEN_DIR}/tDataqueue_tecsgen.c"
    "${TECS_GEN_DIR}/tPriorityDataqueue_tecsgen.c"
    "${TECS_GEN_DIR}/tFixedSizeMemoryPool_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_rKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_rUser_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee.c"
    "tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee.c"
)

set(TECS_CELLTYPE_SOURCES
    "tService.c"
    "tUser.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
)

set(TECS_INCLUDE_DIRS
    "${ASP3_SRCDIR}"
    "${ASP3_SRCDIR}/./gen"
    "${ASP3_SRCDIR}/../tecs_kernel"
    "${ASP3_SRCDIR}/../include"
    "${ASP3_SRCDIR}/../arch"
    "${ASP3_SRCDIR}/.."
    "${ASP3_SRCDIR}/../target/stm32p207_gcc"
    "${ASP3_SRCDIR}/../arch/arm_m_gcc/stm32f"
    "${ASP3_SRCDIR}/../arch/arm_m_gcc/common"
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

