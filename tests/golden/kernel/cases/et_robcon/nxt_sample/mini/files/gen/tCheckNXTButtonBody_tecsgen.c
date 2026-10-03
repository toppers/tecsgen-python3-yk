/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tCheckNXTButtonBody_tecsgen.h"
#include "tCheckNXTButtonBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eiBody */
struct tag_tCheckNXTButtonBody_eiBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    int           idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eiBody */
void           tCheckNXTButtonBody_eiBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tCheckNXTButtonBody_eiBody_main( );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eiBody */
const struct tag_sHandlerBody_VMT tCheckNXTButtonBody_eiBody_MT_ = {
    tCheckNXTButtonBody_eiBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* 受け口ディスクリプタ #_EPD_# */
extern const struct tag_tCheckNXTButtonBody_eiBody_DES CheckNXTButtonBody_eiBody_des;
const struct tag_tCheckNXTButtonBody_eiBody_DES CheckNXTButtonBody_eiBody_des = {
    &tCheckNXTButtonBody_eiBody_MT_,
    0,
};
/* CB 初期化コード #_CIC_# */
void
tCheckNXTButtonBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
