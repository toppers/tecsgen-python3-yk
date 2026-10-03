/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tAVRBody_tecsgen.h"
#include "tAVRBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eAvrMotor : omitted by entry port optimize */

/* eAvrSensor : omitted by entry port optimize */

/* eAvrButton : omitted by entry port optimize */

/* eAvrBattery : omitted by entry port optimize */

/* eAvrPower : omitted by entry port optimize */

/* eInitialize */
struct tag_tAVRBody_eInitialize_DES {
    const struct tag_sHookBody_VMT *vmt;
    tAVRBody_IDX  idx;
};

/* eTerminate */
struct tag_tAVRBody_eTerminate_DES {
    const struct tag_sStatusTypeHookBody_VMT *vmt;
    tAVRBody_IDX  idx;
};

/* eiCyclicBody */
struct tag_tAVRBody_eiCyclicBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    tAVRBody_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eAvrMotor : omitted by entry port optimize */
/* eAvrSensor : omitted by entry port optimize */
/* eAvrButton : omitted by entry port optimize */
/* eAvrBattery : omitted by entry port optimize */
/* eAvrPower : omitted by entry port optimize */
/* eInitialize */
void           tAVRBody_eInitialize_main_skel( const struct tag_sHookBody_VDES *epd)
{
    tAVRBody_eInitialize_main( );
}
/* eTerminate */
void           tAVRBody_eTerminate_main_skel( const struct tag_sStatusTypeHookBody_VDES *epd, StatusType ercd)
{
    tAVRBody_eTerminate_main( ercd );
}
/* eiCyclicBody */
void           tAVRBody_eiCyclicBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tAVRBody_eiCyclicBody_main( );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eAvrMotor : omitted by entry port optimize */
/* eAvrSensor : omitted by entry port optimize */
/* eAvrButton : omitted by entry port optimize */
/* eAvrBattery : omitted by entry port optimize */
/* eAvrPower : omitted by entry port optimize */
/* eInitialize */
const struct tag_sHookBody_VMT tAVRBody_eInitialize_MT_ = {
    tAVRBody_eInitialize_main_skel,
};
/* eTerminate */
const struct tag_sStatusTypeHookBody_VMT tAVRBody_eTerminate_MT_ = {
    tAVRBody_eTerminate_main_skel,
};
/* eiCyclicBody */
const struct tag_sHandlerBody_VMT tAVRBody_eiCyclicBody_MT_ = {
    tAVRBody_eiCyclicBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
uint8_t tAVRBody_SINGLE_CELL_CB_dataFromAvr_INIT[13];
uint8_t tAVRBody_SINGLE_CELL_CB_dataToAvr_INIT[9];
/* セル INIB #_INIB_# */
tAVRBody_INIB tAVRBody_SINGLE_CELL_INIB = 
{
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    tAVRBody_SINGLE_CELL_CB_dataFromAvr_INIT, /* dataFromAvr */
    tAVRBody_SINGLE_CELL_CB_dataToAvr_INIT,  /* dataToAvr */
};

/* セル CB #_CB_# */
struct tag_tAVRBody_CB tAVRBody_SINGLE_CELL_CB;
/* 受け口ディスクリプタ #_EPD_# */
/* eAvrMotor : omitted by entry port optimize */
/* eAvrSensor : omitted by entry port optimize */
/* eAvrButton : omitted by entry port optimize */
/* eAvrBattery : omitted by entry port optimize */
/* eAvrPower : omitted by entry port optimize */
extern const struct tag_tAVRBody_eInitialize_DES AVR_AVRBody_eInitialize_des;
const struct tag_tAVRBody_eInitialize_DES AVR_AVRBody_eInitialize_des = {
    &tAVRBody_eInitialize_MT_,
    &tAVRBody_SINGLE_CELL_CB,      /* CB 3 */
};
extern const struct tag_tAVRBody_eTerminate_DES AVR_AVRBody_eTerminate_des;
const struct tag_tAVRBody_eTerminate_DES AVR_AVRBody_eTerminate_des = {
    &tAVRBody_eTerminate_MT_,
    &tAVRBody_SINGLE_CELL_CB,      /* CB 3 */
};
extern const struct tag_tAVRBody_eiCyclicBody_DES AVR_AVRBody_eiCyclicBody_des;
const struct tag_tAVRBody_eiCyclicBody_DES AVR_AVRBody_eiCyclicBody_des = {
    &tAVRBody_eiCyclicBody_MT_,
    &tAVRBody_SINGLE_CELL_CB,      /* CB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tAVRBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
