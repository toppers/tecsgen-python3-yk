/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef nMruby_tsTask_TECSGEN_H
#define nMruby_tsTask_TECSGEN_H

/*
 * celltype          :  tsTask
 * global name       :  nMruby_tsTask
 * multi-domain      :  yes
 * idx_is_id(actual) :  yes(yes)
 * singleton         :  no
 * has_CB            :  no
 * has_INIB          :  yes
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sTask_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_nMruby_tsTask_INIB {
    /* call port #_TCP_# */
    const struct tag_tTask_INIB * const cTECS;  /* TCP_4 */
}  nMruby_tsTask_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define nMruby_tsTask_CB_ptab           nMruby_tsTask_INIB_ptab
#define nMruby_tsTask_CB               nMruby_tsTask_INIB
#define tag_nMruby_tsTask_CB           tag_nMruby_tsTask_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPP_# */
extern nMruby_tsTask_INIB  *const nMruby_tsTask_INIB_ptab[];
extern nMruby_tsTask_INIB  rDomainEV3_EV3TaskeTaskBridge_INIB;
extern nMruby_tsTask_INIB  rDomainEV3_MrubyMainTaskeTaskBridge_INIB;
extern nMruby_tsTask_INIB  rDomainEV3_MrubySubTask1eTaskBridge_INIB;
extern nMruby_tsTask_INIB  rDomainEV3_MrubySubTask2eTaskBridge_INIB;
extern nMruby_tsTask_INIB  rDomainEV3_MrubyWakeupTaskeTaskBridge_INIB;
extern nMruby_tsTask_INIB  rDomainEV3_MrubyCyclicTaskeTaskBridge_INIB;

/* セルタイプのIDX型 #_CTIX_# */
typedef ID nMruby_tsTask_IDX;
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  nMruby_tsTask_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tTask_tecsgen.h"
#ifdef  nMruby_tsTask_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* nMruby_tsTask_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define nMruby_tsTask_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define nMruby_tsTask_N_CELL        (6)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define nMruby_tsTask_VALID_IDX(IDX) (nMruby_tsTask_ID_BASE <= (IDX) && (IDX) < nMruby_tsTask_ID_BASE+nMruby_tsTask_N_CELL)


