/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sEventHook_TECSGEN_H
#define sEventHook_TECSGEN_H

/*
 * signature   :  sEventHook
 * global name :  sEventHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sEventHook_VDES {
    struct tag_sEventHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sEventHook_VMT {
    StatusType     (*get__T)( const struct tag_sEventHook_VDES *edp, TaskType tskid, EventMaskRefType p_mask );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sEventHook_Defined
#define  Descriptor_of_sEventHook_Defined
typedef struct { struct tag_sEventHook_VDES *vdes; } Descriptor( sEventHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SEVENTHOOK_GET                  (1)

#endif /* sEventHook_TECSGEN_H */
