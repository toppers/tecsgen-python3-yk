/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sBattery_TECSGEN_H
#define sBattery_TECSGEN_H

/*
 * signature   :  sBattery
 * global name :  sBattery
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sBattery_VDES {
    struct tag_sBattery_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sBattery_VMT {
    uint16_t       (*getBatteryVoltage__T)( const struct tag_sBattery_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sBattery_Defined
#define  Descriptor_of_sBattery_Defined
typedef struct { struct tag_sBattery_VDES *vdes; } Descriptor( sBattery );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SBATTERY_GETBATTERYVOLTAGE      (1)

#endif /* sBattery_TECSGEN_H */
