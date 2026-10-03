#ifndef tBattery__INLINE_H
#define tBattery__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tBattery_inline_template.h => src/tBattery_inline.h
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * call port: cAvrBattery signature: sAvrBattery context:task
 *   uint16_t       cAvrBattery_batteryVoltage( );
 *
 * #[</PREAMBLE>]# */

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eBattery
 * entry port: eBattery
 * signature:  sBattery
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eBattery_getBatteryVoltage
 * name:         eBattery_getBatteryVoltage
 * global_name:  tBattery_eBattery_getBatteryVoltage
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline uint16_t
eBattery_getBatteryVoltage()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tBattery_INLINEH */
