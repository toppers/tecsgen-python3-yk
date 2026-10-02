#ifndef tEventflag__INLINE_H
#define tEventflag__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tEventflag_inline_template.h => src/tEventflag_inline.h
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
/* #[<ENTRY_PORT>]# eSetEventflag
 * entry port: eSetEventflag
 * signature:  sSetEventflag
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSetEventflag_set
 * name:         eSetEventflag_set
 * global_name:  tEventflag_eSetEventflag_set
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSetEventflag_set(CELLIDX idx, FLGPTN setPattern)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSetEventflag_set' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSetEventflag_clear
 * name:         eSetEventflag_clear
 * global_name:  tEventflag_eSetEventflag_clear
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSetEventflag_clear(CELLIDX idx, FLGPTN clearPattern)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSetEventflag_clear' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eWaitEventflag
 * entry port: eWaitEventflag
 * signature:  sWaitEventflag
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eWaitEventflag_wait
 * name:         eWaitEventflag_wait
 * global_name:  tEventflag_eWaitEventflag_wait
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eWaitEventflag_wait(CELLIDX idx, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eWaitEventflag_wait' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eWaitEventflag_waitPolling
 * name:         eWaitEventflag_waitPolling
 * global_name:  tEventflag_eWaitEventflag_waitPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eWaitEventflag_waitPolling(CELLIDX idx, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eWaitEventflag_waitPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eWaitEventflag_waitTimeout
 * name:         eWaitEventflag_waitTimeout
 * global_name:  tEventflag_eWaitEventflag_waitTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eWaitEventflag_waitTimeout(CELLIDX idx, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eWaitEventflag_waitTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eManageEventflag
 * entry port: eManageEventflag
 * signature:  sManageEventflag
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eManageEventflag_initialize
 * name:         eManageEventflag_initialize
 * global_name:  tEventflag_eManageEventflag_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eManageEventflag_initialize(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eManageEventflag_initialize' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReferEventflag
 * entry port: eReferEventflag
 * signature:  sReferEventflag
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReferEventflag_refer
 * name:         eReferEventflag_refer
 * global_name:  tEventflag_eReferEventflag_refer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReferEventflag_refer(CELLIDX idx, T_RFLG* pk_eventflagStatus)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReferEventflag_refer' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eiEventflag
 * entry port: eiEventflag
 * signature:  siEventflag
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiEventflag_set
 * name:         eiEventflag_set
 * global_name:  tEventflag_eiEventflag_set
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eiEventflag_set(CELLIDX idx, FLGPTN setPattern)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eiEventflag_set' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tEventflag_INLINEH */
