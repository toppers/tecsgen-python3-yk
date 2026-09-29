/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tZmodemToppers_templ.c => src/tZmodemToppers.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * call port: cZmodemTask signature: sTask context:task
 *   ER             cZmodemTask_activate( );
 *   ER_UINT        cZmodemTask_cancelActivate( );
 *   ER             cZmodemTask_terminate( );
 *   ER             cZmodemTask_changePriority( PRI priority );
 *   ER             cZmodemTask_getPriority( PRI* p_priority );
 *   ER             cZmodemTask_refer( T_RTSK* pk_taskStatus );
 *   ER             cZmodemTask_wakeup( );
 *   ER_UINT        cZmodemTask_cancelWakeup( );
 *   ER             cZmodemTask_releaseWait( );
 *   ER             cZmodemTask_suspend( );
 *   ER             cZmodemTask_resume( );
 *   ER             cZmodemTask_raiseException( TEXPTN pattern );
 *   ER             cZmodemTask_referException( T_RTEX* pk_rtex );
 *   ER             cZmodemTask_startOverRunHandler( OVRTIM ovrtim );
 *   ER             cZmodemTask_stopOverRunHandler( );
 *   ER             cZmodemTask_referOverRunHandler( T_ROVR* pk_rovr );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tZmodemToppers_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eBody
 * entry port: eBody
 * signature:  sTaskBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eBody_main
 * name:         eBody_main
 * global_name:  tZmodemToppers_eBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eBody_main(CELLIDX idx)
{
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eBody_main' needs to be edited."   /* delete this line after edit */

}

/* #[<ENTRY_PORT>]# eZmodemToppers
 * entry port: eZmodemToppers
 * signature:  sZmodemToppers
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eZmodemToppers_zmodem_recv_file
 * name:         eZmodemToppers_zmodem_recv_file
 * global_name:  tZmodemToppers_eZmodemToppers_zmodem_recv_file
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
ER
eZmodemToppers_zmodem_recv_file(CELLIDX idx, ID portid, const uint8_t* buf, uint32_t size, SIZE* filesz)
{
	ER		ercd = E_OK;
	CELLCB	*p_cellcb = GET_CELLCB(idx);

	/* ここに処理本体を記述します #_TEFB_# */
#warning "'eZmodemToppers_zmodem_recv_file' needs to be edited."   /* delete this line after edit */

	return(ercd);
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
