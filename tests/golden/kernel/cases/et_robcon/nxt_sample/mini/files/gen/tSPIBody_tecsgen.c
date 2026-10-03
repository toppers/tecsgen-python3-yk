/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tSPIBody_tecsgen.h"
#include "tSPIBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eSPI : omitted by entry port optimize */

/* eiInterruptBody */
struct tag_tSPIBody_eiInterruptBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    tSPIBody_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eSPI : omitted by entry port optimize */
/* eiInterruptBody */
void           tSPIBody_eiInterruptBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tSPIBody_eiInterruptBody_main( );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eSPI : omitted by entry port optimize */
/* eiInterruptBody */
const struct tag_sHandlerBody_VMT tSPIBody_eiInterruptBody_MT_ = {
    tSPIBody_eiInterruptBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル CB #_CB_# */
struct tag_tSPIBody_CB tSPIBody_SINGLE_CELL_CB;
/* 受け口ディスクリプタ #_EPD_# */
/* eSPI : omitted by entry port optimize */
extern const struct tag_tSPIBody_eiInterruptBody_DES Display_SPI_SPIBody_eiInterruptBody_des;
const struct tag_tSPIBody_eiInterruptBody_DES Display_SPI_SPIBody_eiInterruptBody_des = {
    &tSPIBody_eiInterruptBody_MT_,
    &tSPIBody_SINGLE_CELL_CB,      /* CB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tSPIBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
