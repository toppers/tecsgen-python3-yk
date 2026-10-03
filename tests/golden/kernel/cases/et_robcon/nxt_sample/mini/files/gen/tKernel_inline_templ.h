#ifndef tKernel__INLINE_H
#define tKernel__INLINE_H

/*
 * このファイルは tecsgen によりテンプレートとして自動生成されました
 * このファイルを編集して使用することが意図されていますが
 * tecsgen の再実行により上書きされてしまうため、通常
 *   gen/tKernel_inline_template.h => src/tKernel_inline.h
 * のように名前, フォルダを変更してから修正します
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * 呼び口関数 #_TCPF_#
 * call port: cStartupHookBody signature: sHookBody context:task optional:true
 *   bool_t     is_cStartupHookBody_joined(int subscript)        check if joined
 *   void           cStartupHookBody_main( subscript );
 *       subscript:  0...(NCP_cStartupHookBody-1)
 * call port: cErrorHookBody signature: sStatusTypeHookBody context:task optional:true
 *   bool_t     is_cErrorHookBody_joined()                     check if joined
 *   void           cErrorHookBody_main( StatusType ercd );
 * call port: cShutdownHookBody signature: sStatusTypeHookBody context:task optional:true
 *   bool_t     is_cShutdownHookBody_joined(int subscript)        check if joined
 *   void           cShutdownHookBody_main( subscript, StatusType ercd );
 *       subscript:  0...(NCP_cShutdownHookBody-1)
 *
 * #[</PREAMBLE>]# */

/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eKernelTask
 * entry port: eKernelTask
 * signature:  sKernelTask
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelTask_schedule
 * name:         eKernelTask_schedule
 * global_name:  tKernel_eKernelTask_schedule
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eKernelTask_schedule()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_enableAllInterrupts
 * name:         eKernelTask_enableAllInterrupts
 * global_name:  tKernel_eKernelTask_enableAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_enableAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_disableAllInterrupts
 * name:         eKernelTask_disableAllInterrupts
 * global_name:  tKernel_eKernelTask_disableAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_disableAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_resumeAllInterrupts
 * name:         eKernelTask_resumeAllInterrupts
 * global_name:  tKernel_eKernelTask_resumeAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_resumeAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_suspendAllInterrupts
 * name:         eKernelTask_suspendAllInterrupts
 * global_name:  tKernel_eKernelTask_suspendAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_suspendAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_resumeOsInterrupts
 * name:         eKernelTask_resumeOsInterrupts
 * global_name:  tKernel_eKernelTask_resumeOsInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_resumeOsInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_suspendOsinterrupts
 * name:         eKernelTask_suspendOsinterrupts
 * global_name:  tKernel_eKernelTask_suspendOsinterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_suspendOsinterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_getActiveApplicationMode
 * name:         eKernelTask_getActiveApplicationMode
 * global_name:  tKernel_eKernelTask_getActiveApplicationMode
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline AppModeType
eKernelTask_getActiveApplicationMode()
{
}

