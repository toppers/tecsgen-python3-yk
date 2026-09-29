#include "tCpuExceptionHandler_tecsgen.h"
void tCpuExceptionHandler_rProcessor1Migratable_CpuExceptionHandler_start(void *p_excinf)
{
    CELLCB *p_cellcb = &rProcessor1Migratable_CpuExceptionHandler_INIB;
    ciCpuExceptionHandlerBody_main(p_excinf);
}

void tCpuExceptionHandler_rProcessor2Symmetric_CpuExceptionHandler2_start(void *p_excinf)
{
    CELLCB *p_cellcb = &rProcessor2Symmetric_CpuExceptionHandler2_INIB;
    ciCpuExceptionHandlerBody_main(p_excinf);
}

