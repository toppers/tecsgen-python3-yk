/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sTLSFStatistics_TECSGEN_H
#define sTLSFStatistics_TECSGEN_H

/*
 * signature   :  sTLSFStatistics
 * global name :  sTLSFStatistics
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sTLSFStatistics_VDES {
    struct tag_sTLSFStatistics_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sTLSFStatistics_VMT {
    size_t         (*getUsed__T)( const struct tag_sTLSFStatistics_VDES *edp );
    size_t         (*getMaxUsed__T)( const struct tag_sTLSFStatistics_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sTLSFStatistics_Defined
#define  Descriptor_of_sTLSFStatistics_Defined
typedef struct { struct tag_sTLSFStatistics_VDES *vdes; } Descriptor( sTLSFStatistics );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_STLSFSTATISTICS_GETUSED         (1)
#define	FUNCID_STLSFSTATISTICS_GETMAXUSED      (2)

#endif /* sTLSFStatistics_TECSGEN_H */
