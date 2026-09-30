/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef nMruby_tMrubyTaskBody_TECSGEN_H
#define nMruby_tMrubyTaskBody_TECSGEN_H

/*
 * celltype          :  tMrubyTaskBody
 * global name       :  nMruby_tMrubyTaskBody
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
#include "sTaskBody_tecsgen.h"
#include "nMruby_sMrubyVM_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_nMruby_tMrubyTaskBody_INIB {
    /* call port #_TCP_# */
    struct tag_nMruby_tMrubyVM_CB * const cMrubyVM;  /* TCP_4 */
    /* call port #_NEP_# */ 
}  nMruby_tMrubyTaskBody_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define nMruby_tMrubyTaskBody_CB_tab           nMruby_tMrubyTaskBody_INIB_tab
#define nMruby_tMrubyTaskBody_CB               nMruby_tMrubyTaskBody_INIB
#define tag_nMruby_tMrubyTaskBody_CB           tag_nMruby_tMrubyTaskBody_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern nMruby_tMrubyTaskBody_INIB  nMruby_tMrubyTaskBody_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_nMruby_tMrubyTaskBody_INIB *nMruby_tMrubyTaskBody_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         nMruby_tMrubyTaskBody_eMrubyBody_main(nMruby_tMrubyTaskBody_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  nMruby_tMrubyTaskBody_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "nMruby_tMrubyVM_tecsgen.h"
#ifdef  nMruby_tMrubyTaskBody_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* nMruby_tMrubyTaskBody_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define nMruby_tMrubyTaskBody_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define nMruby_tMrubyTaskBody_N_CELL        (4)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define nMruby_tMrubyTaskBody_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define nMruby_tMrubyTaskBody_GET_CELLCB(idx) (idx)
#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define nMruby_tMrubyTaskBody_cMrubyVM_initialize( p_that ) \
	  nMruby_tMrubyVM_eMrubyVM_initialize( \
	   (p_that)->cMrubyVM )
#define nMruby_tMrubyTaskBody_cMrubyVM_run( p_that ) \
	  nMruby_tMrubyVM_eMrubyVM_run( \
	   (p_that)->cMrubyVM )
#define nMruby_tMrubyTaskBody_cMrubyVM_funcall( p_that, name ) \
	  nMruby_tMrubyVM_eMrubyVM_funcall( \
	   (p_that)->cMrubyVM, (name) )
#define nMruby_tMrubyTaskBody_cMrubyVM_finalize( p_that ) \
	  nMruby_tMrubyVM_eMrubyVM_finalize( \
	   (p_that)->cMrubyVM )

#else  /* TECSFLOW */
#define nMruby_tMrubyTaskBody_cMrubyVM_initialize( p_that ) \
	  (p_that)->cMrubyVM.initialize__T( \
 )
#define nMruby_tMrubyTaskBody_cMrubyVM_run( p_that ) \
	  (p_that)->cMrubyVM.run__T( \
 )
#define nMruby_tMrubyTaskBody_cMrubyVM_funcall( p_that, name ) \
	  (p_that)->cMrubyVM.funcall__T( \
 (name) )
#define nMruby_tMrubyTaskBody_cMrubyVM_finalize( p_that ) \
	  (p_that)->cMrubyVM.finalize__T( \
 )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eMrubyBody */
void           nMruby_tMrubyTaskBody_eMrubyBody_main_skel( const struct tag_sTaskBody_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  nMruby_tMrubyTaskBody_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  nMruby_tMrubyTaskBody_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	nMruby_tMrubyTaskBody_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	nMruby_tMrubyTaskBody_IDX

#define tMrubyTaskBody_IDX  nMruby_tMrubyTaskBody_IDX
/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cMrubyVM_initialize( ) \
          ((void)p_cellcb, nMruby_tMrubyTaskBody_cMrubyVM_initialize( p_cellcb ))
#define cMrubyVM_run( ) \
          ((void)p_cellcb, nMruby_tMrubyTaskBody_cMrubyVM_run( p_cellcb ))
#define cMrubyVM_funcall( name ) \
          ((void)p_cellcb, nMruby_tMrubyTaskBody_cMrubyVM_funcall( p_cellcb, name ))
#define cMrubyVM_finalize( ) \
          ((void)p_cellcb, nMruby_tMrubyTaskBody_cMrubyVM_finalize( p_cellcb ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eMrubyBody_main  nMruby_tMrubyTaskBody_eMrubyBody_main

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nMruby_tMrubyTaskBody_N_CELL; (i)++ ){ \
       (p_cb) = &nMruby_tMrubyTaskBody_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* nMruby_tMrubyTaskBody_TECSGENH */
