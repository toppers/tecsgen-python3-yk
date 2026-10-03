/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tSampleTaskBody_TECSGEN_H
#define tSampleTaskBody_TECSGEN_H

/*
 * celltype          :  tSampleTaskBody
 * global name       :  tSampleTaskBody
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  yes
 * has_CB            :  yes
 * has_INIB          :  no
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sKernelTask_tecsgen.h"
#include "sDisplay_tecsgen.h"
#include "sBattery_tecsgen.h"
#include "sTaskBody_tecsgen.h"
#include "sTask_tecsgen.h"
#include "sSample_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル CB 型宣言 #_CCTPA_# */
typedef struct tag_tSampleTaskBody_CB {
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* var #_VA_# */ 
    int32_t        counter;
}  tSampleTaskBody_CB;
/* シングルトンセル CB プロトタイプ宣言 #_SCP_# */
extern  tSampleTaskBody_CB  tSampleTaskBody_SINGLE_CELL_CB;


/* セルタイプのIDX型 #_CTIX_# */
typedef struct tag_tSampleTaskBody_CB *tSampleTaskBody_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sTaskBody */
void         tSampleTaskBody_eMainTaskBody_main();
/* sSample */
void         tSampleTaskBody_eSample_countUp();
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tSampleTaskBody_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tKernel_tecsgen.h"
#include "tDisplayBody_tecsgen.h"
#include "tBattery_tecsgen.h"
#include "tTask_tecsgen.h"
#ifdef  tSampleTaskBody_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tSampleTaskBody_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ #_GCB_# */
#define tSampleTaskBody_GET_CELLCB(idx) ((void *)0)



/* var アクセスマクロ #_VAM_# */
#define tSampleTaskBody_VAR_counter	(tSampleTaskBody_SINGLE_CELL_CB.counter)

#define tSampleTaskBody_GET_counter()	(tSampleTaskBody_SINGLE_CELL_CB.counter)
#define tSampleTaskBody_SET_counter(val)	(tSampleTaskBody_SINGLE_CELL_CB.counter=(val))

