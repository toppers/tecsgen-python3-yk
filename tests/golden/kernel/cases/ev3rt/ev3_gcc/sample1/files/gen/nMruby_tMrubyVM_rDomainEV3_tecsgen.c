/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "nMruby_tMrubyVM_tecsgen.h"
#include "nMruby_tMrubyVM_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eMrubyVM : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eMrubyVM : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eMrubyVM : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */
extern struct tag_sMalloc_VDES rDomainEV3_MrubyMainVM_TLSFMalloc_eMalloc_des;

extern struct tag_sMalloc_VDES rDomainEV3_MrubySub1_TLSFMalloc_eMalloc_des;

extern struct tag_sMalloc_VDES rDomainEV3_MrubySub2_TLSFMalloc_eMalloc_des;

extern struct tag_sMalloc_VDES rDomainEV3_MrubyWakeupVM_TLSFMalloc_eMalloc_des;

extern struct tag_sMalloc_VDES rDomainEV3_MrubyCyclicVM_TLSFMalloc_eMalloc_des;

/* 呼び口配列 #_CPA_# */





/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
nMruby_tMrubyVM_INIB nMruby_tMrubyVM_INIB_tab[] = {
    /* cell: nMruby_tMrubyVM_CB_tab[0]:  MrubyMainVM_MrubyVM id=1 */
    {
        /* call port (INIB) #_CP_# */ 
        &tTLSFMalloc_INIB_tab[0],                /* cMalloc #_CCP2_# */
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        rDomainEV3_MrubyMainVM_MrubyVM_irep,     /* irep */
    },
    /* cell: nMruby_tMrubyVM_CB_tab[1]:  MrubySub1_MrubyVM id=2 */
    {
        /* call port (INIB) #_CP_# */ 
        &tTLSFMalloc_INIB_tab[1],                /* cMalloc #_CCP2_# */
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        rDomainEV3_MrubySub1_MrubyVM_irep,       /* irep */
    },
    /* cell: nMruby_tMrubyVM_CB_tab[2]:  MrubySub2_MrubyVM id=3 */
    {
        /* call port (INIB) #_CP_# */ 
        &tTLSFMalloc_INIB_tab[2],                /* cMalloc #_CCP2_# */
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        rDomainEV3_MrubySub2_MrubyVM_irep,       /* irep */
    },
    /* cell: nMruby_tMrubyVM_CB_tab[3]:  MrubyWakeupVM_MrubyVM id=4 */
    {
        /* call port (INIB) #_CP_# */ 
        &tTLSFMalloc_INIB_tab[3],                /* cMalloc #_CCP2_# */
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        rDomainEV3_MrubyWakeupVM_MrubyVM_irep,   /* irep */
    },
    /* cell: nMruby_tMrubyVM_CB_tab[4]:  MrubyCyclicVM_MrubyVM id=5 */
    {
        /* call port (INIB) #_CP_# */ 
        &tTLSFMalloc_INIB_tab[4],                /* cMalloc #_CCP2_# */
        /* entry port #_EP_# */ 
        /* attribute(RO) */ 
        rDomainEV3_MrubyCyclicVM_MrubyVM_irep,   /* irep */
    },
};

/* セル CB #_CB_# */
struct tag_nMruby_tMrubyVM_CB nMruby_tMrubyVM_CB_tab[5];
/* 受け口ディスクリプタ #_EPD_# */
/* eMrubyVM : omitted by entry port optimize */
/* eMrubyVM : omitted by entry port optimize */
/* eMrubyVM : omitted by entry port optimize */
/* eMrubyVM : omitted by entry port optimize */
/* eMrubyVM : omitted by entry port optimize */
/* CB 初期化コード #_CIC_# */
void
nMruby_tMrubyVM_CB_initialize()
{
    nMruby_tMrubyVM_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
