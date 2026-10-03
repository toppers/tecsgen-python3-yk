/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelISR1_TECSGEN_H
#define sKernelISR1_TECSGEN_H

/*
 * signature   :  sKernelISR1
 * global name :  sKernelISR1
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelISR1_VDES {
    struct tag_sKernelISR1_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelISR1_VMT {
    void           (*enableAllInterrupts__T)( const struct tag_sKernelISR1_VDES *edp );
    void           (*disableAllInterrupts__T)( const struct tag_sKernelISR1_VDES *edp );
    void           (*resumeAllInterrupts__T)( const struct tag_sKernelISR1_VDES *edp );
    void           (*suspendAllInterrupts__T)( const struct tag_sKernelISR1_VDES *edp );
    void           (*resumeOsInterrupts__T)( const struct tag_sKernelISR1_VDES *edp );
    void           (*suspendOsinterrupts__T)( const struct tag_sKernelISR1_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelISR1_Defined
#define  Descriptor_of_sKernelISR1_Defined
typedef struct { struct tag_sKernelISR1_VDES *vdes; } Descriptor( sKernelISR1 );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELISR1_ENABLEALLINTERRUPTS (1)
#define	FUNCID_SKERNELISR1_DISABLEALLINTERRUPTS (2)
#define	FUNCID_SKERNELISR1_RESUMEALLINTERRUPTS (3)
#define	FUNCID_SKERNELISR1_SUSPENDALLINTERRUPTS (4)
#define	FUNCID_SKERNELISR1_RESUMEOSINTERRUPTS  (5)
#define	FUNCID_SKERNELISR1_SUSPENDOSINTERRUPTS (6)

#endif /* sKernelISR1_TECSGEN_H */
