/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sAvrSensor_TECSGEN_H
#define sAvrSensor_TECSGEN_H

/*
 * signature   :  sAvrSensor
 * global name :  sAvrSensor
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sAvrSensor_VDES {
    struct tag_sAvrSensor_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sAvrSensor_VMT {
    void           (*setInputPower__T)( const struct tag_sAvrSensor_VDES *edp, uint8_t portNumber, uint8_t powerType );
    uint16_t       (*getSensor__T)( const struct tag_sAvrSensor_VDES *edp, uint8_t portNumber );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sAvrSensor_Defined
#define  Descriptor_of_sAvrSensor_Defined
typedef struct { struct tag_sAvrSensor_VDES *vdes; } Descriptor( sAvrSensor );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SAVRSENSOR_SETINPUTPOWER        (1)
#define	FUNCID_SAVRSENSOR_GETSENSOR            (2)

#endif /* sAvrSensor_TECSGEN_H */
