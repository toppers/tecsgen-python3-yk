/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tClient_TECSGEN_H
#define tClient_TECSGEN_H

/*
 * celltype          :  tClient
 * global name       :  tClient
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

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tClient_CB {
    int  dummy;
} tClient_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tClient_IDX;
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tClient_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tMarshaler_sCallee_tecsgen.h"
#ifdef  tClient_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tClient_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tClient_ID_BASE             (1)  /* ID のベース  #_NIDB_# */
#define tClient_N_CELL              (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tClient_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tClient_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tClient_cCallee_add( p_that, a, b ) \
	  tMarshaler_sCallee_eClientEntry_add( \
	   (tMarshaler_sCallee_IDX)0, (a), (b) )
#define tClient_cCallee_scale( p_that, k, v ) \
	  tMarshaler_sCallee_eClientEntry_scale( \
	   (tMarshaler_sCallee_IDX)0, (k), (v) )
#define tClient_cCallee_widen( p_that, v ) \
	  tMarshaler_sCallee_eClientEntry_widen( \
	   (tMarshaler_sCallee_IDX)0, (v) )
#define tClient_cCallee_notify( p_that ) \
	  tMarshaler_sCallee_eClientEntry_notify( \
	   (tMarshaler_sCallee_IDX)0 )

#else  /* TECSFLOW */
#define tClient_cCallee_add( p_that, a, b ) \
	  (p_that)->cCallee.add__T( \
 (a), (b) )
#define tClient_cCallee_scale( p_that, k, v ) \
	  (p_that)->cCallee.scale__T( \
 (k), (v) )
#define tClient_cCallee_widen( p_that, v ) \
	  (p_that)->cCallee.widen__T( \
 (v) )
#define tClient_cCallee_notify( p_that ) \
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
#define VALID_IDX(IDX)  tClient_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tClient_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tClient_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tClient_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cCallee_add( a, b ) \
          ((void)p_cellcb, tClient_cCallee_add( p_cellcb, a, b ))
#define cCallee_scale( k, v ) \
          ((void)p_cellcb, tClient_cCallee_scale( p_cellcb, k, v ))
#define cCallee_widen( v ) \
          ((void)p_cellcb, tClient_cCallee_widen( p_cellcb, v ))
#define cCallee_notify( ) \
          ((void)p_cellcb, tClient_cCallee_notify( p_cellcb ))



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

#endif /* tClient_TECSGENH */
