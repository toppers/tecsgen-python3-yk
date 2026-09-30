/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * call port: cTECS signature: sTask context:task
 *   ER             cTECS_activate( );
 *   ER_UINT        cTECS_cancelActivate( );
 *   ER             cTECS_terminate( );
 *   ER             cTECS_changePriority( PRI priority );
 *   ER             cTECS_getPriority( PRI* p_priority );
 *   ER             cTECS_refer( T_RTSK* pk_taskStatus );
 *   ER             cTECS_wakeup( );
 *   ER_UINT        cTECS_cancelWakeup( );
 *   ER             cTECS_releaseWait( );
 *   ER             cTECS_suspend( );
 *   ER             cTECS_resume( );
 *   ER             cTECS_raiseException( TEXPTN pattern );
 *   ER             cTECS_referException( T_RTEX* pk_rtex );
 *   ER             cTECS_startOverRunHandler( OVRTIM ovrtim );
 *   ER             cTECS_stopOverRunHandler( );
 *   ER             cTECS_referOverRunHandler( T_ROVR* pk_rovr );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "nMruby_tsTask_tecsgen.h"

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
extern nMruby_tsTask_CB  rDomainEV3_EV3TaskeTaskBridge_INIB;
extern nMruby_tsTask_CB  rDomainEV3_MrubyMainTaskeTaskBridge_INIB;
extern nMruby_tsTask_CB  rDomainEV3_MrubySubTask1eTaskBridge_INIB;
extern nMruby_tsTask_CB  rDomainEV3_MrubySubTask2eTaskBridge_INIB;
extern nMruby_tsTask_CB  rDomainEV3_MrubyWakeupTaskeTaskBridge_INIB;
extern nMruby_tsTask_CB  rDomainEV3_MrubyCyclicTaskeTaskBridge_INIB;

/* RData MBP001 */
static void 
tsTask_free( mrb_state *mrb, void *p )
{
	if( p )
		(void)mrb_free( mrb, p );
}

/* RData MBP002 */
struct mrb_data_type data_type_tsTask =
{
	"tsTask",
	tsTask_free
};

/* RData MBP003 */
struct tecs_tsTask {
    CELLCB  *cbp;
};

/* name_to_cbp MBP010 */
const struct name_to_cbp_tsTask {
    char   *name;    /* Cell Name */
    CELLCB *cbp;
} Name_to_cbp_tsTask[] = {
	{ "EV3TaskeTaskBridge", &rDomainEV3_EV3TaskeTaskBridge_INIB },
	{ "MrubyMainTaskeTaskBridge", &rDomainEV3_MrubyMainTaskeTaskBridge_INIB },
	{ "MrubySubTask1eTaskBridge", &rDomainEV3_MrubySubTask1eTaskBridge_INIB },
	{ "MrubySubTask2eTaskBridge", &rDomainEV3_MrubySubTask2eTaskBridge_INIB },
	{ "MrubyWakeupTaskeTaskBridge", &rDomainEV3_MrubyWakeupTaskeTaskBridge_INIB },
	{ "MrubyCyclicTaskeTaskBridge", &rDomainEV3_MrubyCyclicTaskeTaskBridge_INIB },
	{ 0, 0 },
};


