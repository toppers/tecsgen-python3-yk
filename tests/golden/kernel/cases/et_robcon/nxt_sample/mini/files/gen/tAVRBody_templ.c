/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tAVRBody_templ.c => src/tAVRBody.c
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * initializedFlag  bool_t           VAR_initializedFlag
 * ioToAvr          TOAVR            VAR_ioToAvr     
 * ioFromAvr        FROMAVR          VAR_ioFromAvr   
 * dataFromAvr      uint8_t*         VAR_dataFromAvr 
 * dataToAvr        uint8_t*         VAR_dataToAvr   
 * isSend           bool_t           VAR_isSend      
 * linkInitWait     uint8_t          VAR_linkInitWait
 * resetFlag        bool_t           VAR_resetFlag   
 *
 * 呼び口関数 #_TCPF_#
 * call port: cTWI signature: sTWI context:task
 *   bool_t         cTWI_initialize( );
 *   void           cTWI_startWrite( uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, const uint8_t* data, uint32_t nBytes );
 *   void           cTWI_startRead( uint32_t dev_addr, uint32_t int_addr_bytes, uint32_t int_addr, uint8_t* data, uint32_t nBytes );
 *   void           cTWI_pollingUpdate( );
 *   bool_t         cTWI_isBusy( );
 *   bool_t         cTWI_isOk( );
 *   void           cTWI_reset( );
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "tAVRBody_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eAvrMotor
 * entry port: eAvrMotor
 * signature:  sAvrMotor
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAvrMotor_setMotor
 * name:         eAvrMotor_setMotor
 * global_name:  tAVRBody_eAvrMotor_setMotor
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eAvrMotor_setMotor(uint8_t portNumber, int8_t powerPercent, bool_t brake)
{
}

/* #[<ENTRY_PORT>]# eAvrSensor
 * entry port: eAvrSensor
 * signature:  sAvrSensor
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAvrSensor_setInputPower
 * name:         eAvrSensor_setInputPower
 * global_name:  tAVRBody_eAvrSensor_setInputPower
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eAvrSensor_setInputPower(uint8_t portNumber, uint8_t powerType)
{
}

/* #[<ENTRY_FUNC>]# eAvrSensor_getSensor
 * name:         eAvrSensor_getSensor
 * global_name:  tAVRBody_eAvrSensor_getSensor
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
uint16_t
eAvrSensor_getSensor(uint8_t portNumber)
{
}

/* #[<ENTRY_PORT>]# eAvrButton
 * entry port: eAvrButton
 * signature:  sAvrButton
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAvrButton_getButton
 * name:         eAvrButton_getButton
 * global_name:  tAVRBody_eAvrButton_getButton
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
uint8_t
eAvrButton_getButton()
{
}

/* #[<ENTRY_PORT>]# eAvrBattery
 * entry port: eAvrBattery
 * signature:  sAvrBattery
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAvrBattery_batteryVoltage
 * name:         eAvrBattery_batteryVoltage
 * global_name:  tAVRBody_eAvrBattery_batteryVoltage
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
uint16_t
eAvrBattery_batteryVoltage()
{
}

/* #[<ENTRY_PORT>]# eAvrPower
 * entry port: eAvrPower
 * signature:  sAvrPower
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eAvrPower_powerDown
 * name:         eAvrPower_powerDown
 * global_name:  tAVRBody_eAvrPower_powerDown
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eAvrPower_powerDown()
{
}

/* #[<ENTRY_FUNC>]# eAvrPower_update
 * name:         eAvrPower_update
 * global_name:  tAVRBody_eAvrPower_update
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eAvrPower_update()
{
}

/* #[<ENTRY_PORT>]# eInitialize
 * entry port: eInitialize
 * signature:  sHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eInitialize_main
 * name:         eInitialize_main
 * global_name:  tAVRBody_eInitialize_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eInitialize_main()
{
}

/* #[<ENTRY_PORT>]# eTerminate
 * entry port: eTerminate
 * signature:  sStatusTypeHookBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eTerminate_main
 * name:         eTerminate_main
 * global_name:  tAVRBody_eTerminate_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eTerminate_main(StatusType ercd)
{
}

/* #[<ENTRY_PORT>]# eiCyclicBody
 * entry port: eiCyclicBody
 * signature:  sHandlerBody
 * context:    non-task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eiCyclicBody_main
 * name:         eiCyclicBody_main
 * global_name:  tAVRBody_eiCyclicBody_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eiCyclicBody_main()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
