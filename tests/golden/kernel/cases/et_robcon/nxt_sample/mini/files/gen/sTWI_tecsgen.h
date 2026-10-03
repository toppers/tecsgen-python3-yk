/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sTWI_TECSGEN_H
#define sTWI_TECSGEN_H

/*
 * signature   :  sTWI
 * global name :  sTWI
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sTWI_VDES {
    struct tag_sTWI_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sTWI_VMT {
    bool_t         (*initialize__T)( const struct tag_sTWI_VDES *edp );
    void           (*startWrite__T)( const struct tag_sTWI_VDES *edp, uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, const uint8_t* data, uint32_t nBytes );
    void           (*startRead__T)( const struct tag_sTWI_VDES *edp, uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, uint8_t* data, uint32_t nBytes );
    void           (*pollingUpdate__T)( const struct tag_sTWI_VDES *edp );
    bool_t         (*isBusy__T)( const struct tag_sTWI_VDES *edp );
    bool_t         (*isOk__T)( const struct tag_sTWI_VDES *edp );
    void           (*reset__T)( const struct tag_sTWI_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sTWI_Defined
#define  Descriptor_of_sTWI_Defined
typedef struct { struct tag_sTWI_VDES *vdes; } Descriptor( sTWI );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_STWI_INITIALIZE                 (1)
#define	FUNCID_STWI_STARTWRITE                 (2)
#define	FUNCID_STWI_STARTREAD                  (3)
#define	FUNCID_STWI_POLLINGUPDATE              (4)
#define	FUNCID_STWI_ISBUSY                     (5)
#define	FUNCID_STWI_ISOK                       (6)
#define	FUNCID_STWI_RESET                      (7)

#endif /* sTWI_TECSGEN_H */
