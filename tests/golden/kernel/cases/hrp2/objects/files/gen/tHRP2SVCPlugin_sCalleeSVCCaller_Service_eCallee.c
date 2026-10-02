/*
 * §≥§Œ•’•°•§•Î§œ tecsgen §À§Ë§Íº´∆∞¿∏¿Æ§µ§Ï§ﬁ§∑§ø
 * §≥§Œ•’•°•§•Î§Ú ‘Ω∏§∑§∆ª»Õ—§π§Î§≥§»§œ°¢∞’øﬁ§µ§Ï§∆§§§ﬁ§ª§Û
 */
/* #[<PREAMBLE>]#
 * #[<...>]# §´§È #[</...>]# §«∞œ§ﬁ§Ï§ø•≥•·•Û•»§œ ‘Ω∏§∑§ §§§«§Ø§¿§µ§§
 * tecsmerge §À§Ë§Î•ﬁ°º•∏§Àª»Õ—§µ§Ï§ﬁ§π
 *
 * #[</PREAMBLE>]# */

/* •◊•Ì•»•ø•§•◊¿Î∏¿§‰ —øÙ§ŒƒÍµ¡§Ú§≥§≥§ÀΩÒ§≠§ﬁ§π #_PAC_# */
#include "tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* ºı§±∏˝¥ÿøÙ #_TEPF_# */
/* #[<ENTRY_PORT>]# eThroughEntry
 * entry port: eThroughEntry
 * signature:  sCallee
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eThroughEntry_add
 * name:         eThroughEntry_add
 * global_name:  tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_eThroughEntry_add
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
ER
eThroughEntry_add(CELLIDX idx, int32_t a, int32_t b, int32_t* sum)
{
  ER  retval;
  tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_CB    *p_cellcb;
  if( VALID_IDX( idx ) ){
    p_cellcb = tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_GET_CELLCB(idx);
  }else{
     /* „Ç®„É©„ÉºÂá¶ÁêÜ„Ç≥„Éº„Éâ„Çí„Åì„Åì„Å´Ë®òËø∞ */
  }

  retval = (ER)cal_svc( 21, a, b, sum, 0, 0 );
  return retval;
}

/* #[<ENTRY_FUNC>]# eThroughEntry_notify
 * name:         eThroughEntry_notify
 * global_name:  tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_eThroughEntry_notify
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eThroughEntry_notify(CELLIDX idx)
{
  tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_CB    *p_cellcb;
  if( VALID_IDX( idx ) ){
    p_cellcb = tHRP2SVCPlugin_sCalleeSVCCaller_Service_eCallee_GET_CELLCB(idx);
  }else{
     /* „Ç®„É©„ÉºÂá¶ÁêÜ„Ç≥„Éº„Éâ„Çí„Åì„Åì„Å´Ë®òËø∞ */
  }

  cal_svc( 22, 0, 0, 0, 0, 0 );
}

/* #[<POSTAMBLE>]#
 *   §≥§Ï§Ë§Í≤º§À»Ûºı§±∏˝¥ÿøÙ§ÚΩÒ§≠§ﬁ§π
 * #[</POSTAMBLE>]#*/
