/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sFlash_TECSGEN_H
#define sFlash_TECSGEN_H

/*
 * signature   :  sFlash
 * global name :  sFlash
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sFlash_VDES {
    struct tag_sFlash_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sFlash_VMT {
    void           (*rewriteBios__T)( const struct tag_sFlash_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sFlash_Defined
#define  Descriptor_of_sFlash_Defined
typedef struct { struct tag_sFlash_VDES *vdes; } Descriptor( sFlash );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SFLASH_REWRITEBIOS              (1)

#endif /* sFlash_TECSGEN_H */
