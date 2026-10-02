/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sStartCyclic_TECSGEN_H
#define sStartCyclic_TECSGEN_H

/*
 * signature   :  sStartCyclic
 * global name :  sStartCyclic
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sStartCyclic_VDES {
    struct tag_sStartCyclic_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sStartCyclic_VMT {
    ER             (*start__T)( const struct tag_sStartCyclic_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sStartCyclic_Defined
#define  Descriptor_of_sStartCyclic_Defined
typedef struct { struct tag_sStartCyclic_VDES *vdes; } Descriptor( sStartCyclic );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSTARTCYCLIC_START              (1)

#endif /* sStartCyclic_TECSGEN_H */
