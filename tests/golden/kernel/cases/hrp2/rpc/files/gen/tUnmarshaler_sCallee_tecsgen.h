/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tUnmarshaler_sCallee_TECSGEN_H
#define tUnmarshaler_sCallee_TECSGEN_H

/*
 * celltype          :  tUnmarshaler_sCallee
 * global name       :  tUnmarshaler_sCallee
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
#include "sCallee_tecsgen.h"
#include "sEventflag_tecsgen.h"
#include "sSemaphore_tecsgen.h"
#include "sMessageBuffer_tecsgen.h"
#include "sTaskBody_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tUnmarshaler_sCallee_CB {
    int  dummy;
} tUnmarshaler_sCallee_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tUnmarshaler_sCallee_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         tUnmarshaler_sCallee_eUnmarshalAndCallFunction_main(tUnmarshaler_sCallee_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tUnmarshaler_sCallee_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tServer_tecsgen.h"
#include "tEventflag_tecsgen.h"
#include "tSemaphore_tecsgen.h"
#include "tMessageBuffer_tecsgen.h"
#ifdef  tUnmarshaler_sCallee_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tUnmarshaler_sCallee_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tUnmarshaler_sCallee_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tUnmarshaler_sCallee_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tUnmarshaler_sCallee_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tUnmarshaler_sCallee_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tUnmarshaler_sCallee_cServerCall_add( p_that, a, b ) \
	  tServer_eCallee_add( \
	   (tServer_IDX)0, (a), (b) )
#define tUnmarshaler_sCallee_cServerCall_scale( p_that, k, v ) \
	  tServer_eCallee_scale( \
	   (tServer_IDX)0, (k), (v) )
#define tUnmarshaler_sCallee_cServerCall_widen( p_that, v ) \
	  tServer_eCallee_widen( \
	   (tServer_IDX)0, (v) )
#define tUnmarshaler_sCallee_cServerCall_notify( p_that ) \
	  tServer_eCallee_notify( \
	   (tServer_IDX)0 )
#define tUnmarshaler_sCallee_cEventflag_set( p_that, setPattern ) \
	  tEventflag_eEventflag_set( \
	   &tEventflag_INIB_tab[0], (setPattern) )
#define tUnmarshaler_sCallee_cEventflag_clear( p_that, clearPattern ) \
	  tEventflag_eEventflag_clear( \
	   &tEventflag_INIB_tab[0], (clearPattern) )
#define tUnmarshaler_sCallee_cEventflag_wait( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  tEventflag_eEventflag_wait( \
	   &tEventflag_INIB_tab[0], (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tUnmarshaler_sCallee_cEventflag_waitPolling( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  tEventflag_eEventflag_waitPolling( \
	   &tEventflag_INIB_tab[0], (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tUnmarshaler_sCallee_cEventflag_waitTimeout( p_that, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
	  tEventflag_eEventflag_waitTimeout( \
	   &tEventflag_INIB_tab[0], (waitPattern), (waitFlagMode), (p_flagPattern), (timeout) )
#define tUnmarshaler_sCallee_cEventflag_initialize( p_that ) \
	  tEventflag_eEventflag_initialize( \
	   &tEventflag_INIB_tab[0] )
#define tUnmarshaler_sCallee_cEventflag_refer( p_that, pk_eventflagStatus ) \
	  tEventflag_eEventflag_refer( \
	   &tEventflag_INIB_tab[0], (pk_eventflagStatus) )
#define tUnmarshaler_sCallee_cSemaphore_signal( p_that ) \
	  tSemaphore_eSemaphore_signal( \
	   &tSemaphore_INIB_tab[0] )
#define tUnmarshaler_sCallee_cSemaphore_wait( p_that ) \
	  tSemaphore_eSemaphore_wait( \
	   &tSemaphore_INIB_tab[0] )
#define tUnmarshaler_sCallee_cSemaphore_waitPolling( p_that ) \
	  tSemaphore_eSemaphore_waitPolling( \
	   &tSemaphore_INIB_tab[0] )
#define tUnmarshaler_sCallee_cSemaphore_waitTimeout( p_that, timeout ) \
	  tSemaphore_eSemaphore_waitTimeout( \
	   &tSemaphore_INIB_tab[0], (timeout) )
#define tUnmarshaler_sCallee_cSemaphore_initialize( p_that ) \
	  tSemaphore_eSemaphore_initialize( \
	   &tSemaphore_INIB_tab[0] )
#define tUnmarshaler_sCallee_cSemaphore_refer( p_that, pk_semaphoreStatus ) \
	  tSemaphore_eSemaphore_refer( \
	   &tSemaphore_INIB_tab[0], (pk_semaphoreStatus) )
#define tUnmarshaler_sCallee_cMessageBuffer_send( p_that, message, size ) \
	  tMessageBuffer_eMessageBuffer_send( \
	   &tMessageBuffer_INIB_tab[0], (message), (size) )
#define tUnmarshaler_sCallee_cMessageBuffer_sendPolling( p_that, message, size ) \
	  tMessageBuffer_eMessageBuffer_sendPolling( \
	   &tMessageBuffer_INIB_tab[0], (message), (size) )
#define tUnmarshaler_sCallee_cMessageBuffer_sendTimeout( p_that, message, size, timeout ) \
	  tMessageBuffer_eMessageBuffer_sendTimeout( \
	   &tMessageBuffer_INIB_tab[0], (message), (size), (timeout) )
#define tUnmarshaler_sCallee_cMessageBuffer_receive( p_that, message ) \
	  tMessageBuffer_eMessageBuffer_receive( \
	   &tMessageBuffer_INIB_tab[0], (message) )
#define tUnmarshaler_sCallee_cMessageBuffer_receivePolling( p_that, message ) \
	  tMessageBuffer_eMessageBuffer_receivePolling( \
	   &tMessageBuffer_INIB_tab[0], (message) )
#define tUnmarshaler_sCallee_cMessageBuffer_receiveTimeout( p_that, message, timeout ) \
	  tMessageBuffer_eMessageBuffer_receiveTimeout( \
	   &tMessageBuffer_INIB_tab[0], (message), (timeout) )
#define tUnmarshaler_sCallee_cMessageBuffer_initialize( p_that ) \
	  tMessageBuffer_eMessageBuffer_initialize( \
	   &tMessageBuffer_INIB_tab[0] )
#define tUnmarshaler_sCallee_cMessageBuffer_refer( p_that, packet ) \
	  tMessageBuffer_eMessageBuffer_refer( \
	   &tMessageBuffer_INIB_tab[0], (packet) )

#else  /* TECSFLOW */
#define tUnmarshaler_sCallee_cServerCall_add( p_that, a, b ) \
	  (p_that)->cServerCall.add__T( \
 (a), (b) )
