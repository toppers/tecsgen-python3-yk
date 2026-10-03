/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sSensorPort_TECSGEN_H
#define sSensorPort_TECSGEN_H

/*
 * signature   :  sSensorPort
 * global name :  sSensorPort
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sSensorPort_VDES {
    struct tag_sSensorPort_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sSensorPort_VMT {
    void           (*clearSCL__T)( const struct tag_sSensorPort_VDES *edp );
    void           (*clearSDA__T)( const struct tag_sSensorPort_VDES *edp );
    void           (*setSCL__T)( const struct tag_sSensorPort_VDES *edp );
    void           (*setSDA__T)( const struct tag_sSensorPort_VDES *edp );
    void           (*inputPower__T)( const struct tag_sSensorPort_VDES *edp, uint8_t powerType );
    uint16_t       (*getValue__T)( const struct tag_sSensorPort_VDES *edp );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sSensorPort_Defined
#define  Descriptor_of_sSensorPort_Defined
typedef struct { struct tag_sSensorPort_VDES *vdes; } Descriptor( sSensorPort );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSENSORPORT_CLEARSCL            (1)
#define	FUNCID_SSENSORPORT_CLEARSDA            (2)
#define	FUNCID_SSENSORPORT_SETSCL              (3)
#define	FUNCID_SSENSORPORT_SETSDA              (4)
#define	FUNCID_SSENSORPORT_INPUTPOWER          (5)
#define	FUNCID_SSENSORPORT_GETVALUE            (6)

#endif /* sSensorPort_TECSGEN_H */
