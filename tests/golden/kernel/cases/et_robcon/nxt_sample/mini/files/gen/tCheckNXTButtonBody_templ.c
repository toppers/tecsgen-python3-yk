/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tCheckNXTButtonBody_templ.c => src/tCheckNXTButtonBody.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * require port: signature:sKernelAlarmCallback context:task
 *   void           resumeAllInterrupts( );
 *   void           suspendAllInterrupts( );
 * call port: cButton signature: sButton context:task
 *   bool_t         cButton_isENTERButton( );
 *   bool_t         cButton_isRUNButton( );
 *   bool_t         cButton_isSTOPButton( );
 *   bool_t         cButton_isEXITButton( );
 *   bool_t         cButton_isENTERButtonOnly( );
 *   bool_t         cButton_isRUNButtonOnly( );
 *   bool_t         cButton_isSTOPButtonOnly( );
 *   bool_t         cButton_isEXITButtonOnly( );
 * call port: cFlash signature: sFlash context:task optional:true
 *   bool_t     is_cFlash_joined()                     check if joined
 *   void           cFlash_rewriteBios( );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tCheckNXTButtonBody_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eiBody
 * entry port: eiBody
 * signature:  sHandlerBody
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiBody_main
 * name:         eiBody_main
 * global_name:  tCheckNXTButtonBody_eiBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eiBody_main()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