#define tUnmarshaler_sCallee_cServerCall_scale( p_that, k, v ) \
	  (p_that)->cServerCall.scale__T( \
 (k), (v) )
#define tUnmarshaler_sCallee_cServerCall_widen( p_that, v ) \
	  (p_that)->cServerCall.widen__T( \
 (v) )
#define tUnmarshaler_sCallee_cServerCall_notify( p_that ) \
	  (p_that)->cServerCall.notify__T( \
 )
#define tUnmarshaler_sCallee_cEventflag_set( p_that, setPattern ) \
	  (p_that)->cEventflag.set__T( \
 (setPattern) )
#define tUnmarshaler_sCallee_cEventflag_clear( p_that, clearPattern ) \
	  (p_that)->cEventflag.clear__T( \
 (clearPattern) )
#define tUnmarshaler_sCallee_cEventflag_wait( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->cEventflag.wait__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tUnmarshaler_sCallee_cEventflag_waitPolling( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->cEventflag.waitPolling__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tUnmarshaler_sCallee_cEventflag_waitTimeout( p_that, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
	  (p_that)->cEventflag.waitTimeout__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern), (timeout) )
#define tUnmarshaler_sCallee_cEventflag_initialize( p_that ) \
	  (p_that)->cEventflag.initialize__T( \
 )
#define tUnmarshaler_sCallee_cEventflag_refer( p_that, pk_eventflagStatus ) \
	  (p_that)->cEventflag.refer__T( \
 (pk_eventflagStatus) )
#define tUnmarshaler_sCallee_cSemaphore_signal( p_that ) \
	  (p_that)->cSemaphore.signal__T( \
 )
#define tUnmarshaler_sCallee_cSemaphore_wait( p_that ) \
	  (p_that)->cSemaphore.wait__T( \
 )
#define tUnmarshaler_sCallee_cSemaphore_waitPolling( p_that ) \
	  (p_that)->cSemaphore.waitPolling__T( \
 )
#define tUnmarshaler_sCallee_cSemaphore_waitTimeout( p_that, timeout ) \
	  (p_that)->cSemaphore.waitTimeout__T( \
 (timeout) )
#define tUnmarshaler_sCallee_cSemaphore_initialize( p_that ) \
	  (p_that)->cSemaphore.initialize__T( \
 )
#define tUnmarshaler_sCallee_cSemaphore_refer( p_that, pk_semaphoreStatus ) \
	  (p_that)->cSemaphore.refer__T( \
 (pk_semaphoreStatus) )
