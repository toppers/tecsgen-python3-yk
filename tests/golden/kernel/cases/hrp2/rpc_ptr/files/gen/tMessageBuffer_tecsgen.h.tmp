/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tMessageBuffer_TECSGEN_H
#define tMessageBuffer_TECSGEN_H

/*
 * celltype          :  tMessageBuffer
 * global name       :  tMessageBuffer
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
#include "sMessageBuffer_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tMessageBuffer_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    ID             id;
}  tMessageBuffer_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tMessageBuffer_CB_tab           tMessageBuffer_INIB_tab
#define tMessageBuffer_CB               tMessageBuffer_INIB
#define tag_tMessageBuffer_CB           tag_tMessageBuffer_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tMessageBuffer_INIB  tMessageBuffer_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tMessageBuffer_INIB *tMessageBuffer_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sMessageBuffer */
Inline ER           tMessageBuffer_eMessageBuffer_send(tMessageBuffer_IDX idx, const uint8_t* message, uint32_t size);
Inline ER           tMessageBuffer_eMessageBuffer_sendPolling(tMessageBuffer_IDX idx, const uint8_t* message, uint32_t size);
Inline ER           tMessageBuffer_eMessageBuffer_sendTimeout(tMessageBuffer_IDX idx, const uint8_t* message, uint32_t size, TMO timeout);
Inline ER_UINT      tMessageBuffer_eMessageBuffer_receive(tMessageBuffer_IDX idx, uint8_t* message);
Inline ER_UINT      tMessageBuffer_eMessageBuffer_receivePolling(tMessageBuffer_IDX idx, uint8_t* message);
Inline ER_UINT      tMessageBuffer_eMessageBuffer_receiveTimeout(tMessageBuffer_IDX idx, uint8_t* message, TMO timeout);
Inline void         tMessageBuffer_eMessageBuffer_initialize(tMessageBuffer_IDX idx);
Inline ER           tMessageBuffer_eMessageBuffer_refer(tMessageBuffer_IDX idx, T_RMBF* packet);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tMessageBuffer_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tMessageBuffer_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tMessageBuffer_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tMessageBuffer_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tMessageBuffer_ATTR_id( p_that )	((p_that)->id)

#define tMessageBuffer_GET_id(p_that)	((p_that)->id)



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
#define VALID_IDX(IDX)  tMessageBuffer_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tMessageBuffer_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tMessageBuffer_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tMessageBuffer_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tMessageBuffer_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eMessageBuffer_send tMessageBuffer_eMessageBuffer_send
#define eMessageBuffer_sendPolling tMessageBuffer_eMessageBuffer_sendPolling
#define eMessageBuffer_sendTimeout tMessageBuffer_eMessageBuffer_sendTimeout
#define eMessageBuffer_receive tMessageBuffer_eMessageBuffer_receive
#define eMessageBuffer_receivePolling tMessageBuffer_eMessageBuffer_receivePolling
#define eMessageBuffer_receiveTimeout tMessageBuffer_eMessageBuffer_receiveTimeout
#define eMessageBuffer_initialize tMessageBuffer_eMessageBuffer_initialize
#define eMessageBuffer_refer tMessageBuffer_eMessageBuffer_refer

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tMessageBuffer_N_CELL; (i)++ ){ \
       (p_cb) = &tMessageBuffer_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tMessageBuffer_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tMessageBuffer_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tMessageBuffer_ATTR_id
#undef tMessageBuffer_GET_id
#undef ATTR_attribute
#undef tMessageBuffer_ATTR_attribute
#undef tMessageBuffer_GET_attribute
#undef ATTR_maxSize
#undef tMessageBuffer_ATTR_maxSize
#undef tMessageBuffer_GET_maxSize
#undef ATTR_bufferSize
#undef tMessageBuffer_ATTR_bufferSize
#undef tMessageBuffer_GET_bufferSize
#undef ATTR_mbfmb
#undef tMessageBuffer_ATTR_mbfmb
#undef tMessageBuffer_GET_mbfmb
#undef ATTR_accessPattern
#undef tMessageBuffer_ATTR_accessPattern
#undef tMessageBuffer_GET_accessPattern
#undef eMessageBuffer_send
#undef eMessageBuffer_sendPolling
#undef eMessageBuffer_sendTimeout
#undef eMessageBuffer_receive
#undef eMessageBuffer_receivePolling
#undef eMessageBuffer_receiveTimeout
#undef eMessageBuffer_initialize
#undef eMessageBuffer_refer
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tMessageBuffer_TECSGENH */
