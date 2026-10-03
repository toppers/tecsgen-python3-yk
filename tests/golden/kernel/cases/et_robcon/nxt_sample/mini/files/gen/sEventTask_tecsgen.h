/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sEventTask_TECSGEN_H
#define sEventTask_TECSGEN_H

/*
 * signature   :  sEventTask
 * global name :  sEventTask
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sEventTask_VDES {
    struct tag_sEventTask_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sEventTask_VMT {
    StatusType     (*set__T)( const struct tag_sEventTask_VDES *edp, TaskType tskid, EventMaskType mask );
    StatusType     (*clear__T)( const struct tag_sEventTask_VDES *edp, EventMaskType mask );
    StatusType     (*get__T)( const struct tag_sEventTask_VDES *edp, TaskType tskid, EventMaskRefType p_mask );
    StatusType     (*wait__T)( const struct tag_sEventTask_VDES *edp, EventMaskType mask );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sEventTask_Defined
#define  Descriptor_of_sEventTask_Defined
typedef struct { struct tag_sEventTask_VDES *vdes; } Descriptor( sEventTask );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SEVENTTASK_SET                  (1)
#define	FUNCID_SEVENTTASK_CLEAR                (2)
#define	FUNCID_SEVENTTASK_GET                  (3)
#define	FUNCID_SEVENTTASK_WAIT                 (4)

#endif /* sEventTask_TECSGEN_H */
