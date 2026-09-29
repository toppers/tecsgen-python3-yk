/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tReset_TECSGEN_H
#define tReset_TECSGEN_H

/*
 * celltype          :  tReset
 * global name       :  tReset
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
#include "sMotor_tecsgen.h"
#include "sReset_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tReset_INIB {
    /* call port #_TCP_# */
    struct tag_sMotor_VDES *const*cMotor; /* TCP_2 */
    int_t n_cMotor;  /* TCP_3 */
    /* call port #_NEP_# */ 
}  tReset_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tReset_CB_tab           tReset_INIB_tab
#define tReset_CB               tReset_INIB
#define tag_tReset_CB           tag_tReset_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tReset_INIB  tReset_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tReset_INIB *tReset_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sReset */
void         tReset_eReset_reset(tReset_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

#define tReset_ID_BASE              (1)  /* ID のベース  #_NIDB_# */
#define tReset_N_CELL               (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tReset_VALID_IDX(IDX) (1)

/* 呼び口配列の大きさを得るマクロ #_NCPA_# */
#define N_CP_cMotor(p_that)  ((p_that)->n_cMotor)
#define NCP_cMotor           (N_CP_cMotor(p_cellcb))

/* セルCBを得るマクロ #_GCB_# */
#define tReset_GET_CELLCB(idx) (idx)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tReset_cMotor_getType( p_that, subscript ) \
	  (p_that)->cMotor[subscript]->VMT->getType__T( \
	   (p_that)->cMotor[subscript] )
#define tReset_cMotor_getCounts( p_that, subscript ) \
	  (p_that)->cMotor[subscript]->VMT->getCounts__T( \
	   (p_that)->cMotor[subscript] )
#define tReset_cMotor_getPower( p_that, subscript ) \
	  (p_that)->cMotor[subscript]->VMT->getPower__T( \
	   (p_that)->cMotor[subscript] )
#define tReset_cMotor_resetCounts( p_that, subscript ) \
	  (p_that)->cMotor[subscript]->VMT->resetCounts__T( \
	   (p_that)->cMotor[subscript] )
#define tReset_cMotor_setPower( p_that, subscript, power ) \
	  (p_that)->cMotor[subscript]->VMT->setPower__T( \
	   (p_that)->cMotor[subscript], (power) )
#define tReset_cMotor_stop( p_that, subscript, brake ) \
	  (p_that)->cMotor[subscript]->VMT->stop__T( \
	   (p_that)->cMotor[subscript], (brake) )
#define tReset_cMotor_rotate( p_that, subscript, degrees, speed_abs, blocking ) \
	  (p_that)->cMotor[subscript]->VMT->rotate__T( \
	   (p_that)->cMotor[subscript], (degrees), (speed_abs), (blocking) )
#define tReset_cMotor_initializePort( p_that, subscript, type ) \
	  (p_that)->cMotor[subscript]->VMT->initializePort__T( \
	   (p_that)->cMotor[subscript], (type) )

#else  /* TECSFLOW */
#define tReset_cMotor_getType( p_that, subscript ) \
	  (p_that)->cMotor[subscript].getType__T( \
 )
#define tReset_cMotor_getCounts( p_that, subscript ) \
	  (p_that)->cMotor[subscript].getCounts__T( \
 )
#define tReset_cMotor_getPower( p_that, subscript ) \
	  (p_that)->cMotor[subscript].getPower__T( \
 )
#define tReset_cMotor_resetCounts( p_that, subscript ) \
	  (p_that)->cMotor[subscript].resetCounts__T( \
 )
#define tReset_cMotor_setPower( p_that, subscript, power ) \
	  (p_that)->cMotor[subscript].setPower__T( \
 (power) )
#define tReset_cMotor_stop( p_that, subscript, brake ) \
	  (p_that)->cMotor[subscript].stop__T( \
 (brake) )
#define tReset_cMotor_rotate( p_that, subscript, degrees, speed_abs, blocking ) \
	  (p_that)->cMotor[subscript].rotate__T( \
 (degrees), (speed_abs), (blocking) )
#define tReset_cMotor_initializePort( p_that, subscript, type ) \
	  (p_that)->cMotor[subscript].initializePort__T( \
 (type) )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tReset_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tReset_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tReset_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tReset_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cMotor_getType( subscript ) \
          tReset_cMotor_getType( p_cellcb, subscript )
#define cMotor_getCounts( subscript ) \
          tReset_cMotor_getCounts( p_cellcb, subscript )
#define cMotor_getPower( subscript ) \
          tReset_cMotor_getPower( p_cellcb, subscript )
#define cMotor_resetCounts( subscript ) \
          tReset_cMotor_resetCounts( p_cellcb, subscript )
#define cMotor_setPower( subscript, power ) \
          tReset_cMotor_setPower( p_cellcb, subscript, power )
#define cMotor_stop( subscript, brake ) \
          tReset_cMotor_stop( p_cellcb, subscript, brake )
#define cMotor_rotate( subscript, degrees, speed_abs, blocking ) \
          tReset_cMotor_rotate( p_cellcb, subscript, degrees, speed_abs, blocking )
#define cMotor_initializePort( subscript, type ) \
          tReset_cMotor_initializePort( p_cellcb, subscript, type )




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eReset_reset     tReset_eReset_reset

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tReset_N_CELL; (i)++ ){ \
       (p_cb) = &tReset_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tReset_TECSGENH */
