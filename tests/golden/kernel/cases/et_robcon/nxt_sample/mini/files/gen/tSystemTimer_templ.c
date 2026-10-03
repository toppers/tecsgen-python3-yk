/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tSystemTimer_templ.c => src/tSystemTimer.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * call port: cCounter signature: sCounter context:task
 *   StatusType     cCounter_signal( );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tSystemTimer_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eInterruptBody
 * entry port: eInterruptBody
 * signature:  sHandlerBody
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eInterruptBody_main
 * name:         eInterruptBody_main
 * global_name:  tSystemTimer_eInterruptBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eInterruptBody_main()
{
}

/* #[<ENTRY_PORT>]# eStartupHookBody
 * entry port: eStartupHookBody
 * signature:  sHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eStartupHookBody_main
 * name:         eStartupHookBody_main
 * global_name:  tSystemTimer_eStartupHookBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eStartupHookBody_main()
{
}

/* #[<ENTRY_PORT>]# eShutdownHookBody
 * entry port: eShutdownHookBody
 * signature:  sStatusTypeHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eShutdownHookBody_main
 * name:         eShutdownHookBody_main
 * global_name:  tSystemTimer_eShutdownHookBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eShutdownHookBody_main(StatusType ercd)
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
