/*
 * ¤³¤Î¥Õ¥¡¥¤¥ë¤Ï tecsgen ¤Ë¤è¤ê¼«Æ°À¸À®¤µ¤ì¤Ş¤·¤¿
 * ¤³¤Î¥Õ¥¡¥¤¥ë¤òÊÔ½¸¤·¤Æ»ÈÍÑ¤¹¤ë¤³¤È¤Ï¡¢°Õ¿Ş¤µ¤ì¤Æ¤¤¤Ş¤»¤ó
 */
/* #[<PREAMBLE>]#
 * #[<...>]# ¤«¤é #[</...>]# ¤Ç°Ï¤Ş¤ì¤¿¥³¥á¥ó¥È¤ÏÊÔ½¸¤·¤Ê¤¤¤Ç¤¯¤À¤µ¤¤
 * tecsmerge ¤Ë¤è¤ë¥Ş¡¼¥¸¤Ë»ÈÍÑ¤µ¤ì¤Ş¤¹
 *
 * ¸Æ¤Ó¸ı´Ø¿ô #_TCPF_#
 * call port: cServerCall signature: sCallee context:task
 *   ER             cServerCall_add( int32_t a, int32_t b );
 *   int16_t        cServerCall_scale( int8_t k, uint16_t v );
 *   int64_t        cServerCall_widen( uint32_t v );
 *   void           cServerCall_notify( );
 * call port: cEventflag signature: sEventflag context:task
 *   ER             cEventflag_set( FLGPTN setPattern );
 *   ER             cEventflag_clear( FLGPTN clearPattern );
 *   ER             cEventflag_wait( FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern );
 *   ER             cEventflag_waitPolling( FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern );
 *   ER             cEventflag_waitTimeout( FLGPTN waitPattern, MODE waitFlagMode, FLGPTN* p_flagPattern, TMO timeout );
 *   ER             cEventflag_initialize( );
 *   ER             cEventflag_refer( T_RFLG* pk_eventflagStatus );
 * call port: cSemaphore signature: sSemaphore context:task
 *   ER             cSemaphore_signal( );
 *   ER             cSemaphore_wait( );
 *   ER             cSemaphore_waitPolling( );
 *   ER             cSemaphore_waitTimeout( TMO timeout );
 *   ER             cSemaphore_initialize( );
 *   ER             cSemaphore_refer( T_RSEM* pk_semaphoreStatus );
 * call port: cMessageBuffer signature: sMessageBuffer context:task
 *   ER             cMessageBuffer_send( const uint8_t* message, uint32_t size );
 *   ER             cMessageBuffer_sendPolling( const uint8_t* message, uint32_t size );
 *   ER             cMessageBuffer_sendTimeout( const uint8_t* message, uint32_t size, TMO timeout );
 *   ER_UINT        cMessageBuffer_receive( uint8_t* message );
 *   ER_UINT        cMessageBuffer_receivePolling( uint8_t* message );
 *   ER_UINT        cMessageBuffer_receiveTimeout( uint8_t* message, TMO timeout );
 *   void           cMessageBuffer_initialize( );
 *   ER             cMessageBuffer_refer( T_RMBF* packet );
 *
 * #[</PREAMBLE>]# */

/* ¥×¥í¥È¥¿¥¤¥×Àë¸À¤äÊÑ¿ô¤ÎÄêµÁ¤ò¤³¤³¤Ë½ñ¤­¤Ş¤¹ #_PAC_# */
#include "tUnmarshaler_sCallee_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* ã‚¢ãƒ³ãƒãƒ¼ã‚·ãƒ£ãƒ©é–¢æ•°ã®ãƒ—ãƒ­ãƒˆã‚¿ã‚¤ãƒ—å®£è¨€ */
static ER  tTransparentUnmarshaler_sCallee_add();	/* func_id: 1 */
static ER  tTransparentUnmarshaler_sCallee_scale();	/* func_id: 2 */
static ER  tTransparentUnmarshaler_sCallee_widen();	/* func_id: 3 */
static ER  tTransparentUnmarshaler_sCallee_notify();	/* func_id: 4 */

static uint8_t msg[256];

/* ¼õ¤±¸ı´Ø¿ô #_TEPF_# */
/* #[<ENTRY_PORT>]# eUnmarshalAndCallFunction
 * entry port: eUnmarshalAndCallFunction
 * signature:  sTaskBody
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eUnmarshalAndCallFunction_main
 * name:         eUnmarshalAndCallFunction_main
 * global_name:  tUnmarshaler_sCallee_eUnmarshalAndCallFunction_main
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eUnmarshalAndCallFunction_main(CELLIDX idx)
{

    int16_t   func_id_;
    ER        ercd_;

    tUnmarshaler_sCallee_CB *p_cellcb;

    if( VALID_IDX( idx ) ){
        p_cellcb = GET_CELLCB(idx);
    }else{
        /* ã‚¨ãƒ©ãƒ¼å‡¦ç†ã‚³ãƒ¼ãƒ‰ã‚’ã“ã“ã«è¨˜è¿° */
    }

    cSemaphore_wait();

#if 0
    /* SOPã®ãƒã‚§ãƒƒã‚¯ */
    if( (ercd_=cTDR_receiveSOP( false )) != E_OK )
        goto error_reset;
    /* func_id ã®å–å¾— */
    if( (ercd_=cTDR_getInt16( &func_id_ )) != E_OK )
        goto error_reset;
#endif

    if( (ercd_ = cMessageBuffer_receive(msg) < 0 ) )
        goto error_reset;
    func_id_ = ((int16_t *)msg)[0];

#ifdef RPC_DEBUG
    syslog(LOG_INFO, "unmarshaler task: func_id: %d", func_id_ );
