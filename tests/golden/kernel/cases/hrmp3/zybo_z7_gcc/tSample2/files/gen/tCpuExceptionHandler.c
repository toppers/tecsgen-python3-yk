#include "tCpuExceptionHandler_tecsgen.h"
void tCpuExceptionHandler_rKernelDomain_rProcessor1Migratable_CpuExceptionHandler_start(void *p_excinf)
{
    CELLCB *p_cellcb = &rKernelDomain_rProcessor1Migratable_CpuExceptionHandler_INIB;
    ciCpuExceptionHandlerBody_main(p_excinf);
}

void tCpuExceptionHandler_rKernelDomain_rProcessor2Symmetric_CpuExceptionHandler2_start(void *p_excinf)
{
    CELLCB *p_cellcb = &rKernelDomain_rProcessor2Symmetric_CpuExceptionHandler2_INIB;
    ciCpuExceptionHandlerBody_main(p_excinf);
}

