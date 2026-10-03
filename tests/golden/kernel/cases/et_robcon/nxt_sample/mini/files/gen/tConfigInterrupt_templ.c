/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tConfigInterrupt_templ.c => src/tConfigInterrupt.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * interruptNumber  uint_t           ATTR_interruptNumber
 * attribute        uint_t           ATTR_attribute  
 * interruptPriority int_t            ATTR_interruptPriority
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tConfigInterrupt_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eConfigInterrupt
 * entry port: eConfigInterrupt
 * signature:  sConfigInterrupt
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eConfigInterrupt_enable
 * name:         eConfigInterrupt_enable
 * global_name:  tConfigInterrupt_eConfigInterrupt_enable
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eConfigInterrupt_enable(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eConfigInterrupt_enable' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eConfigInterrupt_disable
 * name:         eConfigInterrupt_disable
 * global_name:  tConfigInterrupt_eConfigInterrupt_disable
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eConfigInterrupt_disable(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eConfigInterrupt_disable' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_PORT>]# eStarupHookBody
 * entry port: eStarupHookBody
 * signature:  sHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eStarupHookBody_main
 * name:         eStarupHookBody_main
 * global_name:  tConfigInterrupt_eStarupHookBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eStarupHookBody_main(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eStarupHookBody_main' needs to be edited."   /* delete this line after edit */

}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
