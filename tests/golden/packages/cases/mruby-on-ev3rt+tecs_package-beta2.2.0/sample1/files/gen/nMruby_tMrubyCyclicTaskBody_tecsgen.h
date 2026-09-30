/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef nMruby_tMrubyCyclicTaskBody_TECSGEN_H
#define nMruby_tMrubyCyclicTaskBody_TECSGEN_H

/*
 * celltype          :  tMrubyCyclicTaskBody
 * global name       :  nMruby_tMrubyCyclicTaskBody
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  no
 * has_CB            :  yes
 * has_INIB          :  no
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
/* セル CB 型宣言 #_CCTPA_# */
typedef struct tag_nMruby_tMrubyCyclicTaskBody_CB {
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* var #_VA_# */ 
    bool_t         b_init;
}  nMruby_tMrubyCyclicTaskBody_CB;
/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern nMruby_tMrubyCyclicTaskBody_CB  nMruby_tMrubyCyclicTaskBody_CB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef struct tag_nMruby_tMrubyCyclicTaskBody_CB *nMruby_tMrubyCyclicTaskBody_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         nMruby_tMrubyCyclicTaskBody_eMrubyBody_main(nMruby_tMrubyCyclicTaskBody_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  nMruby_tMrubyCyclicTaskBody_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "nMruby_tMrubyVM_tecsgen.h"
#ifdef  nMruby_tMrubyCyclicTaskBody_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* nMruby_tMrubyCyclicTaskBody_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define nMruby_tMrubyCyclicTaskBody_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define nMruby_tMrubyCyclicTaskBody_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define nMruby_tMrubyCyclicTaskBody_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define nMruby_tMrubyCyclicTaskBody_GET_CELLCB(idx) (idx)



/* var アクセスマクロ #_VAM_# */
#define nMruby_tMrubyCyclicTaskBody_VAR_b_init(p_that)	((p_that)->b_init)

#define nMruby_tMrubyCyclicTaskBody_GET_b_init(p_that)	((p_that)->b_init)
#define nMruby_tMrubyCyclicTaskBody_SET_b_init(p_that,val)	((p_that)->b_init=(val))

#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_initialize( p_that ) \
	  nMruby_tMrubyVM_eMrubyVM_initialize( \
	   &nMruby_tMrubyVM_CB_tab[4] )
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_run( p_that ) \
	  nMruby_tMrubyVM_eMrubyVM_run( \
	   &nMruby_tMrubyVM_CB_tab[4] )
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_funcall( p_that, name ) \
	  nMruby_tMrubyVM_eMrubyVM_funcall( \
	   &nMruby_tMrubyVM_CB_tab[4], (name) )
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_finalize( p_that ) \
	  nMruby_tMrubyVM_eMrubyVM_finalize( \
	   &nMruby_tMrubyVM_CB_tab[4] )

#else  /* TECSFLOW */
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_initialize( p_that ) \
	  (p_that)->cMrubyVM.initialize__T( \
 )
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_run( p_that ) \
	  (p_that)->cMrubyVM.run__T( \
 )
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_funcall( p_that, name ) \
	  (p_that)->cMrubyVM.funcall__T( \
 (name) )
#define nMruby_tMrubyCyclicTaskBody_cMrubyVM_finalize( p_that ) \
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
void           nMruby_tMrubyCyclicTaskBody_eMrubyBody_main_skel( const struct tag_sTaskBody_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  nMruby_tMrubyCyclicTaskBody_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  nMruby_tMrubyCyclicTaskBody_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	nMruby_tMrubyCyclicTaskBody_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	nMruby_tMrubyCyclicTaskBody_IDX

#define tMrubyCyclicTaskBody_IDX  nMruby_tMrubyCyclicTaskBody_IDX


/* var アクセスマクロ(短縮形) #_VAMA_# */
#define VAR_b_init           nMruby_tMrubyCyclicTaskBody_VAR_b_init( p_cellcb )

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cMrubyVM_initialize( ) \
          ((void)p_cellcb, nMruby_tMrubyCyclicTaskBody_cMrubyVM_initialize( p_cellcb ))
#define cMrubyVM_run( ) \
          ((void)p_cellcb, nMruby_tMrubyCyclicTaskBody_cMrubyVM_run( p_cellcb ))
#define cMrubyVM_funcall( name ) \
          ((void)p_cellcb, nMruby_tMrubyCyclicTaskBody_cMrubyVM_funcall( p_cellcb, name ))
#define cMrubyVM_finalize( ) \
          ((void)p_cellcb, nMruby_tMrubyCyclicTaskBody_cMrubyVM_finalize( p_cellcb ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eMrubyBody_main  nMruby_tMrubyCyclicTaskBody_eMrubyBody_main

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nMruby_tMrubyCyclicTaskBody_N_CELL; (i)++ ){ \
       (p_cb) = &nMruby_tMrubyCyclicTaskBody_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* nMruby_tMrubyCyclicTaskBody_TECSGENH */
