/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelISR2_TECSGEN_H
#define sKernelISR2_TECSGEN_H

/*
 * signature   :  sKernelISR2
 * global name :  sKernelISR2
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelISR2_VDES {
    struct tag_sKernelISR2_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelISR2_VMT {
    void           (*enableAllInterrupts__T)( const struct tag_sKernelISR2_VDES *edp );
    void           (*disableAllInterrupts__T)( const struct tag_sKernelISR2_VDES *edp );
    void           (*resumeAllInterrupts__T)( const struct tag_sKernelISR2_VDES *edp );
    void           (*suspendAllInterrupts__T)( const struct tag_sKernelISR2_VDES *edp );
    void           (*resumeOsInterrupts__T)( const struct tag_sKernelISR2_VDES *edp );
    void           (*suspendOsinterrupts__T)( const struct tag_sKernelISR2_VDES *edp );
    AppModeType    (*getActiveApplicationMode__T)( const struct tag_sKernelISR2_VDES *edp );
    void           (*shutdownOs__T)( const struct tag_sKernelISR2_VDES *edp, StatusType ercd );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelISR2_Defined
#define  Descriptor_of_sKernelISR2_Defined
typedef struct { struct tag_sKernelISR2_VDES *vdes; } Descriptor( sKernelISR2 );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELISR2_ENABLEALLINTERRUPTS (1)
#define	FUNCID_SKERNELISR2_DISABLEALLINTERRUPTS (2)
#define	FUNCID_SKERNELISR2_RESUMEALLINTERRUPTS (3)
#define	FUNCID_SKERNELISR2_SUSPENDALLINTERRUPTS (4)
#define	FUNCID_SKERNELISR2_RESUMEOSINTERRUPTS  (5)
#define	FUNCID_SKERNELISR2_SUSPENDOSINTERRUPTS (6)
#define	FUNCID_SKERNELISR2_GETACTIVEAPPLICATIONMODE (7)
#define	FUNCID_SKERNELISR2_SHUTDOWNOS          (8)

#endif /* sKernelISR2_TECSGEN_H */
