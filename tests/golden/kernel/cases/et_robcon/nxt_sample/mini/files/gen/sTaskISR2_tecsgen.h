/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sTaskISR2_TECSGEN_H
#define sTaskISR2_TECSGEN_H

/*
 * signature   :  sTaskISR2
 * global name :  sTaskISR2
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sTaskISR2_VDES {
    struct tag_sTaskISR2_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sTaskISR2_VMT {
    StatusType     (*activate__T)( const struct tag_sTaskISR2_VDES *edp );
    StatusType     (*getId__T)( const struct tag_sTaskISR2_VDES *edp, TaskRefType p_tskid );
    StatusType     (*getState__T)( const struct tag_sTaskISR2_VDES *edp, TaskStateRefType p_state );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sTaskISR2_Defined
#define  Descriptor_of_sTaskISR2_Defined
typedef struct { struct tag_sTaskISR2_VDES *vdes; } Descriptor( sTaskISR2 );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_STASKISR2_ACTIVATE              (1)
#define	FUNCID_STASKISR2_GETID                 (2)
#define	FUNCID_STASKISR2_GETSTATE              (3)

#endif /* sTaskISR2_TECSGEN_H */
