/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sHandlerBody_TECSGEN_H
#define sHandlerBody_TECSGEN_H

/*
 * signature   :  sHandlerBody
 * global name :  sHandlerBody
 * context     :  non-task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sHandlerBody_VDES {
    struct tag_sHandlerBody_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sHandlerBody_VMT {
    void           (*main__T)( const struct tag_sHandlerBody_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sHandlerBody_Defined
#define  Descriptor_of_sHandlerBody_Defined
typedef struct { struct tag_sHandlerBody_VDES *vdes; } Descriptor( sHandlerBody );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SHANDLERBODY_MAIN               (1)

#endif /* sHandlerBody_TECSGEN_H */
