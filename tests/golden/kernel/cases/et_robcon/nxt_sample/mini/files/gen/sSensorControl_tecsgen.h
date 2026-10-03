/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSensorControl_TECSGEN_H
#define sSensorControl_TECSGEN_H

/*
 * signature   :  sSensorControl
 * global name :  sSensorControl
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSensorControl_VDES {
    struct tag_sSensorControl_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSensorControl_VMT {
    void           (*on__T)( const struct tag_sSensorControl_VDES *edp );
    void           (*off__T)( const struct tag_sSensorControl_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSensorControl_Defined
#define  Descriptor_of_sSensorControl_Defined
typedef struct { struct tag_sSensorControl_VDES *vdes; } Descriptor( sSensorControl );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSENSORCONTROL_ON               (1)
#define	FUNCID_SSENSORCONTROL_OFF              (2)

#endif /* sSensorControl_TECSGEN_H */
