/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelErrorHook_TECSGEN_H
#define sKernelErrorHook_TECSGEN_H

/*
 * signature   :  sKernelErrorHook
 * global name :  sKernelErrorHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelErrorHook_VDES {
    struct tag_sKernelErrorHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelErrorHook_VMT {
    void           (*resumeAllInterrupts__T)( const struct tag_sKernelErrorHook_VDES *edp );
    void           (*suspendAllInterrupts__T)( const struct tag_sKernelErrorHook_VDES *edp );
    AppModeType    (*getActiveApplicationMode__T)( const struct tag_sKernelErrorHook_VDES *edp );
    void           (*shutdownOs__T)( const struct tag_sKernelErrorHook_VDES *edp, StatusType ercd );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelErrorHook_Defined
#define  Descriptor_of_sKernelErrorHook_Defined
typedef struct { struct tag_sKernelErrorHook_VDES *vdes; } Descriptor( sKernelErrorHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELERRORHOOK_RESUMEALLINTERRUPTS (1)
#define	FUNCID_SKERNELERRORHOOK_SUSPENDALLINTERRUPTS (2)
#define	FUNCID_SKERNELERRORHOOK_GETACTIVEAPPLICATIONMODE (3)
#define	FUNCID_SKERNELERRORHOOK_SHUTDOWNOS     (4)

#endif /* sKernelErrorHook_TECSGEN_H */
