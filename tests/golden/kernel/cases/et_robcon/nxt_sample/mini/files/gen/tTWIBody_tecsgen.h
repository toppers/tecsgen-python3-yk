/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tTWIBody_TECSGEN_H
#define tTWIBody_TECSGEN_H

/*
 * celltype          :  tTWIBody
 * global name       :  tTWIBody
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
#include "sTWI_tecsgen.h"
#include "sHandlerBody_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tTWIBody_INIB {
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    uint32_t       clockDivisor;
}  tTWIBody_INIB;
/* セル CB 型宣言 #_CCTPA_# */
typedef struct tag_tTWIBody_CB {
    tTWIBody_INIB  *_inib;
    /* call port #_NEP_# */ 
    /* var #_VA_# */ 
    uint32_t       pending;
    uint8_t*       buffer;
    uint8_t        state;
}  tTWIBody_CB;
/* シングルトンセル CB プロトタイプ宣言 #_SCP_# */
extern  tTWIBody_CB  tTWIBody_SINGLE_CELL_CB;
extern  tTWIBody_INIB  tTWIBody_SINGLE_CELL_INIB;


/* セルタイプのIDX型 #_CTIX_# */
typedef struct tag_tTWIBody_CB *tTWIBody_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTWI */
bool_t       tTWIBody_eTWI_initialize();
void         tTWIBody_eTWI_startWrite( uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, const uint8_t* data, uint32_t nBytes);
void         tTWIBody_eTWI_startRead( uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, uint8_t* data, uint32_t nBytes);
void         tTWIBody_eTWI_pollingUpdate();
bool_t       tTWIBody_eTWI_isBusy();
bool_t       tTWIBody_eTWI_isOk();
void         tTWIBody_eTWI_reset();
/* sHandlerBody */
void         tTWIBody_eiInterruptBody_main();
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ #_GCB_# */
#define tTWIBody_GET_CELLCB(idx) ((void *)0)

/* 属性アクセスマクロ #_AAM_# */
#define tTWIBody_ATTR_clockDivisor	(tTWIBody_SINGLE_CELL_INIB.clockDivisor)

#define tTWIBody_GET_clockDivisor()	(tTWIBody_SINGLE_CELL_INIB.clockDivisor)


/* var アクセスマクロ #_VAM_# */
#define tTWIBody_VAR_pending	(tTWIBody_SINGLE_CELL_CB.pending)
#define tTWIBody_VAR_buffer 	(tTWIBody_SINGLE_CELL_CB.buffer)
#define tTWIBody_VAR_state  	(tTWIBody_SINGLE_CELL_CB.state)

#define tTWIBody_GET_pending()	(tTWIBody_SINGLE_CELL_CB.pending)
#define tTWIBody_SET_pending(val)	(tTWIBody_SINGLE_CELL_CB.pending=(val))
#define tTWIBody_GET_buffer()	(tTWIBody_SINGLE_CELL_CB.buffer)
#define tTWIBody_SET_buffer(val)	(tTWIBody_SINGLE_CELL_CB.buffer=(val))
#define tTWIBody_GET_state()	(tTWIBody_SINGLE_CELL_CB.state)
#define tTWIBody_SET_state(val)	(tTWIBody_SINGLE_CELL_CB.state=(val))

#ifndef TECSFLOW
#else  /* TECSFLOW */
#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eiInterruptBody */
void           tTWIBody_eiInterruptBody_main_skel( const struct tag_sHandlerBody_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tTWIBody_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tTWIBody_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tTWIBody_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_clockDivisor    tTWIBody_ATTR_clockDivisor


/* var アクセスマクロ(短縮形) #_VAMA_# */
#define VAR_pending          tTWIBody_VAR_pending
#define VAR_buffer           tTWIBody_VAR_buffer
#define VAR_state            tTWIBody_VAR_state




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eTWI_initialize  tTWIBody_eTWI_initialize
#define eTWI_startWrite  tTWIBody_eTWI_startWrite
#define eTWI_startRead   tTWIBody_eTWI_startRead
#define eTWI_pollingUpdate tTWIBody_eTWI_pollingUpdate
#define eTWI_isBusy      tTWIBody_eTWI_isBusy
#define eTWI_isOk        tTWIBody_eTWI_isOk
#define eTWI_reset       tTWIBody_eTWI_reset
#define eiInterruptBody_main tTWIBody_eiInterruptBody_main

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB()
#define SET_CB_INIB_POINTER(i,p_that)\
	tTWIBody_SINGLE_CELL_CB._inib = &tTWIBody_SINGLE_CELL_INIB;

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tTWIBody_TECSGENH */
