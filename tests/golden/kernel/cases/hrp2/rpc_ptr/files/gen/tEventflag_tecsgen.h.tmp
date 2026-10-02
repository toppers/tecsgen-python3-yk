/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tEventflag_TECSGEN_H
#define tEventflag_TECSGEN_H

/*
 * celltype          :  tEventflag
 * global name       :  tEventflag
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
#include "sEventflag_tecsgen.h"
#include "siEventflag_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tEventflag_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    ID             id;
}  tEventflag_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tEventflag_CB_tab           tEventflag_INIB_tab
#define tEventflag_CB               tEventflag_INIB
#define tag_tEventflag_CB           tag_tEventflag_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tEventflag_INIB  tEventflag_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tEventflag_INIB *tEventflag_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sEventflag */
Inline ER           tEventflag_eEventflag_set(tEventflag_IDX idx, FLGPTN setPattern);
Inline ER           tEventflag_eEventflag_clear(tEventflag_IDX idx, FLGPTN clearPattern);
Inline ER           tEventflag_eEventflag_wait(tEventflag_IDX idx, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern);
Inline ER           tEventflag_eEventflag_waitPolling(tEventflag_IDX idx, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern);
Inline ER           tEventflag_eEventflag_waitTimeout(tEventflag_IDX idx, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern, TMO timeout);
Inline ER           tEventflag_eEventflag_initialize(tEventflag_IDX idx);
Inline ER           tEventflag_eEventflag_refer(tEventflag_IDX idx, T_RFLG* pk_eventflagStatus);
/* siEventflag */
Inline ER           tEventflag_eiEventflag_set(tEventflag_IDX idx, FLGPTN setPattern);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tEventflag_ID_BASE          (1)  /* ID のベース  #_NIDB_# */
#define tEventflag_N_CELL           (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tEventflag_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tEventflag_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tEventflag_ATTR_id( p_that )	((p_that)->id)

#define tEventflag_GET_id(p_that)	((p_that)->id)



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
#define VALID_IDX(IDX)  tEventflag_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tEventflag_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tEventflag_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tEventflag_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tEventflag_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eEventflag_set   tEventflag_eEventflag_set
#define eEventflag_clear tEventflag_eEventflag_clear
#define eEventflag_wait  tEventflag_eEventflag_wait
#define eEventflag_waitPolling tEventflag_eEventflag_waitPolling
#define eEventflag_waitTimeout tEventflag_eEventflag_waitTimeout
#define eEventflag_initialize tEventflag_eEventflag_initialize
#define eEventflag_refer tEventflag_eEventflag_refer
#define eiEventflag_set  tEventflag_eiEventflag_set

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tEventflag_N_CELL; (i)++ ){ \
       (p_cb) = &tEventflag_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tEventflag_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tEventflag_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tEventflag_ATTR_id
#undef tEventflag_GET_id
#undef ATTR_attribute
#undef tEventflag_ATTR_attribute
#undef tEventflag_GET_attribute
#undef ATTR_flagPattern
#undef tEventflag_ATTR_flagPattern
#undef tEventflag_GET_flagPattern
#undef ATTR_accessPattern
#undef tEventflag_ATTR_accessPattern
#undef tEventflag_GET_accessPattern
#undef eEventflag_set
#undef eEventflag_clear
#undef eEventflag_wait
#undef eEventflag_waitPolling
#undef eEventflag_waitTimeout
#undef eEventflag_initialize
#undef eEventflag_refer
#undef eiEventflag_set
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tEventflag_TECSGENH */
