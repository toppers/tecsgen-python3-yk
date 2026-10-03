/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sBalancer_TECSGEN_H
#define sBalancer_TECSGEN_H

/*
 * signature   :  sBalancer
 * global name :  sBalancer
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sBalancer_VDES {
    struct tag_sBalancer_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sBalancer_VMT {
    void           (*control__T)( const struct tag_sBalancer_VDES *edp, int16_t forward, int16_t turn, uint16_t gyro, uint16_t gyroOffset, int32_t leftRevolution, int32_t rightRevolution, uint16_t battery, int8_t* pwm_l, int8_t* pwm_r );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sBalancer_Defined
#define  Descriptor_of_sBalancer_Defined
typedef struct { struct tag_sBalancer_VDES *vdes; } Descriptor( sBalancer );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SBALANCER_CONTROL               (1)

#endif /* sBalancer_TECSGEN_H */
