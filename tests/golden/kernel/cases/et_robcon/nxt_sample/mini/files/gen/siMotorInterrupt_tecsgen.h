/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef siMotorInterrupt_TECSGEN_H
#define siMotorInterrupt_TECSGEN_H

/*
 * signature   :  siMotorInterrupt
 * global name :  siMotorInterrupt
 * context     :  non-task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_siMotorInterrupt_VDES {
    struct tag_siMotorInterrupt_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_siMotorInterrupt_VMT {
    void           (*quadDecode__T)( const struct tag_siMotorInterrupt_VDES *edp, uint32_t pins );
    void           (*stopMotor__T)( const struct tag_siMotorInterrupt_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_siMotorInterrupt_Defined
#define  Descriptor_of_siMotorInterrupt_Defined
typedef struct { struct tag_siMotorInterrupt_VDES *vdes; } Descriptor( siMotorInterrupt );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SIMOTORINTERRUPT_QUADDECODE     (1)
#define	FUNCID_SIMOTORINTERRUPT_STOPMOTOR      (2)

#endif /* siMotorInterrupt_TECSGEN_H */
