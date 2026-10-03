/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tSystemTimer_TECSGEN_H
#define tSystemTimer_TECSGEN_H

/*
 * celltype          :  tSystemTimer
 * global name       :  tSystemTimer
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
#include "sCounter_tecsgen.h"
#include "sHandlerBody_tecsgen.h"
#include "sHookBody_tecsgen.h"
#include "sStatusTypeHookBody_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB (ダミー)型宣言 #_CCDP_# */
typedef struct tag_tSystemTimer_CB {
    int  dummy;
} tSystemTimer_CB;
/* シングルトンセル CB プロトタイプ宣言 #_SCP_# */


/* セルタイプのIDX型 #_CTIX_# */
typedef int   tSystemTimer_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sHandlerBody */
void         tSystemTimer_eInterruptBody_main();
/* sHookBody */
void         tSystemTimer_eStartupHookBody_main();
/* sStatusTypeHookBody */
void         tSystemTimer_eShutdownHookBody_main( StatusType ercd);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tSystemTimer_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tCounter_tecsgen.h"
#ifdef  tSystemTimer_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tSystemTimer_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ #_GCB_# */
#define tSystemTimer_GET_CELLCB(idx) ((void *)0)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tSystemTimer_cCounter_signal( ) \
	  tCounter_eCounter_signal( \
	   &tCounter_INIB_tab[0] )

#else  /* TECSFLOW */
#define tSystemTimer_cCounter_signal( ) \
	  (p_that)->cCounter.signal__T( \
 )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eInterruptBody */
void           tSystemTimer_eInterruptBody_main_skel( const struct tag_sHandlerBody_VDES *epd);
/* eStartupHookBody */
void           tSystemTimer_eStartupHookBody_main_skel( const struct tag_sHookBody_VDES *epd);
/* eShutdownHookBody */
void           tSystemTimer_eShutdownHookBody_main_skel( const struct tag_sStatusTypeHookBody_VDES *epd, StatusType ercd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tSystemTimer_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tSystemTimer_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tSystemTimer_IDX

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cCounter_signal( ) \
          tSystemTimer_cCounter_signal( )




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eInterruptBody_main tSystemTimer_eInterruptBody_main
#define eStartupHookBody_main tSystemTimer_eStartupHookBody_main
#define eShutdownHookBody_main tSystemTimer_eShutdownHookBody_main

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB()
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tSystemTimer_TECSGENH */