/* MBP100 */
mrb_value
MrubyBridge_tsTask_initialize( mrb_state *mrb, mrb_value self)
{
	mrb_value	name;
	struct tecs_tsTask *tecs_cb;
	const struct name_to_cbp_tsTask *ntc;

	/* set DATA_TYPE earlier to avoid SEGV */
	DATA_TYPE( self ) = &data_type_tsTask;

	mrb_get_args(mrb, "o", &name );
	if( mrb_type( name ) != MRB_TT_STRING ){
		mrb_raise(mrb, E_NAME_ERROR, "cell name not string");
	}
	for( ntc = &Name_to_cbp_tsTask[0]; ntc->name != NULL; ntc++ ){
		if( strcmp( ntc->name, RSTRING_PTR( name ) ) == 0 )
			break;
	}
	if( ntc->name == 0 ){
		mrb_raise(mrb, E_ARGUMENT_ERROR, "cell not found");
	}
	tecs_cb = (struct tecs_tsTask *)mrb_malloc(mrb, sizeof(struct tecs_tsTask) );
	tecs_cb->cbp = ntc->cbp;
	DATA_PTR( self ) = (void *)tecs_cb;

	return self;
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_activate( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_activate(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_cancelActivate( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER_UINT	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_cancelActivate(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_terminate( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_terminate(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_changePriority( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_int	mrb_priority;
	PRI	priority;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "i", &mrb_priority );
	/* convert mrb to C (MBP112) */
	VALCHECK_Int( mrb, mrb_priority );
	priority = (PRI)mrb_priority;
	/* calling target (MBP120) */
	ret_val = cTECS_changePriority( priority );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_getPriority( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_value	mrb_p_priority;
	PRI*	p_priority;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "o", &mrb_p_priority );
	/* convert mrb to C for pointer types (MBP113) */
	p_priority = CheckAndGetIntPointer( mrb, mrb_p_priority, 1 );
	/* calling target (MBP120) */
	ret_val = cTECS_getPriority( p_priority );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_refer( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_value	mrb_pk_taskStatus;
	T_RTSK*	pk_taskStatus;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "o", &mrb_pk_taskStatus );
	CHECK_STRUCT( t_rtsk, mrb_pk_taskStatus );
	pk_taskStatus = (struct t_rtsk*)DATA_PTR(mrb_pk_taskStatus);
	/* convert mrb to C for pointer types (MBP113) */
	/* calling target (MBP120) */
	ret_val = cTECS_refer( pk_taskStatus );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_wakeup( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_wakeup(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_cancelWakeup( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER_UINT	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_cancelWakeup(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_releaseWait( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_releaseWait(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_suspend( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_suspend(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_resume( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_resume(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_raiseException( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_int	mrb_pattern;
	TEXPTN	pattern;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "i", &mrb_pattern );
	/* convert mrb to C (MBP112) */
	VALCHECK_UInt( mrb, mrb_pattern );
	pattern = (TEXPTN)mrb_pattern;
	/* calling target (MBP120) */
	ret_val = cTECS_raiseException( pattern );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_referException( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_value	mrb_pk_rtex;
	T_RTEX*	pk_rtex;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "o", &mrb_pk_rtex );
	CHECK_STRUCT( t_rtex, mrb_pk_rtex );
	pk_rtex = (struct t_rtex*)DATA_PTR(mrb_pk_rtex);
	/* convert mrb to C for pointer types (MBP113) */
	/* calling target (MBP120) */
	ret_val = cTECS_referException( pk_rtex );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_startOverRunHandler( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_int	mrb_ovrtim;
	OVRTIM	ovrtim;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "i", &mrb_ovrtim );
	/* convert mrb to C (MBP112) */
	VALCHECK_ULong( mrb, mrb_ovrtim );
	ovrtim = (OVRTIM)mrb_ovrtim;
	/* calling target (MBP120) */
	ret_val = cTECS_startOverRunHandler( ovrtim );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_stopOverRunHandler( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	/* calling target (MBP120) */
	ret_val = cTECS_stopOverRunHandler(  );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}

/* bridge function (MBP101) */
mrb_value
MrubyBridge_tsTask_referOverRunHandler( mrb_state *mrb, mrb_value self )
{
	/* cellcbp (MBP105) */
	CELLCB	*p_cellcb = ((struct tecs_tsTask *)DATA_PTR(self))->cbp;
	/* variables for return & parameter (MBP110) */
	ER	ret_val;
	mrb_value	mrb_pk_rovr;
	T_ROVR*	pk_rovr;
	/* retrieve arguments (MBP111) */
	mrb_get_args(mrb, "o", &mrb_pk_rovr );
	CHECK_STRUCT( t_rovr, mrb_pk_rovr );
	pk_rovr = (struct t_rovr*)DATA_PTR(mrb_pk_rovr);
	/* convert mrb to C for pointer types (MBP113) */
	/* calling target (MBP120) */
	ret_val = cTECS_referOverRunHandler( pk_rovr );
	/* return (MBP130) */
	return mrb_fixnum_value( ret_val );
}
/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
