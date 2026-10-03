/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSPI_TECSGEN_H
#define sSPI_TECSGEN_H

/*
 * signature   :  sSPI
 * global name :  sSPI
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSPI_VDES {
    struct tag_sSPI_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSPI_VMT {
    void           (*initialize__T)( const struct tag_sSPI_VDES *edp );
    void           (*write__T)( const struct tag_sSPI_VDES *edp, uint32_t CD, const uint8_t* data, uint32_t nBytes );
    void           (*setDisplay__T)( const struct tag_sSPI_VDES *edp, const uint8_t* display );
    void           (*refresh__T)( const struct tag_sSPI_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSPI_Defined
#define  Descriptor_of_sSPI_Defined
typedef struct { struct tag_sSPI_VDES *vdes; } Descriptor( sSPI );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSPI_INITIALIZE                 (1)
#define	FUNCID_SSPI_WRITE                      (2)
#define	FUNCID_SSPI_SETDISPLAY                 (3)
#define	FUNCID_SSPI_REFRESH                    (4)

#endif /* sSPI_TECSGEN_H */
