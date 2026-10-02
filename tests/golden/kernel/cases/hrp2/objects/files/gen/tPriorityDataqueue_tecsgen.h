/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tPriorityDataqueue_TECSGEN_H
#define tPriorityDataqueue_TECSGEN_H

/*
 * celltype          :  tPriorityDataqueue
 * global name       :  tPriorityDataqueue
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
#include "sSendPriorityDataqueue_tecsgen.h"
#include "sReceivePriorityDataqueue_tecsgen.h"
#include "sManagePriorityDataqueue_tecsgen.h"
#include "sReferPriorityDataqueue_tecsgen.h"
#include "siPriorityDataqueue_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tPriorityDataqueue_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    ID             id;
}  tPriorityDataqueue_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tPriorityDataqueue_CB_ptab           tPriorityDataqueue_INIB_ptab
#define tPriorityDataqueue_CB               tPriorityDataqueue_INIB
#define tag_tPriorityDataqueue_CB           tag_tPriorityDataqueue_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPP_# */
extern tPriorityDataqueue_INIB  *const tPriorityDataqueue_INIB_ptab[];
extern tPriorityDataqueue_INIB  rKernel_PriorityDataqueueK_INIB;
extern tPriorityDataqueue_INIB  rUser_PriorityDataqueueU_INIB;
extern tPriorityDataqueue_INIB  PriorityDataqueueO_INIB;

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tPriorityDataqueue_INIB *tPriorityDataqueue_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sSendPriorityDataqueue */
Inline ER           tPriorityDataqueue_eSendPriorityDataqueue_send(tPriorityDataqueue_IDX idx, intptr_t data, PRI dataPriority);
Inline ER           tPriorityDataqueue_eSendPriorityDataqueue_sendPolling(tPriorityDataqueue_IDX idx, intptr_t data, PRI dataPriority);
Inline ER           tPriorityDataqueue_eSendPriorityDataqueue_sendTimeout(tPriorityDataqueue_IDX idx, intptr_t data, PRI dataPriority, TMO timeout);
/* sReceivePriorityDataqueue */
Inline ER           tPriorityDataqueue_eReceivePriorityDataqueue_receive(tPriorityDataqueue_IDX idx, intptr_t* p_data, PRI* p_dataPriority);
Inline ER           tPriorityDataqueue_eReceivePriorityDataqueue_receivePolling(tPriorityDataqueue_IDX idx, intptr_t* p_data, PRI* p_dataPriority);
Inline ER           tPriorityDataqueue_eReceivePriorityDataqueue_receiveTimeout(tPriorityDataqueue_IDX idx, intptr_t* p_data, PRI* p_dataPriority, TMO timeout);
/* sManagePriorityDataqueue */
Inline ER           tPriorityDataqueue_eManagePriorityDataqueue_initialize(tPriorityDataqueue_IDX idx);
/* sReferPriorityDataqueue */
Inline ER           tPriorityDataqueue_eReferPriorityDataqueue_refer(tPriorityDataqueue_IDX idx, T_RPDQ* pk_priorityDataqueueStatus);
/* siPriorityDataqueue */
Inline ER           tPriorityDataqueue_eiPriorityDataqueue_sendPolling(tPriorityDataqueue_IDX idx, intptr_t data, PRI dataPriority);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tPriorityDataqueue_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tPriorityDataqueue_N_CELL        (3)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tPriorityDataqueue_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tPriorityDataqueue_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tPriorityDataqueue_ATTR_id( p_that )	((p_that)->id)

#define tPriorityDataqueue_GET_id(p_that)	((p_that)->id)



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
#define VALID_IDX(IDX)  tPriorityDataqueue_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tPriorityDataqueue_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tPriorityDataqueue_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tPriorityDataqueue_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tPriorityDataqueue_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eSendPriorityDataqueue_send tPriorityDataqueue_eSendPriorityDataqueue_send
#define eSendPriorityDataqueue_sendPolling tPriorityDataqueue_eSendPriorityDataqueue_sendPolling
#define eSendPriorityDataqueue_sendTimeout tPriorityDataqueue_eSendPriorityDataqueue_sendTimeout
#define eReceivePriorityDataqueue_receive tPriorityDataqueue_eReceivePriorityDataqueue_receive
#define eReceivePriorityDataqueue_receivePolling tPriorityDataqueue_eReceivePriorityDataqueue_receivePolling
#define eReceivePriorityDataqueue_receiveTimeout tPriorityDataqueue_eReceivePriorityDataqueue_receiveTimeout
#define eManagePriorityDataqueue_initialize tPriorityDataqueue_eManagePriorityDataqueue_initialize
#define eReferPriorityDataqueue_refer tPriorityDataqueue_eReferPriorityDataqueue_refer
#define eiPriorityDataqueue_sendPolling tPriorityDataqueue_eiPriorityDataqueue_sendPolling

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tPriorityDataqueue_N_CELL; (i)++ ){ \
       (p_cb) = tPriorityDataqueue_CB_ptab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tPriorityDataqueue_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tPriorityDataqueue_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tPriorityDataqueue_ATTR_id
#undef tPriorityDataqueue_GET_id
#undef ATTR_attribute
#undef tPriorityDataqueue_ATTR_attribute
#undef tPriorityDataqueue_GET_attribute
#undef ATTR_count
#undef tPriorityDataqueue_ATTR_count
#undef tPriorityDataqueue_GET_count
#undef ATTR_maxDataPriority
#undef tPriorityDataqueue_ATTR_maxDataPriority
#undef tPriorityDataqueue_GET_maxDataPriority
#undef ATTR_pdqmb
#undef tPriorityDataqueue_ATTR_pdqmb
#undef tPriorityDataqueue_GET_pdqmb
#undef ATTR_accessPattern
#undef tPriorityDataqueue_ATTR_accessPattern
#undef tPriorityDataqueue_GET_accessPattern
#undef eSendPriorityDataqueue_send
#undef eSendPriorityDataqueue_sendPolling
#undef eSendPriorityDataqueue_sendTimeout
#undef eReceivePriorityDataqueue_receive
#undef eReceivePriorityDataqueue_receivePolling
#undef eReceivePriorityDataqueue_receiveTimeout
#undef eManagePriorityDataqueue_initialize
#undef eReferPriorityDataqueue_refer
#undef eiPriorityDataqueue_sendPolling
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tPriorityDataqueue_TECSGENH */
