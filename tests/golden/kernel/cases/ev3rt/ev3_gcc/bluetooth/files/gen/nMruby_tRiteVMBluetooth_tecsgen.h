/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef nMruby_tRiteVMBluetooth_TECSGEN_H
#define nMruby_tRiteVMBluetooth_TECSGEN_H

/*
 * celltype          :  tRiteVMBluetooth
 * global name       :  nMruby_tRiteVMBluetooth
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  no
 * has_CB            :  yes
 * has_INIB          :  yes
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sKernel_tecsgen.h"
#include "sTask_tecsgen.h"
#include "sReset_tecsgen.h"
#include "sCyclic_tecsgen.h"
#include "sEventflag_tecsgen.h"
#include "sSemaphore_tecsgen.h"
#include "sTaskBody_tecsgen.h"
#include "sRiteVM_tecsgen.h"
#include "nMruby_sInitializeBridge_tecsgen.h"
#include "sMalloc_tecsgen.h"
#include "sZmodemToppers_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_nMruby_tRiteVMBluetooth_INIB {
    /* call port #_TCP_# */
    struct tag_sEventflag_VDES *const*cEventflag; /* TCP_2 */
    int_t n_cEventflag;  /* TCP_3 */
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    uint8_t*       irepLib;
    uint32_t       irepAppSize;
    FLGPTN         setptn;
    uint8_t*       irepApp;
}  nMruby_tRiteVMBluetooth_INIB;
/* セル CB 型宣言 #_CCTPA_# */
typedef struct tag_nMruby_tRiteVMBluetooth_CB {
    nMruby_tRiteVMBluetooth_INIB  *_inib;
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* var #_VA_# */ 
    mrb_state*     mrb;
    mrbc_context*  context;
}  nMruby_tRiteVMBluetooth_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern nMruby_tRiteVMBluetooth_CB  nMruby_tRiteVMBluetooth_CB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef struct tag_nMruby_tRiteVMBluetooth_CB *nMruby_tRiteVMBluetooth_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         nMruby_tRiteVMBluetooth_eMrubyBody_main(nMruby_tRiteVMBluetooth_IDX idx);
/* sRiteVM */
void         nMruby_tRiteVMBluetooth_eRiteVM_reset(nMruby_tRiteVMBluetooth_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  nMruby_tRiteVMBluetooth_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tKernel_tecsgen.h"
#include "tTask_tecsgen.h"
#include "tReset_tecsgen.h"
#include "tSemaphore_tecsgen.h"
#include "nMruby_tTECSInitializer_tecsgen.h"
#include "tTLSFMalloc_tecsgen.h"
#include "tZmodemToppers_tecsgen.h"
#ifdef  nMruby_tRiteVMBluetooth_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* nMruby_tRiteVMBluetooth_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define nMruby_tRiteVMBluetooth_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define nMruby_tRiteVMBluetooth_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define nMruby_tRiteVMBluetooth_VALID_IDX(IDX) (1)

/* 呼び口配列の大きさを得るマクロ #_NCPA_# */
#define N_CP_cEventflag(p_that)  ((p_that)->_inib->n_cEventflag)
#define NCP_cEventflag           (N_CP_cEventflag(p_cellcb))
/* optional 呼び口をテストするマクロ #_TOCP_# */
#define nMruby_tRiteVMBluetooth_is_cCyclic_joined(p_that) \
	  (0)    /* not joined */
#define nMruby_tRiteVMBluetooth_is_cEventflag_joined(p_that,subscript) \
	  (((p_that)->_inib->cEventflag!=0)\
	  &&((p_that)->_inib->cEventflag[subscript]!=0))
#define nMruby_tRiteVMBluetooth_is_cSemaphore_joined(p_that) \
	  (1)
#define nMruby_tRiteVMBluetooth_is_cInit_joined(p_that) \
	  (1)

/* セルCBを得るマクロ #_GCB_# */
#define nMruby_tRiteVMBluetooth_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define nMruby_tRiteVMBluetooth_ATTR_irepLib( p_that )	((p_that)->_inib->irepLib)
#define nMruby_tRiteVMBluetooth_ATTR_irepAppSize( p_that )	((p_that)->_inib->irepAppSize)
#define nMruby_tRiteVMBluetooth_ATTR_setptn( p_that )	((p_that)->_inib->setptn)

#define nMruby_tRiteVMBluetooth_GET_irepLib(p_that)	((p_that)->_inib->irepLib)
#define nMruby_tRiteVMBluetooth_GET_irepAppSize(p_that)	((p_that)->_inib->irepAppSize)
#define nMruby_tRiteVMBluetooth_GET_setptn(p_that)	((p_that)->_inib->setptn)


/* var アクセスマクロ #_VAM_# */
#define nMruby_tRiteVMBluetooth_VAR_mrb(p_that)	((p_that)->mrb)
#define nMruby_tRiteVMBluetooth_VAR_context(p_that)	((p_that)->context)
#define nMruby_tRiteVMBluetooth_VAR_irepApp(p_that)	((p_that)->_inib->irepApp)

#define nMruby_tRiteVMBluetooth_GET_mrb(p_that)	((p_that)->mrb)
#define nMruby_tRiteVMBluetooth_SET_mrb(p_that,val)	((p_that)->mrb=(val))
#define nMruby_tRiteVMBluetooth_GET_context(p_that)	((p_that)->context)
#define nMruby_tRiteVMBluetooth_SET_context(p_that,val)	((p_that)->context=(val))
#define nMruby_tRiteVMBluetooth_GET_irepApp(p_that)	((p_that)->irepApp)
#define nMruby_tRiteVMBluetooth_SET_irepApp(p_that,val)	((p_that)->irepApp=(val))

#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_sleep( p_that ) \
	  tKernel_eKernel_sleep( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_sleepTimeout( p_that, timeout ) \
	  tKernel_eKernel_sleepTimeout( \
	    (timeout) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_delay( p_that, delayTime ) \
	  tKernel_eKernel_delay( \
	    (delayTime) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_exitTask( p_that ) \
	  tKernel_eKernel_exitTask( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getTaskId( p_that, p_taskId ) \
	  tKernel_eKernel_getTaskId( \
	    (p_taskId) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_rotateReadyQueue( p_that, taskPriority ) \
	  tKernel_eKernel_rotateReadyQueue( \
	    (taskPriority) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getTime( p_that, p_systemTime ) \
	  tKernel_eKernel_getTime( \
	    (p_systemTime) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getMicroTime( p_that, p_systemMicroTime ) \
	  tKernel_eKernel_getMicroTime( \
	    (p_systemMicroTime) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_lockCpu( p_that ) \
	  tKernel_eKernel_lockCpu( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_unlockCpu( p_that ) \
	  tKernel_eKernel_unlockCpu( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_disableDispatch( p_that ) \
	  tKernel_eKernel_disableDispatch( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_enableDispatch( p_that ) \
	  tKernel_eKernel_enableDispatch( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_disableTaskException( p_that ) \
	  tKernel_eKernel_disableTaskException( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_enableTaskException( p_that ) \
	  tKernel_eKernel_enableTaskException( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_changeInterruptPriorityMask( p_that, interruptPriority ) \
	  tKernel_eKernel_changeInterruptPriorityMask( \
	    (interruptPriority) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getInterruptPriorityMask( p_that, p_interruptPriority ) \
	  tKernel_eKernel_getInterruptPriorityMask( \
	    (p_interruptPriority) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_exitKernel( p_that ) \
	  tKernel_eKernel_exitKernel( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseContext( p_that ) \
	  tKernel_eKernel_senseContext( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseLock( p_that ) \
	  tKernel_eKernel_senseLock( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseDispatch( p_that ) \
	  tKernel_eKernel_senseDispatch( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseDispatchPendingState( p_that ) \
	  tKernel_eKernel_senseDispatchPendingState( \
	    )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseKernel( p_that ) \
	  tKernel_eKernel_senseKernel( \
	    )
#define nMruby_tRiteVMBluetooth_cMrubyTask_activate( p_that ) \
	  tTask_eTask_activate( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_cancelActivate( p_that ) \
	  tTask_eTask_cancelActivate( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_terminate( p_that ) \
	  tTask_eTask_terminate( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_changePriority( p_that, priority ) \
	  tTask_eTask_changePriority( \
	   &tTask_INIB_tab[1], (priority) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_getPriority( p_that, p_priority ) \
	  tTask_eTask_getPriority( \
	   &tTask_INIB_tab[1], (p_priority) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_refer( p_that, pk_taskStatus ) \
	  tTask_eTask_refer( \
	   &tTask_INIB_tab[1], (pk_taskStatus) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_wakeup( p_that ) \
	  tTask_eTask_wakeup( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_cancelWakeup( p_that ) \
	  tTask_eTask_cancelWakeup( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_releaseWait( p_that ) \
	  tTask_eTask_releaseWait( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_suspend( p_that ) \
	  tTask_eTask_suspend( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_resume( p_that ) \
	  tTask_eTask_resume( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_raiseException( p_that, pattern ) \
	  tTask_eTask_raiseException( \
	   &tTask_INIB_tab[1], (pattern) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_referException( p_that, pk_rtex ) \
	  tTask_eTask_referException( \
	   &tTask_INIB_tab[1], (pk_rtex) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_startOverRunHandler( p_that, ovrtim ) \
	  tTask_eTask_startOverRunHandler( \
	   &tTask_INIB_tab[1], (ovrtim) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_stopOverRunHandler( p_that ) \
	  tTask_eTask_stopOverRunHandler( \
	   &tTask_INIB_tab[1] )
#define nMruby_tRiteVMBluetooth_cMrubyTask_referOverRunHandler( p_that, pk_rovr ) \
	  tTask_eTask_referOverRunHandler( \
	   &tTask_INIB_tab[1], (pk_rovr) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_activate( p_that ) \
	  tTask_eTask_activate( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_cancelActivate( p_that ) \
	  tTask_eTask_cancelActivate( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_terminate( p_that ) \
	  tTask_eTask_terminate( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_changePriority( p_that, priority ) \
	  tTask_eTask_changePriority( \
	   &tTask_INIB_tab[2], (priority) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_getPriority( p_that, p_priority ) \
	  tTask_eTask_getPriority( \
	   &tTask_INIB_tab[2], (p_priority) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_refer( p_that, pk_taskStatus ) \
	  tTask_eTask_refer( \
	   &tTask_INIB_tab[2], (pk_taskStatus) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_wakeup( p_that ) \
	  tTask_eTask_wakeup( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_cancelWakeup( p_that ) \
	  tTask_eTask_cancelWakeup( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_releaseWait( p_that ) \
	  tTask_eTask_releaseWait( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_suspend( p_that ) \
	  tTask_eTask_suspend( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_resume( p_that ) \
	  tTask_eTask_resume( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_raiseException( p_that, pattern ) \
	  tTask_eTask_raiseException( \
	   &tTask_INIB_tab[2], (pattern) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_referException( p_that, pk_rtex ) \
	  tTask_eTask_referException( \
	   &tTask_INIB_tab[2], (pk_rtex) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_startOverRunHandler( p_that, ovrtim ) \
	  tTask_eTask_startOverRunHandler( \
	   &tTask_INIB_tab[2], (ovrtim) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_stopOverRunHandler( p_that ) \
	  tTask_eTask_stopOverRunHandler( \
	   &tTask_INIB_tab[2] )
#define nMruby_tRiteVMBluetooth_cZmodemTask_referOverRunHandler( p_that, pk_rovr ) \
	  tTask_eTask_referOverRunHandler( \
	   &tTask_INIB_tab[2], (pk_rovr) )
#define nMruby_tRiteVMBluetooth_cReset_reset( p_that ) \
	  tReset_eReset_reset( \
	   &tReset_INIB_tab[0] )
#define nMruby_tRiteVMBluetooth_cCyclic_start( p_that ) \
	  ((ER (*)())0)()
	  /* optional no entry port joined */
#define nMruby_tRiteVMBluetooth_cCyclic_stop( p_that ) \
	  ((ER (*)())0)()
	  /* optional no entry port joined */
#define nMruby_tRiteVMBluetooth_cCyclic_refer( p_that, pk_cyclicHandlerStatus ) \
	  ((ER (*)())0)()
	  /* optional no entry port joined */
#define nMruby_tRiteVMBluetooth_cEventflag_set( p_that, subscript, setPattern ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->set__T( \
	   (p_that)->_inib->cEventflag[subscript], (setPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_clear( p_that, subscript, clearPattern ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->clear__T( \
	   (p_that)->_inib->cEventflag[subscript], (clearPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_wait( p_that, subscript, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->wait__T( \
	   (p_that)->_inib->cEventflag[subscript], (waitPattern), (waitFlagMode), (p_flagPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_waitPolling( p_that, subscript, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->waitPolling__T( \
	   (p_that)->_inib->cEventflag[subscript], (waitPattern), (waitFlagMode), (p_flagPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_waitTimeout( p_that, subscript, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->waitTimeout__T( \
	   (p_that)->_inib->cEventflag[subscript], (waitPattern), (waitFlagMode), (p_flagPattern), (timeout) )
#define nMruby_tRiteVMBluetooth_cEventflag_initialize( p_that, subscript ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->initialize__T( \
	   (p_that)->_inib->cEventflag[subscript] )
#define nMruby_tRiteVMBluetooth_cEventflag_refer( p_that, subscript, pk_eventflagStatus ) \
	  (p_that)->_inib->cEventflag[subscript]->VMT->refer__T( \
	   (p_that)->_inib->cEventflag[subscript], (pk_eventflagStatus) )
#define nMruby_tRiteVMBluetooth_cSemaphore_signal( p_that ) \
	  tSemaphore_eSemaphore_signal( \
	   &tSemaphore_INIB_tab[0] )
#define nMruby_tRiteVMBluetooth_cSemaphore_wait( p_that ) \
	  tSemaphore_eSemaphore_wait( \
	   &tSemaphore_INIB_tab[0] )
#define nMruby_tRiteVMBluetooth_cSemaphore_waitPolling( p_that ) \
	  tSemaphore_eSemaphore_waitPolling( \
	   &tSemaphore_INIB_tab[0] )
#define nMruby_tRiteVMBluetooth_cSemaphore_waitTimeout( p_that, timeout ) \
	  tSemaphore_eSemaphore_waitTimeout( \
	   &tSemaphore_INIB_tab[0], (timeout) )
#define nMruby_tRiteVMBluetooth_cSemaphore_initialize( p_that ) \
	  tSemaphore_eSemaphore_initialize( \
	   &tSemaphore_INIB_tab[0] )
#define nMruby_tRiteVMBluetooth_cSemaphore_refer( p_that, pk_semaphoreStatus ) \
	  tSemaphore_eSemaphore_refer( \
	   &tSemaphore_INIB_tab[0], (pk_semaphoreStatus) )
#define nMruby_tRiteVMBluetooth_cInit_initializeBridge( p_that, mrb ) \
	  nMruby_tTECSInitializer_eInitialize_initializeBridge( \
	   &nMruby_tTECSInitializer_CB_tab[0], (mrb) )
#define nMruby_tRiteVMBluetooth_cMalloc_initializeMemoryPool( p_that ) \
	  tTLSFMalloc_eMalloc_initializeMemoryPool( \
	   &tTLSFMalloc_INIB_tab[0] )
#define nMruby_tRiteVMBluetooth_cMalloc_calloc( p_that, nelem, elem_size ) \
	  tTLSFMalloc_eMalloc_calloc( \
	   &tTLSFMalloc_INIB_tab[0], (nelem), (elem_size) )
#define nMruby_tRiteVMBluetooth_cMalloc_malloc( p_that, size ) \
	  tTLSFMalloc_eMalloc_malloc( \
	   &tTLSFMalloc_INIB_tab[0], (size) )
#define nMruby_tRiteVMBluetooth_cMalloc_realloc( p_that, ptr, new_size ) \
	  tTLSFMalloc_eMalloc_realloc( \
	   &tTLSFMalloc_INIB_tab[0], (ptr), (new_size) )
#define nMruby_tRiteVMBluetooth_cMalloc_free( p_that, ptr ) \
	  tTLSFMalloc_eMalloc_free( \
	   &tTLSFMalloc_INIB_tab[0], (ptr) )
#define nMruby_tRiteVMBluetooth_cZmodemToppers_zmodem_recv_file( p_that, portid, buf, size, filesz ) \
	  tZmodemToppers_eZmodemToppers_zmodem_recv_file( \
	   (tZmodemToppers_IDX)0, (portid), (buf), (size), (filesz) )

#else  /* TECSFLOW */
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_sleep( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.sleep__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_sleepTimeout( p_that, timeout ) \
	  (p_that)->_require_call_port_tKernel_eKernel.sleepTimeout__T( \
 (timeout) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_delay( p_that, delayTime ) \
	  (p_that)->_require_call_port_tKernel_eKernel.delay__T( \
 (delayTime) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_exitTask( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.exitTask__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getTaskId( p_that, p_taskId ) \
	  (p_that)->_require_call_port_tKernel_eKernel.getTaskId__T( \
 (p_taskId) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_rotateReadyQueue( p_that, taskPriority ) \
	  (p_that)->_require_call_port_tKernel_eKernel.rotateReadyQueue__T( \
 (taskPriority) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getTime( p_that, p_systemTime ) \
	  (p_that)->_require_call_port_tKernel_eKernel.getTime__T( \
 (p_systemTime) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getMicroTime( p_that, p_systemMicroTime ) \
	  (p_that)->_require_call_port_tKernel_eKernel.getMicroTime__T( \
 (p_systemMicroTime) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_lockCpu( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.lockCpu__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_unlockCpu( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.unlockCpu__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_disableDispatch( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.disableDispatch__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_enableDispatch( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.enableDispatch__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_disableTaskException( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.disableTaskException__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_enableTaskException( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.enableTaskException__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_changeInterruptPriorityMask( p_that, interruptPriority ) \
	  (p_that)->_require_call_port_tKernel_eKernel.changeInterruptPriorityMask__T( \
 (interruptPriority) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getInterruptPriorityMask( p_that, p_interruptPriority ) \
	  (p_that)->_require_call_port_tKernel_eKernel.getInterruptPriorityMask__T( \
 (p_interruptPriority) )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_exitKernel( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.exitKernel__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseContext( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.senseContext__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseLock( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.senseLock__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseDispatch( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.senseDispatch__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseDispatchPendingState( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.senseDispatchPendingState__T( \
 )
#define nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseKernel( p_that ) \
	  (p_that)->_require_call_port_tKernel_eKernel.senseKernel__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_activate( p_that ) \
	  (p_that)->cMrubyTask.activate__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_cancelActivate( p_that ) \
	  (p_that)->cMrubyTask.cancelActivate__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_terminate( p_that ) \
	  (p_that)->cMrubyTask.terminate__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_changePriority( p_that, priority ) \
	  (p_that)->cMrubyTask.changePriority__T( \
 (priority) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_getPriority( p_that, p_priority ) \
	  (p_that)->cMrubyTask.getPriority__T( \
 (p_priority) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_refer( p_that, pk_taskStatus ) \
	  (p_that)->cMrubyTask.refer__T( \
 (pk_taskStatus) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_wakeup( p_that ) \
	  (p_that)->cMrubyTask.wakeup__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_cancelWakeup( p_that ) \
	  (p_that)->cMrubyTask.cancelWakeup__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_releaseWait( p_that ) \
	  (p_that)->cMrubyTask.releaseWait__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_suspend( p_that ) \
	  (p_that)->cMrubyTask.suspend__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_resume( p_that ) \
	  (p_that)->cMrubyTask.resume__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_raiseException( p_that, pattern ) \
	  (p_that)->cMrubyTask.raiseException__T( \
 (pattern) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_referException( p_that, pk_rtex ) \
	  (p_that)->cMrubyTask.referException__T( \
 (pk_rtex) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_startOverRunHandler( p_that, ovrtim ) \
	  (p_that)->cMrubyTask.startOverRunHandler__T( \
 (ovrtim) )
#define nMruby_tRiteVMBluetooth_cMrubyTask_stopOverRunHandler( p_that ) \
	  (p_that)->cMrubyTask.stopOverRunHandler__T( \
 )
#define nMruby_tRiteVMBluetooth_cMrubyTask_referOverRunHandler( p_that, pk_rovr ) \
	  (p_that)->cMrubyTask.referOverRunHandler__T( \
 (pk_rovr) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_activate( p_that ) \
	  (p_that)->cZmodemTask.activate__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_cancelActivate( p_that ) \
	  (p_that)->cZmodemTask.cancelActivate__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_terminate( p_that ) \
	  (p_that)->cZmodemTask.terminate__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_changePriority( p_that, priority ) \
	  (p_that)->cZmodemTask.changePriority__T( \
 (priority) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_getPriority( p_that, p_priority ) \
	  (p_that)->cZmodemTask.getPriority__T( \
 (p_priority) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_refer( p_that, pk_taskStatus ) \
	  (p_that)->cZmodemTask.refer__T( \
 (pk_taskStatus) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_wakeup( p_that ) \
	  (p_that)->cZmodemTask.wakeup__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_cancelWakeup( p_that ) \
	  (p_that)->cZmodemTask.cancelWakeup__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_releaseWait( p_that ) \
	  (p_that)->cZmodemTask.releaseWait__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_suspend( p_that ) \
	  (p_that)->cZmodemTask.suspend__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_resume( p_that ) \
	  (p_that)->cZmodemTask.resume__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_raiseException( p_that, pattern ) \
	  (p_that)->cZmodemTask.raiseException__T( \
 (pattern) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_referException( p_that, pk_rtex ) \
	  (p_that)->cZmodemTask.referException__T( \
 (pk_rtex) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_startOverRunHandler( p_that, ovrtim ) \
	  (p_that)->cZmodemTask.startOverRunHandler__T( \
 (ovrtim) )
#define nMruby_tRiteVMBluetooth_cZmodemTask_stopOverRunHandler( p_that ) \
	  (p_that)->cZmodemTask.stopOverRunHandler__T( \
 )
#define nMruby_tRiteVMBluetooth_cZmodemTask_referOverRunHandler( p_that, pk_rovr ) \
	  (p_that)->cZmodemTask.referOverRunHandler__T( \
 (pk_rovr) )
#define nMruby_tRiteVMBluetooth_cReset_reset( p_that ) \
	  (p_that)->cReset.reset__T( \
 )
#define nMruby_tRiteVMBluetooth_cCyclic_start( p_that ) \
	  (p_that)->cCyclic.start__T( \
 )
#define nMruby_tRiteVMBluetooth_cCyclic_stop( p_that ) \
	  (p_that)->cCyclic.stop__T( \
 )
#define nMruby_tRiteVMBluetooth_cCyclic_refer( p_that, pk_cyclicHandlerStatus ) \
	  (p_that)->cCyclic.refer__T( \
 (pk_cyclicHandlerStatus) )
#define nMruby_tRiteVMBluetooth_cEventflag_set( p_that, subscript, setPattern ) \
	  (p_that)->cEventflag[subscript].set__T( \
 (setPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_clear( p_that, subscript, clearPattern ) \
	  (p_that)->cEventflag[subscript].clear__T( \
 (clearPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_wait( p_that, subscript, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->cEventflag[subscript].wait__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_waitPolling( p_that, subscript, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->cEventflag[subscript].waitPolling__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern) )
#define nMruby_tRiteVMBluetooth_cEventflag_waitTimeout( p_that, subscript, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
	  (p_that)->cEventflag[subscript].waitTimeout__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern), (timeout) )
#define nMruby_tRiteVMBluetooth_cEventflag_initialize( p_that, subscript ) \
	  (p_that)->cEventflag[subscript].initialize__T( \
 )
#define nMruby_tRiteVMBluetooth_cEventflag_refer( p_that, subscript, pk_eventflagStatus ) \
	  (p_that)->cEventflag[subscript].refer__T( \
 (pk_eventflagStatus) )
#define nMruby_tRiteVMBluetooth_cSemaphore_signal( p_that ) \
	  (p_that)->cSemaphore.signal__T( \
 )
#define nMruby_tRiteVMBluetooth_cSemaphore_wait( p_that ) \
	  (p_that)->cSemaphore.wait__T( \
 )
#define nMruby_tRiteVMBluetooth_cSemaphore_waitPolling( p_that ) \
	  (p_that)->cSemaphore.waitPolling__T( \
 )
#define nMruby_tRiteVMBluetooth_cSemaphore_waitTimeout( p_that, timeout ) \
	  (p_that)->cSemaphore.waitTimeout__T( \
 (timeout) )
#define nMruby_tRiteVMBluetooth_cSemaphore_initialize( p_that ) \
	  (p_that)->cSemaphore.initialize__T( \
 )
#define nMruby_tRiteVMBluetooth_cSemaphore_refer( p_that, pk_semaphoreStatus ) \
	  (p_that)->cSemaphore.refer__T( \
 (pk_semaphoreStatus) )
#define nMruby_tRiteVMBluetooth_cInit_initializeBridge( p_that, mrb ) \
	  (p_that)->cInit.initializeBridge__T( \
 (mrb) )
#define nMruby_tRiteVMBluetooth_cMalloc_initializeMemoryPool( p_that ) \
	  (p_that)->cMalloc.initializeMemoryPool__T( \
 )
#define nMruby_tRiteVMBluetooth_cMalloc_calloc( p_that, nelem, elem_size ) \
	  (p_that)->cMalloc.calloc__T( \
 (nelem), (elem_size) )
#define nMruby_tRiteVMBluetooth_cMalloc_malloc( p_that, size ) \
	  (p_that)->cMalloc.malloc__T( \
 (size) )
#define nMruby_tRiteVMBluetooth_cMalloc_realloc( p_that, ptr, new_size ) \
	  (p_that)->cMalloc.realloc__T( \
 (ptr), (new_size) )
#define nMruby_tRiteVMBluetooth_cMalloc_free( p_that, ptr ) \
	  (p_that)->cMalloc.free__T( \
 (ptr) )
#define nMruby_tRiteVMBluetooth_cZmodemToppers_zmodem_recv_file( p_that, portid, buf, size, filesz ) \
	  (p_that)->cZmodemToppers.zmodem_recv_file__T( \
 (portid), (buf), (size), (filesz) )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eMrubyBody */
void           nMruby_tRiteVMBluetooth_eMrubyBody_main_skel( const struct tag_sTaskBody_VDES *epd);
/* eRiteVM */
void           nMruby_tRiteVMBluetooth_eRiteVM_reset_skel( const struct tag_sRiteVM_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  nMruby_tRiteVMBluetooth_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  nMruby_tRiteVMBluetooth_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	nMruby_tRiteVMBluetooth_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	nMruby_tRiteVMBluetooth_IDX

#define tRiteVMBluetooth_IDX  nMruby_tRiteVMBluetooth_IDX

/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_irepLib         nMruby_tRiteVMBluetooth_ATTR_irepLib( p_cellcb )
#define ATTR_irepAppSize     nMruby_tRiteVMBluetooth_ATTR_irepAppSize( p_cellcb )
#define ATTR_setptn          nMruby_tRiteVMBluetooth_ATTR_setptn( p_cellcb )


/* var アクセスマクロ(短縮形) #_VAMA_# */
#define VAR_mrb              nMruby_tRiteVMBluetooth_VAR_mrb( p_cellcb )
#define VAR_context          nMruby_tRiteVMBluetooth_VAR_context( p_cellcb )
#define VAR_irepApp          nMruby_tRiteVMBluetooth_VAR_irepApp( p_cellcb )

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define sleep( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_sleep( p_cellcb ))
#define sleepTimeout( timeout ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_sleepTimeout( p_cellcb, timeout ))
#define delay( delayTime ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_delay( p_cellcb, delayTime ))
#define exitTask( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_exitTask( p_cellcb ))
#define getTaskId( p_taskId ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getTaskId( p_cellcb, p_taskId ))
#define rotateReadyQueue( taskPriority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_rotateReadyQueue( p_cellcb, taskPriority ))
#define getTime( p_systemTime ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getTime( p_cellcb, p_systemTime ))
#define getMicroTime( p_systemMicroTime ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getMicroTime( p_cellcb, p_systemMicroTime ))
#define lockCpu( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_lockCpu( p_cellcb ))
#define unlockCpu( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_unlockCpu( p_cellcb ))
#define disableDispatch( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_disableDispatch( p_cellcb ))
#define enableDispatch( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_enableDispatch( p_cellcb ))
#define disableTaskException( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_disableTaskException( p_cellcb ))
#define enableTaskException( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_enableTaskException( p_cellcb ))
#define changeInterruptPriorityMask( interruptPriority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_changeInterruptPriorityMask( p_cellcb, interruptPriority ))
#define getInterruptPriorityMask( p_interruptPriority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_getInterruptPriorityMask( p_cellcb, p_interruptPriority ))
#define exitKernel( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_exitKernel( p_cellcb ))
#define senseContext( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseContext( p_cellcb ))
#define senseLock( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseLock( p_cellcb ))
#define senseDispatch( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseDispatch( p_cellcb ))
#define senseDispatchPendingState( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseDispatchPendingState( p_cellcb ))
#define senseKernel( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth__require_call_port_tKernel_eKernel_senseKernel( p_cellcb ))
#define cMrubyTask_activate( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_activate( p_cellcb ))
#define cMrubyTask_cancelActivate( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_cancelActivate( p_cellcb ))
#define cMrubyTask_terminate( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_terminate( p_cellcb ))
#define cMrubyTask_changePriority( priority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_changePriority( p_cellcb, priority ))
#define cMrubyTask_getPriority( p_priority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_getPriority( p_cellcb, p_priority ))
#define cMrubyTask_refer( pk_taskStatus ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_refer( p_cellcb, pk_taskStatus ))
#define cMrubyTask_wakeup( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_wakeup( p_cellcb ))
#define cMrubyTask_cancelWakeup( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_cancelWakeup( p_cellcb ))
#define cMrubyTask_releaseWait( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_releaseWait( p_cellcb ))
#define cMrubyTask_suspend( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_suspend( p_cellcb ))
#define cMrubyTask_resume( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_resume( p_cellcb ))
#define cMrubyTask_raiseException( pattern ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_raiseException( p_cellcb, pattern ))
#define cMrubyTask_referException( pk_rtex ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_referException( p_cellcb, pk_rtex ))
#define cMrubyTask_startOverRunHandler( ovrtim ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_startOverRunHandler( p_cellcb, ovrtim ))
#define cMrubyTask_stopOverRunHandler( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_stopOverRunHandler( p_cellcb ))
#define cMrubyTask_referOverRunHandler( pk_rovr ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMrubyTask_referOverRunHandler( p_cellcb, pk_rovr ))
#define cZmodemTask_activate( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_activate( p_cellcb ))
#define cZmodemTask_cancelActivate( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_cancelActivate( p_cellcb ))
#define cZmodemTask_terminate( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_terminate( p_cellcb ))
#define cZmodemTask_changePriority( priority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_changePriority( p_cellcb, priority ))
#define cZmodemTask_getPriority( p_priority ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_getPriority( p_cellcb, p_priority ))
#define cZmodemTask_refer( pk_taskStatus ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_refer( p_cellcb, pk_taskStatus ))
#define cZmodemTask_wakeup( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_wakeup( p_cellcb ))
#define cZmodemTask_cancelWakeup( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_cancelWakeup( p_cellcb ))
#define cZmodemTask_releaseWait( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_releaseWait( p_cellcb ))
#define cZmodemTask_suspend( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_suspend( p_cellcb ))
#define cZmodemTask_resume( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_resume( p_cellcb ))
#define cZmodemTask_raiseException( pattern ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_raiseException( p_cellcb, pattern ))
#define cZmodemTask_referException( pk_rtex ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_referException( p_cellcb, pk_rtex ))
#define cZmodemTask_startOverRunHandler( ovrtim ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_startOverRunHandler( p_cellcb, ovrtim ))
#define cZmodemTask_stopOverRunHandler( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_stopOverRunHandler( p_cellcb ))
#define cZmodemTask_referOverRunHandler( pk_rovr ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemTask_referOverRunHandler( p_cellcb, pk_rovr ))
#define cReset_reset( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cReset_reset( p_cellcb ))
#define cCyclic_start( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cCyclic_start( p_cellcb ))
#define cCyclic_stop( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cCyclic_stop( p_cellcb ))
#define cCyclic_refer( pk_cyclicHandlerStatus ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cCyclic_refer( p_cellcb, pk_cyclicHandlerStatus ))
#define cEventflag_set( subscript, setPattern ) \
          nMruby_tRiteVMBluetooth_cEventflag_set( p_cellcb, subscript, setPattern )
#define cEventflag_clear( subscript, clearPattern ) \
          nMruby_tRiteVMBluetooth_cEventflag_clear( p_cellcb, subscript, clearPattern )
#define cEventflag_wait( subscript, waitPattern, waitFlagMode, p_flagPattern ) \
          nMruby_tRiteVMBluetooth_cEventflag_wait( p_cellcb, subscript, waitPattern, waitFlagMode, p_flagPattern )
#define cEventflag_waitPolling( subscript, waitPattern, waitFlagMode, p_flagPattern ) \
          nMruby_tRiteVMBluetooth_cEventflag_waitPolling( p_cellcb, subscript, waitPattern, waitFlagMode, p_flagPattern )
#define cEventflag_waitTimeout( subscript, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
          nMruby_tRiteVMBluetooth_cEventflag_waitTimeout( p_cellcb, subscript, waitPattern, waitFlagMode, p_flagPattern, timeout )
#define cEventflag_initialize( subscript ) \
          nMruby_tRiteVMBluetooth_cEventflag_initialize( p_cellcb, subscript )
#define cEventflag_refer( subscript, pk_eventflagStatus ) \
          nMruby_tRiteVMBluetooth_cEventflag_refer( p_cellcb, subscript, pk_eventflagStatus )
#define cSemaphore_signal( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cSemaphore_signal( p_cellcb ))
#define cSemaphore_wait( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cSemaphore_wait( p_cellcb ))
#define cSemaphore_waitPolling( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cSemaphore_waitPolling( p_cellcb ))
#define cSemaphore_waitTimeout( timeout ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cSemaphore_waitTimeout( p_cellcb, timeout ))
#define cSemaphore_initialize( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cSemaphore_initialize( p_cellcb ))
#define cSemaphore_refer( pk_semaphoreStatus ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cSemaphore_refer( p_cellcb, pk_semaphoreStatus ))
#define cInit_initializeBridge( mrb ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cInit_initializeBridge( p_cellcb, mrb ))
#define cMalloc_initializeMemoryPool( ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMalloc_initializeMemoryPool( p_cellcb ))
#define cMalloc_calloc( nelem, elem_size ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMalloc_calloc( p_cellcb, nelem, elem_size ))
#define cMalloc_malloc( size ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMalloc_malloc( p_cellcb, size ))
#define cMalloc_realloc( ptr, new_size ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMalloc_realloc( p_cellcb, ptr, new_size ))
#define cMalloc_free( ptr ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cMalloc_free( p_cellcb, ptr ))
#define cZmodemToppers_zmodem_recv_file( portid, buf, size, filesz ) \
          ((void)p_cellcb, nMruby_tRiteVMBluetooth_cZmodemToppers_zmodem_recv_file( p_cellcb, portid, buf, size, filesz ))



/* optional 呼び口をテストするマクロ（短縮形） #_TOCPA_# */
#define is_cCyclic_joined()\
		nMruby_tRiteVMBluetooth_is_cCyclic_joined(p_cellcb)
#define is_cEventflag_joined(subscript)\
		nMruby_tRiteVMBluetooth_is_cEventflag_joined(p_cellcb,subscript)
#define is_cSemaphore_joined()\
		nMruby_tRiteVMBluetooth_is_cSemaphore_joined(p_cellcb)
#define is_cInit_joined()\
		nMruby_tRiteVMBluetooth_is_cInit_joined(p_cellcb)

/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eMrubyBody_main  nMruby_tRiteVMBluetooth_eMrubyBody_main
#define eRiteVM_reset    nMruby_tRiteVMBluetooth_eRiteVM_reset

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nMruby_tRiteVMBluetooth_N_CELL; (i)++ ){ \
       (p_cb) = &nMruby_tRiteVMBluetooth_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	(p_that)->_inib = &nMruby_tRiteVMBluetooth_INIB_tab[(i)];

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* nMruby_tRiteVMBluetooth_TECSGENH */
