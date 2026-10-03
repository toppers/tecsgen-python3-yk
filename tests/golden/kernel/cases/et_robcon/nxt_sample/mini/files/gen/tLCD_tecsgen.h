/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tLCD_TECSGEN_H
#define tLCD_TECSGEN_H

/*
 * celltype          :  tLCD
 * global name       :  tLCD
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  yes
 * has_CB            :  no
 * has_INIB          :  yes
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sLCD_tecsgen.h"
#include "sSPI_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tLCD_INIB {
    /* call port #_TCP_# */
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    uint8_t        width;
    uint8_t        depth;
}  tLCD_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tLCD_SINGLE_CELL_CB   tLCD_SINGLE_CELL_INIB
#define tLCD_CB               tLCD_INIB
#define tag_tLCD_CB           tag_tLCD_INIB

/* シングルトンセル CB プロトタイプ宣言 #_SCP_# */
extern  tLCD_INIB  tLCD_SINGLE_CELL_INIB;


/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tLCD_INIB *tLCD_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sLCD */
void         tLCD_eLCD_initialize( const uint8_t* display);
void         tLCD_eLCD_powerOn( const uint8_t* display);
void         tLCD_eLCD_powerOff();
void         tLCD_eLCD_sendData( const uint8_t* buffer);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* 最適化のため参照するセルタイプの CB 型の定義を取込む #_ICT_# */
#ifndef  TOPPERS_CB_TYPE_ONLY
#define  tLCD_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#endif  /* TOPPERS_CB_TYPE_ONLY */
#include "tSPIBody_tecsgen.h"
#ifdef  tLCD_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY
#endif /* tLCD_CB_TYPE_ONLY */
#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ #_GCB_# */
#define tLCD_GET_CELLCB(idx) ((void *)0)

/* 属性アクセスマクロ #_AAM_# */
#define tLCD_ATTR_width     	(tLCD_SINGLE_CELL_INIB.width)
#define tLCD_ATTR_depth     	(tLCD_SINGLE_CELL_INIB.depth)

#define tLCD_GET_width()    	(tLCD_SINGLE_CELL_INIB.width)
#define tLCD_GET_depth()    	(tLCD_SINGLE_CELL_INIB.depth)



#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tLCD_cSPI_initialize( ) \
	  tSPIBody_eSPI_initialize( \
	    )
#define tLCD_cSPI_write( CD, data, nBytes ) \
	  tSPIBody_eSPI_write( \
	    (CD), (data), (nBytes) )
#define tLCD_cSPI_setDisplay( display ) \
	  tSPIBody_eSPI_setDisplay( \
	    (display) )
#define tLCD_cSPI_refresh( ) \
	  tSPIBody_eSPI_refresh( \
	    )

#else  /* TECSFLOW */
#define tLCD_cSPI_initialize( ) \
	  (p_that)->cSPI.initialize__T( \
 )
#define tLCD_cSPI_write( CD, data, nBytes ) \
	  (p_that)->cSPI.write__T( \
 (CD), (data), (nBytes) )
#define tLCD_cSPI_setDisplay( display ) \
	  (p_that)->cSPI.setDisplay__T( \
 (display) )
#define tLCD_cSPI_refresh( ) \
	  (p_that)->cSPI.refresh__T( \
 )

#endif /* TECSFLOW */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */

#ifndef TOPPERS_CB_TYPE_ONLY

#endif /* TOPPERS_CB_TYPE_ONLY */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#ifndef TOPPERS_CB_TYPE_ONLY


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tLCD_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tLCD_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tLCD_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_width           tLCD_ATTR_width
#define ATTR_depth           tLCD_ATTR_depth


/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cSPI_initialize( ) \
          tLCD_cSPI_initialize( )
#define cSPI_write( CD, data, nBytes ) \
          tLCD_cSPI_write( CD, data, nBytes )
#define cSPI_setDisplay( display ) \
          tLCD_cSPI_setDisplay( display )
#define cSPI_refresh( ) \
          tLCD_cSPI_refresh( )




/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eLCD_initialize  tLCD_eLCD_initialize
#define eLCD_powerOn     tLCD_eLCD_powerOn
#define eLCD_powerOff    tLCD_eLCD_powerOff
#define eLCD_sendData    tLCD_eLCD_sendData

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB()
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#endif /* TOPPERS_CB_TYPE_ONLY */

#ifndef TOPPERS_MACRO_ONLY

#endif /* TOPPERS_MACRO_ONLY */

#endif /* tLCD_TECSGENH */
