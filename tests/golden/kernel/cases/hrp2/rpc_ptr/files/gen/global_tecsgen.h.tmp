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

 extern void tMarshaler_sCallee_CB_initialize();
 extern void tUnmarshaler_sCallee_CB_initialize();
 extern void tTask_CB_initialize();
 extern void tSemaphore_CB_initialize();
 extern void tEventflag_CB_initialize();
 extern void tMessageBuffer_CB_initialize();
 extern void tRPCDedicatedTaskMain_CB_initialize();
 extern void tServer_CB_initialize();
 extern void tClient_CB_initialize();

#define INITIALIZE_TECS() \
 	tMarshaler_sCallee_CB_initialize();\
 	tUnmarshaler_sCallee_CB_initialize();\
 	tTask_CB_initialize();\
 	tSemaphore_CB_initialize();\
 	tEventflag_CB_initialize();\
 	tMessageBuffer_CB_initialize();\
 	tRPCDedicatedTaskMain_CB_initialize();\
 	tServer_CB_initialize();\
 	tClient_CB_initialize();\
/* INITIALIZE_TECS terminator */

#define INITIALZE_TECSGEN() INITIALIZE_TECS()  /* for backward compatibility */

/* Descriptor for dynamic join */
#define Descriptor( signature_global_name )  DynDesc__ ## signature_global_name
#define is_descriptor_unjoined( desc )  ((desc).vdes==NULL)

#endif /* TOPPERS_MACRO_ONLY */


#endif /* GLOBAL_TECSGEN_H */
