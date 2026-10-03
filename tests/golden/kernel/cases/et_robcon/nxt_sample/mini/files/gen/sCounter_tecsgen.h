/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sCounter_TECSGEN_H
#define sCounter_TECSGEN_H

/*
 * signature   :  sCounter
 * global name :  sCounter
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sCounter_VDES {
    struct tag_sCounter_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sCounter_VMT {
    StatusType     (*signal__T)( const struct tag_sCounter_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sCounter_Defined
#define  Descriptor_of_sCounter_Defined
typedef struct { struct tag_sCounter_VDES *vdes; } Descriptor( sCounter );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SCOUNTER_SIGNAL                 (1)

#endif /* sCounter_TECSGEN_H */