#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_schedule( ) \
	  tKernel_eKernelTask_schedule( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_enableAllInterrupts( ) \
	  tKernel_eKernelTask_enableAllInterrupts( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_disableAllInterrupts( ) \
	  tKernel_eKernelTask_disableAllInterrupts( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_resumeAllInterrupts( ) \
	  tKernel_eKernelTask_resumeAllInterrupts( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_suspendAllInterrupts( ) \
	  tKernel_eKernelTask_suspendAllInterrupts( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_resumeOsInterrupts( ) \
	  tKernel_eKernelTask_resumeOsInterrupts( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_suspendOsinterrupts( ) \
	  tKernel_eKernelTask_suspendOsinterrupts( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_getActiveApplicationMode( ) \
	  tKernel_eKernelTask_getActiveApplicationMode( \
	    )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_shutdownOs( ercd ) \
	  tKernel_eKernelTask_shutdownOs( \
	    (ercd) )
#define tSampleTaskBody_cDisplay_update( ) \
	  tDisplayBody_eDisplay_update( \
	    )
#define tSampleTaskBody_cDisplay_clear( updateToo ) \
	  tDisplayBody_eDisplay_clear( \
	    (updateToo) )
#define tSampleTaskBody_cDisplay_gotoXY( x, y ) \
	  tDisplayBody_eDisplay_gotoXY( \
	    (x), (y) )
#define tSampleTaskBody_cDisplay_putChar( c ) \
	  tDisplayBody_eDisplay_putChar( \
	    (c) )
#define tSampleTaskBody_cDisplay_putString( string ) \
	  tDisplayBody_eDisplay_putString( \
	    (string) )
#define tSampleTaskBody_cDisplay_putInt( val, places ) \
	  tDisplayBody_eDisplay_putInt( \
	    (val), (places) )
#define tSampleTaskBody_cDisplay_putUnsigned( val, places ) \
	  tDisplayBody_eDisplay_putUnsigned( \
	    (val), (places) )
#define tSampleTaskBody_cDisplay_putHex( val, places ) \
	  tDisplayBody_eDisplay_putHex( \
	    (val), (places) )
#define tSampleTaskBody_cDisplay_getBuffer( ) \
	  tDisplayBody_eDisplay_getBuffer( \
	    )
#define tSampleTaskBody_cDisplay_powerOff( updateToo ) \
	  tDisplayBody_eDisplay_powerOff( \
	    (updateToo) )
#define tSampleTaskBody_cBattery_getBatteryVoltage( ) \
	  tBattery_eBattery_getBatteryVoltage( \
	    )
#define tSampleTaskBody_cTask_activate( ) \
	  tTask_eTask_activate( \
	   &tTask_INIB_tab[0] )
#define tSampleTaskBody_cTask_terminate( ) \
	  tTask_eTask_terminate( \
	   &tTask_INIB_tab[0] )
#define tSampleTaskBody_cTask_chain( ) \
	  tTask_eTask_chain( \
	   &tTask_INIB_tab[0] )
#define tSampleTaskBody_cTask_getId( p_tskid ) \
	  tTask_eTask_getId( \
	   &tTask_INIB_tab[0], (p_tskid) )
#define tSampleTaskBody_cTask_getState( p_state ) \
	  tTask_eTask_getState( \
	   &tTask_INIB_tab[0], (p_state) )

#else  /* TECSFLOW */
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_schedule( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.schedule__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_enableAllInterrupts( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.enableAllInterrupts__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_disableAllInterrupts( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.disableAllInterrupts__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_resumeAllInterrupts( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.resumeAllInterrupts__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_suspendAllInterrupts( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.suspendAllInterrupts__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_resumeOsInterrupts( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.resumeOsInterrupts__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_suspendOsinterrupts( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.suspendOsinterrupts__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_getActiveApplicationMode( ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.getActiveApplicationMode__T( \
 )
#define tSampleTaskBody__require_call_port_tKernel_eKernelTask_shutdownOs( ercd ) \
	  (p_that)->_require_call_port_tKernel_eKernelTask.shutdownOs__T( \
 (ercd) )
#define tSampleTaskBody_cDisplay_update( ) \
	  (p_that)->cDisplay.update__T( \
 )
#define tSampleTaskBody_cDisplay_clear( updateToo ) \
	  (p_that)->cDisplay.clear__T( \
 (updateToo) )
#define tSampleTaskBody_cDisplay_gotoXY( x, y ) \
	  (p_that)->cDisplay.gotoXY__T( \
 (x), (y) )
#define tSampleTaskBody_cDisplay_putChar( c ) \
	  (p_that)->cDisplay.putChar__T( \
 (c) )
#define tSampleTaskBody_cDisplay_putString( string ) \
	  (p_that)->cDisplay.putString__T( \
 (string) )
#define tSampleTaskBody_cDisplay_putInt( val, places ) \
	  (p_that)->cDisplay.putInt__T( \
 (val), (places) )
#define tSampleTaskBody_cDisplay_putUnsigned( val, places ) \
	  (p_that)->cDisplay.putUnsigned__T( \
 (val), (places) )
#define tSampleTaskBody_cDisplay_putHex( val, places ) \
	  (p_that)->cDisplay.putHex__T( \
 (val), (places) )
#define tSampleTaskBody_cDisplay_getBuffer( ) \
	  (p_that)->cDisplay.getBuffer__T( \
 )
#define tSampleTaskBody_cDisplay_powerOff( updateToo ) \
	  (p_that)->cDisplay.powerOff__T( \
 (updateToo) )
#define tSampleTaskBody_cBattery_getBatteryVoltage( ) \
	  (p_that)->cBattery.getBatteryVoltage__T( \
 )
#define tSampleTaskBody_cTask_activate( ) \
	  (p_that)->cTask.activate__T( \
 )
#define tSampleTaskBody_cTask_terminate( ) \
	  (p_that)->cTask.terminate__T( \
 )
#define tSampleTaskBody_cTask_chain( ) \
	  (p_that)->cTask.chain__T( \
 )
#define tSampleTaskBody_cTask_getId( p_tskid ) \
	  (p_that)->cTask.getId__T( \
 (p_tskid) )
#define tSampleTaskBody_cTask_getState( p_state ) \
	  (p_that)->cTask.getState__T( \
 (p_state) )

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


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tSampleTaskBody_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tSampleTaskBody_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tSampleTaskBody_IDX



/* var アクセスマクロ(短縮形) #_VAMA_# */
#define VAR_counter          tSampleTaskBody_VAR_counter

/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define schedule( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_schedule( )
#define enableAllInterrupts( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_enableAllInterrupts( )
#define disableAllInterrupts( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_disableAllInterrupts( )
#define resumeAllInterrupts( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_resumeAllInterrupts( )
#define suspendAllInterrupts( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_suspendAllInterrupts( )
#define resumeOsInterrupts( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_resumeOsInterrupts( )
#define suspendOsinterrupts( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_suspendOsinterrupts( )
#define getActiveApplicationMode( ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_getActiveApplicationMode( )
#define shutdownOs( ercd ) \
          tSampleTaskBody__require_call_port_tKernel_eKernelTask_shutdownOs( ercd )
#define cDisplay_update( ) \
          tSampleTaskBody_cDisplay_update( )
#define cDisplay_clear( updateToo ) \
          tSampleTaskBody_cDisplay_clear( updateToo )
#define cDisplay_gotoXY( x, y ) \
          tSampleTaskBody_cDisplay_gotoXY( x, y )
#define cDisplay_putChar( c ) \
          tSampleTaskBody_cDisplay_putChar( c )
#define cDisplay_putString( string ) \
          tSampleTaskBody_cDisplay_putString( string )
#define cDisplay_putInt( val, places ) \
          tSampleTaskBody_cDisplay_putInt( val, places )
#define cDisplay_putUnsigned( val, places ) \
          tSampleTaskBody_cDisplay_putUnsigned( val, places )
#define cDisplay_putHex( val, places ) \
          tSampleTaskBody_cDisplay_putHex( val, places )
#define cDisplay_getBuffer( ) \
          tSampleTaskBody_cDisplay_getBuffer( )
#define cDisplay_powerOff( updateToo ) \
          tSampleTaskBody_cDisplay_powerOff( updateToo )
#define cBattery_getBatteryVoltage( ) \
          tSampleTaskBody_cBattery_getBatteryVoltage( )
#define cTask_activate( ) \
          tSampleTaskBody_cTask_activate( )
#define cTask_terminate( ) \
          tSampleTaskBody_cTask_terminate( )
#define cTask_chain( ) \
          tSampleTaskBody_cTask_chain( )
#define cTask_getId( p_tskid ) \
          tSampleTaskBody_cTask_getId( p_tskid )
#define cTask_getState( p_state ) \
          tSampleTaskBody_cTask_getState( p_state )




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eMainTaskBody_main tSampleTaskBody_eMainTaskBody_main
#define eSample_countUp  tSampleTaskBody_eSample_countUp

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB()\
	tSampleTaskBody_SINGLE_CELL_CB.counter = 0;
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tSampleTaskBody_TECSGENH */
