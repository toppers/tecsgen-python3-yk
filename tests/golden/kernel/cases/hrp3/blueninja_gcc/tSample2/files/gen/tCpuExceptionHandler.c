#include "tCpuExceptionHandler_tecsgen.h"
void tCpuExceptionHandler_rKernelDomain_CpuExceptionHandler_start(void *p_excinf)
{
    CELLCB *p_cellcb = ((tCpuExceptionHandler_IDX)0);
    ciCpuExceptionHandlerBody_main(p_excinf);
}

