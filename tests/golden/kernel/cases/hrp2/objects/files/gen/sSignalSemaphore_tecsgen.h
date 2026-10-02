/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSignalSemaphore_TECSGEN_H
#define sSignalSemaphore_TECSGEN_H

/*
 * signature   :  sSignalSemaphore
 * global name :  sSignalSemaphore
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSignalSemaphore_VDES {
    struct tag_sSignalSemaphore_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSignalSemaphore_VMT {
    ER             (*signal__T)( const struct tag_sSignalSemaphore_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSignalSemaphore_Defined
#define  Descriptor_of_sSignalSemaphore_Defined
typedef struct { struct tag_sSignalSemaphore_VDES *vdes; } Descriptor( sSignalSemaphore );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSIGNALSEMAPHORE_SIGNAL         (1)

#endif /* sSignalSemaphore_TECSGEN_H */
