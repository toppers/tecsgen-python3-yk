/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tCyclicTaskActivator_TECSGEN_H
#define tCyclicTaskActivator_TECSGEN_H

/*
 * celltype          :  tCyclicTaskActivator
 * global name       :  tCyclicTaskActivator
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
#include "siHandlerBody_tecsgen.h"
#include "siTask_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tCyclicTaskActivator_CB {
    int  dummy;
} tCyclicTaskActivator_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tCyclicTaskActivator_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* siHandlerBody */
void         tCyclicTaskActivator_eiBody_main(tCyclicTaskActivator_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tCyclicTaskActivator_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tTask_tecsgen.h"
#ifdef  tCyclicTaskActivator_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tCyclicTaskActivator_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tCyclicTaskActivator_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tCyclicTaskActivator_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tCyclicTaskActivator_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tCyclicTaskActivator_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tCyclicTaskActivator_ciTask_activate( p_that ) \
	  tTask_eiTask_activate( \
	   &tTask_INIB_tab[5] )
#define tCyclicTaskActivator_ciTask_wakeup( p_that ) \
	  tTask_eiTask_wakeup( \
	   &tTask_INIB_tab[5] )
#define tCyclicTaskActivator_ciTask_releaseWait( p_that ) \
	  tTask_eiTask_releaseWait( \
	   &tTask_INIB_tab[5] )
#define tCyclicTaskActivator_ciTask_raiseException( p_that, pattern ) \
	  tTask_eiTask_raiseException( \
	   &tTask_INIB_tab[5], (pattern) )
#define tCyclicTaskActivator_ciTask_disableWait( p_that ) \
	  tTask_eiTask_disableWait( \
	   &tTask_INIB_tab[5] )
#define tCyclicTaskActivator_ciTask_enableWait( p_that ) \
	  tTask_eiTask_enableWait( \
	   &tTask_INIB_tab[5] )
#define tCyclicTaskActivator_ciTask_startOverRunHandler( p_that, ovrtim ) \
	  tTask_eiTask_startOverRunHandler( \
	   &tTask_INIB_tab[5], (ovrtim) )
#define tCyclicTaskActivator_ciTask_stopOverRunHandler( p_that ) \
	  tTask_eiTask_stopOverRunHandler( \
	   &tTask_INIB_tab[5] )

#else  /* TECSFLOW */
#define tCyclicTaskActivator_ciTask_activate( p_that ) \
	  (p_that)->ciTask.activate__T( \
 )
#define tCyclicTaskActivator_ciTask_wakeup( p_that ) \
	  (p_that)->ciTask.wakeup__T( \
 )
#define tCyclicTaskActivator_ciTask_releaseWait( p_that ) \
	  (p_that)->ciTask.releaseWait__T( \
 )
#define tCyclicTaskActivator_ciTask_raiseException( p_that, pattern ) \
	  (p_that)->ciTask.raiseException__T( \
 (pattern) )
#define tCyclicTaskActivator_ciTask_disableWait( p_that ) \
	  (p_that)->ciTask.disableWait__T( \
 )
#define tCyclicTaskActivator_ciTask_enableWait( p_that ) \
	  (p_that)->ciTask.enableWait__T( \
 )
#define tCyclicTaskActivator_ciTask_startOverRunHandler( p_that, ovrtim ) \
	  (p_that)->ciTask.startOverRunHandler__T( \
 (ovrtim) )
#define tCyclicTaskActivator_ciTask_stopOverRunHandler( p_that ) \
	  (p_that)->ciTask.stopOverRunHandler__T( \
 )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eiBody */
void           tCyclicTaskActivator_eiBody_main_skel( const struct tag_siHandlerBody_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tCyclicTaskActivator_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tCyclicTaskActivator_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tCyclicTaskActivator_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tCyclicTaskActivator_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define ciTask_activate( ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_activate( p_cellcb ))
#define ciTask_wakeup( ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_wakeup( p_cellcb ))
#define ciTask_releaseWait( ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_releaseWait( p_cellcb ))
#define ciTask_raiseException( pattern ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_raiseException( p_cellcb, pattern ))
#define ciTask_disableWait( ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_disableWait( p_cellcb ))
#define ciTask_enableWait( ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_enableWait( p_cellcb ))
#define ciTask_startOverRunHandler( ovrtim ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_startOverRunHandler( p_cellcb, ovrtim ))
#define ciTask_stopOverRunHandler( ) \
          ((void)p_cellcb, tCyclicTaskActivator_ciTask_stopOverRunHandler( p_cellcb ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eiBody_main      tCyclicTaskActivator_eiBody_main

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

#endif /* tCyclicTaskActivator_TECSGENH */
