/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "nMruby_tRiteVMBluetooth_tecsgen.h"
#include "nMruby_tRiteVMBluetooth_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eMrubyBody */
struct tag_nMruby_tRiteVMBluetooth_eMrubyBody_DES {
    const struct tag_sTaskBody_VMT *vmt;
    tRiteVMBluetooth_IDX  idx;
};

/* eRiteVM */
struct tag_nMruby_tRiteVMBluetooth_eRiteVM_DES {
    const struct tag_sRiteVM_VMT *vmt;
    tRiteVMBluetooth_IDX  idx;
};

/* 受け口スケルトン関数 #_EPSF_# */
/* eMrubyBody */
void           nMruby_tRiteVMBluetooth_eMrubyBody_main_skel( const struct tag_sTaskBody_VDES *epd)
{
    struct tag_nMruby_tRiteVMBluetooth_eMrubyBody_DES *lepd
        = (struct tag_nMruby_tRiteVMBluetooth_eMrubyBody_DES *)epd;
    nMruby_tRiteVMBluetooth_eMrubyBody_main( lepd->idx );
}
/* eRiteVM */
void           nMruby_tRiteVMBluetooth_eRiteVM_reset_skel( const struct tag_sRiteVM_VDES *epd)
{
    struct tag_nMruby_tRiteVMBluetooth_eRiteVM_DES *lepd
        = (struct tag_nMruby_tRiteVMBluetooth_eRiteVM_DES *)epd;
    nMruby_tRiteVMBluetooth_eRiteVM_reset( lepd->idx );
}

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eMrubyBody */
const struct tag_sTaskBody_VMT nMruby_tRiteVMBluetooth_eMrubyBody_MT_ = {
    nMruby_tRiteVMBluetooth_eMrubyBody_main_skel,
};
/* eRiteVM */
const struct tag_sRiteVM_VMT nMruby_tRiteVMBluetooth_eRiteVM_MT_ = {
    nMruby_tRiteVMBluetooth_eRiteVM_reset_skel,
};

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
uint8_t nMruby_tRiteVMBluetooth_RiteVMBluetooth1_CB_irepApp_INIT[131072];
/* セル INIB #_INIB_# */
nMruby_tRiteVMBluetooth_INIB nMruby_tRiteVMBluetooth_INIB_tab[] = {
    /* cell: nMruby_tRiteVMBluetooth_CB_tab[0]:  RiteVMBluetooth1 id=1 */
    {
        /* call port (INIB) #_CP_# */ 
        0,                                       /* #_CCP9_# */
        0,                                       /* length of cEventflag (n_cEventflag) #_CCP6_# */
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        &rDomainEV3_RiteVMBluetooth1_irep,       /* irepLib */
        131072,                                  /* irepAppSize */
        0x01,                                    /* setptn */
        nMruby_tRiteVMBluetooth_RiteVMBluetooth1_CB_irepApp_INIT, /* irepApp */
    },
};

/* セル CB #_CB_# */
struct tag_nMruby_tRiteVMBluetooth_CB nMruby_tRiteVMBluetooth_CB_tab[1];
extern const struct tag_sTaskBody_VMT nMruby_tRiteVMBluetooth_eMrubyBody_MT_;
extern const struct tag_sRiteVM_VMT nMruby_tRiteVMBluetooth_eRiteVM_MT_;
/* 受け口ディスクリプタ #_EPD_# */
extern const struct tag_nMruby_tRiteVMBluetooth_eMrubyBody_DES rDomainEV3_RiteVMBluetooth1_eMrubyBody_des;
const struct tag_nMruby_tRiteVMBluetooth_eMrubyBody_DES rDomainEV3_RiteVMBluetooth1_eMrubyBody_des = {
    &nMruby_tRiteVMBluetooth_eMrubyBody_MT_,
    &nMruby_tRiteVMBluetooth_CB_tab[0],      /* CB 3 */
};
extern const struct tag_nMruby_tRiteVMBluetooth_eRiteVM_DES rDomainEV3_RiteVMBluetooth1_eRiteVM_des;
const struct tag_nMruby_tRiteVMBluetooth_eRiteVM_DES rDomainEV3_RiteVMBluetooth1_eRiteVM_des = {
    &nMruby_tRiteVMBluetooth_eRiteVM_MT_,
    &nMruby_tRiteVMBluetooth_CB_tab[0],      /* CB 3 */
};
/* CB 初期化コード #_CIC_# */
void
nMruby_tRiteVMBluetooth_CB_initialize()
{
    nMruby_tRiteVMBluetooth_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
