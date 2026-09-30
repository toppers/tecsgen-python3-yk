/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tiReadyQueueRotatorMain_tecsgen.h"
#include "tiReadyQueueRotatorMain_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eiBody */
struct tag_tiReadyQueueRotatorMain_eiBody_DES {
    const struct tag_siHandlerBody_VMT *vmt;
    tiReadyQueueRotatorMain_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eiBody */
void           tiReadyQueueRotatorMain_eiBody_main_skel( const struct tag_siHandlerBody_VDES *epd)
{
    struct tag_tiReadyQueueRotatorMain_eiBody_DES *lepd
        = (struct tag_tiReadyQueueRotatorMain_eiBody_DES *)epd;
    tiReadyQueueRotatorMain_eiBody_main( lepd->idx );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eiBody */
const struct tag_siHandlerBody_VMT tiReadyQueueRotatorMain_eiBody_MT_ = {
    tiReadyQueueRotatorMain_eiBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
tiReadyQueueRotatorMain_INIB tiReadyQueueRotatorMain_INIB_tab[] = {
    /* cell: tiReadyQueueRotatorMain_CB_tab[0]:  ReadyQueueRotator_ReadyQueueRotatorMain id=1 */
    {
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        EV3_MRUBY_VM_PRIORITY,                   /* priority */
    },
};

extern const struct tag_siHandlerBody_VMT tiReadyQueueRotatorMain_eiBody_MT_;
/* 受け口ディスクリプタ #_EPD_# */
extern const struct tag_tiReadyQueueRotatorMain_eiBody_DES rDomainEV3_ReadyQueueRotator_ReadyQueueRotatorMain_eiBody_des;
const struct tag_tiReadyQueueRotatorMain_eiBody_DES rDomainEV3_ReadyQueueRotator_ReadyQueueRotatorMain_eiBody_des = {
    &tiReadyQueueRotatorMain_eiBody_MT_,
    &tiReadyQueueRotatorMain_INIB_tab[0],      /* INIB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tiReadyQueueRotatorMain_CB_initialize()
{
    tiReadyQueueRotatorMain_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
