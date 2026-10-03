/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tLCD_templ.c => src/tLCD.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * width            uint8_t          ATTR_width      
 * depth            uint8_t          ATTR_depth      
 *
 * 呼び口関数 #_TCPF_#
 * call port: cSPI signature: sSPI context:task
 *   void           cSPI_initialize( );
 *   void           cSPI_write( uint32_t CD, const uint8_t* data, uint32_t nBytes );
 *   void           cSPI_setDisplay( const uint8_t* display );
 *   void           cSPI_refresh( );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tLCD_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eLCD
 * entry port: eLCD
 * signature:  sLCD
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eLCD_initialize
 * name:         eLCD_initialize
 * global_name:  tLCD_eLCD_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eLCD_initialize(const uint8_t* display)
{
}

/* #[<ENTRY_FUNC>]# eLCD_powerOn
 * name:         eLCD_powerOn
 * global_name:  tLCD_eLCD_powerOn
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eLCD_powerOn(const uint8_t* display)
{
}

/* #[<ENTRY_FUNC>]# eLCD_powerOff
 * name:         eLCD_powerOff
 * global_name:  tLCD_eLCD_powerOff
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eLCD_powerOff()
{
}

/* #[<ENTRY_FUNC>]# eLCD_sendData
 * name:         eLCD_sendData
 * global_name:  tLCD_eLCD_sendData
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eLCD_sendData(const uint8_t* buffer)
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
