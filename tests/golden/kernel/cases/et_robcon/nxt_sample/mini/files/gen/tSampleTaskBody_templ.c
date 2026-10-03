/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tSampleTaskBody_templ.c => src/tSampleTaskBody.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * counter          int32_t          VAR_counter     
 *
 * 呼び口関数 #_TCPF_#
 * require port: signature:sKernelTask context:task
 *   StatusType     schedule( );
 *   void           enableAllInterrupts( );
 *   void           disableAllInterrupts( );
 *   void           resumeAllInterrupts( );
 *   void           suspendAllInterrupts( );
 *   void           resumeOsInterrupts( );
 *   void           suspendOsinterrupts( );
 *   AppModeType    getActiveApplicationMode( );
 *   void           shutdownOs( StatusType ercd );
 * call port: cDisplay signature: sDisplay context:task
 *   void           cDisplay_update( );
 *   void           cDisplay_clear( bool_t updateToo );
 *   void           cDisplay_gotoXY( uint8_t x, uint8_t y );
 *   void           cDisplay_putChar( char_t c );
 *   void           cDisplay_putString( const char_t* string );
 *   void           cDisplay_putInt( int32_t val, uint8_t places );
 *   void           cDisplay_putUnsigned( uint32_t val, uint8_t places );
 *   void           cDisplay_putHex( uint32_t val, uint8_t places );
 *   uint8_t*       cDisplay_getBuffer( );
 *   void           cDisplay_powerOff( bool_t updateToo );
 * call port: cBattery signature: sBattery context:task
 *   uint16_t       cBattery_getBatteryVoltage( );
 * call port: cTask signature: sTask context:task
 *   StatusType     cTask_activate( );
 *   StatusType     cTask_terminate( );
 *   StatusType     cTask_chain( );
 *   StatusType     cTask_getId( TaskRefType p_tskid );
 *   StatusType     cTask_getState( TaskStateRefType p_state );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tSampleTaskBody_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eMainTaskBody
 * entry port: eMainTaskBody
 * signature:  sTaskBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eMainTaskBody_main
 * name:         eMainTaskBody_main
 * global_name:  tSampleTaskBody_eMainTaskBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eMainTaskBody_main()
{
}

/* #[<ENTRY_PORT>]# eSample
 * entry port: eSample
 * signature:  sSample
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eSample_countUp
 * name:         eSample_countUp
 * global_name:  tSampleTaskBody_eSample_countUp
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eSample_countUp()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
