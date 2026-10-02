/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tEventflag_tecsgen.h"
#include "tEventflag_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eEventflag : omitted by entry port optimize */

/* eiEventflag : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eEventflag : omitted by entry port optimize */
/* eiEventflag : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eEventflag : omitted by entry port optimize */
/* eiEventflag : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
tEventflag_INIB tEventflag_INIB_tab[] = {
    /* cell: tEventflag_CB_tab[0]:  Join_domain_to_through__0_Channel_Eventflag id=1 */
    {
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        FLGID_tEventflag_Join_domain_to_through__0_Channel_Eventflag, /* id */
    },
};

/* 受け口ディスクリプタ #_EPD_# */
/* eEventflag : omitted by entry port optimize */
/* eiEventflag : omitted by entry port optimize */
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
