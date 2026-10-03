/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sEventISR2_TECSGEN_H
#define sEventISR2_TECSGEN_H

/*
 * signature   :  sEventISR2
 * global name :  sEventISR2
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sEventISR2_VDES {
    struct tag_sEventISR2_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sEventISR2_VMT {
    StatusType     (*set__T)( const struct tag_sEventISR2_VDES *edp, TaskType tskid, EventMaskType mask );
    StatusType     (*get__T)( const struct tag_sEventISR2_VDES *edp, TaskType tskid, EventMaskRefType p_mask );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sEventISR2_Defined
#define  Descriptor_of_sEventISR2_Defined
typedef struct { struct tag_sEventISR2_VDES *vdes; } Descriptor( sEventISR2 );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SEVENTISR2_SET                  (1)
#define	FUNCID_SEVENTISR2_GET                  (2)

#endif /* sEventISR2_TECSGEN_H */
