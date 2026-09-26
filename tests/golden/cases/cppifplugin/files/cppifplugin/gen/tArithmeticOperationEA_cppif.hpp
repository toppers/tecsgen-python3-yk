#ifndef TARITHMETICOPERATIONEA_CPPIF_HPP
#define TARITHMETICOPERATIONEA_CPPIF_HPP

/*
 * This file is intended to be included in non-TECS celltype code and in C++ code.
 */
#include "tArithmeticOperationEA_tecsgen.h"
#include "sArithmeticOperation32_cppif.hpp"
#include "sArithmeticOperation64_cppif.hpp"

/*
 * Cell IDX type for Cpp
 */
typedef struct  {
    tArithmeticOperationEA_IDX idx;
} CPP_tArithmeticOperationEA_IDX;

/*
 * Cell IDX macros in celltype 'tArithmeticOperationEA'
 *   type of the macro value is tArithmeticOperationEA_IDX.
 *   macro name is (cell name) + "_IDX"
 */
inline CPP_tArithmeticOperationEA_IDX CPP_IAOEA_IDX__()
{
    CPP_tArithmeticOperationEA_IDX cpp_idx = { &tArithmeticOperationEA_INIB_tab[0] };
    return cpp_idx;
}
#define IAOEA_IDX  CPP_IAOEA_IDX__()

/*-------------- begin: use sample ------------
 * Define variable for Cell with Cnstructor
 *   tCelltypeName    CellNameInCpp( Cell_IDX );
 *   ex) tArithmeticOperationEA     IAOEA(IAOEA_IDX);
 *
 * Call member function
 *   CellNameInCpp.eEntryName.FunctionName( parameters... );
 *   ex) IAOEA.eIAO32.add( parameters... );
 *-------------- end:   use sample ------------*/

/*
 * C++ interface code
 *   This class comes from celltype 'tArithmeticOperationEA'.
 */
class tArithmeticOperationEA {
    /* class for entry sArithmeticOperation32 eIAO32 */
    class eIAO32_ : public sArithmeticOperation32{
        public : 
        /* constructor: internal use only */
        eIAO32_(CPP_tArithmeticOperationEA_IDX idx_, int_t subscript_);
        /* destructor */
        // ~eIAO32_();   unnecessary
    
        /* sArithmeticOperation32 functions */
        int32_t add( int32_t x, int32_t y );
        int32_t sub( int32_t x, int32_t y );
        int32_t mul( int32_t x, int32_t y );
        int32_t div( int32_t x, int32_t y );
        int32_t rem( int32_t x, int32_t y );

        private:
        CPP_tArithmeticOperationEA_IDX cpp_idx;
        private:
        int_t  subscript;
    };
    class eIAO32_EA{
        public : 
        /* constructor: internal use only */
        eIAO32_EA(CPP_tArithmeticOperationEA_IDX idx_);
        /* destructor */
        // ~eIAO32_();   unnecessary

        eIAO32_ operator[]( int_t subscript ) const; 
        private:
        CPP_tArithmeticOperationEA_IDX cpp_idx;
    };
    /* class for entry sArithmeticOperation64 eIAO64 */
    class eIAO64_ : public sArithmeticOperation64{
        public : 
        /* constructor: internal use only */
        eIAO64_(CPP_tArithmeticOperationEA_IDX idx_, int_t subscript_);
        /* destructor */
        // ~eIAO64_();   unnecessary
    
        /* sArithmeticOperation64 functions */
        int64_t add( int64_t x, int64_t y );
        int64_t sub( int64_t x, int64_t y );
        int64_t mul( int64_t x, int64_t y );
        int64_t div( int64_t x, int64_t y );
        int64_t rem( int64_t x, int64_t y );

        private:
        CPP_tArithmeticOperationEA_IDX cpp_idx;
        private:
        int_t  subscript;
    };
    class eIAO64_EA{
        public : 
        /* constructor: internal use only */
        eIAO64_EA(CPP_tArithmeticOperationEA_IDX idx_);
        /* destructor */
        // ~eIAO64_();   unnecessary

        eIAO64_ operator[]( int_t subscript ) const; 
        private:
        CPP_tArithmeticOperationEA_IDX cpp_idx;
    };

    /*--------  begin public ----------*/
    public:
    /* constructor */
    tArithmeticOperationEA( CPP_tArithmeticOperationEA_IDX idx_ );
    /* destructor */
    // ~tArithmeticOperationEA();   unnecessary

