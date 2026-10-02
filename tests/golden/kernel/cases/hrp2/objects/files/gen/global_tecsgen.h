/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef GLOBAL_TECSGEN_H
#define GLOBAL_TECSGEN_H


/* import_C により import されるヘッダ #_IMP_# */
#include "tecs_kernel.h"
/**/

#ifndef TOPPERS_MACRO_ONLY

 extern void tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB_initialize();
 extern void tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_CB_initialize();
 extern void tSemaphore_CB_initialize();
 extern void tEventflag_CB_initialize();
 extern void tDataqueue_CB_initialize();
 extern void tPriorityDataqueue_CB_initialize();
 extern void tFixedSizeMemoryPool_CB_initialize();
 extern void tService_CB_initialize();
 extern void tUser_CB_initialize();

#define INITIALIZE_TECS() \
 	tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB_initialize();\
 	tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_CB_initialize();\
 	tSemaphore_CB_initialize();\
 	tEventflag_CB_initialize();\
 	tDataqueue_CB_initialize();\
 	tPriorityDataqueue_CB_initialize();\
 	tFixedSizeMemoryPool_CB_initialize();\
 	tService_CB_initialize();\
 	tUser_CB_initialize();\
/* INITIALIZE_TECS terminator */

#define INITIALZE_TECSGEN() INITIALIZE_TECS()  /* for backward compatibility */

/* Descriptor for dynamic join */
#define Descriptor( signature_global_name )  DynDesc__ ## signature_global_name
#define is_descriptor_unjoined( desc )  ((desc).vdes==NULL)

#endif /* TOPPERS_MACRO_ONLY */


#endif /* GLOBAL_TECSGEN_H */
