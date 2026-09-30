/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "nMruby_tsCyclic_tecsgen.h"
#include "nMruby_tsCyclic_factory.h"


/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */
extern struct tag_sCyclic_VDES rDomainEV3_TaskCyclicWakeupper_CyclicHandler_eCyclic_des;

extern struct tag_sCyclic_VDES rDomainEV3_CyclicHandler_eCyclic_des;

/* 呼び口配列 #_CPA_# */


/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: rDomainEV3_TaskCyclicWakeuppereCyclicBridge_CB:  TaskCyclicWakeuppereCyclicBridge id=1 */
const nMruby_tsCyclic_INIB rDomainEV3_TaskCyclicWakeuppereCyclicBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tCyclicHandler_INIB_tab[2],             /* cTECS #_CCP2_# */
};

/* cell: rDomainEV3_CyclicHandlereCyclicBridge_CB:  CyclicHandlereCyclicBridge id=2 */
const nMruby_tsCyclic_INIB rDomainEV3_CyclicHandlereCyclicBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tCyclicHandler_INIB_tab[0],             /* cTECS #_CCP2_# */
};

/* 受け口ディスクリプタ #_EPD_# */
/* ID to INIB table #_INTAB_# */
    extern nMruby_tsCyclic_INIB  rDomainEV3_TaskCyclicWakeuppereCyclicBridge_INIB;
    extern nMruby_tsCyclic_INIB  rDomainEV3_CyclicHandlereCyclicBridge_INIB;
nMruby_tsCyclic_INIB *const nMruby_tsCyclic_INIB_ptab[] ={
    &rDomainEV3_TaskCyclicWakeuppereCyclicBridge_INIB,
    &rDomainEV3_CyclicHandlereCyclicBridge_INIB,
};
/* CB 初期化コード #_CIC_# */
void
nMruby_tsCyclic_CB_initialize()
{
    nMruby_tsCyclic_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
