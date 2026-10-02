/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sWaitEventflag_TECSGEN_H
#define sWaitEventflag_TECSGEN_H

/*
 * signature   :  sWaitEventflag
 * global name :  sWaitEventflag
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sWaitEventflag_VDES {
    struct tag_sWaitEventflag_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sWaitEventflag_VMT {
    ER             (*wait__T)( const struct tag_sWaitEventflag_VDES *edp, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern );
    ER             (*waitPolling__T)( const struct tag_sWaitEventflag_VDES *edp, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern );
    ER             (*waitTimeout__T)( const struct tag_sWaitEventflag_VDES *edp, FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern, TMO timeout );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sWaitEventflag_Defined
#define  Descriptor_of_sWaitEventflag_Defined
typedef struct { struct tag_sWaitEventflag_VDES *vdes; } Descriptor( sWaitEventflag );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SWAITEVENTFLAG_WAIT             (1)
#define	FUNCID_SWAITEVENTFLAG_WAITPOLLING      (2)
#define	FUNCID_SWAITEVENTFLAG_WAITTIMEOUT      (3)

#endif /* sWaitEventflag_TECSGEN_H */
