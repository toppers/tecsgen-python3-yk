/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReferTask_TECSGEN_H
#define sReferTask_TECSGEN_H

/*
 * signature   :  sReferTask
 * global name :  sReferTask
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReferTask_VDES {
    struct tag_sReferTask_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReferTask_VMT {
    ER             (*getPriority__T)( const struct tag_sReferTask_VDES *edp, PRI* p_priority );
    ER             (*refer__T)( const struct tag_sReferTask_VDES *edp, T_RTSK* pk_taskStatus );
    ER             (*referException__T)( const struct tag_sReferTask_VDES *edp, T_RTEX* pk_rtex );
    ER             (*referOverRunHandler__T)( const struct tag_sReferTask_VDES *edp, T_ROVR* pk_rovr );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReferTask_Defined
#define  Descriptor_of_sReferTask_Defined
typedef struct { struct tag_sReferTask_VDES *vdes; } Descriptor( sReferTask );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SREFERTASK_GETPRIORITY          (1)
#define	FUNCID_SREFERTASK_REFER                (2)
#define	FUNCID_SREFERTASK_REFEREXCEPTION       (3)
#define	FUNCID_SREFERTASK_REFEROVERRUNHANDLER  (4)

#endif /* sReferTask_TECSGEN_H */
