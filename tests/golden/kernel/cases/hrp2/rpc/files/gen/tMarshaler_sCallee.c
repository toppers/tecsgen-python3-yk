/*
 * ¤³¤Î¥Õ¥¡¥¤¥ë¤Ï tecsgen ¤Ë¤è¤ê¼«Æ°À¸À®¤µ¤ì¤Ş¤·¤¿
 * ¤³¤Î¥Õ¥¡¥¤¥ë¤òÊÔ½¸¤·¤Æ»ÈÍÑ¤¹¤ë¤³¤È¤Ï¡¢°Õ¿Ş¤µ¤ì¤Æ¤¤¤Ş¤»¤ó
 */
/* #[<PREAMBLE>]#
 * #[<...>]# ¤«¤é #[</...>]# ¤Ç°Ï¤Ş¤ì¤¿¥³¥á¥ó¥È¤ÏÊÔ½¸¤·¤Ê¤¤¤Ç¤¯¤À¤µ¤¤
 * tecsmerge ¤Ë¤è¤ë¥Ş¡¼¥¸¤Ë»ÈÍÑ¤µ¤ì¤Ş¤¹
 *
 * ¸Æ¤Ó¸ı´Ø¿ô #_TCPF_#
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
#include "tMarshaler_sCallee_tecsgen.h"

#ifndef E_OK
#define	E_OK	0		/* success */
#define	E_ID	(-18)	/* illegal ID */
#endif

/* ¼õ¤±¸ı´Ø¿ô #_TEPF_# */
/* #[<ENTRY_PORT>]# eClientEntry
 * entry port: eClientEntry
 * signature:  sCallee
 * context:    task
 * #[</ENTRY_PORT>]# */

