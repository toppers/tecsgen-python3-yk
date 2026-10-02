/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tDataqueue_tecsgen.h"
#include "tDataqueue_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eSendDataqueue : omitted by entry port optimize */

/* eReceiveDataqueue : omitted by entry port optimize */

/* eManageDataqueue : omitted by entry port optimize */

/* eReferDataqueue : omitted by entry port optimize */

/* eiDataqueue : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eSendDataqueue : omitted by entry port optimize */
/* eReceiveDataqueue : omitted by entry port optimize */
/* eManageDataqueue : omitted by entry port optimize */
/* eReferDataqueue : omitted by entry port optimize */
/* eiDataqueue : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eSendDataqueue : omitted by entry port optimize */
/* eReceiveDataqueue : omitted by entry port optimize */
/* eManageDataqueue : omitted by entry port optimize */
/* eReferDataqueue : omitted by entry port optimize */
/* eiDataqueue : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: DataqueueO_CB:  DataqueueO id=3 */
const tDataqueue_INIB DataqueueO_INIB = {
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    DTQID_tDataqueue_DataqueueO,             /* id */
};

/* 受け口ディスクリプタ #_EPD_# */
/* eSendDataqueue : omitted by entry port optimize */
/* eReceiveDataqueue : omitted by entry port optimize */
/* eManageDataqueue : omitted by entry port optimize */
/* eReferDataqueue : omitted by entry port optimize */
/* eiDataqueue : omitted by entry port optimize */
/* ID to INIB table #_INTAB_# */
    extern tDataqueue_INIB  rKernel_DataqueueK_INIB;
    extern tDataqueue_INIB  rUser_DataqueueU_INIB;
tDataqueue_INIB *const tDataqueue_INIB_ptab[] ={
    &rKernel_DataqueueK_INIB,
    &rUser_DataqueueU_INIB,
    &DataqueueO_INIB,
};
/* CB 初期化コード #_CIC_# */
void
tDataqueue_CB_initialize()
{
    tDataqueue_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
