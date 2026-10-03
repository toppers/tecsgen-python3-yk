/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sAvrPower_TECSGEN_H
#define sAvrPower_TECSGEN_H

/*
 * signature   :  sAvrPower
 * global name :  sAvrPower
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sAvrPower_VDES {
    struct tag_sAvrPower_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sAvrPower_VMT {
    void           (*powerDown__T)( const struct tag_sAvrPower_VDES *edp );
    void           (*update__T)( const struct tag_sAvrPower_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sAvrPower_Defined
#define  Descriptor_of_sAvrPower_Defined
typedef struct { struct tag_sAvrPower_VDES *vdes; } Descriptor( sAvrPower );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SAVRPOWER_POWERDOWN             (1)
#define	FUNCID_SAVRPOWER_UPDATE                (2)

#endif /* sAvrPower_TECSGEN_H */
