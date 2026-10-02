/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sReferAlarm_TECSGEN_H
#define sReferAlarm_TECSGEN_H

/*
 * signature   :  sReferAlarm
 * global name :  sReferAlarm
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sReferAlarm_VDES {
    struct tag_sReferAlarm_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sReferAlarm_VMT {
    ER             (*refer__T)( const struct tag_sReferAlarm_VDES *edp, T_RALM* pk_alarmStatus );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sReferAlarm_Defined
#define  Descriptor_of_sReferAlarm_Defined
typedef struct { struct tag_sReferAlarm_VDES *vdes; } Descriptor( sReferAlarm );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SREFERALARM_REFER               (1)

#endif /* sReferAlarm_TECSGEN_H */
