/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sGetFixedSizeMemoryPool_TECSGEN_H
#define sGetFixedSizeMemoryPool_TECSGEN_H

/*
 * signature   :  sGetFixedSizeMemoryPool
 * global name :  sGetFixedSizeMemoryPool
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sGetFixedSizeMemoryPool_VDES {
    struct tag_sGetFixedSizeMemoryPool_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sGetFixedSizeMemoryPool_VMT {
    ER             (*get__T)( const struct tag_sGetFixedSizeMemoryPool_VDES *edp, void** p_block );
    ER             (*getPolling__T)( const struct tag_sGetFixedSizeMemoryPool_VDES *edp, void** p_block );
    ER             (*getTimeout__T)( const struct tag_sGetFixedSizeMemoryPool_VDES *edp, void** p_block, TMO timeout );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sGetFixedSizeMemoryPool_Defined
#define  Descriptor_of_sGetFixedSizeMemoryPool_Defined
typedef struct { struct tag_sGetFixedSizeMemoryPool_VDES *vdes; } Descriptor( sGetFixedSizeMemoryPool );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SGETFIXEDSIZEMEMORYPOOL_GET     (1)
#define	FUNCID_SGETFIXEDSIZEMEMORYPOOL_GETPOLLING (2)
#define	FUNCID_SGETFIXEDSIZEMEMORYPOOL_GETTIMEOUT (3)

#endif /* sGetFixedSizeMemoryPool_TECSGEN_H */
