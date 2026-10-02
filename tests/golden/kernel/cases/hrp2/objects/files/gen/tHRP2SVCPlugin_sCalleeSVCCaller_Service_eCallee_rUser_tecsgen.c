/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_tecsgen.h"
#include "tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eThroughEntry : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eThroughEntry : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eThroughEntry : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* 受け口ディスクリプタ #_EPD_# */
/* eThroughEntry : omitted by entry port optimize */
/* CB 初期化コード #_CIC_# */
void
tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_CB_initialize()
{
    tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
