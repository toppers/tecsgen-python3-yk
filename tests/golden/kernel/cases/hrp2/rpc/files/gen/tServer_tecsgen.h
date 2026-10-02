/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tServer_TECSGEN_H
#define tServer_TECSGEN_H

/*
 * celltype          :  tServer
 * global name       :  tServer
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
typedef struct tag_tServer_CB {
    int  dummy;
} tServer_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */

/* セルタイプのIDX型 #_CTIX_# */
typedef int   tServer_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sCallee */
ER           tServer_eCallee_add(tServer_IDX idx, int32_t a, int32_t b);
int16_t      tServer_eCallee_scale(tServer_IDX idx, int8_t k, uint16_t v);
int64_t      tServer_eCallee_widen(tServer_IDX idx, uint32_t v);
void         tServer_eCallee_notify(tServer_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

#define tServer_ID_BASE             (1)  /* ID のベース  #_NIDB_# */
#define tServer_N_CELL              (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tServer_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tServer_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
#else  /* TECSFLOW */
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
#define VALID_IDX(IDX)  tServer_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tServer_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tServer_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tServer_IDX




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eCallee_add      tServer_eCallee_add
#define eCallee_scale    tServer_eCallee_scale
#define eCallee_widen    tServer_eCallee_widen
#define eCallee_notify   tServer_eCallee_notify

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

#endif /* tServer_TECSGENH */