/* #[<ENTRY_FUNC>]# eClientEntry_add
 * name:         eClientEntry_add
 * global_name:  tMarshaler_sCallee_eClientEntry_add
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
ER
eClientEntry_add(CELLIDX idx, int32_t a, int32_t b)
{
    ER  retval_ = E_OK;
    ER      ercd_;
    FLGPTN  flgptn;
    int16_t  func_id_ = 1;    /* id of add: 1 */
    uint8_t  msg[256];
    tMarshaler_sCallee_CB *p_cellcb;

    if( VALID_IDX( idx ) ){
        p_cellcb = GET_CELLCB(idx);
    }else{
         return ERCD( E_RPC, E_ID );
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_wait();

    /* é–¢æ•° id ã®é€å‡º */
    *((int16_t *)(&msg[0])) = func_id_;
    /* å…¥åŠ›å¼•æ•°é€å‡º */
    *((int32_t *)(&msg[2])) = a;
    *((int32_t *)(&msg[6])) = b;
    /* EOPã®é€å‡ºï¼ˆãƒ‘ã‚±ãƒƒãƒˆã®æƒãã ã—ï¼‰ */
    if( (ercd_=cMessageBuffer_send(msg, 10)) != E_OK )
        goto error_reset;

        cSemaphore_signal();

    if( (ercd_=cEventflag_wait( 0x01, TWF_ANDW, &flgptn )) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    if( (ercd_=cEventflag_clear( 0x00 ) ) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();
    cMessageBuffer_receive(&retval_);
    return retval_;

error_reset:
#if 0
    if( ercd_ != ERCD( E_RPC, E_RESET ) )
        (void)cTDR_reset();
#endif
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();

    return ercd_;
}

/* #[<ENTRY_FUNC>]# eClientEntry_scale
 * name:         eClientEntry_scale
 * global_name:  tMarshaler_sCallee_eClientEntry_scale
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
int16_t
eClientEntry_scale(CELLIDX idx, int8_t k, uint16_t v)
{
    int16_t  retval_;
    ER      ercd_;
    FLGPTN  flgptn;
    int16_t  func_id_ = 2;    /* id of scale: 2 */
    uint8_t  msg[256];
    tMarshaler_sCallee_CB *p_cellcb;

    if( VALID_IDX( idx ) ){
        p_cellcb = GET_CELLCB(idx);
    }else{
        /* ã‚¨ãƒ©ãƒ¼å‡¦ç†ã‚³ãƒ¼ãƒ‰ã‚’ã“ã“ã«è¨˜è¿° */
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_wait();

    /* é–¢æ•° id ã®é€å‡º */
    *((int16_t *)(&msg[0])) = func_id_;
    /* å…¥åŠ›å¼•æ•°é€å‡º */
    *((int8_t *)(&msg[2])) = k;
    *((uint16_t *)(&msg[3])) = v;
    /* EOPã®é€å‡ºï¼ˆãƒ‘ã‚±ãƒƒãƒˆã®æƒãã ã—ï¼‰ */
    if( (ercd_=cMessageBuffer_send(msg, 5)) != E_OK )
        goto error_reset;

        cSemaphore_signal();

    if( (ercd_=cEventflag_wait( 0x01, TWF_ANDW, &flgptn )) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    if( (ercd_=cEventflag_clear( 0x00 ) ) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();
    cMessageBuffer_receive(&retval_);
    return retval_;

error_reset:
#if 0
    if( ercd_ != ERCD( E_RPC, E_RESET ) )
        (void)cTDR_reset();
#endif
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();

    return;
}

/* #[<ENTRY_FUNC>]# eClientEntry_widen
 * name:         eClientEntry_widen
 * global_name:  tMarshaler_sCallee_eClientEntry_widen
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
int64_t
eClientEntry_widen(CELLIDX idx, uint32_t v)
{
    int64_t  retval_;
    ER      ercd_;
    FLGPTN  flgptn;
    int16_t  func_id_ = 3;    /* id of widen: 3 */
    uint8_t  msg[256];
    tMarshaler_sCallee_CB *p_cellcb;

    if( VALID_IDX( idx ) ){
        p_cellcb = GET_CELLCB(idx);
    }else{
        /* ã‚¨ãƒ©ãƒ¼å‡¦ç†ã‚³ãƒ¼ãƒ‰ã‚’ã“ã“ã«è¨˜è¿° */
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_wait();

    /* é–¢æ•° id ã®é€å‡º */
    *((int16_t *)(&msg[0])) = func_id_;
    /* å…¥åŠ›å¼•æ•°é€å‡º */
    *((uint32_t *)(&msg[2])) = v;
    /* EOPã®é€å‡ºï¼ˆãƒ‘ã‚±ãƒƒãƒˆã®æƒãã ã—ï¼‰ */
    if( (ercd_=cMessageBuffer_send(msg, 6)) != E_OK )
        goto error_reset;

        cSemaphore_signal();

    if( (ercd_=cEventflag_wait( 0x01, TWF_ANDW, &flgptn )) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    if( (ercd_=cEventflag_clear( 0x00 ) ) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();
    cMessageBuffer_receive(&retval_);
    return retval_;

error_reset:
#if 0
    if( ercd_ != ERCD( E_RPC, E_RESET ) )
        (void)cTDR_reset();
#endif
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();

    return;
}

/* #[<ENTRY_FUNC>]# eClientEntry_notify
 * name:         eClientEntry_notify
 * global_name:  tMarshaler_sCallee_eClientEntry_notify
 * oneway:       false
 * #[</ENTRY_FUNC>]# */
void
eClientEntry_notify(CELLIDX idx)
{
    ER      ercd_;
    FLGPTN  flgptn;
    int16_t  func_id_ = 4;    /* id of notify: 4 */
    uint8_t  msg[256];
    tMarshaler_sCallee_CB *p_cellcb;

    if( VALID_IDX( idx ) ){
        p_cellcb = GET_CELLCB(idx);
    }else{
        /* ã‚¨ãƒ©ãƒ¼å‡¦ç†ã‚³ãƒ¼ãƒ‰ã‚’ã“ã“ã«è¨˜è¿° */
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_wait();

    /* é–¢æ•° id ã®é€å‡º */
    *((int16_t *)(&msg[0])) = func_id_;
    /* å…¥åŠ›å¼•æ•°é€å‡º */
    /* EOPã®é€å‡ºï¼ˆãƒ‘ã‚±ãƒƒãƒˆã®æƒãã ã—ï¼‰ */
    if( (ercd_=cMessageBuffer_send(msg, 2)) != E_OK )
        goto error_reset;

        cSemaphore_signal();

    if( (ercd_=cEventflag_wait( 0x01, TWF_ANDW, &flgptn )) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    if( (ercd_=cEventflag_clear( 0x00 ) ) != E_OK ){
      ercd_ = ERCD(E_RPC,ercd_);
      goto error_reset;
    }
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();
    return;

error_reset:
#if 0
    if( ercd_ != ERCD( E_RPC, E_RESET ) )
        (void)cTDR_reset();
#endif
    ///* Channel Lock */
    //if( is_cLockChannel_joined() )
    //  cLockChannel_signal();

    return;
}

/* #[<POSTAMBLE>]#
 *   ¤³¤ì¤è¤ê²¼¤ËÈó¼õ¤±¸ı´Ø¿ô¤ò½ñ¤­¤Ş¤¹
 * #[</POSTAMBLE>]#*/
