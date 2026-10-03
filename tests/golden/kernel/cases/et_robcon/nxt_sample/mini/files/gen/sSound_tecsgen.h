/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSound_TECSGEN_H
#define sSound_TECSGEN_H

/*
 * signature   :  sSound
 * global name :  sSound
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSound_VDES {
    struct tag_sSound_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSound_VMT {
    void           (*beepTone__T)( const struct tag_sSound_VDES *edp, uint32_t frequency, uint32_t msecond );
    void           (*setVolume__T)( const struct tag_sSound_VDES *edp, uint8_t volume );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSound_Defined
#define  Descriptor_of_sSound_Defined
typedef struct { struct tag_sSound_VDES *vdes; } Descriptor( sSound );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSOUND_BEEPTONE                 (1)
#define	FUNCID_SSOUND_SETVOLUME                (2)

#endif /* sSound_TECSGEN_H */