/* セルCBを得るマクロ #_GCB_# */
#define nMruby_tsTask_GET_CELLCB(idx) (nMruby_tsTask_CB_ptab[(idx) - nMruby_tsTask_ID_BASE])
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define nMruby_tsTask_cTECS_activate( p_that ) \
	  tTask_eTask_activate( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_cancelActivate( p_that ) \
	  tTask_eTask_cancelActivate( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_terminate( p_that ) \
	  tTask_eTask_terminate( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_changePriority( p_that, priority ) \
	  tTask_eTask_changePriority( \
	   (p_that)->cTECS, (priority) )
#define nMruby_tsTask_cTECS_getPriority( p_that, p_priority ) \
	  tTask_eTask_getPriority( \
	   (p_that)->cTECS, (p_priority) )
#define nMruby_tsTask_cTECS_refer( p_that, pk_taskStatus ) \
	  tTask_eTask_refer( \
	   (p_that)->cTECS, (pk_taskStatus) )
#define nMruby_tsTask_cTECS_wakeup( p_that ) \
	  tTask_eTask_wakeup( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_cancelWakeup( p_that ) \
	  tTask_eTask_cancelWakeup( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_releaseWait( p_that ) \
	  tTask_eTask_releaseWait( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_suspend( p_that ) \
	  tTask_eTask_suspend( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_resume( p_that ) \
	  tTask_eTask_resume( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_raiseException( p_that, pattern ) \
	  tTask_eTask_raiseException( \
	   (p_that)->cTECS, (pattern) )
#define nMruby_tsTask_cTECS_referException( p_that, pk_rtex ) \
	  tTask_eTask_referException( \
	   (p_that)->cTECS, (pk_rtex) )
#define nMruby_tsTask_cTECS_startOverRunHandler( p_that, ovrtim ) \
	  tTask_eTask_startOverRunHandler( \
	   (p_that)->cTECS, (ovrtim) )
#define nMruby_tsTask_cTECS_stopOverRunHandler( p_that ) \
	  tTask_eTask_stopOverRunHandler( \
	   (p_that)->cTECS )
#define nMruby_tsTask_cTECS_referOverRunHandler( p_that, pk_rovr ) \
	  tTask_eTask_referOverRunHandler( \
	   (p_that)->cTECS, (pk_rovr) )

#else  /* TECSFLOW */
#define nMruby_tsTask_cTECS_activate( p_that ) \
	  (p_that)->cTECS.activate__T( \
 )
#define nMruby_tsTask_cTECS_cancelActivate( p_that ) \
	  (p_that)->cTECS.cancelActivate__T( \
 )
#define nMruby_tsTask_cTECS_terminate( p_that ) \
	  (p_that)->cTECS.terminate__T( \
 )
#define nMruby_tsTask_cTECS_changePriority( p_that, priority ) \
	  (p_that)->cTECS.changePriority__T( \
 (priority) )
#define nMruby_tsTask_cTECS_getPriority( p_that, p_priority ) \
	  (p_that)->cTECS.getPriority__T( \
 (p_priority) )
#define nMruby_tsTask_cTECS_refer( p_that, pk_taskStatus ) \
	  (p_that)->cTECS.refer__T( \
 (pk_taskStatus) )
#define nMruby_tsTask_cTECS_wakeup( p_that ) \
	  (p_that)->cTECS.wakeup__T( \
 )
#define nMruby_tsTask_cTECS_cancelWakeup( p_that ) \
	  (p_that)->cTECS.cancelWakeup__T( \
 )
#define nMruby_tsTask_cTECS_releaseWait( p_that ) \
	  (p_that)->cTECS.releaseWait__T( \
 )
#define nMruby_tsTask_cTECS_suspend( p_that ) \
	  (p_that)->cTECS.suspend__T( \
 )
#define nMruby_tsTask_cTECS_resume( p_that ) \
	  (p_that)->cTECS.resume__T( \
 )
#define nMruby_tsTask_cTECS_raiseException( p_that, pattern ) \
	  (p_that)->cTECS.raiseException__T( \
 (pattern) )
#define nMruby_tsTask_cTECS_referException( p_that, pk_rtex ) \
	  (p_that)->cTECS.referException__T( \
 (pk_rtex) )
#define nMruby_tsTask_cTECS_startOverRunHandler( p_that, ovrtim ) \
	  (p_that)->cTECS.startOverRunHandler__T( \
 (ovrtim) )
#define nMruby_tsTask_cTECS_stopOverRunHandler( p_that ) \
	  (p_that)->cTECS.stopOverRunHandler__T( \
 )
#define nMruby_tsTask_cTECS_referOverRunHandler( p_that, pk_rovr ) \
	  (p_that)->cTECS.referOverRunHandler__T( \
 (pk_rovr) )

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
#define VALID_IDX(IDX)  nMruby_tsTask_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  nMruby_tsTask_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	nMruby_tsTask_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	nMruby_tsTask_IDX

#define tsTask_IDX  nMruby_tsTask_IDX
/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cTECS_activate( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_activate( p_cellcb ))
#define cTECS_cancelActivate( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_cancelActivate( p_cellcb ))
#define cTECS_terminate( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_terminate( p_cellcb ))
#define cTECS_changePriority( priority ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_changePriority( p_cellcb, priority ))
#define cTECS_getPriority( p_priority ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_getPriority( p_cellcb, p_priority ))
#define cTECS_refer( pk_taskStatus ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_refer( p_cellcb, pk_taskStatus ))
#define cTECS_wakeup( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_wakeup( p_cellcb ))
#define cTECS_cancelWakeup( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_cancelWakeup( p_cellcb ))
#define cTECS_releaseWait( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_releaseWait( p_cellcb ))
#define cTECS_suspend( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_suspend( p_cellcb ))
#define cTECS_resume( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_resume( p_cellcb ))
#define cTECS_raiseException( pattern ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_raiseException( p_cellcb, pattern ))
#define cTECS_referException( pk_rtex ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_referException( p_cellcb, pk_rtex ))
#define cTECS_startOverRunHandler( ovrtim ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_startOverRunHandler( p_cellcb, ovrtim ))
#define cTECS_stopOverRunHandler( ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_stopOverRunHandler( p_cellcb ))
#define cTECS_referOverRunHandler( pk_rovr ) \
          ((void)p_cellcb, nMruby_tsTask_cTECS_referOverRunHandler( p_cellcb, pk_rovr ))



/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nMruby_tsTask_N_CELL; (i)++ ){ \
       (p_cb) = nMruby_tsTask_CB_ptab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* nMruby_tsTask_TECSGENH */
