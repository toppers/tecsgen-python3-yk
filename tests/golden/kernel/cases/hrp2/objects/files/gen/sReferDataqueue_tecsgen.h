/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReferDataqueue_TECSGEN_H
#define sReferDataqueue_TECSGEN_H

/*
 * signature   :  sReferDataqueue
 * global name :  sReferDataqueue
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReferDataqueue_VDES {
    struct tag_sReferDataqueue_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReferDataqueue_VMT {
    ER             (*refer__T)( const struct tag_sReferDataqueue_VDES *edp, T_RDTQ* pk_dataqueueStatus );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReferDataqueue_Defined
#define  Descriptor_of_sReferDataqueue_Defined
typedef struct { struct tag_sReferDataqueue_VDES *vdes; } Descriptor( sReferDataqueue );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SREFERDATAQUEUE_REFER           (1)

#endif /* sReferDataqueue_TECSGEN_H */