/* #[<ENTRY_FUNC>]# eKernelTask_shutdownOs
 * name:         eKernelTask_shutdownOs
 * global_name:  tKernel_eKernelTask_shutdownOs
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTask_shutdownOs(StatusType ercd)
{
}

/* #[<ENTRY_PORT>]# eKernelISR1
 * entry port: eKernelISR1
 * signature:  sKernelISR1
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelISR1_enableAllInterrupts
 * name:         eKernelISR1_enableAllInterrupts
 * global_name:  tKernel_eKernelISR1_enableAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR1_enableAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR1_disableAllInterrupts
 * name:         eKernelISR1_disableAllInterrupts
 * global_name:  tKernel_eKernelISR1_disableAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR1_disableAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR1_resumeAllInterrupts
 * name:         eKernelISR1_resumeAllInterrupts
 * global_name:  tKernel_eKernelISR1_resumeAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR1_resumeAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR1_suspendAllInterrupts
 * name:         eKernelISR1_suspendAllInterrupts
 * global_name:  tKernel_eKernelISR1_suspendAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR1_suspendAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR1_resumeOsInterrupts
 * name:         eKernelISR1_resumeOsInterrupts
 * global_name:  tKernel_eKernelISR1_resumeOsInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR1_resumeOsInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR1_suspendOsinterrupts
 * name:         eKernelISR1_suspendOsinterrupts
 * global_name:  tKernel_eKernelISR1_suspendOsinterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR1_suspendOsinterrupts()
{
}

/* #[<ENTRY_PORT>]# eKernelISR2
 * entry port: eKernelISR2
 * signature:  sKernelISR2
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelISR2_enableAllInterrupts
 * name:         eKernelISR2_enableAllInterrupts
 * global_name:  tKernel_eKernelISR2_enableAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_enableAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_disableAllInterrupts
 * name:         eKernelISR2_disableAllInterrupts
 * global_name:  tKernel_eKernelISR2_disableAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_disableAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_resumeAllInterrupts
 * name:         eKernelISR2_resumeAllInterrupts
 * global_name:  tKernel_eKernelISR2_resumeAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_resumeAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_suspendAllInterrupts
 * name:         eKernelISR2_suspendAllInterrupts
 * global_name:  tKernel_eKernelISR2_suspendAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_suspendAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_resumeOsInterrupts
 * name:         eKernelISR2_resumeOsInterrupts
 * global_name:  tKernel_eKernelISR2_resumeOsInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_resumeOsInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_suspendOsinterrupts
 * name:         eKernelISR2_suspendOsinterrupts
 * global_name:  tKernel_eKernelISR2_suspendOsinterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_suspendOsinterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_getActiveApplicationMode
 * name:         eKernelISR2_getActiveApplicationMode
 * global_name:  tKernel_eKernelISR2_getActiveApplicationMode
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline AppModeType
eKernelISR2_getActiveApplicationMode()
{
}

/* #[<ENTRY_FUNC>]# eKernelISR2_shutdownOs
 * name:         eKernelISR2_shutdownOs
 * global_name:  tKernel_eKernelISR2_shutdownOs
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelISR2_shutdownOs(StatusType ercd)
{
}

/* #[<ENTRY_PORT>]# eKernelErrorHook
 * entry port: eKernelErrorHook
 * signature:  sKernelErrorHook
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelErrorHook_resumeAllInterrupts
 * name:         eKernelErrorHook_resumeAllInterrupts
 * global_name:  tKernel_eKernelErrorHook_resumeAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelErrorHook_resumeAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelErrorHook_suspendAllInterrupts
 * name:         eKernelErrorHook_suspendAllInterrupts
 * global_name:  tKernel_eKernelErrorHook_suspendAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelErrorHook_suspendAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelErrorHook_getActiveApplicationMode
 * name:         eKernelErrorHook_getActiveApplicationMode
 * global_name:  tKernel_eKernelErrorHook_getActiveApplicationMode
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline AppModeType
eKernelErrorHook_getActiveApplicationMode()
{
}

/* #[<ENTRY_FUNC>]# eKernelErrorHook_shutdownOs
 * name:         eKernelErrorHook_shutdownOs
 * global_name:  tKernel_eKernelErrorHook_shutdownOs
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelErrorHook_shutdownOs(StatusType ercd)
{
}

/* #[<ENTRY_PORT>]# eKernelTaskHook
 * entry port: eKernelTaskHook
 * signature:  sKernelTaskHook
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelTaskHook_resumeAllInterrupts
 * name:         eKernelTaskHook_resumeAllInterrupts
 * global_name:  tKernel_eKernelTaskHook_resumeAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTaskHook_resumeAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTaskHook_suspendAllInterrupts
 * name:         eKernelTaskHook_suspendAllInterrupts
 * global_name:  tKernel_eKernelTaskHook_suspendAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelTaskHook_suspendAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelTaskHook_getActiveApplicationMode
 * name:         eKernelTaskHook_getActiveApplicationMode
 * global_name:  tKernel_eKernelTaskHook_getActiveApplicationMode
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline AppModeType
eKernelTaskHook_getActiveApplicationMode()
{
}

/* #[<ENTRY_PORT>]# eKernelStartupHook
 * entry port: eKernelStartupHook
 * signature:  sKernelStartupHook
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelStartupHook_getActiveApplicationMode
 * name:         eKernelStartupHook_getActiveApplicationMode
 * global_name:  tKernel_eKernelStartupHook_getActiveApplicationMode
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline AppModeType
eKernelStartupHook_getActiveApplicationMode()
{
}

/* #[<ENTRY_FUNC>]# eKernelStartupHook_shutdownOs
 * name:         eKernelStartupHook_shutdownOs
 * global_name:  tKernel_eKernelStartupHook_shutdownOs
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelStartupHook_shutdownOs(StatusType ercd)
{
}

/* #[<ENTRY_PORT>]# eKernelShutdownHook
 * entry port: eKernelShutdownHook
 * signature:  sKernelShutdownHook
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelShutdownHook_getActiveApplicationMode
 * name:         eKernelShutdownHook_getActiveApplicationMode
 * global_name:  tKernel_eKernelShutdownHook_getActiveApplicationMode
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline AppModeType
eKernelShutdownHook_getActiveApplicationMode()
{
}

/* #[<ENTRY_PORT>]# eKernelAlarmCallback
 * entry port: eKernelAlarmCallback
 * signature:  sKernelAlarmCallback
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eKernelAlarmCallback_resumeAllInterrupts
 * name:         eKernelAlarmCallback_resumeAllInterrupts
 * global_name:  tKernel_eKernelAlarmCallback_resumeAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelAlarmCallback_resumeAllInterrupts()
{
}

/* #[<ENTRY_FUNC>]# eKernelAlarmCallback_suspendAllInterrupts
 * name:         eKernelAlarmCallback_suspendAllInterrupts
 * global_name:  tKernel_eKernelAlarmCallback_suspendAllInterrupts
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
eKernelAlarmCallback_suspendAllInterrupts()
{
}

/* #[<ENTRY_PORT>]# ePreKernel
 * entry port: ePreKernel
 * signature:  sPreKernel
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# ePreKernel_startOs
 * name:         ePreKernel_startOs
 * global_name:  tKernel_ePreKernel_startOs
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline void
ePreKernel_startOs(AppModeType mode)
{
}

/* #[<ENTRY_PORT>]# eEventTask
 * entry port: eEventTask
 * signature:  sEventTask
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eEventTask_set
 * name:         eEventTask_set
 * global_name:  tKernel_eEventTask_set
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventTask_set(TaskType tskid, EventMaskType mask)
{
}

/* #[<ENTRY_FUNC>]# eEventTask_clear
 * name:         eEventTask_clear
 * global_name:  tKernel_eEventTask_clear
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventTask_clear(EventMaskType mask)
{
}

/* #[<ENTRY_FUNC>]# eEventTask_get
 * name:         eEventTask_get
 * global_name:  tKernel_eEventTask_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventTask_get(TaskType tskid, EventMaskRefType p_mask)
{
}

/* #[<ENTRY_FUNC>]# eEventTask_wait
 * name:         eEventTask_wait
 * global_name:  tKernel_eEventTask_wait
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventTask_wait(EventMaskType mask)
{
}

/* #[<ENTRY_PORT>]# eEventISR2
 * entry port: eEventISR2
 * signature:  sEventISR2
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eEventISR2_set
 * name:         eEventISR2_set
 * global_name:  tKernel_eEventISR2_set
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventISR2_set(TaskType tskid, EventMaskType mask)
{
}

/* #[<ENTRY_FUNC>]# eEventISR2_get
 * name:         eEventISR2_get
 * global_name:  tKernel_eEventISR2_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventISR2_get(TaskType tskid, EventMaskRefType p_mask)
{
}

/* #[<ENTRY_PORT>]# eEventHook
 * entry port: eEventHook
 * signature:  sEventHook
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eEventHook_get
 * name:         eEventHook_get
 * global_name:  tKernel_eEventHook_get
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
Inline StatusType
eEventHook_get(TaskType tskid, EventMaskRefType p_mask)
{
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/

#endif /* tKernel_INLINEH */
