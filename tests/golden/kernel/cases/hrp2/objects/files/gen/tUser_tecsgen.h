/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tUser_TECSGEN_H
#define tUser_TECSGEN_H

/*
 * celltype          :  tUser
 * global name       :  tUser
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  no
 * has_CB            :  no
 * has_INIB          :  no
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sSignalSemaphore_tecsgen.h"
#include "sSetEventflag_tecsgen.h"
#include "sSendDataqueue_tecsgen.h"
#include "sSendPriorityDataqueue_tecsgen.h"
#include "sGetFixedSizeMemoryPool_tecsgen.h"
#include "sCallee_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tUser_CB {
    int  dummy;
} tUser_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tUser_IDX;
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tUser_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tSemaphore_tecsgen.h"
#include "tEventflag_tecsgen.h"
#include "tDataqueue_tecsgen.h"
#include "tPriorityDataqueue_tecsgen.h"
#include "tFixedSizeMemoryPool_tecsgen.h"
#include "tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_tecsgen.h"
#ifdef  tUser_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tUser_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tUser_ID_BASE               (1)  /* ID のベース  #_NIDB_# */
#define tUser_N_CELL                (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tUser_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tUser_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tUser_cSignalSemaphore_signal( p_that ) \
	  tSemaphore_eSignalSemaphore_signal( \
	   &rUser_SemaphoreU_INIB )
#define tUser_cSetEventflag_set( p_that, setPattern ) \
	  tEventflag_eSetEventflag_set( \
	   &rUser_EventflagU_INIB, (setPattern) )
#define tUser_cSetEventflag_clear( p_that, clearPattern ) \
	  tEventflag_eSetEventflag_clear( \
	   &rUser_EventflagU_INIB, (clearPattern) )
#define tUser_cSendDataqueue_send( p_that, data ) \
	  tDataqueue_eSendDataqueue_send( \
	   &rUser_DataqueueU_INIB, (data) )
#define tUser_cSendDataqueue_sendPolling( p_that, data ) \
	  tDataqueue_eSendDataqueue_sendPolling( \
	   &rUser_DataqueueU_INIB, (data) )
#define tUser_cSendDataqueue_sendTimeout( p_that, data, timeout ) \
	  tDataqueue_eSendDataqueue_sendTimeout( \
	   &rUser_DataqueueU_INIB, (data), (timeout) )
#define tUser_cSendDataqueue_sendForce( p_that, data ) \
	  tDataqueue_eSendDataqueue_sendForce( \
	   &rUser_DataqueueU_INIB, (data) )
#define tUser_cSendPriorityDataqueue_send( p_that, data, dataPriority ) \
	  tPriorityDataqueue_eSendPriorityDataqueue_send( \
	   &rUser_PriorityDataqueueU_INIB, (data), (dataPriority) )
#define tUser_cSendPriorityDataqueue_sendPolling( p_that, data, dataPriority ) \
	  tPriorityDataqueue_eSendPriorityDataqueue_sendPolling( \
	   &rUser_PriorityDataqueueU_INIB, (data), (dataPriority) )
#define tUser_cSendPriorityDataqueue_sendTimeout( p_that, data, dataPriority, timeout ) \
	  tPriorityDataqueue_eSendPriorityDataqueue_sendTimeout( \
	   &rUser_PriorityDataqueueU_INIB, (data), (dataPriority), (timeout) )
#define tUser_cGetFixedSizeMemoryPool_get( p_that, p_block ) \
	  tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_get( \
	   &rUser_FixedSizeMemoryPoolU_INIB, (p_block) )
#define tUser_cGetFixedSizeMemoryPool_getPolling( p_that, p_block ) \
	  tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getPolling( \
	   &rUser_FixedSizeMemoryPoolU_INIB, (p_block) )
#define tUser_cGetFixedSizeMemoryPool_getTimeout( p_that, p_block, timeout ) \
	  tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getTimeout( \
	   &rUser_FixedSizeMemoryPoolU_INIB, (p_block), (timeout) )
#define tUser_cCallee_add( p_that, a, b, sum ) \
	  tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_eThroughEntry_add( \
	   (tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_IDX)0, (a), (b), (sum) )
#define tUser_cCallee_notify( p_that ) \
	  tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_eThroughEntry_notify( \
	   (tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_IDX)0 )

#else  /* TECSFLOW */
#define tUser_cSignalSemaphore_signal( p_that ) \
	  (p_that)->cSignalSemaphore.signal__T( \
 )
#define tUser_cSetEventflag_set( p_that, setPattern ) \
	  (p_that)->cSetEventflag.set__T( \
 (setPattern) )
#define tUser_cSetEventflag_clear( p_that, clearPattern ) \
	  (p_that)->cSetEventflag.clear__T( \
 (clearPattern) )
#define tUser_cSendDataqueue_send( p_that, data ) \
	  (p_that)->cSendDataqueue.send__T( \
 (data) )
