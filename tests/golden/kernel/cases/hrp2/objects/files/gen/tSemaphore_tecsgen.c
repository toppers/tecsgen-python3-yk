/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tSemaphore_tecsgen.h"
#include "tSemaphore_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eSignalSemaphore : omitted by entry port optimize */

/* eWaitSemaphore : omitted by entry port optimize */

/* eManageSemaphore : omitted by entry port optimize */

/* eReferSemaphore : omitted by entry port optimize */

/* eiSemaphore : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eSignalSemaphore : omitted by entry port optimize */
/* eWaitSemaphore : omitted by entry port optimize */
/* eManageSemaphore : omitted by entry port optimize */
/* eReferSemaphore : omitted by entry port optimize */
/* eiSemaphore : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eSignalSemaphore : omitted by entry port optimize */
/* eWaitSemaphore : omitted by entry port optimize */
/* eManageSemaphore : omitted by entry port optimize */
/* eReferSemaphore : omitted by entry port optimize */
/* eiSemaphore : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: SemaphoreO_CB:  SemaphoreO id=3 */
const tSemaphore_INIB SemaphoreO_INIB = {
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    SEMID_tSemaphore_SemaphoreO,             /* id */
};

/* 受け口ディスクリプタ #_EPD_# */
/* eSignalSemaphore : omitted by entry port optimize */
/* eWaitSemaphore : omitted by entry port optimize */
/* eManageSemaphore : omitted by entry port optimize */
/* eReferSemaphore : omitted by entry port optimize */
/* eiSemaphore : omitted by entry port optimize */
/* ID to INIB table #_INTAB_# */
    extern tSemaphore_INIB  rKernel_SemaphoreK_INIB;
    extern tSemaphore_INIB  rUser_SemaphoreU_INIB;
tSemaphore_INIB *const tSemaphore_INIB_ptab[] ={
    &rKernel_SemaphoreK_INIB,
    &rUser_SemaphoreU_INIB,
    &SemaphoreO_INIB,
};
/* CB 初期化コード #_CIC_# */
void
tSemaphore_CB_initialize()
{
    tSemaphore_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
