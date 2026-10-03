/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sLCD_TECSGEN_H
#define sLCD_TECSGEN_H

/*
 * signature   :  sLCD
 * global name :  sLCD
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sLCD_VDES {
    struct tag_sLCD_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sLCD_VMT {
    void           (*initialize__T)( const struct tag_sLCD_VDES *edp, const uint8_t* display );
    void           (*powerOn__T)( const struct tag_sLCD_VDES *edp, const uint8_t* display );
    void           (*powerOff__T)( const struct tag_sLCD_VDES *edp );
    void           (*sendData__T)( const struct tag_sLCD_VDES *edp, const uint8_t* buffer );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sLCD_Defined
#define  Descriptor_of_sLCD_Defined
typedef struct { struct tag_sLCD_VDES *vdes; } Descriptor( sLCD );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SLCD_INITIALIZE                 (1)
#define	FUNCID_SLCD_POWERON                    (2)
#define	FUNCID_SLCD_POWEROFF                   (3)
#define	FUNCID_SLCD_SENDDATA                   (4)

#endif /* sLCD_TECSGEN_H */
