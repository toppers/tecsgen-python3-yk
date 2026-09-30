/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tCyclicTaskActivator_tecsgen.h"
#include "tCyclicTaskActivator_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eiBody */
struct tag_tCyclicTaskActivator_eiBody_DES {
    const struct tag_siHandlerBody_VMT *vmt;
    int           idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eiBody */
void           tCyclicTaskActivator_eiBody_main_skel( const struct tag_siHandlerBody_VDES *epd)
{
    struct tag_tCyclicTaskActivator_eiBody_DES *lepd
        = (struct tag_tCyclicTaskActivator_eiBody_DES *)epd;
    tCyclicTaskActivator_eiBody_main( lepd->idx );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eiBody */
const struct tag_siHandlerBody_VMT tCyclicTaskActivator_eiBody_MT_ = {
    tCyclicTaskActivator_eiBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
extern const struct tag_siHandlerBody_VMT tCyclicTaskActivator_eiBody_MT_;
/* 受け口ディスクリプタ #_EPD_# */
extern const struct tag_tCyclicTaskActivator_eiBody_DES rDomainEV3_CyclicMain3_eiBody_des;
const struct tag_tCyclicTaskActivator_eiBody_DES rDomainEV3_CyclicMain3_eiBody_des = {
    &tCyclicTaskActivator_eiBody_MT_,
    0,
};
/* CB 初期化コード #_CIC_# */
void
tCyclicTaskActivator_CB_initialize()
{
    tCyclicTaskActivator_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
