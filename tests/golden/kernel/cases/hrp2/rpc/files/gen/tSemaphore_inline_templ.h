#ifndef tSemaphore__INLINE_H
#define tSemaphore__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tSemaphore_inline_template.h => src/tSemaphore_inline.h
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
/* #[<ENTRY_PORT>]# eSemaphore
 * entry port: eSemaphore
 * signature:  sSemaphore
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSemaphore_signal
 * name:         eSemaphore_signal
 * global_name:  tSemaphore_eSemaphore_signal
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSemaphore_signal(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSemaphore_signal' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSemaphore_wait
 * name:         eSemaphore_wait
 * global_name:  tSemaphore_eSemaphore_wait
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSemaphore_wait(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSemaphore_wait' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSemaphore_waitPolling
 * name:         eSemaphore_waitPolling
 * global_name:  tSemaphore_eSemaphore_waitPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSemaphore_waitPolling(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSemaphore_waitPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSemaphore_waitTimeout
 * name:         eSemaphore_waitTimeout
 * global_name:  tSemaphore_eSemaphore_waitTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSemaphore_waitTimeout(CELLIDX idx, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSemaphore_waitTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSemaphore_initialize
 * name:         eSemaphore_initialize
 * global_name:  tSemaphore_eSemaphore_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSemaphore_initialize(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSemaphore_initialize' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSemaphore_refer
 * name:         eSemaphore_refer
 * global_name:  tSemaphore_eSemaphore_refer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSemaphore_refer(CELLIDX idx, T_RSEM* pk_semaphoreStatus)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSemaphore_refer' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eiSemaphore
 * entry port: eiSemaphore
 * signature:  siSemaphore
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiSemaphore_signal
 * name:         eiSemaphore_signal
 * global_name:  tSemaphore_eiSemaphore_signal
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eiSemaphore_signal(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eiSemaphore_signal' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tSemaphore_INLINEH */
