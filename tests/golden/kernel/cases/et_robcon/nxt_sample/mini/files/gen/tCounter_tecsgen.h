/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tCounter_TECSGEN_H
#define tCounter_TECSGEN_H

/*
 * celltype          :  tCounter
 * global name       :  tCounter
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  no
 * has_CB            :  no
 * has_INIB          :  yes
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sCounter_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tCounter_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    UINT8          id;
}  tCounter_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tCounter_CB_tab           tCounter_INIB_tab
#define tCounter_CB               tCounter_INIB
#define tag_tCounter_CB           tag_tCounter_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tCounter_INIB  tCounter_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tCounter_INIB *tCounter_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sCounter */
Inline StatusType   tCounter_eCounter_signal(tCounter_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tCounter_ID_BASE            (1)  /* ID のベース  #_NIDB_# */
#define tCounter_N_CELL             (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tCounter_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tCounter_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tCounter_ATTR_id( p_that )	((p_that)->id)

#define tCounter_GET_id(p_that)	((p_that)->id)



#ifndef TECSFLOW
#else  /* TECSFLOW */
#endif /* TECSFLOW */
#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tCounter_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tCounter_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tCounter_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tCounter_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tCounter_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eCounter_signal  tCounter_eCounter_signal

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tCounter_N_CELL; (i)++ ){ \
       (p_cb) = &tCounter_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tCounter_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tCounter_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tCounter_ATTR_id
#undef tCounter_GET_id
#undef ATTR_name
#undef tCounter_ATTR_name
#undef tCounter_GET_name
#undef ATTR_minimumCycle
#undef tCounter_ATTR_minimumCycle
#undef tCounter_GET_minimumCycle
#undef ATTR_maximumAllowedValue
#undef tCounter_ATTR_maximumAllowedValue
#undef tCounter_GET_maximumAllowedValue
#undef ATTR_ticksPerBase
#undef tCounter_ATTR_ticksPerBase
#undef tCounter_GET_ticksPerBase
#undef eCounter_signal
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tCounter_TECSGENH */
