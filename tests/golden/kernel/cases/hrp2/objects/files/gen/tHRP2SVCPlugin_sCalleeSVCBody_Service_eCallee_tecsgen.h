/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_TECSGEN_H
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_TECSGEN_H

/*
 * celltype          :  tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee
 * global name       :  tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee
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
typedef struct tag_tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB {
    int  dummy;
} tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_IDX;
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tService_tecsgen.h"
#ifdef  tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_cCall_add( p_that, a, b, sum ) \
	  tService_eCallee_add( \
	   (tService_IDX)0, (a), (b), (sum) )
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_cCall_notify( p_that ) \
	  tService_eCallee_notify( \
	   (tService_IDX)0 )

#else  /* TECSFLOW */
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_cCall_add( p_that, a, b, sum ) \
	  (p_that)->cCall.add__T( \
 (a), (b), (sum) )
#define tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_cCall_notify( p_that ) \
	  (p_that)->cCall.notify__T( \
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
#define VALID_IDX(IDX)  tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cCall_add( a, b, sum ) \
          ((void)p_cellcb, tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_cCall_add( p_cellcb, a, b, sum ))
#define cCall_notify( ) \
          ((void)p_cellcb, tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_cCall_notify( p_cellcb ))



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

#endif /* tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_TECSGENH */
