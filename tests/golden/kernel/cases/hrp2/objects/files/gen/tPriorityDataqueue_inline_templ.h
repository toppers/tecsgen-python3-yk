#ifndef tPriorityDataqueue__INLINE_H
#define tPriorityDataqueue__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tPriorityDataqueue_inline_template.h => src/tPriorityDataqueue_inline.h
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
/* #[<ENTRY_PORT>]# eSendPriorityDataqueue
 * entry port: eSendPriorityDataqueue
 * signature:  sSendPriorityDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSendPriorityDataqueue_send
 * name:         eSendPriorityDataqueue_send
 * global_name:  tPriorityDataqueue_eSendPriorityDataqueue_send
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendPriorityDataqueue_send(CELLIDX idx, intptr_t data, PRI dataPriority)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendPriorityDataqueue_send' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSendPriorityDataqueue_sendPolling
 * name:         eSendPriorityDataqueue_sendPolling
 * global_name:  tPriorityDataqueue_eSendPriorityDataqueue_sendPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendPriorityDataqueue_sendPolling(CELLIDX idx, intptr_t data, PRI dataPriority)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendPriorityDataqueue_sendPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSendPriorityDataqueue_sendTimeout
 * name:         eSendPriorityDataqueue_sendTimeout
 * global_name:  tPriorityDataqueue_eSendPriorityDataqueue_sendTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendPriorityDataqueue_sendTimeout(CELLIDX idx, intptr_t data, PRI dataPriority, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendPriorityDataqueue_sendTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReceivePriorityDataqueue
 * entry port: eReceivePriorityDataqueue
 * signature:  sReceivePriorityDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReceivePriorityDataqueue_receive
 * name:         eReceivePriorityDataqueue_receive
 * global_name:  tPriorityDataqueue_eReceivePriorityDataqueue_receive
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReceivePriorityDataqueue_receive(CELLIDX idx, intptr_t* p_data, PRI* p_dataPriority)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReceivePriorityDataqueue_receive' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eReceivePriorityDataqueue_receivePolling
 * name:         eReceivePriorityDataqueue_receivePolling
 * global_name:  tPriorityDataqueue_eReceivePriorityDataqueue_receivePolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReceivePriorityDataqueue_receivePolling(CELLIDX idx, intptr_t* p_data, PRI* p_dataPriority)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReceivePriorityDataqueue_receivePolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eReceivePriorityDataqueue_receiveTimeout
 * name:         eReceivePriorityDataqueue_receiveTimeout
 * global_name:  tPriorityDataqueue_eReceivePriorityDataqueue_receiveTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReceivePriorityDataqueue_receiveTimeout(CELLIDX idx, intptr_t* p_data, PRI* p_dataPriority, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReceivePriorityDataqueue_receiveTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eManagePriorityDataqueue
 * entry port: eManagePriorityDataqueue
 * signature:  sManagePriorityDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eManagePriorityDataqueue_initialize
 * name:         eManagePriorityDataqueue_initialize
 * global_name:  tPriorityDataqueue_eManagePriorityDataqueue_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eManagePriorityDataqueue_initialize(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eManagePriorityDataqueue_initialize' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReferPriorityDataqueue
 * entry port: eReferPriorityDataqueue
 * signature:  sReferPriorityDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReferPriorityDataqueue_refer
 * name:         eReferPriorityDataqueue_refer
 * global_name:  tPriorityDataqueue_eReferPriorityDataqueue_refer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReferPriorityDataqueue_refer(CELLIDX idx, T_RPDQ* pk_priorityDataqueueStatus)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReferPriorityDataqueue_refer' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eiPriorityDataqueue
 * entry port: eiPriorityDataqueue
 * signature:  siPriorityDataqueue
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiPriorityDataqueue_sendPolling
 * name:         eiPriorityDataqueue_sendPolling
 * global_name:  tPriorityDataqueue_eiPriorityDataqueue_sendPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eiPriorityDataqueue_sendPolling(CELLIDX idx, intptr_t data, PRI dataPriority)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eiPriorityDataqueue_sendPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tPriorityDataqueue_INLINEH */
