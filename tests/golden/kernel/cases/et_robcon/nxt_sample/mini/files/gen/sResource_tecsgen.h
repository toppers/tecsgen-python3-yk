/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sResource_TECSGEN_H
#define sResource_TECSGEN_H

/*
 * signature   :  sResource
 * global name :  sResource
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sResource_VDES {
    struct tag_sResource_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sResource_VMT {
    StatusType     (*get__T)( const struct tag_sResource_VDES *edp );
    StatusType     (*release__T)( const struct tag_sResource_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sResource_Defined
#define  Descriptor_of_sResource_Defined
typedef struct { struct tag_sResource_VDES *vdes; } Descriptor( sResource );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SRESOURCE_GET                   (1)
#define	FUNCID_SRESOURCE_RELEASE               (2)

#endif /* sResource_TECSGEN_H */
