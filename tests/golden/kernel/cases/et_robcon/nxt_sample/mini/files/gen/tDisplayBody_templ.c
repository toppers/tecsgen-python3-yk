/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tDisplayBody_templ.c => src/tDisplayBody.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * width            uint8_t          ATTR_width      
 * depth            uint8_t          ATTR_depth      
 * cellWidth        uint8_t          ATTR_cellWidth  
 * charWidth        uint8_t          ATTR_charWidth  
 * charDepth        uint8_t          ATTR_charDepth  
 * buffer           uint8_t*         VAR_buffer      
 * currentX         uint8_t          VAR_currentX    
 * currentY         uint8_t          VAR_currentY    
 *
 * 呼び口関数 #_TCPF_#
 * call port: cLCD signature: sLCD context:task
 *   void           cLCD_initialize( const uint8_t* display );
 *   void           cLCD_powerOn( const uint8_t* display );
 *   void           cLCD_powerOff( );
 *   void           cLCD_sendData( const uint8_t* buffer );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tDisplayBody_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eDisplay
 * entry port: eDisplay
 * signature:  sDisplay
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eDisplay_update
 * name:         eDisplay_update
 * global_name:  tDisplayBody_eDisplay_update
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_update()
{
}

/* #[<ENTRY_FUNC>]# eDisplay_clear
 * name:         eDisplay_clear
 * global_name:  tDisplayBody_eDisplay_clear
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_clear(bool_t updateToo)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_gotoXY
 * name:         eDisplay_gotoXY
 * global_name:  tDisplayBody_eDisplay_gotoXY
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_gotoXY(uint8_t x, uint8_t y)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_putChar
 * name:         eDisplay_putChar
 * global_name:  tDisplayBody_eDisplay_putChar
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_putChar(char_t c)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_putString
 * name:         eDisplay_putString
 * global_name:  tDisplayBody_eDisplay_putString
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_putString(const char_t* string)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_putInt
 * name:         eDisplay_putInt
 * global_name:  tDisplayBody_eDisplay_putInt
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_putInt(int32_t val, uint8_t places)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_putUnsigned
 * name:         eDisplay_putUnsigned
 * global_name:  tDisplayBody_eDisplay_putUnsigned
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_putUnsigned(uint32_t val, uint8_t places)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_putHex
 * name:         eDisplay_putHex
 * global_name:  tDisplayBody_eDisplay_putHex
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_putHex(uint32_t val, uint8_t places)
{
}

/* #[<ENTRY_FUNC>]# eDisplay_getBuffer
 * name:         eDisplay_getBuffer
 * global_name:  tDisplayBody_eDisplay_getBuffer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
uint8_t*
eDisplay_getBuffer()
{
}

/* #[<ENTRY_FUNC>]# eDisplay_powerOff
 * name:         eDisplay_powerOff
 * global_name:  tDisplayBody_eDisplay_powerOff
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eDisplay_powerOff(bool_t updateToo)
{
}

/* #[<ENTRY_PORT>]# eInitialize
 * entry port: eInitialize
 * signature:  sHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eInitialize_main
 * name:         eInitialize_main
 * global_name:  tDisplayBody_eInitialize_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eInitialize_main()
{
}

/* #[<ENTRY_PORT>]# eTerminate
 * entry port: eTerminate
 * signature:  sStatusTypeHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eTerminate_main
 * name:         eTerminate_main
 * global_name:  tDisplayBody_eTerminate_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eTerminate_main(StatusType ercd)
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
