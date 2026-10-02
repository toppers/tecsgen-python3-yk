/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tPriorityDataqueue_tecsgen.h"
#include "tPriorityDataqueue_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eSendPriorityDataqueue : omitted by entry port optimize */

/* eReceivePriorityDataqueue : omitted by entry port optimize */

/* eManagePriorityDataqueue : omitted by entry port optimize */

/* eReferPriorityDataqueue : omitted by entry port optimize */

/* eiPriorityDataqueue : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eSendPriorityDataqueue : omitted by entry port optimize */
/* eReceivePriorityDataqueue : omitted by entry port optimize */
/* eManagePriorityDataqueue : omitted by entry port optimize */
/* eReferPriorityDataqueue : omitted by entry port optimize */
/* eiPriorityDataqueue : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eSendPriorityDataqueue : omitted by entry port optimize */
/* eReceivePriorityDataqueue : omitted by entry port optimize */
/* eManagePriorityDataqueue : omitted by entry port optimize */
/* eReferPriorityDataqueue : omitted by entry port optimize */
/* eiPriorityDataqueue : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: PriorityDataqueueO_CB:  PriorityDataqueueO id=3 */
const tPriorityDataqueue_INIB PriorityDataqueueO_INIB = {
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    PDTQID_tPriorityDataqueue_PriorityDataqueueO, /* id */
};

/* 受け口ディスクリプタ #_EPD_# */
/* eSendPriorityDataqueue : omitted by entry port optimize */
/* eReceivePriorityDataqueue : omitted by entry port optimize */
/* eManagePriorityDataqueue : omitted by entry port optimize */
/* eReferPriorityDataqueue : omitted by entry port optimize */
/* eiPriorityDataqueue : omitted by entry port optimize */
/* ID to INIB table #_INTAB_# */
    extern tPriorityDataqueue_INIB  rKernel_PriorityDataqueueK_INIB;
    extern tPriorityDataqueue_INIB  rUser_PriorityDataqueueU_INIB;
tPriorityDataqueue_INIB *const tPriorityDataqueue_INIB_ptab[] ={
    &rKernel_PriorityDataqueueK_INIB,
    &rUser_PriorityDataqueueU_INIB,
    &PriorityDataqueueO_INIB,
};
/* CB 初期化コード #_CIC_# */
void
tPriorityDataqueue_CB_initialize()
{
    tPriorityDataqueue_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
