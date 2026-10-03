/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelStartupHook_TECSGEN_H
#define sKernelStartupHook_TECSGEN_H

/*
 * signature   :  sKernelStartupHook
 * global name :  sKernelStartupHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelStartupHook_VDES {
    struct tag_sKernelStartupHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelStartupHook_VMT {
    AppModeType    (*getActiveApplicationMode__T)( const struct tag_sKernelStartupHook_VDES *edp );
    void           (*shutdownOs__T)( const struct tag_sKernelStartupHook_VDES *edp, StatusType ercd );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelStartupHook_Defined
#define  Descriptor_of_sKernelStartupHook_Defined
typedef struct { struct tag_sKernelStartupHook_VDES *vdes; } Descriptor( sKernelStartupHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELSTARTUPHOOK_GETACTIVEAPPLICATIONMODE (1)
#define	FUNCID_SKERNELSTARTUPHOOK_SHUTDOWNOS   (2)

#endif /* sKernelStartupHook_TECSGEN_H */
