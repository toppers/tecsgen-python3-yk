/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelAlarmCallback_TECSGEN_H
#define sKernelAlarmCallback_TECSGEN_H

/*
 * signature   :  sKernelAlarmCallback
 * global name :  sKernelAlarmCallback
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelAlarmCallback_VDES {
    struct tag_sKernelAlarmCallback_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelAlarmCallback_VMT {
    void           (*resumeAllInterrupts__T)( const struct tag_sKernelAlarmCallback_VDES *edp );
    void           (*suspendAllInterrupts__T)( const struct tag_sKernelAlarmCallback_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelAlarmCallback_Defined
#define  Descriptor_of_sKernelAlarmCallback_Defined
typedef struct { struct tag_sKernelAlarmCallback_VDES *vdes; } Descriptor( sKernelAlarmCallback );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELALARMCALLBACK_RESUMEALLINTERRUPTS (1)
#define	FUNCID_SKERNELALARMCALLBACK_SUSPENDALLINTERRUPTS (2)

#endif /* sKernelAlarmCallback_TECSGEN_H */
