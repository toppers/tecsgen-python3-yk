/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tButtonBody_tecsgen.h"
#include "tButtonBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eButton : omitted by entry port optimize */

/* eiBody */
struct tag_tButtonBody_eiBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    tButtonBody_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eButton : omitted by entry port optimize */
/* eiBody */
void           tButtonBody_eiBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tButtonBody_eiBody_main( );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eButton : omitted by entry port optimize */
/* eiBody */
const struct tag_sHandlerBody_VMT tButtonBody_eiBody_MT_ = {
    tButtonBody_eiBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
tButtonBody_INIB tButtonBody_SINGLE_CELL_INIB = 
{
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    20,                                      /* threshold */
};

/* セル CB #_CB_# */
struct tag_tButtonBody_CB tButtonBody_SINGLE_CELL_CB;
/* 受け口ディスクリプタ #_EPD_# */
/* eButton : omitted by entry port optimize */
extern const struct tag_tButtonBody_eiBody_DES Button_ButtonBody_eiBody_des;
const struct tag_tButtonBody_eiBody_DES Button_ButtonBody_eiBody_des = {
    &tButtonBody_eiBody_MT_,
    &tButtonBody_SINGLE_CELL_CB,      /* CB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tButtonBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
