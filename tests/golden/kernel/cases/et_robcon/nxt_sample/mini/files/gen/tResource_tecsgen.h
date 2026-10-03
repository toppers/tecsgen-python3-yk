/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tResource_TECSGEN_H
#define tResource_TECSGEN_H

/*
 * celltype          :  tResource
 * global name       :  tResource
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
#include "sResource_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tResource_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    UINT8          id;
}  tResource_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tResource_CB_tab           tResource_INIB_tab
#define tResource_CB               tResource_INIB
#define tag_tResource_CB           tag_tResource_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tResource_INIB  tResource_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tResource_INIB *tResource_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sResource */
Inline StatusType   tResource_eResource_get(tResource_IDX idx);
Inline StatusType   tResource_eResource_release(tResource_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tResource_ID_BASE           (1)  /* ID のベース  #_NIDB_# */
#define tResource_N_CELL            (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tResource_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tResource_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tResource_ATTR_id( p_that )	((p_that)->id)

#define tResource_GET_id(p_that)	((p_that)->id)



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
#define VALID_IDX(IDX)  tResource_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tResource_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tResource_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tResource_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tResource_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eResource_get    tResource_eResource_get
#define eResource_release tResource_eResource_release

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tResource_N_CELL; (i)++ ){ \
       (p_cb) = &tResource_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tResource_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tResource_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tResource_ATTR_id
#undef tResource_GET_id
#undef ATTR_name
#undef tResource_ATTR_name
#undef tResource_GET_name
#undef ATTR_property
#undef tResource_ATTR_property
#undef tResource_GET_property
#undef ATTR_linkedResource
#undef tResource_ATTR_linkedResource
#undef tResource_GET_linkedResource
#undef eResource_get
#undef eResource_release
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tResource_TECSGENH */
