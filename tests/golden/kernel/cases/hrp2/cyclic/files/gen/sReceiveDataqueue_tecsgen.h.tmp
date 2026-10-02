/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReceiveDataqueue_TECSGEN_H
#define sReceiveDataqueue_TECSGEN_H

/*
 * signature   :  sReceiveDataqueue
 * global name :  sReceiveDataqueue
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReceiveDataqueue_VDES {
    struct tag_sReceiveDataqueue_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReceiveDataqueue_VMT {
    ER             (*receive__T)( const struct tag_sReceiveDataqueue_VDES *edp, intptr_t* p_data );
    ER             (*receivePolling__T)( const struct tag_sReceiveDataqueue_VDES *edp, intptr_t* p_data );
    ER             (*receiveTimeout__T)( const struct tag_sReceiveDataqueue_VDES *edp, intptr_t* p_data, TMO timeout );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReceiveDataqueue_Defined
#define  Descriptor_of_sReceiveDataqueue_Defined
typedef struct { struct tag_sReceiveDataqueue_VDES *vdes; } Descriptor( sReceiveDataqueue );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SRECEIVEDATAQUEUE_RECEIVE       (1)
#define	FUNCID_SRECEIVEDATAQUEUE_RECEIVEPOLLING (2)
#define	FUNCID_SRECEIVEDATAQUEUE_RECEIVETIMEOUT (3)

#endif /* sReceiveDataqueue_TECSGEN_H */
