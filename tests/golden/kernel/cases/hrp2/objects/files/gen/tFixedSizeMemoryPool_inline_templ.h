#ifndef tFixedSizeMemoryPool__INLINE_H
#define tFixedSizeMemoryPool__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tFixedSizeMemoryPool_inline_template.h => src/tFixedSizeMemoryPool_inline.h
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * id               ID               ATTR_id         
 *
 * #[</PREAMBLE>]# */

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eGetFixedSizeMemoryPool
 * entry port: eGetFixedSizeMemoryPool
 * signature:  sGetFixedSizeMemoryPool
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eGetFixedSizeMemoryPool_get
 * name:         eGetFixedSizeMemoryPool_get
 * global_name:  tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eGetFixedSizeMemoryPool_get(CELLIDX idx, void** p_block)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eGetFixedSizeMemoryPool_get' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eGetFixedSizeMemoryPool_getPolling
 * name:         eGetFixedSizeMemoryPool_getPolling
 * global_name:  tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eGetFixedSizeMemoryPool_getPolling(CELLIDX idx, void** p_block)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eGetFixedSizeMemoryPool_getPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eGetFixedSizeMemoryPool_getTimeout
 * name:         eGetFixedSizeMemoryPool_getTimeout
 * global_name:  tFixedSizeMemoryPool_eGetFixedSizeMemoryPool_getTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eGetFixedSizeMemoryPool_getTimeout(CELLIDX idx, void** p_block, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eGetFixedSizeMemoryPool_getTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReleaseFixedSizeMemoryPool
 * entry port: eReleaseFixedSizeMemoryPool
 * signature:  sReleaseFixedSizeMemoryPool
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReleaseFixedSizeMemoryPool_release
 * name:         eReleaseFixedSizeMemoryPool_release
 * global_name:  tFixedSizeMemoryPool_eReleaseFixedSizeMemoryPool_release
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReleaseFixedSizeMemoryPool_release(CELLIDX idx, const void* block)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReleaseFixedSizeMemoryPool_release' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eManageFixedSizeMemoryPool
 * entry port: eManageFixedSizeMemoryPool
 * signature:  sManageFixedSizeMemoryPool
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eManageFixedSizeMemoryPool_initialize
 * name:         eManageFixedSizeMemoryPool_initialize
 * global_name:  tFixedSizeMemoryPool_eManageFixedSizeMemoryPool_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eManageFixedSizeMemoryPool_initialize(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eManageFixedSizeMemoryPool_initialize' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReferFixedSizeMemoryPool
 * entry port: eReferFixedSizeMemoryPool
 * signature:  sReferFixedSizeMemoryPool
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReferFixedSizeMemoryPool_refer
 * name:         eReferFixedSizeMemoryPool_refer
 * global_name:  tFixedSizeMemoryPool_eReferFixedSizeMemoryPool_refer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReferFixedSizeMemoryPool_refer(CELLIDX idx, T_RMPF* pk_memoryPoolFixedSizeStatus)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReferFixedSizeMemoryPool_refer' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tFixedSizeMemoryPool_INLINEH */
