/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tUser_templ.c => src/tUser.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * call port: cSignalSemaphore signature: sSignalSemaphore context:task
 *   ER             cSignalSemaphore_signal( );
 * call port: cSetEventflag signature: sSetEventflag context:task
 *   ER             cSetEventflag_set( FLGPTN setPattern );
 *   ER             cSetEventflag_clear( FLGPTN clearPattern );
 * call port: cSendDataqueue signature: sSendDataqueue context:task
 *   ER             cSendDataqueue_send( intptr_t data );
 *   ER             cSendDataqueue_sendPolling( intptr_t data );
 *   ER             cSendDataqueue_sendTimeout( intptr_t data, TMO timeout );
 *   ER             cSendDataqueue_sendForce( intptr_t data );
 * call port: cSendPriorityDataqueue signature: sSendPriorityDataqueue context:task
 *   ER             cSendPriorityDataqueue_send( intptr_t data, PRI dataPriority );
 *   ER             cSendPriorityDataqueue_sendPolling( intptr_t data, PRI dataPriority );
 *   ER             cSendPriorityDataqueue_sendTimeout( intptr_t data, PRI dataPriority, TMO timeout );
 * call port: cGetFixedSizeMemoryPool signature: sGetFixedSizeMemoryPool context:task
 *   ER             cGetFixedSizeMemoryPool_get( void** p_block );
 *   ER             cGetFixedSizeMemoryPool_getPolling( void** p_block );
 *   ER             cGetFixedSizeMemoryPool_getTimeout( void** p_block, TMO timeout );
 * call port: cCallee signature: sCallee context:task
 *   ER             cCallee_add( int32_t a, int32_t b, int32_t* sum );
 *   void           cCallee_notify( );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tUser_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
