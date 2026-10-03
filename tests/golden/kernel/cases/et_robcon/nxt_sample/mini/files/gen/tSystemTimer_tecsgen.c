/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tSystemTimer_tecsgen.h"
#include "tSystemTimer_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eInterruptBody */
struct tag_tSystemTimer_eInterruptBody_DES {
    const struct tag_sHandlerBody_VMT *vmt;
    int           idx;
};

/* eStartupHookBody */
struct tag_tSystemTimer_eStartupHookBody_DES {
    const struct tag_sHookBody_VMT *vmt;
    int           idx;
};

/* eShutdownHookBody */
struct tag_tSystemTimer_eShutdownHookBody_DES {
    const struct tag_sStatusTypeHookBody_VMT *vmt;
    int           idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eInterruptBody */
void           tSystemTimer_eInterruptBody_main_skel( const struct tag_sHandlerBody_VDES *epd)
{
    tSystemTimer_eInterruptBody_main( );
}
/* eStartupHookBody */
void           tSystemTimer_eStartupHookBody_main_skel( const struct tag_sHookBody_VDES *epd)
{
    tSystemTimer_eStartupHookBody_main( );
}
/* eShutdownHookBody */
void           tSystemTimer_eShutdownHookBody_main_skel( const struct tag_sStatusTypeHookBody_VDES *epd, StatusType ercd)
{
    tSystemTimer_eShutdownHookBody_main( ercd );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eInterruptBody */
const struct tag_sHandlerBody_VMT tSystemTimer_eInterruptBody_MT_ = {
    tSystemTimer_eInterruptBody_main_skel,
};
/* eStartupHookBody */
const struct tag_sHookBody_VMT tSystemTimer_eStartupHookBody_MT_ = {
    tSystemTimer_eStartupHookBody_main_skel,
};
/* eShutdownHookBody */
const struct tag_sStatusTypeHookBody_VMT tSystemTimer_eShutdownHookBody_MT_ = {
    tSystemTimer_eShutdownHookBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* 受け口ディスクリプタ #_EPD_# */
extern const struct tag_tSystemTimer_eInterruptBody_DES SystemTimer_eInterruptBody_des;
const struct tag_tSystemTimer_eInterruptBody_DES SystemTimer_eInterruptBody_des = {
    &tSystemTimer_eInterruptBody_MT_,
    0,
};
extern const struct tag_tSystemTimer_eStartupHookBody_DES SystemTimer_eStartupHookBody_des;
const struct tag_tSystemTimer_eStartupHookBody_DES SystemTimer_eStartupHookBody_des = {
    &tSystemTimer_eStartupHookBody_MT_,
    0,
};
extern const struct tag_tSystemTimer_eShutdownHookBody_DES SystemTimer_eShutdownHookBody_des;
const struct tag_tSystemTimer_eShutdownHookBody_DES SystemTimer_eShutdownHookBody_des = {
    &tSystemTimer_eShutdownHookBody_MT_,
    0,
};
/* CB 初期化コード #_CIC_# */
void
tSystemTimer_CB_initialize()
{
    SET_CB_INIB_POINTER(i,p_cb)
    INITIALIZE_CB()
}
