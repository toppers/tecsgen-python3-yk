/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
/* #[<PREAMBLE>]#
 * #[<...>]# から #[</...>]# で囲まれたコメントは編集しないでください
 * tecsmerge によるマージに使用されます
 *
 * #[</PREAMBLE>]# */

/* プロトタイプ宣言や変数の定義をここに書きます #_PAC_# */
#include "nMruby_t_rcyc_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

  /* struct t_rcyc */
  STRUCT_CLASS( t_rcyc )
MEMBER_GET_SET_INT( t_rcyc, cycstat, Int, int )
MEMBER_GET_SET_INT( t_rcyc, lefttim, Int, int )
/* 受け口関数 #_TEPF_# */
/* #[<ENTRY_PORT>]# eInitialize
 * entry port: eInitialize
 * signature:  nMruby_sInitializeTECSBridge
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eInitialize_initializeBridge
 * name:         eInitialize_initializeBridge
 * global_name:  nMruby_t_rcyc_eInitialize_initializeBridge
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eInitialize_initializeBridge(mrb_state* mrb, struct RClass* TECS)
{
    struct RClass *a;                                /* MBP720 */

    a = mrb_define_class_under(mrb, TECS, "Structt_rcyc", mrb->object_class);
    MRB_SET_INSTANCE_TT(a, MRB_TT_DATA);

    mrb_define_method(mrb, a, "initialize", Struct_t_rcyc_initialize, MRB_ARGS_NONE());
  STRUCT_INIT_MEMBER( t_rcyc, cycstat )
  STRUCT_INIT_MEMBER( t_rcyc, lefttim )
}

/* #[<POSTAMBLE>]#
 *   これより下に非受け口関数を書きます
 * #[</POSTAMBLE>]#*/
