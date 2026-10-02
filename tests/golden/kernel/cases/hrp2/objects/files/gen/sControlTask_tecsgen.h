/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sControlTask_TECSGEN_H
#define sControlTask_TECSGEN_H

/*
 * signature   :  sControlTask
 * global name :  sControlTask
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sControlTask_VDES {
    struct tag_sControlTask_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sControlTask_VMT {
    ER             (*terminate__T)( const struct tag_sControlTask_VDES *edp );
    ER             (*changePriority__T)( const struct tag_sControlTask_VDES *edp, PRI priority );
    ER             (*releaseWait__T)( const struct tag_sControlTask_VDES *edp );
    ER             (*suspend__T)( const struct tag_sControlTask_VDES *edp );
    ER             (*resume__T)( const struct tag_sControlTask_VDES *edp );
    ER             (*raiseException__T)( const struct tag_sControlTask_VDES *edp, TEXPTN pattern );
    ER             (*disableWait__T)( const struct tag_sControlTask_VDES *edp );
    ER             (*enableWait__T)( const struct tag_sControlTask_VDES *edp );
    ER             (*startOverRunHandler__T)( const struct tag_sControlTask_VDES *edp, OVRTIM ovrtim );
    ER             (*stopOverRunHandler__T)( const struct tag_sControlTask_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sControlTask_Defined
#define  Descriptor_of_sControlTask_Defined
typedef struct { struct tag_sControlTask_VDES *vdes; } Descriptor( sControlTask );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SCONTROLTASK_TERMINATE          (1)
#define	FUNCID_SCONTROLTASK_CHANGEPRIORITY     (2)
#define	FUNCID_SCONTROLTASK_RELEASEWAIT        (3)
#define	FUNCID_SCONTROLTASK_SUSPEND            (4)
#define	FUNCID_SCONTROLTASK_RESUME             (5)
#define	FUNCID_SCONTROLTASK_RAISEEXCEPTION     (6)
#define	FUNCID_SCONTROLTASK_DISABLEWAIT        (7)
#define	FUNCID_SCONTROLTASK_ENABLEWAIT         (8)
#define	FUNCID_SCONTROLTASK_STARTOVERRUNHANDLER (9)
#define	FUNCID_SCONTROLTASK_STOPOVERRUNHANDLER (10)

#endif /* sControlTask_TECSGEN_H */
