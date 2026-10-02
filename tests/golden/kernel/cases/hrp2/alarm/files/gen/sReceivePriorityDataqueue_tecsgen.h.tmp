/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReceivePriorityDataqueue_TECSGEN_H
#define sReceivePriorityDataqueue_TECSGEN_H

/*
 * signature   :  sReceivePriorityDataqueue
 * global name :  sReceivePriorityDataqueue
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReceivePriorityDataqueue_VDES {
    struct tag_sReceivePriorityDataqueue_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReceivePriorityDataqueue_VMT {
    ER             (*receive__T)( const struct tag_sReceivePriorityDataqueue_VDES *edp, intptr_t* p_data, PRI* p_dataPriority );
    ER             (*receivePolling__T)( const struct tag_sReceivePriorityDataqueue_VDES *edp, intptr_t* p_data, PRI* p_dataPriority );
    ER             (*receiveTimeout__T)( const struct tag_sReceivePriorityDataqueue_VDES *edp, intptr_t* p_data, PRI* p_dataPriority, TMO timeout );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReceivePriorityDataqueue_Defined
#define  Descriptor_of_sReceivePriorityDataqueue_Defined
typedef struct { struct tag_sReceivePriorityDataqueue_VDES *vdes; } Descriptor( sReceivePriorityDataqueue );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SRECEIVEPRIORITYDATAQUEUE_RECEIVE (1)
#define	FUNCID_SRECEIVEPRIORITYDATAQUEUE_RECEIVEPOLLING (2)
#define	FUNCID_SRECEIVEPRIORITYDATAQUEUE_RECEIVETIMEOUT (3)

#endif /* sReceivePriorityDataqueue_TECSGEN_H */
