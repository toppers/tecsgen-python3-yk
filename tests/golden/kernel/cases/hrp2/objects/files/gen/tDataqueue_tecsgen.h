/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tDataqueue_TECSGEN_H
#define tDataqueue_TECSGEN_H

/*
 * celltype          :  tDataqueue
 * global name       :  tDataqueue
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
#include "sSendDataqueue_tecsgen.h"
#include "sReceiveDataqueue_tecsgen.h"
#include "sManageDataqueue_tecsgen.h"
#include "sReferDataqueue_tecsgen.h"
#include "siDataqueue_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tDataqueue_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    ID             id;
}  tDataqueue_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tDataqueue_CB_ptab           tDataqueue_INIB_ptab
#define tDataqueue_CB               tDataqueue_INIB
#define tag_tDataqueue_CB           tag_tDataqueue_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPP_# */
extern tDataqueue_INIB  *const tDataqueue_INIB_ptab[];
extern tDataqueue_INIB  rKernel_DataqueueK_INIB;
extern tDataqueue_INIB  rUser_DataqueueU_INIB;
extern tDataqueue_INIB  DataqueueO_INIB;

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tDataqueue_INIB *tDataqueue_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sSendDataqueue */
Inline ER           tDataqueue_eSendDataqueue_send(tDataqueue_IDX idx, intptr_t data);
Inline ER           tDataqueue_eSendDataqueue_sendPolling(tDataqueue_IDX idx, intptr_t data);
Inline ER           tDataqueue_eSendDataqueue_sendTimeout(tDataqueue_IDX idx, intptr_t data, TMO timeout);
Inline ER           tDataqueue_eSendDataqueue_sendForce(tDataqueue_IDX idx, intptr_t data);
/* sReceiveDataqueue */
Inline ER           tDataqueue_eReceiveDataqueue_receive(tDataqueue_IDX idx, intptr_t* p_data);
Inline ER           tDataqueue_eReceiveDataqueue_receivePolling(tDataqueue_IDX idx, intptr_t* p_data);
Inline ER           tDataqueue_eReceiveDataqueue_receiveTimeout(tDataqueue_IDX idx, intptr_t* p_data, TMO timeout);
/* sManageDataqueue */
Inline ER           tDataqueue_eManageDataqueue_initialize(tDataqueue_IDX idx);
/* sReferDataqueue */
Inline ER           tDataqueue_eReferDataqueue_refer(tDataqueue_IDX idx, T_RDTQ* pk_dataqueueStatus);
/* siDataqueue */
Inline ER           tDataqueue_eiDataqueue_sendPolling(tDataqueue_IDX idx, intptr_t data);
Inline ER           tDataqueue_eiDataqueue_sendForce(tDataqueue_IDX idx, intptr_t data);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tDataqueue_ID_BASE          (1)  /* ID のベース  #_NIDB_# */
#define tDataqueue_N_CELL           (3)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tDataqueue_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tDataqueue_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tDataqueue_ATTR_id( p_that )	((p_that)->id)

#define tDataqueue_GET_id(p_that)	((p_that)->id)



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
#define VALID_IDX(IDX)  tDataqueue_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tDataqueue_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tDataqueue_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tDataqueue_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tDataqueue_ATTR_id( p_cellcb )





/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eSendDataqueue_send tDataqueue_eSendDataqueue_send
#define eSendDataqueue_sendPolling tDataqueue_eSendDataqueue_sendPolling
#define eSendDataqueue_sendTimeout tDataqueue_eSendDataqueue_sendTimeout
#define eSendDataqueue_sendForce tDataqueue_eSendDataqueue_sendForce
#define eReceiveDataqueue_receive tDataqueue_eReceiveDataqueue_receive
#define eReceiveDataqueue_receivePolling tDataqueue_eReceiveDataqueue_receivePolling
#define eReceiveDataqueue_receiveTimeout tDataqueue_eReceiveDataqueue_receiveTimeout
#define eManageDataqueue_initialize tDataqueue_eManageDataqueue_initialize
#define eReferDataqueue_refer tDataqueue_eReferDataqueue_refer
#define eiDataqueue_sendPolling tDataqueue_eiDataqueue_sendPolling
#define eiDataqueue_sendForce tDataqueue_eiDataqueue_sendForce

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tDataqueue_N_CELL; (i)++ ){ \
       (p_cb) = tDataqueue_CB_ptab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tDataqueue_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tDataqueue_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tDataqueue_ATTR_id
#undef tDataqueue_GET_id
#undef ATTR_attribute
#undef tDataqueue_ATTR_attribute
#undef tDataqueue_GET_attribute
#undef ATTR_count
#undef tDataqueue_ATTR_count
#undef tDataqueue_GET_count
#undef ATTR_dtqmb
#undef tDataqueue_ATTR_dtqmb
#undef tDataqueue_GET_dtqmb
#undef ATTR_accessPattern
#undef tDataqueue_ATTR_accessPattern
#undef tDataqueue_GET_accessPattern
#undef eSendDataqueue_send
#undef eSendDataqueue_sendPolling
#undef eSendDataqueue_sendTimeout
#undef eSendDataqueue_sendForce
#undef eReceiveDataqueue_receive
#undef eReceiveDataqueue_receivePolling
#undef eReceiveDataqueue_receiveTimeout
#undef eManageDataqueue_initialize
#undef eReferDataqueue_refer
#undef eiDataqueue_sendPolling
#undef eiDataqueue_sendForce
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tDataqueue_TECSGENH */
