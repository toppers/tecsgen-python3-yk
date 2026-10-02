/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReferFixedSizeMemoryPool_TECSGEN_H
#define sReferFixedSizeMemoryPool_TECSGEN_H

/*
 * signature   :  sReferFixedSizeMemoryPool
 * global name :  sReferFixedSizeMemoryPool
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReferFixedSizeMemoryPool_VDES {
    struct tag_sReferFixedSizeMemoryPool_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReferFixedSizeMemoryPool_VMT {
    ER             (*refer__T)( const struct tag_sReferFixedSizeMemoryPool_VDES *edp, T_RMPF* pk_memoryPoolFixedSizeStatus );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReferFixedSizeMemoryPool_Defined
#define  Descriptor_of_sReferFixedSizeMemoryPool_Defined
typedef struct { struct tag_sReferFixedSizeMemoryPool_VDES *vdes; } Descriptor( sReferFixedSizeMemoryPool );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SREFERFIXEDSIZEMEMORYPOOL_REFER (1)

#endif /* sReferFixedSizeMemoryPool_TECSGEN_H */
