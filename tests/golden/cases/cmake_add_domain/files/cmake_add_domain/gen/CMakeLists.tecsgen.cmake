# generated automatically by tecsgen.
# included by cmake/Asp3Tecs.cmake (TECS_GEN_DIR must be set).

set(TECS_IMPORT_CDLS
    "restrict.cdl"
    "../cygwin3/cygwin_kernel.cdl"
    "../cygwin3/tSysLog.cdl"
    "gen/tMyTracePlugin_sSig.cdl"
    "gen/tmp_MyDomainPlugin_post_code.cdl"
    "gen/tmp_MyTracePlugin_post_code.cdl"
)

set(TECS_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tTask_rRegionSrc_tecsgen.c"
    "${TECS_GEN_DIR}/tCelltypeClient_rRegionSrc_tecsgen.c"
    "${TECS_GEN_DIR}/tKernel_tecsgen.c"
    "${TECS_GEN_DIR}/tSysLog_tecsgen.c"
    "${TECS_GEN_DIR}/tCelltype_rRegionDst_tecsgen.c"
)

set(TECS_PLUGIN_TECSGEN_SOURCES
    "${TECS_GEN_DIR}/tMyTracePlugin_sSig_rRegionSrc_tecsgen.c"
)

set(TECS_PLUGIN_CELLTYPE_SOURCES
    "tMyTracePlugin_sSig.c"
)

set(TECS_CELLTYPE_SOURCES
    "tTask.c"
    "tCelltypeClient.c"
    "tSysLog.c"
    "tCelltype.c"
)

set(TECS_PLUGIN_EXTRA_SOURCES
    "domain_plugin.c"
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
    "inc_domain"
)

set(TECS_COMPILE_DEFINITIONS
    "K_DOMAIN=1"
)

# plugin additional cmake lines
# from domain

