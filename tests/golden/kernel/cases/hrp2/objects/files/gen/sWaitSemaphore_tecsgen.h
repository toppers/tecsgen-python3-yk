/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sWaitSemaphore_TECSGEN_H
#define sWaitSemaphore_TECSGEN_H

/*
 * signature   :  sWaitSemaphore
 * global name :  sWaitSemaphore
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sWaitSemaphore_VDES {
    struct tag_sWaitSemaphore_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sWaitSemaphore_VMT {
    ER             (*wait__T)( const struct tag_sWaitSemaphore_VDES *edp );
    ER             (*waitPolling__T)( const struct tag_sWaitSemaphore_VDES *edp );
    ER             (*waitTimeout__T)( const struct tag_sWaitSemaphore_VDES *edp, TMO timeout );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sWaitSemaphore_Defined
#define  Descriptor_of_sWaitSemaphore_Defined
typedef struct { struct tag_sWaitSemaphore_VDES *vdes; } Descriptor( sWaitSemaphore );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SWAITSEMAPHORE_WAIT             (1)
#define	FUNCID_SWAITSEMAPHORE_WAITPOLLING      (2)
#define	FUNCID_SWAITSEMAPHORE_WAITTIMEOUT      (3)

#endif /* sWaitSemaphore_TECSGEN_H */
