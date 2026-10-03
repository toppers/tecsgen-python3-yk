/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tSPIBody_templ.c => src/tSPIBody.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * display          uint8_t*         VAR_display     
 * dirty            volatile bool_t  VAR_dirty       
 * page             volatile uint8_t  VAR_page        
 * data             volatile uint8_t*  VAR_data        
 * mode             uint8_t          VAR_mode        
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tSPIBody_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eSPI
 * entry port: eSPI
 * signature:  sSPI
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSPI_initialize
 * name:         eSPI_initialize
 * global_name:  tSPIBody_eSPI_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eSPI_initialize()
{
}

/* #[<ENTRY_FUNC>]# eSPI_write
 * name:         eSPI_write
 * global_name:  tSPIBody_eSPI_write
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eSPI_write(uint32_t CD, const uint8_t* data, uint32_t nBytes)
{
}

/* #[<ENTRY_FUNC>]# eSPI_setDisplay
 * name:         eSPI_setDisplay
 * global_name:  tSPIBody_eSPI_setDisplay
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eSPI_setDisplay(const uint8_t* display)
{
}

/* #[<ENTRY_FUNC>]# eSPI_refresh
 * name:         eSPI_refresh
 * global_name:  tSPIBody_eSPI_refresh
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eSPI_refresh()
{
}

/* #[<ENTRY_PORT>]# eiInterruptBody
 * entry port: eiInterruptBody
 * signature:  sHandlerBody
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiInterruptBody_main
 * name:         eiInterruptBody_main
 * global_name:  tSPIBody_eiInterruptBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eiInterruptBody_main()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
