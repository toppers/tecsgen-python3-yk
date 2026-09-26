/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSig2_TECSGEN_H
#define sSig2_TECSGEN_H

/*
 * signature   :  sSig2
 * global name :  sSig2
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSig2_VDES {
    struct tag_sSig2_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSig2_VMT {
    void           (*func__T)( const struct tag_sSig2_VDES *edp );
    void           (*func2__T)( const struct tag_sSig2_VDES *edp );
    void           (*func3__T)( const struct tag_sSig2_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSig2_Defined
#define  Descriptor_of_sSig2_Defined
typedef struct { struct tag_sSig2_VDES *vdes; } Descriptor( sSig2 );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSIG2_FUNC                      (1)
#define	FUNCID_SSIG2_FUNC2                     (2)
#define	FUNCID_SSIG2_FUNC3                     (3)

#endif /* sSig2_TECSGEN_H */
