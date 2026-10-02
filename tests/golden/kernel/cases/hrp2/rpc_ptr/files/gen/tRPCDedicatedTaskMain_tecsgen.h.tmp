/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tRPCDedicatedTaskMain_TECSGEN_H
#define tRPCDedicatedTaskMain_TECSGEN_H

/*
 * celltype          :  tRPCDedicatedTaskMain
 * global name       :  tRPCDedicatedTaskMain
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
#include "sTaskBody_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tRPCDedicatedTaskMain_CB {
    int  dummy;
} tRPCDedicatedTaskMain_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tRPCDedicatedTaskMain_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         tRPCDedicatedTaskMain_eMain_main(tRPCDedicatedTaskMain_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tRPCDedicatedTaskMain_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tUnmarshaler_sCallee_tecsgen.h"
#ifdef  tRPCDedicatedTaskMain_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tRPCDedicatedTaskMain_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tRPCDedicatedTaskMain_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tRPCDedicatedTaskMain_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tRPCDedicatedTaskMain_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tRPCDedicatedTaskMain_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tRPCDedicatedTaskMain_cMain_main( p_that ) \
	  tUnmarshaler_sCallee_eUnmarshalAndCallFunction_main( \
	   (tUnmarshaler_sCallee_IDX)0 )

#else  /* TECSFLOW */
#define tRPCDedicatedTaskMain_cMain_main( p_that ) \
	  (p_that)->cMain.main__T( \
 )

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
#define VALID_IDX(IDX)  tRPCDedicatedTaskMain_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tRPCDedicatedTaskMain_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tRPCDedicatedTaskMain_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tRPCDedicatedTaskMain_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cMain_main( ) \
          ((void)p_cellcb, tRPCDedicatedTaskMain_cMain_main( p_cellcb ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eMain_main       tRPCDedicatedTaskMain_eMain_main

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

#endif /* tRPCDedicatedTaskMain_TECSGENH */
