/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSensorArray_TECSGEN_H
#define sSensorArray_TECSGEN_H

/*
 * signature   :  sSensorArray
 * global name :  sSensorArray
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSensorArray_VDES {
    struct tag_sSensorArray_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSensorArray_VMT {
    void           (*getValue__T)( const struct tag_sSensorArray_VDES *edp, int16_t* buf, int8_t bufferSize );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSensorArray_Defined
#define  Descriptor_of_sSensorArray_Defined
typedef struct { struct tag_sSensorArray_VDES *vdes; } Descriptor( sSensorArray );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSENSORARRAY_GETVALUE           (1)

#endif /* sSensorArray_TECSGEN_H */
