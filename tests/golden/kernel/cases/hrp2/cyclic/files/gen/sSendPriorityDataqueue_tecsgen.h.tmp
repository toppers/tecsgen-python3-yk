/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSendPriorityDataqueue_TECSGEN_H
#define sSendPriorityDataqueue_TECSGEN_H

/*
 * signature   :  sSendPriorityDataqueue
 * global name :  sSendPriorityDataqueue
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSendPriorityDataqueue_VDES {
    struct tag_sSendPriorityDataqueue_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSendPriorityDataqueue_VMT {
    ER             (*send__T)( const struct tag_sSendPriorityDataqueue_VDES *edp, intptr_t data, PRI dataPriority );
    ER             (*sendPolling__T)( const struct tag_sSendPriorityDataqueue_VDES *edp, intptr_t data, PRI dataPriority );
    ER             (*sendTimeout__T)( const struct tag_sSendPriorityDataqueue_VDES *edp, intptr_t data, PRI dataPriority, TMO timeout );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSendPriorityDataqueue_Defined
#define  Descriptor_of_sSendPriorityDataqueue_Defined
typedef struct { struct tag_sSendPriorityDataqueue_VDES *vdes; } Descriptor( sSendPriorityDataqueue );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSENDPRIORITYDATAQUEUE_SEND     (1)
#define	FUNCID_SSENDPRIORITYDATAQUEUE_SENDPOLLING (2)
#define	FUNCID_SSENDPRIORITYDATAQUEUE_SENDTIMEOUT (3)

#endif /* sSendPriorityDataqueue_TECSGEN_H */