#define tUnmarshaler_sCallee_cMessageBuffer_send( p_that, message, size ) \
	  (p_that)->cMessageBuffer.send__T( \
 (message), (size) )
#define tUnmarshaler_sCallee_cMessageBuffer_sendPolling( p_that, message, size ) \
	  (p_that)->cMessageBuffer.sendPolling__T( \
 (message), (size) )
#define tUnmarshaler_sCallee_cMessageBuffer_sendTimeout( p_that, message, size, timeout ) \
	  (p_that)->cMessageBuffer.sendTimeout__T( \
 (message), (size), (timeout) )
#define tUnmarshaler_sCallee_cMessageBuffer_receive( p_that, message ) \
	  (p_that)->cMessageBuffer.receive__T( \
 (message) )
#define tUnmarshaler_sCallee_cMessageBuffer_receivePolling( p_that, message ) \
	  (p_that)->cMessageBuffer.receivePolling__T( \
 (message) )
#define tUnmarshaler_sCallee_cMessageBuffer_receiveTimeout( p_that, message, timeout ) \
	  (p_that)->cMessageBuffer.receiveTimeout__T( \
 (message), (timeout) )
#define tUnmarshaler_sCallee_cMessageBuffer_initialize( p_that ) \
	  (p_that)->cMessageBuffer.initialize__T( \
 )
#define tUnmarshaler_sCallee_cMessageBuffer_refer( p_that, packet ) \
	  (p_that)->cMessageBuffer.refer__T( \
 (packet) )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tUnmarshaler_sCallee_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tUnmarshaler_sCallee_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tUnmarshaler_sCallee_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tUnmarshaler_sCallee_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cServerCall_add( a, b ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cServerCall_add( p_cellcb, a, b ))
#define cServerCall_scale( k, v ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cServerCall_scale( p_cellcb, k, v ))
#define cServerCall_widen( v ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cServerCall_widen( p_cellcb, v ))
#define cServerCall_notify( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cServerCall_notify( p_cellcb ))
#define cEventflag_set( setPattern ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_set( p_cellcb, setPattern ))
#define cEventflag_clear( clearPattern ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_clear( p_cellcb, clearPattern ))
#define cEventflag_wait( waitPattern, waitFlagMode, p_flagPattern ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_wait( p_cellcb, waitPattern, waitFlagMode, p_flagPattern ))
#define cEventflag_waitPolling( waitPattern, waitFlagMode, p_flagPattern ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_waitPolling( p_cellcb, waitPattern, waitFlagMode, p_flagPattern ))
#define cEventflag_waitTimeout( waitPattern, waitFlagMode, p_flagPattern, timeout ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_waitTimeout( p_cellcb, waitPattern, waitFlagMode, p_flagPattern, timeout ))
#define cEventflag_initialize( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_initialize( p_cellcb ))
#define cEventflag_refer( pk_eventflagStatus ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cEventflag_refer( p_cellcb, pk_eventflagStatus ))
#define cSemaphore_signal( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cSemaphore_signal( p_cellcb ))
#define cSemaphore_wait( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cSemaphore_wait( p_cellcb ))
#define cSemaphore_waitPolling( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cSemaphore_waitPolling( p_cellcb ))
#define cSemaphore_waitTimeout( timeout ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cSemaphore_waitTimeout( p_cellcb, timeout ))
#define cSemaphore_initialize( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cSemaphore_initialize( p_cellcb ))
#define cSemaphore_refer( pk_semaphoreStatus ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cSemaphore_refer( p_cellcb, pk_semaphoreStatus ))
#define cMessageBuffer_send( message, size ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_send( p_cellcb, message, size ))
#define cMessageBuffer_sendPolling( message, size ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_sendPolling( p_cellcb, message, size ))
#define cMessageBuffer_sendTimeout( message, size, timeout ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_sendTimeout( p_cellcb, message, size, timeout ))
#define cMessageBuffer_receive( message ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_receive( p_cellcb, message ))
#define cMessageBuffer_receivePolling( message ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_receivePolling( p_cellcb, message ))
#define cMessageBuffer_receiveTimeout( message, timeout ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_receiveTimeout( p_cellcb, message, timeout ))
#define cMessageBuffer_initialize( ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_initialize( p_cellcb ))
#define cMessageBuffer_refer( packet ) \
          ((void)p_cellcb, tUnmarshaler_sCallee_cMessageBuffer_refer( p_cellcb, packet ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eUnmarshalAndCallFunction_main tUnmarshaler_sCallee_eUnmarshalAndCallFunction_main

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

#endif /* tUnmarshaler_sCallee_TECSGENH */
