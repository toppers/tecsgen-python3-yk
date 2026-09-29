/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sZmodemToppers_TECSGEN_H
#define sZmodemToppers_TECSGEN_H

/*
 * signature   :  sZmodemToppers
 * global name :  sZmodemToppers
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sZmodemToppers_VDES {
    struct tag_sZmodemToppers_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sZmodemToppers_VMT {
    ER             (*zmodem_recv_file__T)( const struct tag_sZmodemToppers_VDES *edp, ID portid, const uint8_t* buf, uint32_t size, SIZE* filesz );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sZmodemToppers_Defined
#define  Descriptor_of_sZmodemToppers_Defined
typedef struct { struct tag_sZmodemToppers_VDES *vdes; } Descriptor( sZmodemToppers );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SZMODEMTOPPERS_ZMODEM_RECV_FILE (1)

#endif /* sZmodemToppers_TECSGEN_H */
