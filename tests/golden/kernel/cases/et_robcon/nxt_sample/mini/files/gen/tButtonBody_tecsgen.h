/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tButtonBody_TECSGEN_H
#define tButtonBody_TECSGEN_H

/*
 * celltype          :  tButtonBody
 * global name       :  tButtonBody
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  yes
 * has_CB            :  yes
 * has_INIB          :  yes
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sButton_tecsgen.h"
#include "sHandlerBody_tecsgen.h"
#include "sAvrButton_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tButtonBody_INIB {
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    int32_t        threshold;
}  tButtonBody_INIB;
/* セル CB 型宣言 #_CCTPA_# */
typedef struct tag_tButtonBody_CB {
    tButtonBody_INIB  *_inib;
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* var #_VA_# */ 
    uint8_t        button;
    int32_t        count;
    uint8_t        preState;
}  tButtonBody_CB;
/* シングルトンセル CB プロトタイプ宣言 #_SCP_# */
extern  tButtonBody_CB  tButtonBody_SINGLE_CELL_CB;
extern  tButtonBody_INIB  tButtonBody_SINGLE_CELL_INIB;


/* セルタイプのIDX型 #_CTIX_# */
typedef struct tag_tButtonBody_CB *tButtonBody_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sButton */
Inline bool_t       tButtonBody_eButton_isENTERButton();
Inline bool_t       tButtonBody_eButton_isRUNButton();
Inline bool_t       tButtonBody_eButton_isSTOPButton();
Inline bool_t       tButtonBody_eButton_isEXITButton();
Inline bool_t       tButtonBody_eButton_isENTERButtonOnly();
Inline bool_t       tButtonBody_eButton_isRUNButtonOnly();
Inline bool_t       tButtonBody_eButton_isSTOPButtonOnly();
Inline bool_t       tButtonBody_eButton_isEXITButtonOnly();
/* sHandlerBody */
void         tButtonBody_eiBody_main();
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tButtonBody_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tAVRBody_tecsgen.h"
#ifdef  tButtonBody_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tButtonBody_CB_TYPE_ONLY */

/* セルCBを得るマクロ #_GCB_# */
#define tButtonBody_GET_CELLCB(idx) ((void *)0)

/* 属性アクセスマクロ #_AAM_# */
#define tButtonBody_ATTR_threshold	(tButtonBody_SINGLE_CELL_INIB.threshold)

#define tButtonBody_GET_threshold()	(tButtonBody_SINGLE_CELL_INIB.threshold)


/* var アクセスマクロ #_VAM_# */
#define tButtonBody_VAR_button	(tButtonBody_SINGLE_CELL_CB.button)
#define tButtonBody_VAR_count	(tButtonBody_SINGLE_CELL_CB.count)
#define tButtonBody_VAR_preState	(tButtonBody_SINGLE_CELL_CB.preState)

#define tButtonBody_GET_button()	(tButtonBody_SINGLE_CELL_CB.button)
#define tButtonBody_SET_button(val)	(tButtonBody_SINGLE_CELL_CB.button=(val))
#define tButtonBody_GET_count()	(tButtonBody_SINGLE_CELL_CB.count)
#define tButtonBody_SET_count(val)	(tButtonBody_SINGLE_CELL_CB.count=(val))
#define tButtonBody_GET_preState()	(tButtonBody_SINGLE_CELL_CB.preState)
#define tButtonBody_SET_preState(val)	(tButtonBody_SINGLE_CELL_CB.preState=(val))

#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tButtonBody_cAvrButton_getButton( ) \
	  tAVRBody_eAvrButton_getButton( \
	    )

#else  /* TECSFLOW */
#define tButtonBody_cAvrButton_getButton( ) \
	  (p_that)->cAvrButton.getButton__T( \
 )

#endif /* TECSFLOW */
#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eiBody */
void           tButtonBody_eiBody_main_skel( const struct tag_sHandlerBody_VDES *epd);

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tButtonBody_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tButtonBody_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tButtonBody_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_threshold       tButtonBody_ATTR_threshold


/* var アクセスマクロ(短縮形) #_VAMA_# */
#define VAR_button           tButtonBody_VAR_button
#define VAR_count            tButtonBody_VAR_count
#define VAR_preState         tButtonBody_VAR_preState

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cAvrButton_getButton( ) \
          tButtonBody_cAvrButton_getButton( )




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eButton_isENTERButton tButtonBody_eButton_isENTERButton
#define eButton_isRUNButton tButtonBody_eButton_isRUNButton
#define eButton_isSTOPButton tButtonBody_eButton_isSTOPButton
#define eButton_isEXITButton tButtonBody_eButton_isEXITButton
#define eButton_isENTERButtonOnly tButtonBody_eButton_isENTERButtonOnly
#define eButton_isRUNButtonOnly tButtonBody_eButton_isRUNButtonOnly
#define eButton_isSTOPButtonOnly tButtonBody_eButton_isSTOPButtonOnly
#define eButton_isEXITButtonOnly tButtonBody_eButton_isEXITButtonOnly
#define eiBody_main      tButtonBody_eiBody_main

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB()
#define SET_CB_INIB_POINTER(i,p_that)\
	tButtonBody_SINGLE_CELL_CB._inib = &tButtonBody_SINGLE_CELL_INIB;

#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tButtonBody_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tButtonBody_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_threshold
#undef tButtonBody_ATTR_threshold
#undef tButtonBody_GET_threshold
#undef VAR_button
#undef VAR_button
#undef tButtonBody_VAR_button
#undef tButtonBody_GET_button
#undef tButtonBody_SET_button
#undef VAR_count
#undef VAR_count
#undef tButtonBody_VAR_count
#undef tButtonBody_GET_count
#undef tButtonBody_SET_count
#undef VAR_preState
#undef VAR_preState
#undef tButtonBody_VAR_preState
#undef tButtonBody_GET_preState
#undef tButtonBody_SET_preState
#undef tButtonBody_cAvrButton_getButton
#undef cAvrButton_getButton
#undef eButton_isENTERButton
#undef eButton_isRUNButton
#undef eButton_isSTOPButton
#undef eButton_isEXITButton
#undef eButton_isENTERButtonOnly
#undef eButton_isRUNButtonOnly
#undef eButton_isSTOPButtonOnly
#undef eButton_isEXITButtonOnly
#undef eiBody_main
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tButtonBody_TECSGENH */
