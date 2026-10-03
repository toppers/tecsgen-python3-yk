/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sDelayTask_TECSGEN_H
#define sDelayTask_TECSGEN_H

/*
 * signature   :  sDelayTask
 * global name :  sDelayTask
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sDelayTask_VDES {
    struct tag_sDelayTask_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sDelayTask_VMT {
    void           (*delay__T)( const struct tag_sDelayTask_VDES *edp, TickType msec );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sDelayTask_Defined
#define  Descriptor_of_sDelayTask_Defined
typedef struct { struct tag_sDelayTask_VDES *vdes; } Descriptor( sDelayTask );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SDELAYTASK_DELAY                (1)

#endif /* sDelayTask_TECSGEN_H */
