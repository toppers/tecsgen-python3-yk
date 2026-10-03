/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tDisplayBody_tecsgen.h"
#include "tDisplayBody_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eDisplay : omitted by entry port optimize */

/* eInitialize */
struct tag_tDisplayBody_eInitialize_DES {
    const struct tag_sHookBody_VMT *vmt;
    tDisplayBody_IDX  idx;
};

/* eTerminate */
struct tag_tDisplayBody_eTerminate_DES {
    const struct tag_sStatusTypeHookBody_VMT *vmt;
    tDisplayBody_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eDisplay : omitted by entry port optimize */
/* eInitialize */
void           tDisplayBody_eInitialize_main_skel( const struct tag_sHookBody_VDES *epd)
{
    tDisplayBody_eInitialize_main( );
}
/* eTerminate */
void           tDisplayBody_eTerminate_main_skel( const struct tag_sStatusTypeHookBody_VDES *epd, StatusType ercd)
{
    tDisplayBody_eTerminate_main( ercd );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eDisplay : omitted by entry port optimize */
/* eInitialize */
const struct tag_sHookBody_VMT tDisplayBody_eInitialize_MT_ = {
    tDisplayBody_eInitialize_main_skel,
};
/* eTerminate */
const struct tag_sStatusTypeHookBody_VMT tDisplayBody_eTerminate_MT_ = {
    tDisplayBody_eTerminate_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
uint8_t tDisplayBody_SINGLE_CELL_CB_buffer_INIT[900];
/* セル INIB #_INIB_# */
tDisplayBody_INIB tDisplayBody_SINGLE_CELL_INIB = 
{
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    100,                                     /* width */
    8,                                       /* depth */
    6,                                       /* cellWidth */
    16,                                      /* charWidth */
    8,                                       /* charDepth */
    tDisplayBody_SINGLE_CELL_CB_buffer_INIT, /* buffer */
};

/* セル CB #_CB_# */
struct tag_tDisplayBody_CB tDisplayBody_SINGLE_CELL_CB;
/* 受け口ディスクリプタ #_EPD_# */
/* eDisplay : omitted by entry port optimize */
extern const struct tag_tDisplayBody_eInitialize_DES Display_DisplayBody_eInitialize_des;
const struct tag_tDisplayBody_eInitialize_DES Display_DisplayBody_eInitialize_des = {
    &tDisplayBody_eInitialize_MT_,
    &tDisplayBody_SINGLE_CELL_CB,      /* CB 3 */
};
extern const struct tag_tDisplayBody_eTerminate_DES Display_DisplayBody_eTerminate_des;
const struct tag_tDisplayBody_eTerminate_DES Display_DisplayBody_eTerminate_des = {
    &tDisplayBody_eTerminate_MT_,
    &tDisplayBody_SINGLE_CELL_CB,      /* CB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tDisplayBody_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
