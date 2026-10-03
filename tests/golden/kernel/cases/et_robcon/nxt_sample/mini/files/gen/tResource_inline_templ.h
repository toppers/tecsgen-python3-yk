#ifndef tResource__INLINE_H
#define tResource__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tResource_inline_template.h => src/tResource_inline.h
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * id               UINT8            ATTR_id         
 *
 * #[</PREAMBLE>]# */

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eResource
 * entry port: eResource
 * signature:  sResource
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eResource_get
 * name:         eResource_get
 * global_name:  tResource_eResource_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eResource_get(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eResource_get' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eResource_release
 * name:         eResource_release
 * global_name:  tResource_eResource_release
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eResource_release(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eResource_release' needs to be edited."   /* delete this line after edit */

}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tResource_INLINEH */
