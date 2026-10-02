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
/* #[<ENTRY_PORT>]# eSignalSemaphore
 * entry port: eSignalSemaphore
 * signature:  sSignalSemaphore
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSignalSemaphore_signal
 * name:         eSignalSemaphore_signal
 * global_name:  tSemaphore_eSignalSemaphore_signal
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSignalSemaphore_signal(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSignalSemaphore_signal' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eWaitSemaphore
 * entry port: eWaitSemaphore
 * signature:  sWaitSemaphore
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eWaitSemaphore_wait
 * name:         eWaitSemaphore_wait
 * global_name:  tSemaphore_eWaitSemaphore_wait
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eWaitSemaphore_wait(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eWaitSemaphore_wait' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eWaitSemaphore_waitPolling
 * name:         eWaitSemaphore_waitPolling
 * global_name:  tSemaphore_eWaitSemaphore_waitPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eWaitSemaphore_waitPolling(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eWaitSemaphore_waitPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eWaitSemaphore_waitTimeout
 * name:         eWaitSemaphore_waitTimeout
 * global_name:  tSemaphore_eWaitSemaphore_waitTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eWaitSemaphore_waitTimeout(CELLIDX idx, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eWaitSemaphore_waitTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eManageSemaphore
 * entry port: eManageSemaphore
 * signature:  sManageSemaphore
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eManageSemaphore_initialize
 * name:         eManageSemaphore_initialize
 * global_name:  tSemaphore_eManageSemaphore_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eManageSemaphore_initialize(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eManageSemaphore_initialize' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReferSemaphore
 * entry port: eReferSemaphore
 * signature:  sReferSemaphore
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReferSemaphore_refer
 * name:         eReferSemaphore_refer
 * global_name:  tSemaphore_eReferSemaphore_refer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReferSemaphore_refer(CELLIDX idx, T_RSEM* pk_semaphoreStatus)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReferSemaphore_refer' needs to be edited."   /* delete this line after edit */

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
