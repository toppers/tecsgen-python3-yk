#ifndef tButtonBody__INLINE_H
#define tButtonBody__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tButtonBody_inline_template.h => src/tButtonBody_inline.h
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 属性アクセスマクロ #_CAAM_#
 * threshold        int32_t          ATTR_threshold  
 * button           uint8_t          VAR_button      
 * count            int32_t          VAR_count       
 * preState         uint8_t          VAR_preState    
 *
 * 呼び口関数 #_TCPF_#
 * call port: cAvrButton signature: sAvrButton context:task
 *   uint8_t        cAvrButton_getButton( );
 *
 * #[</PREAMBLE>]# */

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eButton
 * entry port: eButton
 * signature:  sButton
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eButton_isENTERButton
 * name:         eButton_isENTERButton
 * global_name:  tButtonBody_eButton_isENTERButton
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isENTERButton()
{
}

/* #[<ENTRY_FUNC>]# eButton_isRUNButton
 * name:         eButton_isRUNButton
 * global_name:  tButtonBody_eButton_isRUNButton
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isRUNButton()
{
}

/* #[<ENTRY_FUNC>]# eButton_isSTOPButton
 * name:         eButton_isSTOPButton
 * global_name:  tButtonBody_eButton_isSTOPButton
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isSTOPButton()
{
}

/* #[<ENTRY_FUNC>]# eButton_isEXITButton
 * name:         eButton_isEXITButton
 * global_name:  tButtonBody_eButton_isEXITButton
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isEXITButton()
{
}

/* #[<ENTRY_FUNC>]# eButton_isENTERButtonOnly
 * name:         eButton_isENTERButtonOnly
 * global_name:  tButtonBody_eButton_isENTERButtonOnly
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isENTERButtonOnly()
{
}

/* #[<ENTRY_FUNC>]# eButton_isRUNButtonOnly
 * name:         eButton_isRUNButtonOnly
 * global_name:  tButtonBody_eButton_isRUNButtonOnly
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isRUNButtonOnly()
{
}

/* #[<ENTRY_FUNC>]# eButton_isSTOPButtonOnly
 * name:         eButton_isSTOPButtonOnly
 * global_name:  tButtonBody_eButton_isSTOPButtonOnly
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isSTOPButtonOnly()
{
}

/* #[<ENTRY_FUNC>]# eButton_isEXITButtonOnly
 * name:         eButton_isEXITButtonOnly
 * global_name:  tButtonBody_eButton_isEXITButtonOnly
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline bool_t
eButton_isEXITButtonOnly()
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tButtonBody_INLINEH */
