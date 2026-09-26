#ifndef TARITHMETICOPERATIONSINGLETON_CPPIF_HPP
#define TARITHMETICOPERATIONSINGLETON_CPPIF_HPP

/*
 * This file is intended to be included in non-TECS celltype code and in C++ code.
 */
#include "tArithmeticOperationSingleton_tecsgen.h"
#include "sArithmeticOperation32_cppif.hpp"
#include "sArithmeticOperation64_cppif.hpp"


/*-------------- begin: use sample ------------
 * Define variable for Cell with Cnstructor
 *   tCelltypeName    CellNameInCpp;     // don't put empty parenthesis for singleton
 *   ex) tArithmeticOperationSingleton     IAOSingleton;
 *
 * Call member function
 *   CellNameInCpp.eEntryName.FunctionName( parameters... );
 *   ex) IAOSingleton.eIAO32.add( parameters... );
 *-------------- end:   use sample ------------*/

/*
 * C++ interface code
 *   This class comes from celltype 'tArithmeticOperationSingleton'.
 */
class tArithmeticOperationSingleton {
    /* class for entry sArithmeticOperation32 eIAO32 */
    class eIAO32_ : public sArithmeticOperation32{
        public : 
        /* constructor: internal use only */
        eIAO32_();
        /* destructor */
        // ~eIAO32_();   unnecessary
    
        /* sArithmeticOperation32 functions */
        int32_t add( int32_t x, int32_t y );
        int32_t sub( int32_t x, int32_t y );
        int32_t mul( int32_t x, int32_t y );
        int32_t div( int32_t x, int32_t y );
        int32_t rem( int32_t x, int32_t y );

    };
    /* class for entry sArithmeticOperation64 eIAO64 */
    class eIAO64_ : public sArithmeticOperation64{
        public : 
        /* constructor: internal use only */
        eIAO64_();
        /* destructor */
        // ~eIAO64_();   unnecessary
    
        /* sArithmeticOperation64 functions */
        int64_t add( int64_t x, int64_t y );
        int64_t sub( int64_t x, int64_t y );
        int64_t mul( int64_t x, int64_t y );
        int64_t div( int64_t x, int64_t y );
        int64_t rem( int64_t x, int64_t y );

    };

    /*--------  begin public ----------*/
    public:
    /* constructor */
    tArithmeticOperationSingleton(  );
    /* destructor */
    // ~tArithmeticOperationSingleton();   unnecessary

    /* entry sArithmeticOperation32 eIAO32 */
    eIAO32_ eIAO32; 
    /* entry sArithmeticOperation64 eIAO64 */
    eIAO64_ eIAO64; 
    /*--------  end public ----------*/
};

/*-------------- begin: implementation (I/F code only) ----------------*/
/* constructor  */
inline    tArithmeticOperationSingleton::tArithmeticOperationSingleton() : eIAO32(), eIAO64(){}

/* ------------- entry port: eIAO32 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperationSingleton::eIAO32_::eIAO32_(  ) {}

/* entry eIAO32 functions */
inline int32_t tArithmeticOperationSingleton::eIAO32_::add( int32_t x, int32_t y )
{ return tArithmeticOperationSingleton_eIAO32_add( x, y ); }

inline int32_t tArithmeticOperationSingleton::eIAO32_::sub( int32_t x, int32_t y )
{ return tArithmeticOperationSingleton_eIAO32_sub( x, y ); }

inline int32_t tArithmeticOperationSingleton::eIAO32_::mul( int32_t x, int32_t y )
{ return tArithmeticOperationSingleton_eIAO32_mul( x, y ); }

inline int32_t tArithmeticOperationSingleton::eIAO32_::div( int32_t x, int32_t y )
{ return tArithmeticOperationSingleton_eIAO32_div( x, y ); }

inline int32_t tArithmeticOperationSingleton::eIAO32_::rem( int32_t x, int32_t y )
{ return tArithmeticOperationSingleton_eIAO32_rem( x, y ); }

/* ------------- entry port: eIAO64 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperationSingleton::eIAO64_::eIAO64_(  ) {}

/* entry eIAO64 functions */
inline int64_t tArithmeticOperationSingleton::eIAO64_::add( int64_t x, int64_t y )
{ return tArithmeticOperationSingleton_eIAO64_add( x, y ); }

inline int64_t tArithmeticOperationSingleton::eIAO64_::sub( int64_t x, int64_t y )
{ return tArithmeticOperationSingleton_eIAO64_sub( x, y ); }

inline int64_t tArithmeticOperationSingleton::eIAO64_::mul( int64_t x, int64_t y )
{ return tArithmeticOperationSingleton_eIAO64_mul( x, y ); }

inline int64_t tArithmeticOperationSingleton::eIAO64_::div( int64_t x, int64_t y )
{ return tArithmeticOperationSingleton_eIAO64_div( x, y ); }

inline int64_t tArithmeticOperationSingleton::eIAO64_::rem( int64_t x, int64_t y )
{ return tArithmeticOperationSingleton_eIAO64_rem( x, y ); }

/* undef for inline #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tArithmeticOperationSingleton_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef eIAO32_add
#undef eIAO32_sub
#undef eIAO32_mul
#undef eIAO32_div
#undef eIAO32_rem
#undef eIAO64_add
#undef eIAO64_sub
#undef eIAO64_mul
#undef eIAO64_div
#undef eIAO64_rem
/*-------------- end: implementation (I/F code only) ----------------*/

#endif /* TARITHMETICOPERATIONSINGLETON_CPPIF_HPP */
