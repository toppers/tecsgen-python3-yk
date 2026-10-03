/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sHookBody_TECSGEN_H
#define sHookBody_TECSGEN_H

/*
 * signature   :  sHookBody
 * global name :  sHookBody
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sHookBody_VDES {
    struct tag_sHookBody_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sHookBody_VMT {
    void           (*main__T)( const struct tag_sHookBody_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sHookBody_Defined
#define  Descriptor_of_sHookBody_Defined
typedef struct { struct tag_sHookBody_VDES *vdes; } Descriptor( sHookBody );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SHOOKBODY_MAIN                  (1)

#endif /* sHookBody_TECSGEN_H */
