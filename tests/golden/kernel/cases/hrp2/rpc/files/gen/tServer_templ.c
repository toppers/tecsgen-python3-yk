/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tServer_templ.c => src/tServer.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tServer_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eCallee
 * entry port: eCallee
 * signature:  sCallee
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eCallee_add
 * name:         eCallee_add
 * global_name:  tServer_eCallee_add
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
ER
eCallee_add(CELLIDX idx, int32_t a, int32_t b)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eCallee_add' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eCallee_scale
 * name:         eCallee_scale
 * global_name:  tServer_eCallee_scale
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
int16_t
eCallee_scale(CELLIDX idx, int8_t k, uint16_t v)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eCallee_scale' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eCallee_widen
 * name:         eCallee_widen
 * global_name:  tServer_eCallee_widen
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
int64_t
eCallee_widen(CELLIDX idx, uint32_t v)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eCallee_widen' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eCallee_notify
 * name:         eCallee_notify
 * global_name:  tServer_eCallee_notify
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eCallee_notify(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eCallee_notify' needs to be edited."   /* delete this line after edit */

}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
