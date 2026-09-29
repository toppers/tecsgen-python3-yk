/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReset_TECSGEN_H
#define sReset_TECSGEN_H

/*
 * signature   :  sReset
 * global name :  sReset
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReset_VDES {
    struct tag_sReset_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReset_VMT {
    void           (*reset__T)( const struct tag_sReset_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReset_Defined
#define  Descriptor_of_sReset_Defined
typedef struct { struct tag_sReset_VDES *vdes; } Descriptor( sReset );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SRESET_RESET                    (1)

#endif /* sReset_TECSGEN_H */
