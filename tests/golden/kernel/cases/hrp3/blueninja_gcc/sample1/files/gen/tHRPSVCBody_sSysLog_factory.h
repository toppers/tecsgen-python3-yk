#ifndef tHRPSVCBody_sSysLog_FACTORY_H
#define tHRPSVCBody_sSysLog_FACTORY_H
/* HRP013 */
#include "tHRPSVCCaller_sSysLog_id.h"

#ifndef SSZ_SVCBody_SysLog_eSysLog_write
#define SSZ_SVCBody_SysLog_eSysLog_write DefaultExtsvcStackSize
#endif /* SSZ_SVCBody_SysLog_eSysLog_write */
ER_UINT rKernelDomain_SVCBody_SysLog_eSysLog_write(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);

/* HRP013 */
#include "tHRPSVCCaller_sSysLog_id.h"

#ifndef SSZ_SVCBody_SysLog_eSysLog_read
#define SSZ_SVCBody_SysLog_eSysLog_read DefaultExtsvcStackSize
#endif /* SSZ_SVCBody_SysLog_eSysLog_read */
ER_UINT rKernelDomain_SVCBody_SysLog_eSysLog_read(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);

/* HRP013 */
#include "tHRPSVCCaller_sSysLog_id.h"

#ifndef SSZ_SVCBody_SysLog_eSysLog_mask
#define SSZ_SVCBody_SysLog_eSysLog_mask DefaultExtsvcStackSize
#endif /* SSZ_SVCBody_SysLog_eSysLog_mask */
ER_UINT rKernelDomain_SVCBody_SysLog_eSysLog_mask(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);

/* HRP013 */
#include "tHRPSVCCaller_sSysLog_id.h"

#ifndef SSZ_SVCBody_SysLog_eSysLog_refer
#define SSZ_SVCBody_SysLog_eSysLog_refer DefaultExtsvcStackSize
#endif /* SSZ_SVCBody_SysLog_eSysLog_refer */
ER_UINT rKernelDomain_SVCBody_SysLog_eSysLog_refer(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);

/* HRP013 */
#include "tHRPSVCCaller_sSysLog_id.h"

#ifndef SSZ_SVCBody_SysLog_eSysLog_flush
#define SSZ_SVCBody_SysLog_eSysLog_flush DefaultExtsvcStackSize
#endif /* SSZ_SVCBody_SysLog_eSysLog_flush */
ER_UINT rKernelDomain_SVCBody_SysLog_eSysLog_flush(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);

#endif /* tHRPSVCBody_sSysLog_FACTORY_H */
