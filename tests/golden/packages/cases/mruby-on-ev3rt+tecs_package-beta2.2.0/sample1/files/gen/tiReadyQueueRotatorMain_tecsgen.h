/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tiReadyQueueRotatorMain_TECSGEN_H
#define tiReadyQueueRotatorMain_TECSGEN_H

/*
 * celltype          :  tiReadyQueueRotatorMain
 * global name       :  tiReadyQueueRotatorMain
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
#include "siHandlerBody_tecsgen.h"
#include "siKernel_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tiReadyQueueRotatorMain_INIB {
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    PRI            priority;
}  tiReadyQueueRotatorMain_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tiReadyQueueRotatorMain_CB_tab           tiReadyQueueRotatorMain_INIB_tab
#define tiReadyQueueRotatorMain_CB               tiReadyQueueRotatorMain_INIB
#define tag_tiReadyQueueRotatorMain_CB           tag_tiReadyQueueRotatorMain_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tiReadyQueueRotatorMain_INIB  tiReadyQueueRotatorMain_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tiReadyQueueRotatorMain_INIB *tiReadyQueueRotatorMain_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* siHandlerBody */
void         tiReadyQueueRotatorMain_eiBody_main(tiReadyQueueRotatorMain_IDX idx);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tiReadyQueueRotatorMain_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tKernel_tecsgen.h"
#ifdef  tiReadyQueueRotatorMain_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tiReadyQueueRotatorMain_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY

#define tiReadyQueueRotatorMain_ID_BASE        (1)  /* ID のベース  #_NIDB_# */
#define tiReadyQueueRotatorMain_N_CELL        (1)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tiReadyQueueRotatorMain_VALID_IDX(IDX) (1)


/* セルCBを得るマクロ #_GCB_# */
#define tiReadyQueueRotatorMain_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tiReadyQueueRotatorMain_ATTR_priority( p_that )	((p_that)->priority)

#define tiReadyQueueRotatorMain_GET_priority(p_that)	((p_that)->priority)



#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_getTaskId( p_that, p_taskId ) \
	  tKernel_eiKernel_getTaskId( \
	    (p_taskId) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_rotateReadyQueue( p_that, taskPriority ) \
	  tKernel_eiKernel_rotateReadyQueue( \
	    (taskPriority) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_getMicroTime( p_that, p_systemMicroTime ) \
	  tKernel_eiKernel_getMicroTime( \
	    (p_systemMicroTime) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_lockCpu( p_that ) \
	  tKernel_eiKernel_lockCpu( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_unlockCpu( p_that ) \
	  tKernel_eiKernel_unlockCpu( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_exitKernel( p_that ) \
	  tKernel_eiKernel_exitKernel( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseContext( p_that ) \
	  tKernel_eiKernel_senseContext( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseLock( p_that ) \
	  tKernel_eiKernel_senseLock( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatch( p_that ) \
	  tKernel_eiKernel_senseDispatch( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatchPendingState( p_that ) \
	  tKernel_eiKernel_senseDispatchPendingState( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseKernel( p_that ) \
	  tKernel_eiKernel_senseKernel( \
	    )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatchPendingStateCPU( p_that, p_exceptionInfomation ) \
	  tKernel_eiKernel_senseDispatchPendingStateCPU( \
	    (p_exceptionInfomation) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseTaskExceptionPendingStateCPU( p_that, p_exceptionInfomation ) \
	  tKernel_eiKernel_senseTaskExceptionPendingStateCPU( \
	    (p_exceptionInfomation) )

#else  /* TECSFLOW */
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_getTaskId( p_that, p_taskId ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.getTaskId__T( \
 (p_taskId) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_rotateReadyQueue( p_that, taskPriority ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.rotateReadyQueue__T( \
 (taskPriority) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_getMicroTime( p_that, p_systemMicroTime ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.getMicroTime__T( \
 (p_systemMicroTime) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_lockCpu( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.lockCpu__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_unlockCpu( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.unlockCpu__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_exitKernel( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.exitKernel__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseContext( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseContext__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseLock( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseLock__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatch( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseDispatch__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatchPendingState( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseDispatchPendingState__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseKernel( p_that ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseKernel__T( \
 )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatchPendingStateCPU( p_that, p_exceptionInfomation ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseDispatchPendingStateCPU__T( \
 (p_exceptionInfomation) )
#define tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseTaskExceptionPendingStateCPU( p_that, p_exceptionInfomation ) \
	  (p_that)->_require_call_port_tKernel_eiKernel.senseTaskExceptionPendingStateCPU__T( \
 (p_exceptionInfomation) )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */
/* eiBody */
void           tiReadyQueueRotatorMain_eiBody_main_skel( const struct tag_siHandlerBody_VDES *epd);

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tiReadyQueueRotatorMain_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tiReadyQueueRotatorMain_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tiReadyQueueRotatorMain_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tiReadyQueueRotatorMain_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_priority        tiReadyQueueRotatorMain_ATTR_priority( p_cellcb )


/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define getTaskId( p_taskId ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_getTaskId( p_cellcb, p_taskId ))
#define rotateReadyQueue( taskPriority ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_rotateReadyQueue( p_cellcb, taskPriority ))
#define getMicroTime( p_systemMicroTime ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_getMicroTime( p_cellcb, p_systemMicroTime ))
#define lockCpu( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_lockCpu( p_cellcb ))
#define unlockCpu( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_unlockCpu( p_cellcb ))
#define exitKernel( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_exitKernel( p_cellcb ))
#define senseContext( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseContext( p_cellcb ))
#define senseLock( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseLock( p_cellcb ))
#define senseDispatch( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatch( p_cellcb ))
#define senseDispatchPendingState( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatchPendingState( p_cellcb ))
#define senseKernel( ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseKernel( p_cellcb ))
#define senseDispatchPendingStateCPU( p_exceptionInfomation ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseDispatchPendingStateCPU( p_cellcb, p_exceptionInfomation ))
#define senseTaskExceptionPendingStateCPU( p_exceptionInfomation ) \
          ((void)p_cellcb, tiReadyQueueRotatorMain__require_call_port_tKernel_eiKernel_senseTaskExceptionPendingStateCPU( p_cellcb, p_exceptionInfomation ))




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eiBody_main      tiReadyQueueRotatorMain_eiBody_main

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tiReadyQueueRotatorMain_N_CELL; (i)++ ){ \
       (p_cb) = &tiReadyQueueRotatorMain_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tiReadyQueueRotatorMain_TECSGENH */
