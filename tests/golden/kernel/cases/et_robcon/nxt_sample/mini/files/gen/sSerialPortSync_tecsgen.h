/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSerialPortSync_TECSGEN_H
#define sSerialPortSync_TECSGEN_H

/*
 * signature   :  sSerialPortSync
 * global name :  sSerialPortSync
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSerialPortSync_VDES {
    struct tag_sSerialPortSync_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSerialPortSync_VMT {
    void           (*wait__T)( const struct tag_sSerialPortSync_VDES *edp );
    void           (*setBroadcast__T)( const struct tag_sSerialPortSync_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSerialPortSync_Defined
#define  Descriptor_of_sSerialPortSync_Defined
typedef struct { struct tag_sSerialPortSync_VDES *vdes; } Descriptor( sSerialPortSync );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSERIALPORTSYNC_WAIT            (1)
#define	FUNCID_SSERIALPORTSYNC_SETBROADCAST    (2)

#endif /* sSerialPortSync_TECSGEN_H */
