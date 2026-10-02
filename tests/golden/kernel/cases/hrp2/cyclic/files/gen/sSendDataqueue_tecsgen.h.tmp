/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSendDataqueue_TECSGEN_H
#define sSendDataqueue_TECSGEN_H

/*
 * signature   :  sSendDataqueue
 * global name :  sSendDataqueue
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSendDataqueue_VDES {
    struct tag_sSendDataqueue_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSendDataqueue_VMT {
    ER             (*send__T)( const struct tag_sSendDataqueue_VDES *edp, intptr_t data );
    ER             (*sendPolling__T)( const struct tag_sSendDataqueue_VDES *edp, intptr_t data );
    ER             (*sendTimeout__T)( const struct tag_sSendDataqueue_VDES *edp, intptr_t data, TMO timeout );
    ER             (*sendForce__T)( const struct tag_sSendDataqueue_VDES *edp, intptr_t data );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSendDataqueue_Defined
#define  Descriptor_of_sSendDataqueue_Defined
typedef struct { struct tag_sSendDataqueue_VDES *vdes; } Descriptor( sSendDataqueue );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSENDDATAQUEUE_SEND             (1)
#define	FUNCID_SSENDDATAQUEUE_SENDPOLLING      (2)
#define	FUNCID_SSENDDATAQUEUE_SENDTIMEOUT      (3)
#define	FUNCID_SSENDDATAQUEUE_SENDFORCE        (4)

#endif /* sSendDataqueue_TECSGEN_H */
