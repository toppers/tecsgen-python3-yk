/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef sStatusTypeHookBody_TECSGEN_H
#define sStatusTypeHookBody_TECSGEN_H

/*
 * signature   :  sStatusTypeHookBody
 * global name :  sStatusTypeHookBody
 * context     :  task
 */

#ifndef TOPPERS_MACRO_ONLY

/* シグニチャディスクリプタ #_SD_# */
struct tag_sStatusTypeHookBody_VDES {
    struct tag_sStatusTypeHookBody_VMT *VMT;
};

/* シグニチャ関数テーブル #_SFT_# */
struct tag_sStatusTypeHookBody_VMT {
    void           (*main__T)( const struct tag_sStatusTypeHookBody_VDES *edp, StatusType ercd );
};

/* シグニチャディスクリプタ(動的結合用) #_SDES_# */
#ifndef Descriptor_of_sStatusTypeHookBody_Defined
#define  Descriptor_of_sStatusTypeHookBody_Defined
typedef struct { struct tag_sStatusTypeHookBody_VDES *vdes; } Descriptor( sStatusTypeHookBody );
#endif
#endif /* TOPPERS_MACRO_ONLY */

/* function id */
#define	FUNCID_SSTATUSTYPEHOOKBODY_MAIN        (1)

#endif /* sStatusTypeHookBody_TECSGEN_H */
