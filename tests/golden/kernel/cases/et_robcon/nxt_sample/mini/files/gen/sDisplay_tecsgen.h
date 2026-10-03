/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sDisplay_TECSGEN_H
#define sDisplay_TECSGEN_H

/*
 * signature   :  sDisplay
 * global name :  sDisplay
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sDisplay_VDES {
    struct tag_sDisplay_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sDisplay_VMT {
    void           (*update__T)( const struct tag_sDisplay_VDES *edp );
    void           (*clear__T)( const struct tag_sDisplay_VDES *edp, bool_t updateToo );
    void           (*gotoXY__T)( const struct tag_sDisplay_VDES *edp, uint8_t x, uint8_t y );
    void           (*putChar__T)( const struct tag_sDisplay_VDES *edp, char_t c );
    void           (*putString__T)( const struct tag_sDisplay_VDES *edp, const char_t* string );
    void           (*putInt__T)( const struct tag_sDisplay_VDES *edp, int32_t val, uint8_t places );
    void           (*putUnsigned__T)( const struct tag_sDisplay_VDES *edp, uint32_t val, uint8_t places );
    void           (*putHex__T)( const struct tag_sDisplay_VDES *edp, uint32_t val, uint8_t places );
    uint8_t*       (*getBuffer__T)( const struct tag_sDisplay_VDES *edp );
    void           (*powerOff__T)( const struct tag_sDisplay_VDES *edp, bool_t updateToo );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sDisplay_Defined
#define  Descriptor_of_sDisplay_Defined
typedef struct { struct tag_sDisplay_VDES *vdes; } Descriptor( sDisplay );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SDISPLAY_UPDATE                 (1)
#define	FUNCID_SDISPLAY_CLEAR                  (2)
#define	FUNCID_SDISPLAY_GOTOXY                 (3)
#define	FUNCID_SDISPLAY_PUTCHAR                (4)
#define	FUNCID_SDISPLAY_PUTSTRING              (5)
#define	FUNCID_SDISPLAY_PUTINT                 (6)
#define	FUNCID_SDISPLAY_PUTUNSIGNED            (7)
#define	FUNCID_SDISPLAY_PUTHEX                 (8)
#define	FUNCID_SDISPLAY_GETBUFFER              (9)
#define	FUNCID_SDISPLAY_POWEROFF               (10)

#endif /* sDisplay_TECSGEN_H */
