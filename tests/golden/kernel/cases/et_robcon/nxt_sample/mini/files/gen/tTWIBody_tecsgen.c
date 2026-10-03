/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tTWIBody_tecsgen.h"
#include "tTWIBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eTWI : omitted by entry port optimize */

/* eiInterruptBody */
struct tag_tTWIBody_eiInterruptBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    tTWIBody_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eTWI : omitted by entry port optimize */
/* eiInterruptBody */
void           tTWIBody_eiInterruptBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tTWIBody_eiInterruptBody_main( );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eTWI : omitted by entry port optimize */
/* eiInterruptBody */
const struct tag_sHandlerBody_VMT tTWIBody_eiInterruptBody_MT_ = {
    tTWIBody_eiInterruptBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
tTWIBody_INIB tTWIBody_SINGLE_CELL_INIB = 
{
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    (((48000000/400000L)/2)-3),              /* clockDivisor */
};

/* セル CB #_CB_# */
struct tag_tTWIBody_CB tTWIBody_SINGLE_CELL_CB;
/* 受け口ディスクリプタ #_EPD_# */
/* eTWI : omitted by entry port optimize */
extern const struct tag_tTWIBody_eiInterruptBody_DES AVR_TWI_TWIBody_eiInterruptBody_des;
const struct tag_tTWIBody_eiInterruptBody_DES AVR_TWI_TWIBody_eiInterruptBody_des = {
    &tTWIBody_eiInterruptBody_MT_,
    &tTWIBody_SINGLE_CELL_CB,      /* CB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tTWIBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
