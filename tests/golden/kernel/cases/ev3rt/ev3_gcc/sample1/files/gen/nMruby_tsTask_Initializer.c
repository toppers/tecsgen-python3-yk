/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "nMruby_tsTask_Initializer_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* MBP: MrubyBridgePlugin: MBP000 */
#ifndef TECSGEN
#include "mruby.h"
#include "mruby/class.h"
#include "mruby/data.h"
#include "mruby/string.h"
#endif /* TECSGEN */
#include "TECSPointer.h"
#include "TECSStruct.h"

#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifndef NULL
#define NULL 0
#endif
//  Prototype MBP400
mrb_value  MrubyBridge_tsTask_initialize( mrb_state *mrb, mrb_value self);
mrb_value  MrubyBridge_tsTask_activate( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_cancelActivate( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_terminate( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_changePriority( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_getPriority( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_refer( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_wakeup( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_cancelWakeup( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_releaseWait( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_suspend( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_resume( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_raiseException( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_referException( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_startOverRunHandler( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_stopOverRunHandler( mrb_state *mrb, mrb_value self );
mrb_value  MrubyBridge_tsTask_referOverRunHandler( mrb_state *mrb, mrb_value self );
/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eInitialize
 * entry port: eInitialize
 * signature:  nMruby_sInitializeTECSBridge
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eInitialize_initializeBridge
 * name:         eInitialize_initializeBridge
 * global_name:  nMruby_tsTask_Initializer_eInitialize_initializeBridge
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eInitialize_initializeBridge(CELLIDX idx, mrb_state* mrb, struct RClass* TECS)
{
    // CELLCB *p_cellcb = GET_CELLCB( idx );  /* no error check */     /* MBP700 */
    struct RClass	*rc;

    rc = mrb_define_class_under( mrb, TECS, "TsTask", mrb->object_class );
    mrb_define_method( mrb, rc, "initialize", MrubyBridge_tsTask_initialize, MRB_ARGS_REQ(1) );
    MRB_SET_INSTANCE_TT(rc, MRB_TT_DATA);
	mrb_define_method( mrb, rc, "activate", MrubyBridge_tsTask_activate, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "cancelActivate", MrubyBridge_tsTask_cancelActivate, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "terminate", MrubyBridge_tsTask_terminate, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "changePriority", MrubyBridge_tsTask_changePriority, MRB_ARGS_REQ( 1 ) );
	mrb_define_method( mrb, rc, "getPriority", MrubyBridge_tsTask_getPriority, MRB_ARGS_REQ( 1 ) );
	mrb_define_method( mrb, rc, "refer", MrubyBridge_tsTask_refer, MRB_ARGS_REQ( 1 ) );
	mrb_define_method( mrb, rc, "wakeup", MrubyBridge_tsTask_wakeup, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "cancelWakeup", MrubyBridge_tsTask_cancelWakeup, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "releaseWait", MrubyBridge_tsTask_releaseWait, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "suspend", MrubyBridge_tsTask_suspend, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "resume", MrubyBridge_tsTask_resume, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "raiseException", MrubyBridge_tsTask_raiseException, MRB_ARGS_REQ( 1 ) );
	mrb_define_method( mrb, rc, "referException", MrubyBridge_tsTask_referException, MRB_ARGS_REQ( 1 ) );
	mrb_define_method( mrb, rc, "startOverRunHandler", MrubyBridge_tsTask_startOverRunHandler, MRB_ARGS_REQ( 1 ) );
	mrb_define_method( mrb, rc, "stopOverRunHandler", MrubyBridge_tsTask_stopOverRunHandler, MRB_ARGS_NONE() );
	mrb_define_method( mrb, rc, "referOverRunHandler", MrubyBridge_tsTask_referOverRunHandler, MRB_ARGS_REQ( 1 ) );
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
