#ifndef TARITHMETICOPERATIONSINGLETONEA_CPPIF_HPP
#define TARITHMETICOPERATIONSINGLETONEA_CPPIF_HPP

/*
 * This file is intended to be included in non-TECS celltype code and in C++ code.
 */
#include "tArithmeticOperationSingletonEA_tecsgen.h"
#include "sArithmeticOperation32_cppif.hpp"
#include "sArithmeticOperation64_cppif.hpp"


/*-------------- begin: use sample ------------
 * Define variable for Cell with Cnstructor
 *   tCelltypeName    CellNameInCpp;     // don't put empty parenthesis for singleton
 *   ex) tArithmeticOperationSingletonEA     IAOSingletonEA;
 *
 * Call member function
 *   CellNameInCpp.eEntryName.FunctionName( parameters... );
 *   ex) IAOSingletonEA.eIAO32.add( parameters... );
 *-------------- end:   use sample ------------*/

/*
 * C++ interface code
 *   This class comes from celltype 'tArithmeticOperationSingletonEA'.
 */
class tArithmeticOperationSingletonEA {
    /* class for entry sArithmeticOperation32 eIAO32 */
    class eIAO32_ : public sArithmeticOperation32{
        public : 
        /* constructor: internal use only */
        eIAO32_(int_t subscript_);
        /* destructor */
        // ~eIAO32_();   unnecessary
    
        /* sArithmeticOperation32 functions */
        int32_t add( int32_t x, int32_t y );
        int32_t sub( int32_t x, int32_t y );
        int32_t mul( int32_t x, int32_t y );
        int32_t div( int32_t x, int32_t y );
        int32_t rem( int32_t x, int32_t y );

        private:
        int_t  subscript;
    };
    class eIAO32_EA{
        public : 
        /* constructor: internal use only */
        eIAO32_EA();
        /* destructor */
        // ~eIAO32_();   unnecessary

        eIAO32_ operator[]( int_t subscript ) const; 
    };
    /* class for entry sArithmeticOperation64 eIAO64 */
    class eIAO64_ : public sArithmeticOperation64{
        public : 
        /* constructor: internal use only */
        eIAO64_(int_t subscript_);
        /* destructor */
        // ~eIAO64_();   unnecessary
    
        /* sArithmeticOperation64 functions */
        int64_t add( int64_t x, int64_t y );
        int64_t sub( int64_t x, int64_t y );
        int64_t mul( int64_t x, int64_t y );
        int64_t div( int64_t x, int64_t y );
        int64_t rem( int64_t x, int64_t y );

        private:
        int_t  subscript;
    };
    class eIAO64_EA{
        public : 
        /* constructor: internal use only */
        eIAO64_EA();
        /* destructor */
        // ~eIAO64_();   unnecessary

        eIAO64_ operator[]( int_t subscript ) const; 
    };

    /*--------  begin public ----------*/
    public:
    /* constructor */
    tArithmeticOperationSingletonEA(  );
    /* destructor */
    // ~tArithmeticOperationSingletonEA();   unnecessary

    /* entry sArithmeticOperation32 eIAO32 */
    eIAO32_EA eIAO32; 
    /* entry sArithmeticOperation64 eIAO64 */
    eIAO64_EA eIAO64; 
    /*--------  end public ----------*/
};

/*-------------- begin: implementation (I/F code only) ----------------*/
/* constructor  */
inline    tArithmeticOperationSingletonEA::tArithmeticOperationSingletonEA() : eIAO32(), eIAO64(){}

/* ------------- entry port: eIAO32 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperationSingletonEA::eIAO32_::eIAO32_( int_t subscript_ ) :subscript(subscript_){}

/* entry eIAO32 functions */
inline int32_t tArithmeticOperationSingletonEA::eIAO32_::add( int32_t x, int32_t y )
{ return tArithmeticOperationSingletonEA_eIAO32_add( subscript, x, y ); }

inline int32_t tArithmeticOperationSingletonEA::eIAO32_::sub( int32_t x, int32_t y )
{ return tArithmeticOperationSingletonEA_eIAO32_sub( subscript, x, y ); }

inline int32_t tArithmeticOperationSingletonEA::eIAO32_::mul( int32_t x, int32_t y )
{ return tArithmeticOperationSingletonEA_eIAO32_mul( subscript, x, y ); }

inline int32_t tArithmeticOperationSingletonEA::eIAO32_::div( int32_t x, int32_t y )
{ return tArithmeticOperationSingletonEA_eIAO32_div( subscript, x, y ); }

inline int32_t tArithmeticOperationSingletonEA::eIAO32_::rem( int32_t x, int32_t y )
{ return tArithmeticOperationSingletonEA_eIAO32_rem( subscript, x, y ); }

/* constructor for entry array (internal use only)*/
inline  tArithmeticOperationSingletonEA::eIAO32_EA::eIAO32_EA(  ){}
/* operator[] */
inline  tArithmeticOperationSingletonEA::eIAO32_ tArithmeticOperationSingletonEA::eIAO32_EA::operator[]( int_t subscript ) const
{
    /*
     * subscript is not checked here. No way to return error.
     */
    return tArithmeticOperationSingletonEA::eIAO32_(subscript);
};

/* ------------- entry port: eIAO64 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperationSingletonEA::eIAO64_::eIAO64_( int_t subscript_ ) :subscript(subscript_){}

/* entry eIAO64 functions */
inline int64_t tArithmeticOperationSingletonEA::eIAO64_::add( int64_t x, int64_t y )
{ return tArithmeticOperationSingletonEA_eIAO64_add( subscript, x, y ); }

inline int64_t tArithmeticOperationSingletonEA::eIAO64_::sub( int64_t x, int64_t y )
{ return tArithmeticOperationSingletonEA_eIAO64_sub( subscript, x, y ); }

inline int64_t tArithmeticOperationSingletonEA::eIAO64_::mul( int64_t x, int64_t y )
{ return tArithmeticOperationSingletonEA_eIAO64_mul( subscript, x, y ); }

inline int64_t tArithmeticOperationSingletonEA::eIAO64_::div( int64_t x, int64_t y )
{ return tArithmeticOperationSingletonEA_eIAO64_div( subscript, x, y ); }

inline int64_t tArithmeticOperationSingletonEA::eIAO64_::rem( int64_t x, int64_t y )
{ return tArithmeticOperationSingletonEA_eIAO64_rem( subscript, x, y ); }

/* constructor for entry array (internal use only)*/
inline  tArithmeticOperationSingletonEA::eIAO64_EA::eIAO64_EA(  ){}
/* operator[] */
inline  tArithmeticOperationSingletonEA::eIAO64_ tArithmeticOperationSingletonEA::eIAO64_EA::operator[]( int_t subscript ) const
{
    /*
     * subscript is not checked here. No way to return error.
     */
    return tArithmeticOperationSingletonEA::eIAO64_(subscript);
};

/* undef for inline #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tArithmeticOperationSingletonEA_IDX
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#undef SET_CB_INIB_POINTER
#undef eIAO32_add
#undef eIAO32_sub
#undef eIAO32_mul
#undef eIAO32_div
#undef eIAO32_rem
#undef NEP_eIAO32
#undef eIAO64_add
#undef eIAO64_sub
#undef eIAO64_mul
#undef eIAO64_div
#undef eIAO64_rem
#undef NEP_eIAO64
/*-------------- end: implementation (I/F code only) ----------------*/

#endif /* TARITHMETICOPERATIONSINGLETONEA_CPPIF_HPP */
