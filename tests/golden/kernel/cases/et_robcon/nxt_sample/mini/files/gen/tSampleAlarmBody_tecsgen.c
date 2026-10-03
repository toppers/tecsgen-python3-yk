/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tSampleAlarmBody_tecsgen.h"
#include "tSampleAlarmBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eBody */
struct tag_tSampleAlarmBody_eBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    int           idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eBody */
void           tSampleAlarmBody_eBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tSampleAlarmBody_eBody_main( );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eBody */
const struct tag_sHandlerBody_VMT tSampleAlarmBody_eBody_MT_ = {
    tSampleAlarmBody_eBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* 受け口ディスクリプタ #_EPD_# */
extern const struct tag_tSampleAlarmBody_eBody_DES SampleAlarmBody_eBody_des;
const struct tag_tSampleAlarmBody_eBody_DES SampleAlarmBody_eBody_des = {
    &tSampleAlarmBody_eBody_MT_,
    0,
};
/* CB 初期化コード #_CIC_# */
void
tSampleAlarmBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
