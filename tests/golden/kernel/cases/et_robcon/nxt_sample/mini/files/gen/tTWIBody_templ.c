/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tTWIBody_templ.c => src/tTWIBody.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * clockDivisor     uint32_t         ATTR_clockDivisor
 * pending          uint32_t         VAR_pending     
 * buffer           uint8_t*         VAR_buffer      
 * state            uint8_t          VAR_state       
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tTWIBody_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eTWI
 * entry port: eTWI
 * signature:  sTWI
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eTWI_initialize
 * name:         eTWI_initialize
 * global_name:  tTWIBody_eTWI_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
bool_t
eTWI_initialize()
{
}

/* #[<ENTRY_FUNC>]# eTWI_startWrite
 * name:         eTWI_startWrite
 * global_name:  tTWIBody_eTWI_startWrite
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eTWI_startWrite(uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, const uint8_t* data, uint32_t nBytes)
{
}

/* #[<ENTRY_FUNC>]# eTWI_startRead
 * name:         eTWI_startRead
 * global_name:  tTWIBody_eTWI_startRead
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eTWI_startRead(uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, uint8_t* data, uint32_t nBytes)
{
}

/* #[<ENTRY_FUNC>]# eTWI_pollingUpdate
 * name:         eTWI_pollingUpdate
 * global_name:  tTWIBody_eTWI_pollingUpdate
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eTWI_pollingUpdate()
{
}

/* #[<ENTRY_FUNC>]# eTWI_isBusy
 * name:         eTWI_isBusy
 * global_name:  tTWIBody_eTWI_isBusy
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
bool_t
eTWI_isBusy()
{
}

/* #[<ENTRY_FUNC>]# eTWI_isOk
 * name:         eTWI_isOk
 * global_name:  tTWIBody_eTWI_isOk
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
bool_t
eTWI_isOk()
{
}

/* #[<ENTRY_FUNC>]# eTWI_reset
 * name:         eTWI_reset
 * global_name:  tTWIBody_eTWI_reset
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eTWI_reset()
{
}

/* #[<ENTRY_PORT>]# eiInterruptBody
 * entry port: eiInterruptBody
 * signature:  sHandlerBody
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiInterruptBody_main
 * name:         eiInterruptBody_main
 * global_name:  tTWIBody_eiInterruptBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eiInterruptBody_main()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
