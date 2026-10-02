/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tFixedSizeMemoryPool_TECSGEN_H
#define tFixedSizeMemoryPool_TECSGEN_H

/*
 * celltype          :  tFixedSizeMemoryPool
 * global name       :  tFixedSizeMemoryPool
 * multi-domain      :  yes
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
#include "sGetFixedSizeMemoryPool_tecsgen.h"
#include "sReleaseFixedSizeMemoryPool_tecsgen.h"
#include "sManageFixedSizeMemoryPool_tecsgen.h"
#include "sReferFixedSizeMemoryPool_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tFixedSizeMemoryPool_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    ID             id;
}  tFixedSizeMemoryPool_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tFixedSizeMemoryPool_CB_ptab           tFixedSizeMemoryPool_INIB_ptab
#define tFixedSizeMemoryPool_CB               tFixedSizeMemoryPool_INIB
#define tag_tFixedSizeMemoryPool_CB           tag_tFixedSizeMemoryPool_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPP_# */
extern tFixedSizeMemoryPool_INIB  *const tFixedSizeMemoryPool_INIB_ptab[];
extern tFixedSizeMemoryPool_INIB  rKernel_FixedSizeMemoryPoolK_INIB;
extern tFixedSizeMemoryPool_INIB  rUser_FixedSizeMemoryPoolU_INIB;
extern tFixedSizeMemoryPool_INIB  FixedSizeMemoryPoolO_INIB;

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tFixedSizeMemoryPool_INIB *tFixedSizeMemoryPool_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sGetFixedSizeMemoryPool */
Inline ER           tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_get(tFixedSizeMemoryPool_IDX idx, void** p_block);
Inline ER           tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getPolling(tFixedSizeMemoryPool_IDX idx, void** p_block);
Inline ER           tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getTimeout(tFixedSizeMemoryPool_IDX idx, void** p_block, TMO timeout);
/* sReleaseFixedSizeMemoryPool */
Inline ER           tFixedSizeMemoryPool_eReleaseFixedSizeMemoryPool_release(tFixedSizeMemoryPool_IDX idx, const void* block);
/* sManageFixedSizeMemoryPool */
Inline ER           tFixedSizeMemoryPool_eManageFixedSizeMemoryPool_initialize(tFixedSizeMemoryPool_IDX idx);
/* sReferFixedSizeMemoryPool */
Inline ER           tFixedSizeMemoryPool_eReferFixedSizeMemoryPool_refer(tFixedSizeMemoryPool_IDX idx, T_RMPF* pk_memoryPoolFixedSizeStatus);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tFixedSizeMemoryPool_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tFixedSizeMemoryPool_N_CELL        (3)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tFixedSizeMemoryPool_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tFixedSizeMemoryPool_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tFixedSizeMemoryPool_ATTR_id( p_that )	((p_that)->id)

#define tFixedSizeMemoryPool_GET_id(p_that)	((p_that)->id)



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
#define VALID_IDX(IDX)  tFixedSizeMemoryPool_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tFixedSizeMemoryPool_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tFixedSizeMemoryPool_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tFixedSizeMemoryPool_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tFixedSizeMemoryPool_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eGetFixedSizeMemoryPool_get tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_get
#define eGetFixedSizeMemoryPool_getPolling tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getPolling
#define eGetFixedSizeMemoryPool_getTimeout tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getTimeout
#define eReleaseFixedSizeMemoryPool_release tFixedSizeMemoryPool_eReleaseFixedSizeMemoryPool_release
#define eManageFixedSizeMemoryPool_initialize tFixedSizeMemoryPool_eManageFixedSizeMemoryPool_initialize
#define eReferFixedSizeMemoryPool_refer tFixedSizeMemoryPool_eReferFixedSizeMemoryPool_refer

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tFixedSizeMemoryPool_N_CELL; (i)++ ){ \
       (p_cb) = tFixedSizeMemoryPool_CB_ptab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tFixedSizeMemoryPool_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tFixedSizeMemoryPool_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tFixedSizeMemoryPool_ATTR_id
#undef tFixedSizeMemoryPool_GET_id
#undef ATTR_attribute
#undef tFixedSizeMemoryPool_ATTR_attribute
#undef tFixedSizeMemoryPool_GET_attribute
#undef ATTR_blockCount
#undef tFixedSizeMemoryPool_ATTR_blockCount
#undef tFixedSizeMemoryPool_GET_blockCount
#undef ATTR_blockSize
#undef tFixedSizeMemoryPool_ATTR_blockSize
#undef tFixedSizeMemoryPool_GET_blockSize
#undef ATTR_mpf
#undef tFixedSizeMemoryPool_ATTR_mpf
#undef tFixedSizeMemoryPool_GET_mpf
#undef ATTR_mpfmb
#undef tFixedSizeMemoryPool_ATTR_mpfmb
#undef tFixedSizeMemoryPool_GET_mpfmb
#undef ATTR_accessPattern
#undef tFixedSizeMemoryPool_ATTR_accessPattern
#undef tFixedSizeMemoryPool_GET_accessPattern
#undef eGetFixedSizeMemoryPool_get
#undef eGetFixedSizeMemoryPool_getPolling
#undef eGetFixedSizeMemoryPool_getTimeout
#undef eReleaseFixedSizeMemoryPool_release
#undef eManageFixedSizeMemoryPool_initialize
#undef eReferFixedSizeMemoryPool_refer
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tFixedSizeMemoryPool_TECSGENH */
