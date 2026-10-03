/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelTaskHook_TECSGEN_H
#define sKernelTaskHook_TECSGEN_H

/*
 * signature   :  sKernelTaskHook
 * global name :  sKernelTaskHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelTaskHook_VDES {
    struct tag_sKernelTaskHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelTaskHook_VMT {
    void           (*resumeAllInterrupts__T)( const struct tag_sKernelTaskHook_VDES *edp );
    void           (*suspendAllInterrupts__T)( const struct tag_sKernelTaskHook_VDES *edp );
    AppModeType    (*getActiveApplicationMode__T)( const struct tag_sKernelTaskHook_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelTaskHook_Defined
#define  Descriptor_of_sKernelTaskHook_Defined
typedef struct { struct tag_sKernelTaskHook_VDES *vdes; } Descriptor( sKernelTaskHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELTASKHOOK_RESUMEALLINTERRUPTS (1)
#define	FUNCID_SKERNELTASKHOOK_SUSPENDALLINTERRUPTS (2)
#define	FUNCID_SKERNELTASKHOOK_GETACTIVEAPPLICATIONMODE (3)

#endif /* sKernelTaskHook_TECSGEN_H */
