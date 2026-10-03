/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tBattery_TECSGEN_H
#define tBattery_TECSGEN_H

/*
 * celltype          :  tBattery
 * global name       :  tBattery
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  yes
 * has_CB            :  no
 * has_INIB          :  no
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sBattery_tecsgen.h"
#include "sAvrBattery_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tBattery_CB {
    int  dummy;
} tBattery_CB;
/* シングルトンセル CB プロトタイプ宣言 #_SCP_# */


/* セルタイプのIDX型 #_CTIX_# */
typedef int   tBattery_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sBattery */
Inline uint16_t     tBattery_eBattery_getBatteryVoltage();
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tBattery_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tAVRBody_tecsgen.h"
#ifdef  tBattery_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tBattery_CB_TYPE_ONLY */

/* セルCBを得るマクロ #_GCB_# */
#define tBattery_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tBattery_cAvrBattery_batteryVoltage( ) \
	  tAVRBody_eAvrBattery_batteryVoltage( \
	    )

#else  /* TECSFLOW */
#define tBattery_cAvrBattery_batteryVoltage( ) \
	  (p_that)->cAvrBattery.batteryVoltage__T( \
 )

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


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tBattery_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tBattery_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tBattery_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cAvrBattery_batteryVoltage( ) \
          tBattery_cAvrBattery_batteryVoltage( )




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eBattery_getBatteryVoltage tBattery_eBattery_getBatteryVoltage

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB()
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tBattery_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tBattery_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef tBattery_cAvrBattery_batteryVoltage
#undef cAvrBattery_batteryVoltage
#undef eBattery_getBatteryVoltage
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tBattery_TECSGENH */
