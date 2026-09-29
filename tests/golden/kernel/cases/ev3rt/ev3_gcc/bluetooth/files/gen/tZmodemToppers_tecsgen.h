/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tZmodemToppers_TECSGEN_H
#define tZmodemToppers_TECSGEN_H

/*
 * celltype          :  tZmodemToppers
 * global name       :  tZmodemToppers
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
#include "sTask_tecsgen.h"
#include "sTaskBody_tecsgen.h"
#include "sZmodemToppers_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tZmodemToppers_CB {
    int  dummy;
} tZmodemToppers_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tZmodemToppers_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         tZmodemToppers_eBody_main(tZmodemToppers_IDX idx);
/* sZmodemToppers */
ER           tZmodemToppers_eZmodemToppers_zmodem_recv_file(tZmodemToppers_IDX idx, ID portid, const uint8_t* buf, uint32_t size, SIZE* filesz);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tZmodemToppers_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tTask_tecsgen.h"
#ifdef  tZmodemToppers_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tZmodemToppers_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tZmodemToppers_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tZmodemToppers_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tZmodemToppers_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tZmodemToppers_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tZmodemToppers_cZmodemTask_activate( p_that ) \
	  tTask_eTask_activate( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_cancelActivate( p_that ) \
	  tTask_eTask_cancelActivate( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_terminate( p_that ) \
	  tTask_eTask_terminate( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_changePriority( p_that, priority ) \
	  tTask_eTask_changePriority( \
	   &tTask_INIB_tab[2], (priority) )
#define tZmodemToppers_cZmodemTask_getPriority( p_that, p_priority ) \
	  tTask_eTask_getPriority( \
	   &tTask_INIB_tab[2], (p_priority) )
#define tZmodemToppers_cZmodemTask_refer( p_that, pk_taskStatus ) \
	  tTask_eTask_refer( \
	   &tTask_INIB_tab[2], (pk_taskStatus) )
#define tZmodemToppers_cZmodemTask_wakeup( p_that ) \
	  tTask_eTask_wakeup( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_cancelWakeup( p_that ) \
	  tTask_eTask_cancelWakeup( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_releaseWait( p_that ) \
	  tTask_eTask_releaseWait( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_suspend( p_that ) \
	  tTask_eTask_suspend( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_resume( p_that ) \
	  tTask_eTask_resume( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_raiseException( p_that, pattern ) \
	  tTask_eTask_raiseException( \
	   &tTask_INIB_tab[2], (pattern) )
#define tZmodemToppers_cZmodemTask_referException( p_that, pk_rtex ) \
	  tTask_eTask_referException( \
	   &tTask_INIB_tab[2], (pk_rtex) )
#define tZmodemToppers_cZmodemTask_startOverRunHandler( p_that, ovrtim ) \
	  tTask_eTask_startOverRunHandler( \
	   &tTask_INIB_tab[2], (ovrtim) )
#define tZmodemToppers_cZmodemTask_stopOverRunHandler( p_that ) \
	  tTask_eTask_stopOverRunHandler( \
	   &tTask_INIB_tab[2] )
#define tZmodemToppers_cZmodemTask_referOverRunHandler( p_that, pk_rovr ) \
	  tTask_eTask_referOverRunHandler( \
	   &tTask_INIB_tab[2], (pk_rovr) )

#else  /* TECSFLOW */
#define tZmodemToppers_cZmodemTask_activate( p_that ) \
	  (p_that)->cZmodemTask.activate__T( \
 )
#define tZmodemToppers_cZmodemTask_cancelActivate( p_that ) \
	  (p_that)->cZmodemTask.cancelActivate__T( \
 )
#define tZmodemToppers_cZmodemTask_terminate( p_that ) \
	  (p_that)->cZmodemTask.terminate__T( \
 )
#define tZmodemToppers_cZmodemTask_changePriority( p_that, priority ) \
	  (p_that)->cZmodemTask.changePriority__T( \
 (priority) )
#define tZmodemToppers_cZmodemTask_getPriority( p_that, p_priority ) \
	  (p_that)->cZmodemTask.getPriority__T( \
 (p_priority) )
#define tZmodemToppers_cZmodemTask_refer( p_that, pk_taskStatus ) \
	  (p_that)->cZmodemTask.refer__T( \
 (pk_taskStatus) )
#define tZmodemToppers_cZmodemTask_wakeup( p_that ) \
	  (p_that)->cZmodemTask.wakeup__T( \
 )
#define tZmodemToppers_cZmodemTask_cancelWakeup( p_that ) \
	  (p_that)->cZmodemTask.cancelWakeup__T( \
 )
#define tZmodemToppers_cZmodemTask_releaseWait( p_that ) \
	  (p_that)->cZmodemTask.releaseWait__T( \
 )
#define tZmodemToppers_cZmodemTask_suspend( p_that ) \
	  (p_that)->cZmodemTask.suspend__T( \
 )
#define tZmodemToppers_cZmodemTask_resume( p_that ) \
	  (p_that)->cZmodemTask.resume__T( \
 )
#define tZmodemToppers_cZmodemTask_raiseException( p_that, pattern ) \
	  (p_that)->cZmodemTask.raiseException__T( \
 (pattern) )
#define tZmodemToppers_cZmodemTask_referException( p_that, pk_rtex ) \
	  (p_that)->cZmodemTask.referException__T( \
 (pk_rtex) )
#define tZmodemToppers_cZmodemTask_startOverRunHandler( p_that, ovrtim ) \
	  (p_that)->cZmodemTask.startOverRunHandler__T( \
 (ovrtim) )
#define tZmodemToppers_cZmodemTask_stopOverRunHandler( p_that ) \
	  (p_that)->cZmodemTask.stopOverRunHandler__T( \
 )
#define tZmodemToppers_cZmodemTask_referOverRunHandler( p_that, pk_rovr ) \
	  (p_that)->cZmodemTask.referOverRunHandler__T( \
 (pk_rovr) )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eBody */
void           tZmodemToppers_eBody_main_skel( const struct tag_sTaskBody_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tZmodemToppers_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tZmodemToppers_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tZmodemToppers_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tZmodemToppers_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cZmodemTask_activate( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_activate( p_cellcb ))
#define cZmodemTask_cancelActivate( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_cancelActivate( p_cellcb ))
#define cZmodemTask_terminate( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_terminate( p_cellcb ))
#define cZmodemTask_changePriority( priority ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_changePriority( p_cellcb, priority ))
#define cZmodemTask_getPriority( p_priority ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_getPriority( p_cellcb, p_priority ))
#define cZmodemTask_refer( pk_taskStatus ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_refer( p_cellcb, pk_taskStatus ))
#define cZmodemTask_wakeup( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_wakeup( p_cellcb ))
#define cZmodemTask_cancelWakeup( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_cancelWakeup( p_cellcb ))
#define cZmodemTask_releaseWait( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_releaseWait( p_cellcb ))
#define cZmodemTask_suspend( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_suspend( p_cellcb ))
#define cZmodemTask_resume( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_resume( p_cellcb ))
#define cZmodemTask_raiseException( pattern ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_raiseException( p_cellcb, pattern ))
#define cZmodemTask_referException( pk_rtex ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_referException( p_cellcb, pk_rtex ))
#define cZmodemTask_startOverRunHandler( ovrtim ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_startOverRunHandler( p_cellcb, ovrtim ))
#define cZmodemTask_stopOverRunHandler( ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_stopOverRunHandler( p_cellcb ))
#define cZmodemTask_referOverRunHandler( pk_rovr ) \
          ((void)p_cellcb, tZmodemToppers_cZmodemTask_referOverRunHandler( p_cellcb, pk_rovr ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eBody_main       tZmodemToppers_eBody_main
#define eZmodemToppers_zmodem_recv_file tZmodemToppers_eZmodemToppers_zmodem_recv_file

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

#endif /* tZmodemToppers_TECSGENH */
