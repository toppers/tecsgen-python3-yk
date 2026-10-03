/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sEventMask_TECSGEN_H
#define sEventMask_TECSGEN_H

/*
 * signature   :  sEventMask
 * global name :  sEventMask
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sEventMask_VDES {
    struct tag_sEventMask_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sEventMask_VMT {
    EventMaskType  (*get__T)( const struct tag_sEventMask_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sEventMask_Defined
#define  Descriptor_of_sEventMask_Defined
typedef struct { struct tag_sEventMask_VDES *vdes; } Descriptor( sEventMask );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SEVENTMASK_GET                  (1)

#endif /* sEventMask_TECSGEN_H */
