#ifndef tAlarm__INLINE_H
#define tAlarm__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tAlarm_inline_template.h => src/tAlarm_inline.h
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * id               UINT8            ATTR_id         
 *
 * 呼び口関数 #_TCPF_#
 * call port: cBody signature: sHandlerBody context:non-task optional:true
 *   bool_t     is_cBody_joined()                     check if joined
 *   void           cBody_main( );
 *
 * #[</PREAMBLE>]# */

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eAlarm
 * entry port: eAlarm
 * signature:  sAlarm
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAlarm_getBase
 * name:         eAlarm_getBase
 * global_name:  tAlarm_eAlarm_getBase
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarm_getBase(CELLIDX idx, AlarmBaseRefType p_info)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarm_getBase' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eAlarm_get
 * name:         eAlarm_get
 * global_name:  tAlarm_eAlarm_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarm_get(CELLIDX idx, TickRefType p_tick)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarm_get' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eAlarm_setRelative
 * name:         eAlarm_setRelative
 * global_name:  tAlarm_eAlarm_setRelative
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarm_setRelative(CELLIDX idx, TickType incr, TickType cycle)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarm_setRelative' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eAlarm_setAbsolute
 * name:         eAlarm_setAbsolute
 * global_name:  tAlarm_eAlarm_setAbsolute
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarm_setAbsolute(CELLIDX idx, TickType start, TickType cycle)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarm_setAbsolute' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eAlarm_cancel
 * name:         eAlarm_cancel
 * global_name:  tAlarm_eAlarm_cancel
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarm_cancel(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarm_cancel' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_PORT>]# eAlarmHook
 * entry port: eAlarmHook
 * signature:  sAlarmHook
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAlarmHook_getBase
 * name:         eAlarmHook_getBase
 * global_name:  tAlarm_eAlarmHook_getBase
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarmHook_getBase(CELLIDX idx, AlarmBaseRefType p_info)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarmHook_getBase' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_FUNC>]# eAlarmHook_get
 * name:         eAlarmHook_get
 * global_name:  tAlarm_eAlarmHook_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eAlarmHook_get(CELLIDX idx, TickRefType p_tick)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eAlarmHook_get' needs to be edited."   /* delete this line after edit */

}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tAlarm_INLINEH */
