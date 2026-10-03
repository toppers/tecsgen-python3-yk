/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sMotor_TECSGEN_H
#define sMotor_TECSGEN_H

/*
 * signature   :  sMotor
 * global name :  sMotor
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sMotor_VDES {
    struct tag_sMotor_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sMotor_VMT {
    void           (*setPWM__T)( const struct tag_sMotor_VDES *edp, int8_t pwm, bool_t brakeMode );
    void           (*setRevolution__T)( const struct tag_sMotor_VDES *edp, int32_t revolution );
    void           (*getRevolution__T)( const struct tag_sMotor_VDES *edp, int32_t* revolution );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sMotor_Defined
#define  Descriptor_of_sMotor_Defined
typedef struct { struct tag_sMotor_VDES *vdes; } Descriptor( sMotor );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SMOTOR_SETPWM                   (1)
#define	FUNCID_SMOTOR_SETREVOLUTION            (2)
#define	FUNCID_SMOTOR_GETREVOLUTION            (3)

#endif /* sMotor_TECSGEN_H */