    /* entry sArithmeticOperation32 eIAO32 */
    eIAO32_EA eIAO32; 
    /* entry sArithmeticOperation64 eIAO64 */
    eIAO64_EA eIAO64; 
    /*--------  end public ----------*/
};

/*-------------- begin: implementation (I/F code only) ----------------*/
/* constructor  */
inline    tArithmeticOperationEA::tArithmeticOperationEA(CPP_tArithmeticOperationEA_IDX idx_) : eIAO32(idx_), eIAO64(idx_){}

/* ------------- entry port: eIAO32 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperationEA::eIAO32_::eIAO32_( CPP_tArithmeticOperationEA_IDX idx_, int_t subscript_ ) :cpp_idx( idx_ ), subscript(subscript_){}

/* entry eIAO32 functions */
inline int32_t tArithmeticOperationEA::eIAO32_::add( int32_t x, int32_t y )
{ return tArithmeticOperationEA_eIAO32_add( cpp_idx.idx, subscript, x, y ); }

inline int32_t tArithmeticOperationEA::eIAO32_::sub( int32_t x, int32_t y )
{ return tArithmeticOperationEA_eIAO32_sub( cpp_idx.idx, subscript, x, y ); }

inline int32_t tArithmeticOperationEA::eIAO32_::mul( int32_t x, int32_t y )
{ return tArithmeticOperationEA_eIAO32_mul( cpp_idx.idx, subscript, x, y ); }

inline int32_t tArithmeticOperationEA::eIAO32_::div( int32_t x, int32_t y )
{ return tArithmeticOperationEA_eIAO32_div( cpp_idx.idx, subscript, x, y ); }

inline int32_t tArithmeticOperationEA::eIAO32_::rem( int32_t x, int32_t y )
{ return tArithmeticOperationEA_eIAO32_rem( cpp_idx.idx, subscript, x, y ); }

/* constructor for entry array (internal use only)*/
inline  tArithmeticOperationEA::eIAO32_EA::eIAO32_EA( CPP_tArithmeticOperationEA_IDX idx_ ):cpp_idx( idx_ ){}
/* operator[] */
inline  tArithmeticOperationEA::eIAO32_ tArithmeticOperationEA::eIAO32_EA::operator[]( int_t subscript ) const
{
    /*
     * subscript is not checked here. No way to return error.
     */
    return tArithmeticOperationEA::eIAO32_(cpp_idx, subscript);
};

/* ------------- entry port: eIAO64 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperationEA::eIAO64_::eIAO64_( CPP_tArithmeticOperationEA_IDX idx_, int_t subscript_ ) :cpp_idx( idx_ ), subscript(subscript_){}

/* entry eIAO64 functions */
inline int64_t tArithmeticOperationEA::eIAO64_::add( int64_t x, int64_t y )
{ return tArithmeticOperationEA_eIAO64_add( cpp_idx.idx, subscript, x, y ); }

inline int64_t tArithmeticOperationEA::eIAO64_::sub( int64_t x, int64_t y )
{ return tArithmeticOperationEA_eIAO64_sub( cpp_idx.idx, subscript, x, y ); }

inline int64_t tArithmeticOperationEA::eIAO64_::mul( int64_t x, int64_t y )
{ return tArithmeticOperationEA_eIAO64_mul( cpp_idx.idx, subscript, x, y ); }

inline int64_t tArithmeticOperationEA::eIAO64_::div( int64_t x, int64_t y )
{ return tArithmeticOperationEA_eIAO64_div( cpp_idx.idx, subscript, x, y ); }

inline int64_t tArithmeticOperationEA::eIAO64_::rem( int64_t x, int64_t y )
{ return tArithmeticOperationEA_eIAO64_rem( cpp_idx.idx, subscript, x, y ); }

/* constructor for entry array (internal use only)*/
inline  tArithmeticOperationEA::eIAO64_EA::eIAO64_EA( CPP_tArithmeticOperationEA_IDX idx_ ):cpp_idx( idx_ ){}
/* operator[] */
inline  tArithmeticOperationEA::eIAO64_ tArithmeticOperationEA::eIAO64_EA::operator[]( int_t subscript ) const
{
    /*
     * subscript is not checked here. No way to return error.
     */
    return tArithmeticOperationEA::eIAO64_(cpp_idx, subscript);
};

/* undef for inline #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tArithmeticOperationEA_IDX
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

#endif /* TARITHMETICOPERATIONEA_CPPIF_HPP */
