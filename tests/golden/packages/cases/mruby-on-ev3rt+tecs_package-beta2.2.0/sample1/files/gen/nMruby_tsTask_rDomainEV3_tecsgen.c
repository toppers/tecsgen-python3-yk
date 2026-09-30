/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "nMruby_tsTask_tecsgen.h"
#include "nMruby_tsTask_factory.h"


/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */
extern struct tag_sTask_VDES rDomainEV3_EV3Task_eTask_des;

extern struct tag_sTask_VDES rDomainEV3_MrubyMainTask_eTask_des;

extern struct tag_sTask_VDES rDomainEV3_MrubySubTask1_eTask_des;

extern struct tag_sTask_VDES rDomainEV3_MrubySubTask2_eTask_des;

extern struct tag_sTask_VDES rDomainEV3_MrubyWakeupTask_eTask_des;

extern struct tag_sTask_VDES rDomainEV3_MrubyCyclicTask_eTask_des;

/* 呼び口配列 #_CPA_# */






/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: rDomainEV3_EV3TaskeTaskBridge_CB:  EV3TaskeTaskBridge id=1 */
const nMruby_tsTask_INIB rDomainEV3_EV3TaskeTaskBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tTask_INIB_tab[0],                      /* cTECS #_CCP2_# */
};

/* cell: rDomainEV3_MrubyMainTaskeTaskBridge_CB:  MrubyMainTaskeTaskBridge id=2 */
const nMruby_tsTask_INIB rDomainEV3_MrubyMainTaskeTaskBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tTask_INIB_tab[1],                      /* cTECS #_CCP2_# */
};

/* cell: rDomainEV3_MrubySubTask1eTaskBridge_CB:  MrubySubTask1eTaskBridge id=3 */
const nMruby_tsTask_INIB rDomainEV3_MrubySubTask1eTaskBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tTask_INIB_tab[2],                      /* cTECS #_CCP2_# */
};

/* cell: rDomainEV3_MrubySubTask2eTaskBridge_CB:  MrubySubTask2eTaskBridge id=4 */
const nMruby_tsTask_INIB rDomainEV3_MrubySubTask2eTaskBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tTask_INIB_tab[3],                      /* cTECS #_CCP2_# */
};

/* cell: rDomainEV3_MrubyWakeupTaskeTaskBridge_CB:  MrubyWakeupTaskeTaskBridge id=5 */
const nMruby_tsTask_INIB rDomainEV3_MrubyWakeupTaskeTaskBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tTask_INIB_tab[4],                      /* cTECS #_CCP2_# */
};

/* cell: rDomainEV3_MrubyCyclicTaskeTaskBridge_CB:  MrubyCyclicTaskeTaskBridge id=6 */
const nMruby_tsTask_INIB rDomainEV3_MrubyCyclicTaskeTaskBridge_INIB = {
    /* call port (INIB) #_CP_# */ 
    &tTask_INIB_tab[5],                      /* cTECS #_CCP2_# */
};

/* 受け口ディスクリプタ #_EPD_# */
/* ID to INIB table #_INTAB_# */
    extern nMruby_tsTask_INIB  rDomainEV3_EV3TaskeTaskBridge_INIB;
    extern nMruby_tsTask_INIB  rDomainEV3_MrubyMainTaskeTaskBridge_INIB;
    extern nMruby_tsTask_INIB  rDomainEV3_MrubySubTask1eTaskBridge_INIB;
    extern nMruby_tsTask_INIB  rDomainEV3_MrubySubTask2eTaskBridge_INIB;
    extern nMruby_tsTask_INIB  rDomainEV3_MrubyWakeupTaskeTaskBridge_INIB;
    extern nMruby_tsTask_INIB  rDomainEV3_MrubyCyclicTaskeTaskBridge_INIB;
nMruby_tsTask_INIB *const nMruby_tsTask_INIB_ptab[] ={
    &rDomainEV3_EV3TaskeTaskBridge_INIB,
    &rDomainEV3_MrubyMainTaskeTaskBridge_INIB,
    &rDomainEV3_MrubySubTask1eTaskBridge_INIB,
    &rDomainEV3_MrubySubTask2eTaskBridge_INIB,
    &rDomainEV3_MrubyWakeupTaskeTaskBridge_INIB,
    &rDomainEV3_MrubyCyclicTaskeTaskBridge_INIB,
};
/* CB 初期化コード #_CIC_# */
void
nMruby_tsTask_CB_initialize()
{
    nMruby_tsTask_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
