/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sCyclic_TECSGEN_H
#define sCyclic_TECSGEN_H

/*
 * signature   :  sCyclic
 * global name :  sCyclic
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sCyclic_VDES {
    struct tag_sCyclic_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sCyclic_VMT {
    void           (*start__T)( const struct tag_sCyclic_VDES *edp );
    void           (*stop__T)( const struct tag_sCyclic_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sCyclic_Defined
#define  Descriptor_of_sCyclic_Defined
typedef struct { struct tag_sCyclic_VDES *vdes; } Descriptor( sCyclic );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SCYCLIC_START                   (1)
#define	FUNCID_SCYCLIC_STOP                    (2)

#endif /* sCyclic_TECSGEN_H */
