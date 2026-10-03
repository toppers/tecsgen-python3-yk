/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef tAlarm_TECSGEN_H
#define tAlarm_TECSGEN_H

/*
 * celltype          :  tAlarm
 * global name       :  tAlarm
 * multi-domain      :  no
 * idx_is_id(actual) :  no(no)
 * singleton         :  no
 * has_CB            :  no
 * has_INIB          :  yes
 * rom               :  yes
 * CB initializer    :  yes
 */

/* グローバルヘッダ #_IGH_# */
#include "global_tecsgen.h"

/* シグニチャヘッダ #_ISH_# */
#include "sAlarm_tecsgen.h"
#include "sAlarmHook_tecsgen.h"
#include "sHandlerBody_tecsgen.h"

#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
/* セル INIB 型宣言 #_CIP_# */
typedef const struct tag_tAlarm_INIB {
    /* call port #_TCP_# */
    struct tag_sHandlerBody_VDES const*cBody; /* TCP_2 */
    /* call port #_NEP_# */ 
    /* attribute(RO) #_ATO_# */ 
    UINT8          id;
}  tAlarm_INIB;

/* CB は存在しない。INIB を CB の代わりに使用するための define #_DCI_# */
#define tAlarm_CB_tab           tAlarm_INIB_tab
#define tAlarm_CB               tAlarm_INIB
#define tag_tAlarm_CB           tag_tAlarm_INIB

/* シングルトンセル CB プロトタイプ宣言 #_MCPB_# */
extern tAlarm_INIB  tAlarm_INIB_tab[];

/* セルタイプのIDX型 #_CTIX_# */
typedef const struct tag_tAlarm_INIB *tAlarm_IDX;

/* 受け口関数プロトタイプ宣言 #_EPP_# */
/* sAlarm */
Inline StatusType   tAlarm_eAlarm_getBase(tAlarm_IDX idx, AlarmBaseRefType p_info);
Inline StatusType   tAlarm_eAlarm_get(tAlarm_IDX idx, TickRefType p_tick);
Inline StatusType   tAlarm_eAlarm_setRelative(tAlarm_IDX idx, TickType incr, TickType cycle);
Inline StatusType   tAlarm_eAlarm_setAbsolute(tAlarm_IDX idx, TickType start, TickType cycle);
Inline StatusType   tAlarm_eAlarm_cancel(tAlarm_IDX idx);
/* sAlarmHook */
Inline StatusType   tAlarm_eAlarmHook_getBase(tAlarm_IDX idx, AlarmBaseRefType p_info);
Inline StatusType   tAlarm_eAlarmHook_get(tAlarm_IDX idx, TickRefType p_tick);
#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

#define tAlarm_ID_BASE              (1)  /* ID のベース  #_NIDB_# */
#define tAlarm_N_CELL               (4)  /* セルの個数  #_NCEL_# */

/* IDXの正当性チェックマクロ #_CVI_# */
#define tAlarm_VALID_IDX(IDX) (1)

/* optional 呼び口をテストするマクロ #_TOCP_# */
#define tAlarm_is_cBody_joined(p_that) \
	  ((p_that)->cBody!=0)

/* セルCBを得るマクロ #_GCB_# */
#define tAlarm_GET_CELLCB(idx) (idx)

/* 属性アクセスマクロ #_AAM_# */
#define tAlarm_ATTR_id( p_that )	((p_that)->id)

#define tAlarm_GET_id(p_that)	((p_that)->id)



#ifndef TECSFLOW
 /* 呼び口関数マクロ #_CPM_# */
#define tAlarm_cBody_main( p_that ) \
	  (p_that)->cBody->VMT->main__T( \
	   (p_that)->cBody )

#else  /* TECSFLOW */
#define tAlarm_cBody_main( p_that ) \
	  (p_that)->cBody.main__T( \
 )

