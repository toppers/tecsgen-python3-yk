/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelShutdownHook_TECSGEN_H
#define sKernelShutdownHook_TECSGEN_H

/*
 * signature   :  sKernelShutdownHook
 * global name :  sKernelShutdownHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelShutdownHook_VDES {
    struct tag_sKernelShutdownHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelShutdownHook_VMT {
    AppModeType    (*getActiveApplicationMode__T)( const struct tag_sKernelShutdownHook_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelShutdownHook_Defined
#define  Descriptor_of_sKernelShutdownHook_Defined
typedef struct { struct tag_sKernelShutdownHook_VDES *vdes; } Descriptor( sKernelShutdownHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELSHUTDOWNHOOK_GETACTIVEAPPLICATIONMODE (1)

#endif /* sKernelShutdownHook_TECSGEN_H */
