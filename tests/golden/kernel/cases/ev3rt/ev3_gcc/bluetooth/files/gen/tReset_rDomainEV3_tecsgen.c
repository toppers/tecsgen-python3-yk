/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#include "tReset_tecsgen.h"
#include "tReset_factory.h"

/* 受け口ディスクリプタ型 #_EDT_# */
/* eReset : omitted by entry port optimize */

/* 受け口スケルトン関数 #_EPSF_# */
/* eReset : omitted by entry port optimize */

/* 受け口スケルトン関数テーブル #_EPSFT_# */
/* eReset : omitted by entry port optimize */

/* 呼び口の参照する受け口ディスクリプタ(実際の型と相違した定義) #_CPEPD_# */
extern struct tag_sMotor_VDES rDomainEV3_MotorA_eMotor_des;
extern struct tag_sMotor_VDES rDomainEV3_MotorB_eMotor_des;
extern struct tag_sMotor_VDES rDomainEV3_MotorC_eMotor_des;
extern struct tag_sMotor_VDES rDomainEV3_MotorD_eMotor_des;

/* 呼び口配列 #_CPA_# */
struct tag_sMotor_VDES * const rDomainEV3_Reset_cMotor[] = {
    &rDomainEV3_MotorA_eMotor_des,
    &rDomainEV3_MotorB_eMotor_des,
    &rDomainEV3_MotorC_eMotor_des,
    &rDomainEV3_MotorD_eMotor_des,
};

/* 属性・変数の配列 #_AVAI_# */
/* セル INIB #_INIB_# */
tReset_INIB tReset_INIB_tab[] = {
    /* cell: tReset_CB_tab[0]:  Reset id=1 */
    {
        /* call port (INIB) #_CP_# */ 
        rDomainEV3_Reset_cMotor,                 /* #_CCP3B_# */
        4,                                       /* length of cMotor (n_cMotor) #_CCP4_# */
        /* entry port #_EP_# */ 
    },
};

/* 受け口ディスクリプタ #_EPD_# */
/* eReset : omitted by entry port optimize */
/* CB 初期化コード #_CIC_# */
void
tReset_CB_initialize()
{
    tReset_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
}
