/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tFixedSizeMemoryPool_tecsgen.h"
#include "tFixedSizeMemoryPool_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eGetFixedSizeMemoryPool : omitted by entry port optimize */

/* eReleaseFixedSizeMemoryPool : omitted by entry port optimize */

/* eManageFixedSizeMemoryPool : omitted by entry port optimize */

/* eReferFixedSizeMemoryPool : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eGetFixedSizeMemoryPool : omitted by entry port optimize */
/* eReleaseFixedSizeMemoryPool : omitted by entry port optimize */
/* eManageFixedSizeMemoryPool : omitted by entry port optimize */
/* eReferFixedSizeMemoryPool : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eGetFixedSizeMemoryPool : omitted by entry port optimize */
/* eReleaseFixedSizeMemoryPool : omitted by entry port optimize */
/* eManageFixedSizeMemoryPool : omitted by entry port optimize */
/* eReferFixedSizeMemoryPool : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */

/* 呼び口配列 #_CPA_# */

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
/* cell: FixedSizeMemoryPoolO_CB:  FixedSizeMemoryPoolO id=3 */
const tFixedSizeMemoryPool_INIB FixedSizeMemoryPoolO_INIB = {
    /* entry port #_EP_# */ 
    /* attribute(RO) */ 
    MPFID_tFixedSizeMemoryPool_FixedSizeMemoryPoolO, /* id */
};

/* 受け口ディスクリプタ #_EPD_# */
/* eGetFixedSizeMemoryPool : omitted by entry port optimize */
/* eReleaseFixedSizeMemoryPool : omitted by entry port optimize */
/* eManageFixedSizeMemoryPool : omitted by entry port optimize */
/* eReferFixedSizeMemoryPool : omitted by entry port optimize */
/* ID to INIB table #_INTAB_# */
    extern tFixedSizeMemoryPool_INIB  rKernel_FixedSizeMemoryPoolK_INIB;
    extern tFixedSizeMemoryPool_INIB  rUser_FixedSizeMemoryPoolU_INIB;
tFixedSizeMemoryPool_INIB *const tFixedSizeMemoryPool_INIB_ptab[] ={
    &rKernel_FixedSizeMemoryPoolK_INIB,
    &rUser_FixedSizeMemoryPoolU_INIB,
    &FixedSizeMemoryPoolO_INIB,
};
/* CB 初期化コード #_CIC_# */
void
tFixedSizeMemoryPool_CB_initialize()
{
    tFixedSizeMemoryPool_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
