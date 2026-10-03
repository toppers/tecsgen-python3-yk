/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sAvrButton_TECSGEN_H
#define sAvrButton_TECSGEN_H

/*
 * signature   :  sAvrButton
 * global name :  sAvrButton
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sAvrButton_VDES {
    struct tag_sAvrButton_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sAvrButton_VMT {
    uint8_t        (*getButton__T)( const struct tag_sAvrButton_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sAvrButton_Defined
#define  Descriptor_of_sAvrButton_Defined
typedef struct { struct tag_sAvrButton_VDES *vdes; } Descriptor( sAvrButton );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SAVRBUTTON_GETBUTTON            (1)

#endif /* sAvrButton_TECSGEN_H */
