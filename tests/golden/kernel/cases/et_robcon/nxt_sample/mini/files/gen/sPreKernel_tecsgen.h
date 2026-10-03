/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sPreKernel_TECSGEN_H
#define sPreKernel_TECSGEN_H

/*
 * signature   :  sPreKernel
 * global name :  sPreKernel
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sPreKernel_VDES {
    struct tag_sPreKernel_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sPreKernel_VMT {
    void           (*startOs__T)( const struct tag_sPreKernel_VDES *edp, AppModeType mode );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sPreKernel_Defined
#define  Descriptor_of_sPreKernel_Defined
typedef struct { struct tag_sPreKernel_VDES *vdes; } Descriptor( sPreKernel );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SPREKERNEL_STARTOS              (1)

#endif /* sPreKernel_TECSGEN_H */
