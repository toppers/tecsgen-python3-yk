/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tMarshaler_sCallee_TECSGEN_H
#define tMarshaler_sCallee_TECSGEN_H

/*
 * celltype          :  tMarshaler_sCallee
 * global name       :  tMarshaler_sCallee
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

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tMarshaler_sCallee_CB {
    int  dummy;
} tMarshaler_sCallee_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tMarshaler_sCallee_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sCallee */
ER           tMarshaler_sCallee_eClientEntry_add(tMarshaler_sCallee_IDX idx, int32_t a, int32_t b);
int16_t      tMarshaler_sCallee_eClientEntry_scale(tMarshaler_sCallee_IDX idx, int8_t k, uint16_t v);
int64_t      tMarshaler_sCallee_eClientEntry_widen(tMarshaler_sCallee_IDX idx, uint32_t v);
void         tMarshaler_sCallee_eClientEntry_notify(tMarshaler_sCallee_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tMarshaler_sCallee_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tEventflag_tecsgen.h"
#include "tSemaphore_tecsgen.h"
#include "tMessageBuffer_tecsgen.h"
#ifdef  tMarshaler_sCallee_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tMarshaler_sCallee_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tMarshaler_sCallee_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tMarshaler_sCallee_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tMarshaler_sCallee_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tMarshaler_sCallee_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tMarshaler_sCallee_cEventflag_set( p_that, setPattern ) \
	  tEventflag_eEventflag_set( \
	   &tEventflag_INIB_tab[0], (setPattern) )
#define tMarshaler_sCallee_cEventflag_clear( p_that, clearPattern ) \
	  tEventflag_eEventflag_clear( \
	   &tEventflag_INIB_tab[0], (clearPattern) )
#define tMarshaler_sCallee_cEventflag_wait( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  tEventflag_eEventflag_wait( \
	   &tEventflag_INIB_tab[0], (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tMarshaler_sCallee_cEventflag_waitPolling( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  tEventflag_eEventflag_waitPolling( \
	   &tEventflag_INIB_tab[0], (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tMarshaler_sCallee_cEventflag_waitTimeout( p_that, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
	  tEventflag_eEventflag_waitTimeout( \
	   &tEventflag_INIB_tab[0], (waitPattern), (waitFlagMode), (p_flagPattern), (timeout) )
#define tMarshaler_sCallee_cEventflag_initialize( p_that ) \
	  tEventflag_eEventflag_initialize( \
	   &tEventflag_INIB_tab[0] )
#define tMarshaler_sCallee_cEventflag_refer( p_that, pk_eventflagStatus ) \
	  tEventflag_eEventflag_refer( \
	   &tEventflag_INIB_tab[0], (pk_eventflagStatus) )
#define tMarshaler_sCallee_cSemaphore_signal( p_that ) \
	  tSemaphore_eSemaphore_signal( \
	   &tSemaphore_INIB_tab[0] )
#define tMarshaler_sCallee_cSemaphore_wait( p_that ) \
	  tSemaphore_eSemaphore_wait( \
	   &tSemaphore_INIB_tab[0] )
#define tMarshaler_sCallee_cSemaphore_waitPolling( p_that ) \
	  tSemaphore_eSemaphore_waitPolling( \
	   &tSemaphore_INIB_tab[0] )
#define tMarshaler_sCallee_cSemaphore_waitTimeout( p_that, timeout ) \
	  tSemaphore_eSemaphore_waitTimeout( \
	   &tSemaphore_INIB_tab[0], (timeout) )
#define tMarshaler_sCallee_cSemaphore_initialize( p_that ) \
	  tSemaphore_eSemaphore_initialize( \
	   &tSemaphore_INIB_tab[0] )
#define tMarshaler_sCallee_cSemaphore_refer( p_that, pk_semaphoreStatus ) \
	  tSemaphore_eSemaphore_refer( \
	   &tSemaphore_INIB_tab[0], (pk_semaphoreStatus) )
#define tMarshaler_sCallee_cMessageBuffer_send( p_that, message, size ) \
	  tMessageBuffer_eMessageBuffer_send( \
	   &tMessageBuffer_INIB_tab[0], (message), (size) )
#define tMarshaler_sCallee_cMessageBuffer_sendPolling( p_that, message, size ) \
	  tMessageBuffer_eMessageBuffer_sendPolling( \
	   &tMessageBuffer_INIB_tab[0], (message), (size) )
#define tMarshaler_sCallee_cMessageBuffer_sendTimeout( p_that, message, size, timeout ) \
	  tMessageBuffer_eMessageBuffer_sendTimeout( \
	   &tMessageBuffer_INIB_tab[0], (message), (size), (timeout) )
#define tMarshaler_sCallee_cMessageBuffer_receive( p_that, message ) \
	  tMessageBuffer_eMessageBuffer_receive( \
	   &tMessageBuffer_INIB_tab[0], (message) )
#define tMarshaler_sCallee_cMessageBuffer_receivePolling( p_that, message ) \
	  tMessageBuffer_eMessageBuffer_receivePolling( \
	   &tMessageBuffer_INIB_tab[0], (message) )
#define tMarshaler_sCallee_cMessageBuffer_receiveTimeout( p_that, message, timeout ) \
	  tMessageBuffer_eMessageBuffer_receiveTimeout( \
	   &tMessageBuffer_INIB_tab[0], (message), (timeout) )
#define tMarshaler_sCallee_cMessageBuffer_initialize( p_that ) \
	  tMessageBuffer_eMessageBuffer_initialize( \
	   &tMessageBuffer_INIB_tab[0] )
#define tMarshaler_sCallee_cMessageBuffer_refer( p_that, packet ) \
	  tMessageBuffer_eMessageBuffer_refer( \
	   &tMessageBuffer_INIB_tab[0], (packet) )

#else  /* TECSFLOW */
#define tMarshaler_sCallee_cEventflag_set( p_that, setPattern ) \
	  (p_that)->cEventflag.set__T( \
 (setPattern) )
#define tMarshaler_sCallee_cEventflag_clear( p_that, clearPattern ) \
	  (p_that)->cEventflag.clear__T( \
 (clearPattern) )
#define tMarshaler_sCallee_cEventflag_wait( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->cEventflag.wait__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tMarshaler_sCallee_cEventflag_waitPolling( p_that, waitPattern, waitFlagMode, p_flagPattern ) \
	  (p_that)->cEventflag.waitPolling__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern) )
#define tMarshaler_sCallee_cEventflag_waitTimeout( p_that, waitPattern, waitFlagMode, p_flagPattern, timeout ) \
	  (p_that)->cEventflag.waitTimeout__T( \
 (waitPattern), (waitFlagMode), (p_flagPattern), (timeout) )
#define tMarshaler_sCallee_cEventflag_initialize( p_that ) \
	  (p_that)->cEventflag.initialize__T( \
 )
#define tMarshaler_sCallee_cEventflag_refer( p_that, pk_eventflagStatus ) \
	  (p_that)->cEventflag.refer__T( \
 (pk_eventflagStatus) )
#define tMarshaler_sCallee_cSemaphore_signal( p_that ) \
	  (p_that)->cSemaphore.signal__T( \
 )
#define tMarshaler_sCallee_cSemaphore_wait( p_that ) \
	  (p_that)->cSemaphore.wait__T( \
 )
#define tMarshaler_sCallee_cSemaphore_waitPolling( p_that ) \
	  (p_that)->cSemaphore.waitPolling__T( \
 )
#define tMarshaler_sCallee_cSemaphore_waitTimeout( p_that, timeout ) \
	  (p_that)->cSemaphore.waitTimeout__T( \
 (timeout) )
#define tMarshaler_sCallee_cSemaphore_initialize( p_that ) \
	  (p_that)->cSemaphore.initialize__T( \
 )
#define tMarshaler_sCallee_cSemaphore_refer( p_that, pk_semaphoreStatus ) \
	  (p_that)->cSemaphore.refer__T( \
 (pk_semaphoreStatus) )
#define tMarshaler_sCallee_cMessageBuffer_send( p_that, message, size ) \
	  (p_that)->cMessageBuffer.send__T( \
 (message), (size) )
#define tMarshaler_sCallee_cMessageBuffer_sendPolling( p_that, message, size ) \
	  (p_that)->cMessageBuffer.sendPolling__T( \
 (message), (size) )
#define tMarshaler_sCallee_cMessageBuffer_sendTimeout( p_that, message, size, timeout ) \
	  (p_that)->cMessageBuffer.sendTimeout__T( \
 (message), (size), (timeout) )
#define tMarshaler_sCallee_cMessageBuffer_receive( p_that, message ) \
	  (p_that)->cMessageBuffer.receive__T( \
 (message) )
#define tMarshaler_sCallee_cMessageBuffer_receivePolling( p_that, message ) \
	  (p_that)->cMessageBuffer.receivePolling__T( \
 (message) )
#define tMarshaler_sCallee_cMessageBuffer_receiveTimeout( p_that, message, timeout ) \
	  (p_that)->cMessageBuffer.receiveTimeout__T( \
 (message), (timeout) )
#define tMarshaler_sCallee_cMessageBuffer_initialize( p_that ) \
	  (p_that)->cMessageBuffer.initialize__T( \
 )
#define tMarshaler_sCallee_cMessageBuffer_refer( p_that, packet ) \
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
#define VALID_IDX(IDX)  tMarshaler_sCallee_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tMarshaler_sCallee_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tMarshaler_sCallee_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tMarshaler_sCallee_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cEventflag_set( setPattern ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_set( p_cellcb, setPattern ))
#define cEventflag_clear( clearPattern ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_clear( p_cellcb, clearPattern ))
#define cEventflag_wait( waitPattern, waitFlagMode, p_flagPattern ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_wait( p_cellcb, waitPattern, waitFlagMode, p_flagPattern ))
#define cEventflag_waitPolling( waitPattern, waitFlagMode, p_flagPattern ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_waitPolling( p_cellcb, waitPattern, waitFlagMode, p_flagPattern ))
#define cEventflag_waitTimeout( waitPattern, waitFlagMode, p_flagPattern, timeout ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_waitTimeout( p_cellcb, waitPattern, waitFlagMode, p_flagPattern, timeout ))
#define cEventflag_initialize( ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_initialize( p_cellcb ))
#define cEventflag_refer( pk_eventflagStatus ) \
          ((void)p_cellcb, tMarshaler_sCallee_cEventflag_refer( p_cellcb, pk_eventflagStatus ))
#define cSemaphore_signal( ) \
          ((void)p_cellcb, tMarshaler_sCallee_cSemaphore_signal( p_cellcb ))
#define cSemaphore_wait( ) \
          ((void)p_cellcb, tMarshaler_sCallee_cSemaphore_wait( p_cellcb ))
#define cSemaphore_waitPolling( ) \
          ((void)p_cellcb, tMarshaler_sCallee_cSemaphore_waitPolling( p_cellcb ))
#define cSemaphore_waitTimeout( timeout ) \
          ((void)p_cellcb, tMarshaler_sCallee_cSemaphore_waitTimeout( p_cellcb, timeout ))
#define cSemaphore_initialize( ) \
          ((void)p_cellcb, tMarshaler_sCallee_cSemaphore_initialize( p_cellcb ))
#define cSemaphore_refer( pk_semaphoreStatus ) \
          ((void)p_cellcb, tMarshaler_sCallee_cSemaphore_refer( p_cellcb, pk_semaphoreStatus ))
#define cMessageBuffer_send( message, size ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_send( p_cellcb, message, size ))
#define cMessageBuffer_sendPolling( message, size ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_sendPolling( p_cellcb, message, size ))
#define cMessageBuffer_sendTimeout( message, size, timeout ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_sendTimeout( p_cellcb, message, size, timeout ))
#define cMessageBuffer_receive( message ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_receive( p_cellcb, message ))
#define cMessageBuffer_receivePolling( message ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_receivePolling( p_cellcb, message ))
#define cMessageBuffer_receiveTimeout( message, timeout ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_receiveTimeout( p_cellcb, message, timeout ))
#define cMessageBuffer_initialize( ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_initialize( p_cellcb ))
#define cMessageBuffer_refer( packet ) \
          ((void)p_cellcb, tMarshaler_sCallee_cMessageBuffer_refer( p_cellcb, packet ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eClientEntry_add tMarshaler_sCallee_eClientEntry_add
#define eClientEntry_scale tMarshaler_sCallee_eClientEntry_scale
#define eClientEntry_widen tMarshaler_sCallee_eClientEntry_widen
#define eClientEntry_notify tMarshaler_sCallee_eClientEntry_notify

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

#endif /* tMarshaler_sCallee_TECSGENH */