#endif
    switch( func_id_ ){
    case 1:       /*** add ***/ 
        if( tTransparentUnmarshaler_sCallee_add() != E_OK )
            goto error_reset;
        break;
    case 2:       /*** scale ***/ 
        if( tTransparentUnmarshaler_sCallee_scale() != E_OK )
            goto error_reset;
        break;
    case 3:       /*** widen ***/ 
        if( tTransparentUnmarshaler_sCallee_widen() != E_OK )
            goto error_reset;
        break;
    case 4:       /*** notify ***/ 
        if( tTransparentUnmarshaler_sCallee_notify() != E_OK )
            goto error_reset;
        break;
    default:
#if 0 // deleted by ishikawa: tSysLogãŒæœªå®Ÿè£…
        syslog(LOG_INFO, "unmarshaler task: ERROR: unknown func_id: %d", func_id_ );
#endif /* 0 */
        break;
    };

    return;

error_reset:
#if 0
    if( ercd_ != ERCD( E_RPC, E_RESET ) )
        (void)cTDR_reset();
#else
    return ercd_;
#endif

}

/* #[<POSTAMBLE>]#
 *   ¤³¤ì¤è¤ê²¼¤ËÈó¼õ¤±¸ı´Ø¿ô¤ò½ñ¤­¤Ş¤¹
 * #[</POSTAMBLE>]#*/

/*** ã‚¢ãƒ³ãƒãƒ¼ã‚·ãƒ£ãƒ©é–¢æ•° ***/

/*
 * name:    add
 * func_id: 1 
 */
static ER
tTransparentUnmarshaler_sCallee_add()
{
	ER  ercd_;
    int32_t      a;
    int32_t      b;
    ER           retval_;

        /* å…¥åŠ›å¼•æ•°å—å– */
    a = *((int32_t *)(&msg[2]));
    b = *((int32_t *)(&msg[6]));
        /* ãƒ‘ã‚±ãƒƒãƒˆçµ‚ã‚ã‚Šã‚’ãƒã‚§ãƒƒã‚¯ */
    /* å¯¾è±¡é–¢æ•°ã®å‘¼å‡ºã— */
    retval_ = cServerCall_add( a, b );
    if( (ercd_ = cMessageBuffer_send(&retval_, sizeof(ER)) != E_OK ) )
        goto error_reset;
    /* é–¢æ•°å‡¦ç†ã®çµ‚äº†ã‚’é€šçŸ¥ */
    if( ( ercd_ = cEventflag_set( 0x01 ) ) != E_OK ){
      goto error_reset;
    }
    return E_OK;
error_reset:
    return ercd_;
}

/*
 * name:    scale
 * func_id: 2 
 */
static ER
tTransparentUnmarshaler_sCallee_scale()
{
	ER  ercd_;
    int8_t       k;
    uint16_t     v;
    int16_t      retval_;

        /* å…¥åŠ›å¼•æ•°å—å– */
    k = *((int8_t *)(&msg[2]));
    v = *((uint16_t *)(&msg[3]));
        /* ãƒ‘ã‚±ãƒƒãƒˆçµ‚ã‚ã‚Šã‚’ãƒã‚§ãƒƒã‚¯ */
    /* å¯¾è±¡é–¢æ•°ã®å‘¼å‡ºã— */
    retval_ = cServerCall_scale( k, v );
    if( (ercd_ = cMessageBuffer_send(&retval_, sizeof(int16_t)) != E_OK ) )
        goto error_reset;
    /* é–¢æ•°å‡¦ç†ã®çµ‚äº†ã‚’é€šçŸ¥ */
    if( ( ercd_ = cEventflag_set( 0x01 ) ) != E_OK ){
      goto error_reset;
    }
    return E_OK;
error_reset:
    return ercd_;
}

/*
 * name:    widen
 * func_id: 3 
 */
static ER
tTransparentUnmarshaler_sCallee_widen()
{
	ER  ercd_;
    uint32_t     v;
    int64_t      retval_;

        /* å…¥åŠ›å¼•æ•°å—å– */
    v = *((uint32_t *)(&msg[2]));
        /* ãƒ‘ã‚±ãƒƒãƒˆçµ‚ã‚ã‚Šã‚’ãƒã‚§ãƒƒã‚¯ */
    /* å¯¾è±¡é–¢æ•°ã®å‘¼å‡ºã— */
    retval_ = cServerCall_widen( v );
    if( (ercd_ = cMessageBuffer_send(&retval_, sizeof(int64_t)) != E_OK ) )
        goto error_reset;
    /* é–¢æ•°å‡¦ç†ã®çµ‚äº†ã‚’é€šçŸ¥ */
    if( ( ercd_ = cEventflag_set( 0x01 ) ) != E_OK ){
      goto error_reset;
    }
    return E_OK;
error_reset:
    return ercd_;
}

/*
 * name:    notify
 * func_id: 4 
 */
static ER
tTransparentUnmarshaler_sCallee_notify()
{
	ER  ercd_;

        /* å…¥åŠ›å¼•æ•°å—å– */
        /* ãƒ‘ã‚±ãƒƒãƒˆçµ‚ã‚ã‚Šã‚’ãƒã‚§ãƒƒã‚¯ */
    /* å¯¾è±¡é–¢æ•°ã®å‘¼å‡ºã— */
    cServerCall_notify( );
    /* é–¢æ•°å‡¦ç†ã®çµ‚äº†ã‚’é€šçŸ¥ */
    if( ( ercd_ = cEventflag_set( 0x01 ) ) != E_OK ){
      goto error_reset;
    }
    return E_OK;
error_reset:
    return ercd_;
}