#define tUser_cSendDataqueue_sendPolling( p_that, data ) \
	  (p_that)->cSendDataqueue.sendPolling__T( \
 (data) )
#define tUser_cSendDataqueue_sendTimeout( p_that, data, timeout ) \
	  (p_that)->cSendDataqueue.sendTimeout__T( \
 (data), (timeout) )
#define tUser_cSendDataqueue_sendForce( p_that, data ) \
	  (p_that)->cSendDataqueue.sendForce__T( \
 (data) )
#define tUser_cSendPriorityDataqueue_send( p_that, data, dataPriority ) \
	  (p_that)->cSendPriorityDataqueue.send__T( \
 (data), (dataPriority) )
#define tUser_cSendPriorityDataqueue_sendPolling( p_that, data, dataPriority ) \
	  (p_that)->cSendPriorityDataqueue.sendPolling__T( \
 (data), (dataPriority) )
#define tUser_cSendPriorityDataqueue_sendTimeout( p_that, data, dataPriority, timeout ) \
	  (p_that)->cSendPriorityDataqueue.sendTimeout__T( \
 (data), (dataPriority), (timeout) )
#define tUser_cGetFixedSizeMemoryPool_get( p_that, p_block ) \
	  (p_that)->cGetFixedSizeMemoryPool.get__T( \
 (p_block) )
#define tUser_cGetFixedSizeMemoryPool_getPolling( p_that, p_block ) \
	  (p_that)->cGetFixedSizeMemoryPool.getPolling__T( \
 (p_block) )
#define tUser_cGetFixedSizeMemoryPool_getTimeout( p_that, p_block, timeout ) \
	  (p_that)->cGetFixedSizeMemoryPool.getTimeout__T( \
 (p_block), (timeout) )
#define tUser_cCallee_add( p_that, a, b, sum ) \
	  (p_that)->cCallee.add__T( \
 (a), (b), (sum) )
#define tUser_cCallee_notify( p_that ) \
	  (p_that)->cCallee.notify__T( \
 )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tUser_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tUser_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tUser_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tUser_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cSignalSemaphore_signal( ) \
          ((void)p_cellcb, tUser_cSignalSemaphore_signal( p_cellcb ))
#define cSetEventflag_set( setPattern ) \
          ((void)p_cellcb, tUser_cSetEventflag_set( p_cellcb, setPattern ))
#define cSetEventflag_clear( clearPattern ) \
          ((void)p_cellcb, tUser_cSetEventflag_clear( p_cellcb, clearPattern ))
#define cSendDataqueue_send( data ) \
          ((void)p_cellcb, tUser_cSendDataqueue_send( p_cellcb, data ))
#define cSendDataqueue_sendPolling( data ) \
          ((void)p_cellcb, tUser_cSendDataqueue_sendPolling( p_cellcb, data ))
#define cSendDataqueue_sendTimeout( data, timeout ) \
          ((void)p_cellcb, tUser_cSendDataqueue_sendTimeout( p_cellcb, data, timeout ))
#define cSendDataqueue_sendForce( data ) \
          ((void)p_cellcb, tUser_cSendDataqueue_sendForce( p_cellcb, data ))
#define cSendPriorityDataqueue_send( data, dataPriority ) \
          ((void)p_cellcb, tUser_cSendPriorityDataqueue_send( p_cellcb, data, dataPriority ))
#define cSendPriorityDataqueue_sendPolling( data, dataPriority ) \
          ((void)p_cellcb, tUser_cSendPriorityDataqueue_sendPolling( p_cellcb, data, dataPriority ))
#define cSendPriorityDataqueue_sendTimeout( data, dataPriority, timeout ) \
          ((void)p_cellcb, tUser_cSendPriorityDataqueue_sendTimeout( p_cellcb, data, dataPriority, timeout ))
#define cGetFixedSizeMemoryPool_get( p_block ) \
          ((void)p_cellcb, tUser_cGetFixedSizeMemoryPool_get( p_cellcb, p_block ))
#define cGetFixedSizeMemoryPool_getPolling( p_block ) \
          ((void)p_cellcb, tUser_cGetFixedSizeMemoryPool_getPolling( p_cellcb, p_block ))
#define cGetFixedSizeMemoryPool_getTimeout( p_block, timeout ) \
          ((void)p_cellcb, tUser_cGetFixedSizeMemoryPool_getTimeout( p_cellcb, p_block, timeout ))
#define cCallee_add( a, b, sum ) \
          ((void)p_cellcb, tUser_cCallee_add( p_cellcb, a, b, sum ))
#define cCallee_notify( ) \
          ((void)p_cellcb, tUser_cCallee_notify( p_cellcb ))



/* イテレータコード (FOREACH_CELL)の生成(CB,INIB は存在しない) #_NFEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for((i)=0;(i)<0;(i)++){

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tUser_TECSGENH */
