/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tConfigInterrupt_tecsgen.h"
#include "tConfigInterrupt_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eConfigInterrupt : omitted by entry port optimize */

/* eStarupHookBody */
struct tag_tConfigInterrupt_eStarupHookBody_DES {
    const struct tag_sHookBody_VMT *vmt;
    tConfigInterrupt_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eConfigInterrupt : omitted by entry port optimize */
/* eStarupHookBody */
void           tConfigInterrupt_eStarupHookBody_main_skel( const struct tag_sHookBody_VDES *epd)
{
    struct tag_tConfigInterrupt_eStarupHookBody_DES *lepd
        = (struct tag_tConfigInterrupt_eStarupHookBody_DES *)epd;
    tConfigInterrupt_eStarupHookBody_main( lepd->idx );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eConfigInterrupt : omitted by entry port optimize */
/* eStarupHookBody */
const struct tag_sHookBody_VMT tConfigInterrupt_eStarupHookBody_MT_ = {
    tConfigInterrupt_eStarupHookBody_main_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */



/* 呼び口配列 #_CPA_# */



/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
tConfigInterrupt_INIB tConfigInterrupt_INIB_tab[] = {
    /* cell: tConfigInterrupt_CB_tab[0]:  interruptTimer id=1 */
    {
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        INTNO_SYSIRQ_PID,                        /* interruptNumber */
        TA_ENAINT | TA_POSEDGE,                  /* attribute */
        -5,                                      /* interruptPriority */
    },
    /* cell: tConfigInterrupt_CB_tab[1]:  AVR_TWI_interruptTWI id=2 */
    {
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        INTNO_TWI_PID,                           /* interruptNumber */
        (TA_ENAINT | TA_LOWLEVEL),               /* attribute */
        -6,                                      /* interruptPriority */
    },
    /* cell: tConfigInterrupt_CB_tab[2]:  Display_SPI_interruptSPI id=3 */
    {
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        INTNO_SPI_PID,                           /* interruptNumber */
        (TA_ENAINT | TA_LOWLEVEL),               /* attribute */
        -4,                                      /* interruptPriority */
    },
};

/* 受け口ディスクリプタ #_EPD_# */
/* eConfigInterrupt : omitted by entry port optimize */
extern const struct tag_tConfigInterrupt_eStarupHookBody_DES interruptTimer_eStarupHookBody_des;
const struct tag_tConfigInterrupt_eStarupHookBody_DES interruptTimer_eStarupHookBody_des = {
    &tConfigInterrupt_eStarupHookBody_MT_,
    &tConfigInterrupt_INIB_tab[0],      /* INIB 3 */
};
/* eConfigInterrupt : omitted by entry port optimize */
extern const struct tag_tConfigInterrupt_eStarupHookBody_DES AVR_TWI_interruptTWI_eStarupHookBody_des;
const struct tag_tConfigInterrupt_eStarupHookBody_DES AVR_TWI_interruptTWI_eStarupHookBody_des = {
    &tConfigInterrupt_eStarupHookBody_MT_,
    &tConfigInterrupt_INIB_tab[1],      /* INIB 3 */
};
/* eConfigInterrupt : omitted by entry port optimize */
extern const struct tag_tConfigInterrupt_eStarupHookBody_DES Display_SPI_interruptSPI_eStarupHookBody_des;
const struct tag_tConfigInterrupt_eStarupHookBody_DES Display_SPI_interruptSPI_eStarupHookBody_des = {
    &tConfigInterrupt_eStarupHookBody_MT_,
    &tConfigInterrupt_INIB_tab[2],      /* INIB 3 */
};
/* CB 初期化コード #_CIC_# */
void
tConfigInterrupt_CB_initialize()
{
    tConfigInterrupt_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
