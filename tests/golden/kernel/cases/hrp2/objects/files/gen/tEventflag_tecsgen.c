/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tEventflag_tecsgen.h"
#include "tEventflag_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eSetEventflag : omitted by entry port optimize */

/* eWaitEventflag : omitted by entry port optimize */

/* eManageEventflag : omitted by entry port optimize */

/* eReferEventflag : omitted by entry port optimize */

/* eiEventflag : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eSetEventflag : omitted by entry port optimize */
/* eWaitEventflag : omitted by entry port optimize */
/* eManageEventflag : omitted by entry port optimize */
/* eReferEventflag : omitted by entry port optimize */
/* eiEventflag : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eSetEventflag : omitted by entry port optimize */
/* eWaitEventflag : omitted by entry port optimize */
/* eManageEventflag : omitted by entry port optimize */
/* eReferEventflag : omitted by entry port optimize */
/* eiEventflag : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: EventflagO_CB:  EventflagO id=3 */
const tEventflag_INIB EventflagO_INIB = {
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    FLGID_tEventflag_EventflagO,             /* id */
};

/* 受け口ディスクリプタ #_EPD_# */
/* eSetEventflag : omitted by entry port optimize */
/* eWaitEventflag : omitted by entry port optimize */
/* eManageEventflag : omitted by entry port optimize */
/* eReferEventflag : omitted by entry port optimize */
/* eiEventflag : omitted by entry port optimize */
/* ID to INIB table #_INTAB_# */
    extern tEventflag_INIB  rKernel_EventflagK_INIB;
    extern tEventflag_INIB  rUser_EventflagU_INIB;
tEventflag_INIB *const tEventflag_INIB_ptab[] ={
    &rKernel_EventflagK_INIB,
    &rUser_EventflagU_INIB,
    &EventflagO_INIB,
};
/* CB 初期化コード #_CIC_# */
void
tEventflag_CB_initialize()
{
    tEventflag_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
