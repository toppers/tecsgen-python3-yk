/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sKernelShared_TECSGEN_H
#define sKernelShared_TECSGEN_H

/*
 * signature   :  sKernelShared
 * global name :  sKernelShared
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sKernelShared_VDES {
    struct tag_sKernelShared_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sKernelShared_VMT {
    ER             (*exitTask__T)( const struct tag_sKernelShared_VDES *edp );
    ER             (*sleep__T)( const struct tag_sKernelShared_VDES *edp );
    ER             (*sleepTimeout__T)( const struct tag_sKernelShared_VDES *edp, TMO timeout );
    ER             (*delay__T)( const struct tag_sKernelShared_VDES *edp, RELTIM delayTime );
    ER             (*disableTaskException__T)( const struct tag_sKernelShared_VDES *edp );
    ER             (*enableTaskException__T)( const struct tag_sKernelShared_VDES *edp );
    bool_t         (*senseTaskException__T)( const struct tag_sKernelShared_VDES *edp );
    ER             (*getMicroTime__T)( const struct tag_sKernelShared_VDES *edp, SYSUTM* p_systemMicroTime );
    ER             (*getTaskId__T)( const struct tag_sKernelShared_VDES *edp, ID* p_taskId );
    ER             (*getDomainId__T)( const struct tag_sKernelShared_VDES *edp, ID* p_domainId );
    bool_t         (*senseContext__T)( const struct tag_sKernelShared_VDES *edp );
    bool_t         (*senseLock__T)( const struct tag_sKernelShared_VDES *edp );
    bool_t         (*senseDispatch__T)( const struct tag_sKernelShared_VDES *edp );
    bool_t         (*senseDispatchPendingState__T)( const struct tag_sKernelShared_VDES *edp );
    bool_t         (*senseKernel__T)( const struct tag_sKernelShared_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sKernelShared_Defined
#define  Descriptor_of_sKernelShared_Defined
typedef struct { struct tag_sKernelShared_VDES *vdes; } Descriptor( sKernelShared );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SKERNELSHARED_EXITTASK          (1)
#define	FUNCID_SKERNELSHARED_SLEEP             (2)
#define	FUNCID_SKERNELSHARED_SLEEPTIMEOUT      (3)
#define	FUNCID_SKERNELSHARED_DELAY             (4)
#define	FUNCID_SKERNELSHARED_DISABLETASKEXCEPTION (5)
#define	FUNCID_SKERNELSHARED_ENABLETASKEXCEPTION (6)
#define	FUNCID_SKERNELSHARED_SENSETASKEXCEPTION (7)
#define	FUNCID_SKERNELSHARED_GETMICROTIME      (8)
#define	FUNCID_SKERNELSHARED_GETTASKID         (9)
#define	FUNCID_SKERNELSHARED_GETDOMAINID       (10)
#define	FUNCID_SKERNELSHARED_SENSECONTEXT      (11)
#define	FUNCID_SKERNELSHARED_SENSELOCK         (12)
#define	FUNCID_SKERNELSHARED_SENSEDISPATCH     (13)
#define	FUNCID_SKERNELSHARED_SENSEDISPATCHPENDINGSTATE (14)
#define	FUNCID_SKERNELSHARED_SENSEKERNEL       (15)

#endif /* sKernelShared_TECSGEN_H */
