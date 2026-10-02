#ifndef tDataqueue__INLINE_H
#define tDataqueue__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tDataqueue_inline_template.h => src/tDataqueue_inline.h
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
/* #[<ENTRY_PORT>]# eSendDataqueue
 * entry port: eSendDataqueue
 * signature:  sSendDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSendDataqueue_send
 * name:         eSendDataqueue_send
 * global_name:  tDataqueue_eSendDataqueue_send
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendDataqueue_send(CELLIDX idx, intptr_t data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendDataqueue_send' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSendDataqueue_sendPolling
 * name:         eSendDataqueue_sendPolling
 * global_name:  tDataqueue_eSendDataqueue_sendPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendDataqueue_sendPolling(CELLIDX idx, intptr_t data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendDataqueue_sendPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSendDataqueue_sendTimeout
 * name:         eSendDataqueue_sendTimeout
 * global_name:  tDataqueue_eSendDataqueue_sendTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendDataqueue_sendTimeout(CELLIDX idx, intptr_t data, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendDataqueue_sendTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eSendDataqueue_sendForce
 * name:         eSendDataqueue_sendForce
 * global_name:  tDataqueue_eSendDataqueue_sendForce
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eSendDataqueue_sendForce(CELLIDX idx, intptr_t data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eSendDataqueue_sendForce' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReceiveDataqueue
 * entry port: eReceiveDataqueue
 * signature:  sReceiveDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReceiveDataqueue_receive
 * name:         eReceiveDataqueue_receive
 * global_name:  tDataqueue_eReceiveDataqueue_receive
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReceiveDataqueue_receive(CELLIDX idx, intptr_t* p_data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReceiveDataqueue_receive' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eReceiveDataqueue_receivePolling
 * name:         eReceiveDataqueue_receivePolling
 * global_name:  tDataqueue_eReceiveDataqueue_receivePolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReceiveDataqueue_receivePolling(CELLIDX idx, intptr_t* p_data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReceiveDataqueue_receivePolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eReceiveDataqueue_receiveTimeout
 * name:         eReceiveDataqueue_receiveTimeout
 * global_name:  tDataqueue_eReceiveDataqueue_receiveTimeout
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReceiveDataqueue_receiveTimeout(CELLIDX idx, intptr_t* p_data, TMO timeout)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReceiveDataqueue_receiveTimeout' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eManageDataqueue
 * entry port: eManageDataqueue
 * signature:  sManageDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eManageDataqueue_initialize
 * name:         eManageDataqueue_initialize
 * global_name:  tDataqueue_eManageDataqueue_initialize
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eManageDataqueue_initialize(CELLIDX idx)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eManageDataqueue_initialize' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eReferDataqueue
 * entry port: eReferDataqueue
 * signature:  sReferDataqueue
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eReferDataqueue_refer
 * name:         eReferDataqueue_refer
 * global_name:  tDataqueue_eReferDataqueue_refer
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eReferDataqueue_refer(CELLIDX idx, T_RDTQ* pk_dataqueueStatus)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eReferDataqueue_refer' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_PORT>]# eiDataqueue
 * entry port: eiDataqueue
 * signature:  siDataqueue
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiDataqueue_sendPolling
 * name:         eiDataqueue_sendPolling
 * global_name:  tDataqueue_eiDataqueue_sendPolling
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eiDataqueue_sendPolling(CELLIDX idx, intptr_t data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eiDataqueue_sendPolling' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<ENTRY_FUNC>]# eiDataqueue_sendForce
 * name:         eiDataqueue_sendForce
 * global_name:  tDataqueue_eiDataqueue_sendForce
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline ER
eiDataqueue_sendForce(CELLIDX idx, intptr_t data)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eiDataqueue_sendForce' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tDataqueue_INLINEH */
