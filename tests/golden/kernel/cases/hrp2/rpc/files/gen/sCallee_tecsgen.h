/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sCallee_TECSGEN_H
#define sCallee_TECSGEN_H

/*
 * signature   :  sCallee
 * global name :  sCallee
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sCallee_VDES {
    struct tag_sCallee_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sCallee_VMT {
    ER             (*add__T)( const struct tag_sCallee_VDES *edp, int32_t a, int32_t b );
    int16_t        (*scale__T)( const struct tag_sCallee_VDES *edp, int8_t k, uint16_t v );
    int64_t        (*widen__T)( const struct tag_sCallee_VDES *edp, uint32_t v );
    void           (*notify__T)( const struct tag_sCallee_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sCallee_Defined
#define  Descriptor_of_sCallee_Defined
typedef struct { struct tag_sCallee_VDES *vdes; } Descriptor( sCallee );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SCALLEE_ADD                     (1)
#define	FUNCID_SCALLEE_SCALE                   (2)
#define	FUNCID_SCALLEE_WIDEN                   (3)
#define	FUNCID_SCALLEE_NOTIFY                  (4)

#endif /* sCallee_TECSGEN_H */