#endif /* TECSFLOW */
#ifndef TOPPERS_MACRO_ONLY

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* 受け口スケルトン関数プロトタイプ宣言（VMT不要最適化により参照するもの） #_EPSP_# */

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* TOPPERS_MACRO_ONLY */

/* IDXの正当性チェックマクロ（短縮形） #_CVIA_# */
#define VALID_IDX(IDX)  tAlarm_VALID_IDX(IDX)


/* セルCBを得るマクロ(短縮形) #_GCBA_# */
#define GET_CELLCB(idx)  tAlarm_GET_CELLCB(idx)

/* CELLCB 型(短縮形) #_CCT_# */
#define CELLCB	tAlarm_CB

/* セルタイプのIDX型(短縮形) #_CTIXA_# */
#define CELLIDX	tAlarm_IDX


/* 属性アクセスマクロ(短縮形) #_AAMA_# */
#define ATTR_id              tAlarm_ATTR_id( p_cellcb )


/* 呼び口関数マクロ（短縮形）#_CPMA_# */
#define cBody_main( ) \
          tAlarm_cBody_main( p_cellcb )



/* optional 呼び口をテストするマクロ（短縮形） #_TOCPA_# */
#define is_cBody_joined()\
		tAlarm_is_cBody_joined(p_cellcb)

/* 受け口関数マクロ（短縮形） #_EPM_# */
#define eAlarm_getBase   tAlarm_eAlarm_getBase
#define eAlarm_get       tAlarm_eAlarm_get
#define eAlarm_setRelative tAlarm_eAlarm_setRelative
#define eAlarm_setAbsolute tAlarm_eAlarm_setAbsolute
#define eAlarm_cancel    tAlarm_eAlarm_cancel
#define eAlarmHook_getBase tAlarm_eAlarmHook_getBase
#define eAlarmHook_get   tAlarm_eAlarmHook_get

/* イテレータコード (FOREACH_CELL)の生成 #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < tAlarm_N_CELL; (i)++ ){ \
       (p_cb) = &tAlarm_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB 初期化マクロ #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */
#ifndef TOPPERS_MACRO_ONLY

/* inline ヘッダの include #_INL_# */
#include "tAlarm_inline.h"

#endif /* TOPPERS_MACRO_ONLY */

#ifdef TOPPERS_CB_TYPE_ONLY

/* inline のための undef #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tAlarm_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef ATTR_id
#undef tAlarm_ATTR_id
#undef tAlarm_GET_id
#undef ATTR_name
#undef tAlarm_ATTR_name
#undef tAlarm_GET_name
#undef ATTR_counter
#undef tAlarm_ATTR_counter
#undef tAlarm_GET_counter
#undef ATTR_action
#undef tAlarm_ATTR_action
#undef tAlarm_GET_action
#undef ATTR_task
#undef tAlarm_ATTR_task
#undef tAlarm_GET_task
#undef ATTR_event
#undef tAlarm_ATTR_event
#undef tAlarm_GET_event
#undef ATTR_callbackName
#undef tAlarm_ATTR_callbackName
#undef tAlarm_GET_callbackName
#undef ATTR_autoStart
#undef tAlarm_ATTR_autoStart
#undef tAlarm_GET_autoStart
#undef ATTR_alarmTime
#undef tAlarm_ATTR_alarmTime
#undef tAlarm_GET_alarmTime
#undef ATTR_cycleTime
#undef tAlarm_ATTR_cycleTime
#undef tAlarm_GET_cycleTime
#undef ATTR_appMode
#undef tAlarm_ATTR_appMode
#undef tAlarm_GET_appMode
#undef is_cBody_joined
#undef tAlarm_cBody_main
#undef cBody_main
#undef eAlarm_getBase
#undef eAlarm_get
#undef eAlarm_setRelative
#undef eAlarm_setAbsolute
#undef eAlarm_cancel
#undef eAlarmHook_getBase
#undef eAlarmHook_get
#endif /* TOPPERS_CB_TYPE_ONLY */

#endif /* tAlarm_TECSGENH */
