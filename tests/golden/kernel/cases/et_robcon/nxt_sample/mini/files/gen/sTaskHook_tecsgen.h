/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sTaskHook_TECSGEN_H
#define sTaskHook_TECSGEN_H

/*
 * signature   :  sTaskHook
 * global name :  sTaskHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sTaskHook_VDES {
    struct tag_sTaskHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sTaskHook_VMT {
    StatusType     (*getId__T)( const struct tag_sTaskHook_VDES *edp, TaskRefType p_tskid );
    StatusType     (*getState__T)( const struct tag_sTaskHook_VDES *edp, TaskStateRefType p_state );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sTaskHook_Defined
#define  Descriptor_of_sTaskHook_Defined
typedef struct { struct tag_sTaskHook_VDES *vdes; } Descriptor( sTaskHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_STASKHOOK_GETID                 (1)
#define	FUNCID_STASKHOOK_GETSTATE              (2)

#endif /* sTaskHook_TECSGEN_H */
