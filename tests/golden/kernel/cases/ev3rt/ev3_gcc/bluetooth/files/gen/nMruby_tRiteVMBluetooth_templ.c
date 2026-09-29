/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tRiteVMBluetooth_templ.c => src/tRiteVMBluetooth.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * irepLib          uint8_t*         ATTR_irepLib    
 * irepAppSize      uint32_t         ATTR_irepAppSize
 * setptn           FLGPTN           ATTR_setptn     
 * mrb              mrb_state*       VAR_mrb         
 * context          mrbc_context*    VAR_context     
 * irepApp          uint8_t*         VAR_irepApp     
 *
 * 呼び口関数 #_TCPF_#
 * require port: signature:sKernel context:task
 *   ER             sleep( );
 *   ER             sleepTimeout( TMO timeout );
 *   ER             delay( RELTIM delayTime );
 *   ER             exitTask( );
 *   ER             getTaskId( ID* p_taskId );
 *   ER             rotateReadyQueue( PRI taskPriority );
 *   ER             getTime( SYSTIM* p_systemTime );
 *   ER             getMicroTime( SYSUTM* p_systemMicroTime );
 *   ER             lockCpu( );
 *   ER             unlockCpu( );
 *   ER             disableDispatch( );
 *   ER             enableDispatch( );
 *   ER             disableTaskException( );
 *   ER             enableTaskException( );
 *   ER             changeInterruptPriorityMask( PRI interruptPriority );
 *   ER             getInterruptPriorityMask( PRI* p_interruptPriority );
 *   ER             exitKernel( );
 *   bool_t         senseContext( );
 *   bool_t         senseLock( );
 *   bool_t         senseDispatch( );
 *   bool_t         senseDispatchPendingState( );
 *   bool_t         senseKernel( );
 * call port: cMrubyTask signature: sTask context:task
 *   ER             cMrubyTask_activate( );
 *   ER_UINT        cMrubyTask_cancelActivate( );
 *   ER             cMrubyTask_terminate( );
 *   ER             cMrubyTask_changePriority( PRI priority );
 *   ER             cMrubyTask_getPriority( PRI* p_priority );
 *   ER             cMrubyTask_refer( T_RTSK* pk_taskStatus );
 *   ER             cMrubyTask_wakeup( );
 *   ER_UINT        cMrubyTask_cancelWakeup( );
 *   ER             cMrubyTask_releaseWait( );
 *   ER             cMrubyTask_suspend( );
 *   ER             cMrubyTask_resume( );
 *   ER             cMrubyTask_raiseException( TEXPTN pattern );
 *   ER             cMrubyTask_referException( T_RTEX* pk_rtex );
 *   ER             cMrubyTask_startOverRunHandler( OVRTIM ovrtim );
 *   ER             cMrubyTask_stopOverRunHandler( );
 *   ER             cMrubyTask_referOverRunHandler( T_ROVR* pk_rovr );
 * call port: cZmodemTask signature: sTask context:task
 *   ER             cZmodemTask_activate( );
 *   ER_UINT        cZmodemTask_cancelActivate( );
 *   ER             cZmodemTask_terminate( );
 *   ER             cZmodemTask_changePriority( PRI priority );
 *   ER             cZmodemTask_getPriority( PRI* p_priority );
 *   ER             cZmodemTask_refer( T_RTSK* pk_taskStatus );
 *   ER             cZmodemTask_wakeup( );
 *   ER_UINT        cZmodemTask_cancelWakeup( );
 *   ER             cZmodemTask_releaseWait( );
 *   ER             cZmodemTask_suspend( );
 *   ER             cZmodemTask_resume( );
 *   ER             cZmodemTask_raiseException( TEXPTN pattern );
 *   ER             cZmodemTask_referException( T_RTEX* pk_rtex );
 *   ER             cZmodemTask_startOverRunHandler( OVRTIM ovrtim );
 *   ER             cZmodemTask_stopOverRunHandler( );
 *   ER             cZmodemTask_referOverRunHandler( T_ROVR* pk_rovr );
 * call port: cReset signature: sReset context:task
 *   void           cReset_reset( );
 * call port: cCyclic signature: sCyclic context:task optional:true
 *   bool_t     is_cCyclic_joined()                     check if joined
 *   ER             cCyclic_start( );
 *   ER             cCyclic_stop( );
 *   ER             cCyclic_refer( T_RCYC* pk_cyclicHandlerStatus );
 * call port: cEventflag signature: sEventflag context:task optional:true
 *   bool_t     is_cEventflag_joined(int subscript)        check if joined
 *   ER             cEventflag_set( subscript, FLGPTN setPattern );
 *   ER             cEventflag_clear( subscript, FLGPTN clearPattern );
 *   ER             cEventflag_wait( subscript, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern );
 *   ER             cEventflag_waitPolling( subscript, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern );
 *   ER             cEventflag_waitTimeout( subscript, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern, TMO timeout );
 *   ER             cEventflag_initialize( subscript );
 *   ER             cEventflag_refer( subscript, T_RFLG* pk_eventflagStatus );
 *       subscript:  0...(NCP_cEventflag-1)
 * call port: cSemaphore signature: sSemaphore context:task optional:true
 *   bool_t     is_cSemaphore_joined()                     check if joined
 *   ER             cSemaphore_signal( );
 *   ER             cSemaphore_wait( );
 *   ER             cSemaphore_waitPolling( );
 *   ER             cSemaphore_waitTimeout( TMO timeout );
 *   ER             cSemaphore_initialize( );
 *   ER             cSemaphore_refer( T_RSEM* pk_semaphoreStatus );
 * call port: cInit signature: nMruby_sInitializeBridge context:task optional:true
 *   bool_t     is_cInit_joined()                     check if joined
 *   void           cInit_initializeBridge( const mrb_state* mrb );
 * call port: cMalloc signature: sMalloc context:task
 *   int            cMalloc_initializeMemoryPool( );
 *   void*          cMalloc_calloc( size_t nelem, size_t elem_size );
 *   void*          cMalloc_malloc( size_t size );
 *   void*          cMalloc_realloc( const void* ptr, size_t new_size );
 *   void           cMalloc_free( const void* ptr );
 * call port: cZmodemToppers signature: sZmodemToppers context:task
 *   ER             cZmodemToppers_zmodem_recv_file( ID portid, const uint8_t* buf, uint32_t size, SIZE* filesz );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "nMruby_tRiteVMBluetooth_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eMrubyBody
 * entry port: eMrubyBody
 * signature:  sTaskBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eMrubyBody_main
 * name:         eMrubyBody_main
 * global_name:  nMruby_tRiteVMBluetooth_eMrubyBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eMrubyBody_main(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eMrubyBody_main' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_PORT>]# eRiteVM
 * entry port: eRiteVM
 * signature:  sRiteVM
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eRiteVM_reset
 * name:         eRiteVM_reset
 * global_name:  nMruby_tRiteVMBluetooth_eRiteVM_reset
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eRiteVM_reset(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eRiteVM_reset' needs to be edited."   /* delete this line after edit */

}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
