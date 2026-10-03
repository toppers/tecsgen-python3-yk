/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sAlarmHook_TECSGEN_H
#define sAlarmHook_TECSGEN_H

/*
 * signature   :  sAlarmHook
 * global name :  sAlarmHook
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sAlarmHook_VDES {
    struct tag_sAlarmHook_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sAlarmHook_VMT {
    StatusType     (*getBase__T)( const struct tag_sAlarmHook_VDES *edp, AlarmBaseRefType p_info );
    StatusType     (*get__T)( const struct tag_sAlarmHook_VDES *edp, TickRefType p_tick );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sAlarmHook_Defined
#define  Descriptor_of_sAlarmHook_Defined
typedef struct { struct tag_sAlarmHook_VDES *vdes; } Descriptor( sAlarmHook );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SALARMHOOK_GETBASE              (1)
#define	FUNCID_SALARMHOOK_GET                  (2)

#endif /* sAlarmHook_TECSGEN_H */
