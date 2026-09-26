#ifndef TARITHMETICOPERATION_CPPIF_HPP
#define TARITHMETICOPERATION_CPPIF_HPP

/*
 * This file is intended to be included in non-TECS celltype code and in C++ code.
 */
#include "tArithmeticOperation_tecsgen.h"
#include "sArithmeticOperation32_cppif.hpp"
#include "sArithmeticOperation64_cppif.hpp"

/*
 * Cell IDX type for Cpp
 */
typedef struct  {
    tArithmeticOperation_IDX idx;
} CPP_tArithmeticOperation_IDX;

/*
 * Cell IDX macros in celltype 'tArithmeticOperation'
 *   type of the macro value is tArithmeticOperation_IDX.
 *   macro name is (cell name) + "_IDX"
 */
inline CPP_tArithmeticOperation_IDX CPP_IAO_IDX__()
{
    CPP_tArithmeticOperation_IDX cpp_idx = { ((tArithmeticOperation_IDX)0) };
    return cpp_idx;
}
#define IAO_IDX  CPP_IAO_IDX__()

/*-------------- begin: use sample ------------
 * Define variable for Cell with Cnstructor
 *   tCelltypeName    CellNameInCpp( Cell_IDX );
 *   ex) tArithmeticOperation     IAO(IAO_IDX);
 *
 * Call member function
 *   CellNameInCpp.eEntryName.FunctionName( parameters... );
 *   ex) IAO.eIAO32.add( parameters... );
 *-------------- end:   use sample ------------*/

/*
 * C++ interface code
 *   This class comes from celltype 'tArithmeticOperation'.
 */
class tArithmeticOperation {
    /* class for entry sArithmeticOperation32 eIAO32 */
    class eIAO32_ : public sArithmeticOperation32{
        public : 
        /* constructor: internal use only */
        eIAO32_(CPP_tArithmeticOperation_IDX idx_);
        /* destructor */
        // ~eIAO32_();   unnecessary
    
        /* sArithmeticOperation32 functions */
        int32_t add( int32_t x, int32_t y );
        int32_t sub( int32_t x, int32_t y );
        int32_t mul( int32_t x, int32_t y );
        int32_t div( int32_t x, int32_t y );
        int32_t rem( int32_t x, int32_t y );

        private:
        CPP_tArithmeticOperation_IDX cpp_idx;
    };
    /* class for entry sArithmeticOperation64 eIAO64 */
    class eIAO64_ : public sArithmeticOperation64{
        public : 
        /* constructor: internal use only */
        eIAO64_(CPP_tArithmeticOperation_IDX idx_);
        /* destructor */
        // ~eIAO64_();   unnecessary
    
        /* sArithmeticOperation64 functions */
        int64_t add( int64_t x, int64_t y );
        int64_t sub( int64_t x, int64_t y );
        int64_t mul( int64_t x, int64_t y );
        int64_t div( int64_t x, int64_t y );
        int64_t rem( int64_t x, int64_t y );

        private:
        CPP_tArithmeticOperation_IDX cpp_idx;
    };

    /*--------  begin public ----------*/
    public:
    /* constructor */
    tArithmeticOperation( CPP_tArithmeticOperation_IDX idx_ );
    /* destructor */
    // ~tArithmeticOperation();   unnecessary

    /* entry sArithmeticOperation32 eIAO32 */
    eIAO32_ eIAO32; 
    /* entry sArithmeticOperation64 eIAO64 */
    eIAO64_ eIAO64; 
    /*--------  end public ----------*/
};

/*-------------- begin: implementation (I/F code only) ----------------*/
/* constructor  */
inline    tArithmeticOperation::tArithmeticOperation(CPP_tArithmeticOperation_IDX idx_) : eIAO32(idx_), eIAO64(idx_){}

/* ------------- entry port: eIAO32 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperation::eIAO32_::eIAO32_( CPP_tArithmeticOperation_IDX idx_ ) :cpp_idx( idx_ ){}

/* entry eIAO32 functions */
inline int32_t tArithmeticOperation::eIAO32_::add( int32_t x, int32_t y )
{ return tArithmeticOperation_eIAO32_add( cpp_idx.idx, x, y ); }

inline int32_t tArithmeticOperation::eIAO32_::sub( int32_t x, int32_t y )
{ return tArithmeticOperation_eIAO32_sub( cpp_idx.idx, x, y ); }

inline int32_t tArithmeticOperation::eIAO32_::mul( int32_t x, int32_t y )
{ return tArithmeticOperation_eIAO32_mul( cpp_idx.idx, x, y ); }

inline int32_t tArithmeticOperation::eIAO32_::div( int32_t x, int32_t y )
{ return tArithmeticOperation_eIAO32_div( cpp_idx.idx, x, y ); }

inline int32_t tArithmeticOperation::eIAO32_::rem( int32_t x, int32_t y )
{ return tArithmeticOperation_eIAO32_rem( cpp_idx.idx, x, y ); }

/* ------------- entry port: eIAO64 ------------------*/
/* constructor: internal use only */
inline    tArithmeticOperation::eIAO64_::eIAO64_( CPP_tArithmeticOperation_IDX idx_ ) :cpp_idx( idx_ ){}

/* entry eIAO64 functions */
inline int64_t tArithmeticOperation::eIAO64_::add( int64_t x, int64_t y )
{ return tArithmeticOperation_eIAO64_add( cpp_idx.idx, x, y ); }

inline int64_t tArithmeticOperation::eIAO64_::sub( int64_t x, int64_t y )
{ return tArithmeticOperation_eIAO64_sub( cpp_idx.idx, x, y ); }

inline int64_t tArithmeticOperation::eIAO64_::mul( int64_t x, int64_t y )
{ return tArithmeticOperation_eIAO64_mul( cpp_idx.idx, x, y ); }

inline int64_t tArithmeticOperation::eIAO64_::div( int64_t x, int64_t y )
{ return tArithmeticOperation_eIAO64_div( cpp_idx.idx, x, y ); }

inline int64_t tArithmeticOperation::eIAO64_::rem( int64_t x, int64_t y )
{ return tArithmeticOperation_eIAO64_rem( cpp_idx.idx, x, y ); }

/* undef for inline #_UDF_# */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tArithmeticOperation_IDX
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

#endif /* TARITHMETICOPERATION_CPPIF_HPP */
