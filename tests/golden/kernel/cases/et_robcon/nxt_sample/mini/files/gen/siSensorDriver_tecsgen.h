/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef siSensorDriver_TECSGEN_H
#define siSensorDriver_TECSGEN_H

/*
 * signature   :  siSensorDriver
 * global name :  siSensorDriver
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_siSensorDriver_VDES {
    struct tag_siSensorDriver_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_siSensorDriver_VMT {
    void           (*initialize__T)( const struct tag_siSensorDriver_VDES *edp );
    void           (*i2cInterruptBody__T)( const struct tag_siSensorDriver_VDES *edp, uint32_t inputs );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_siSensorDriver_Defined
#define  Descriptor_of_siSensorDriver_Defined
typedef struct { struct tag_siSensorDriver_VDES *vdes; } Descriptor( siSensorDriver );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SISENSORDRIVER_INITIALIZE       (1)
#define	FUNCID_SISENSORDRIVER_I2CINTERRUPTBODY (2)

#endif /* siSensorDriver_TECSGEN_H */
