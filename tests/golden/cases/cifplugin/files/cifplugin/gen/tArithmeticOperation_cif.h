#ifndef TARITHMETICOPERATION_H
#define TARITHMETICOPERATION_H

/*
 * This header file is intedned to be included in non-TECS celltype code.
 * Don not include in celltype code.
 * Mutiple *_cif.h files can be included non-TECS celltype code.
 */

/* include celltype definition header */
#ifndef TOPPERS_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY_defined_tArithmeticOperation_CIF_H
#endif

#include "tArithmeticOperation_tecsgen.h"

#ifdef TOPPERS_CB_TYPE_ONLY_defined_tArithmeticOperation_CIF_H
#undef TOPPERS_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY_defined_tArithmeticOperation_CIF_H
#endif

/**/

/*** cell: IAO ***/
/** port: eIAO32 **/
/* funcition: add */
#define IAO_eIAO32_add( x, y ) \
        tArithmeticOperation_eIAO32_add( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: sub */
#define IAO_eIAO32_sub( x, y ) \
        tArithmeticOperation_eIAO32_sub( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: mul */
#define IAO_eIAO32_mul( x, y ) \
        tArithmeticOperation_eIAO32_mul( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: div */
#define IAO_eIAO32_div( x, y ) \
        tArithmeticOperation_eIAO32_div( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: rem */
#define IAO_eIAO32_rem( x, y ) \
        tArithmeticOperation_eIAO32_rem( ((tArithmeticOperation_IDX)0), x, y )

/** port: eIAO64 **/
/* funcition: add */
#define IAO_eIAO64_add( x, y ) \
        tArithmeticOperation_eIAO64_add( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: sub */
#define IAO_eIAO64_sub( x, y ) \
        tArithmeticOperation_eIAO64_sub( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: mul */
#define IAO_eIAO64_mul( x, y ) \
        tArithmeticOperation_eIAO64_mul( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: div */
#define IAO_eIAO64_div( x, y ) \
        tArithmeticOperation_eIAO64_div( ((tArithmeticOperation_IDX)0), x, y )
/* funcition: rem */
#define IAO_eIAO64_rem( x, y ) \
        tArithmeticOperation_eIAO64_rem( ((tArithmeticOperation_IDX)0), x, y )

/** port: eIAO32EA **/
/* funcition: add */
#define IAO_eIAO32EA_add( subscript, x, y ) \
        tArithmeticOperation_eIAO32EA_add( ((tArithmeticOperation_IDX)0), subscript, x, y )
/* funcition: sub */
#define IAO_eIAO32EA_sub( subscript, x, y ) \
        tArithmeticOperation_eIAO32EA_sub( ((tArithmeticOperation_IDX)0), subscript, x, y )
/* funcition: mul */
#define IAO_eIAO32EA_mul( subscript, x, y ) \
        tArithmeticOperation_eIAO32EA_mul( ((tArithmeticOperation_IDX)0), subscript, x, y )
/* funcition: div */
#define IAO_eIAO32EA_div( subscript, x, y ) \
        tArithmeticOperation_eIAO32EA_div( ((tArithmeticOperation_IDX)0), subscript, x, y )
/* funcition: rem */
#define IAO_eIAO32EA_rem( subscript, x, y ) \
        tArithmeticOperation_eIAO32EA_rem( ((tArithmeticOperation_IDX)0), subscript, x, y )

#endif /* TARITHMETICOPERATION_H */
