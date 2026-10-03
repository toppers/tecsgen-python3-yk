/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sAvrBattery_TECSGEN_H
#define sAvrBattery_TECSGEN_H

/*
 * signature   :  sAvrBattery
 * global name :  sAvrBattery
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sAvrBattery_VDES {
    struct tag_sAvrBattery_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sAvrBattery_VMT {
    uint16_t       (*batteryVoltage__T)( const struct tag_sAvrBattery_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sAvrBattery_Defined
#define  Descriptor_of_sAvrBattery_Defined
typedef struct { struct tag_sAvrBattery_VDES *vdes; } Descriptor( sAvrBattery );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SAVRBATTERY_BATTERYVOLTAGE      (1)

#endif /* sAvrBattery_TECSGEN_H */
