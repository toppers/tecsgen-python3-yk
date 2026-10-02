/*
 * §≥§Œ•’•°•§•Î§œ tecsgen §À§Ë§Íº´∆∞¿∏¿Æ§µ§Ï§ﬁ§∑§ø
 * §≥§Œ•’•°•§•Î§Ú ‘Ω∏§∑§∆ª»Õ—§π§Î§≥§»§œ°¢∞’øﬁ§µ§Ï§∆§§§ﬁ§ª§Û
 */
/* #[<PREAMBLE>]#
 * #[<...>]# §´§È #[</...>]# §«∞œ§ﬁ§Ï§ø•≥•·•Û•»§œ ‘Ω∏§∑§ §§§«§Ø§¿§µ§§
 * tecsmerge §À§Ë§Î•ﬁ°º•∏§Àª»Õ—§µ§Ï§ﬁ§π
 *
 * ∏∆§”∏˝¥ÿøÙ #_TCPF_#
 * call port: cCall signature: sCallee context:task
 *   ER             cCall_add( int32_t a, int32_t b, int32_t* sum );
 *   void           cCall_notify( );
 *
 * #[</PREAMBLE>]# */

/* •◊•Ì•»•ø•§•◊¿Î∏¿§‰ —øÙ§ŒƒÍµ¡§Ú§≥§≥§ÀΩÒ§≠§ﬁ§π #_PAC_# */
#include "tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* #[<POSTAMBLE>]#
 *   §≥§Ï§Ë§Í≤º§À»Ûºı§±∏˝¥ÿøÙ§ÚΩÒ§≠§ﬁ§π
 * #[</POSTAMBLE>]#*/
ER_UINT
tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_add(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid)
{
    tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB    *p_cellcb;
#if 0
    if( VALID_IDX( idx ) ){
      p_cellcb = tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_GET_CELLCB(idx);
    }else{
       /* „Ç®„É©„ÉºÂá¶ÁêÜ„Ç≥„Éº„Éâ„Çí„Åì„Åì„Å´Ë®òËø∞ */
    }
#else
    p_cellcb = NULL;
#endif

    ER_UINT retval = 0;

    if(prb_mem((void *)par3, sizeof(int32_t*), TSK_SELF, TPM_WRITE) != E_OK){
        return E_MACV;
    }
    retval = (ER_UINT)cCall_add((int32_t)par1, (int32_t)par2, (int32_t*)par3);

    return retval;
}

ER_UINT
tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_notify(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid)
{
    tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_CB    *p_cellcb;
#if 0
    if( VALID_IDX( idx ) ){
      p_cellcb = tHRP2SVCPlugin_sCalleeSVCBody_Service_eCallee_GET_CELLCB(idx);
    }else{
       /* „Ç®„É©„ÉºÂá¶ÁêÜ„Ç≥„Éº„Éâ„Çí„Åì„Åì„Å´Ë®òËø∞ */
    }
#else
    p_cellcb = NULL;
#endif

    ER_UINT retval = 0;

    cCall_notify();
}

