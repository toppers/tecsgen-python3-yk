/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sTaskEvent_TECSGEN_H
#define sTaskEvent_TECSGEN_H

/*
 * signature   :  sTaskEvent
 * global name :  sTaskEvent
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sTaskEvent_VDES {
    struct tag_sTaskEvent_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sTaskEvent_VMT {
    StatusType     (*set__T)( const struct tag_sTaskEvent_VDES *edp, EventMaskType mask );
    StatusType     (*get__T)( const struct tag_sTaskEvent_VDES *edp, EventMaskRefType p_mask );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sTaskEvent_Defined
#define  Descriptor_of_sTaskEvent_Defined
typedef struct { struct tag_sTaskEvent_VDES *vdes; } Descriptor( sTaskEvent );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_STASKEVENT_SET                  (1)
#define	FUNCID_STASKEVENT_GET                  (2)

#endif /* sTaskEvent_TECSGEN_H */
