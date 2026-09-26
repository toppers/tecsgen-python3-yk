#ifndef TARITHMETICOPERATIONSINGLETON_H
#define TARITHMETICOPERATIONSINGLETON_H

/*
 * This header file is intedned to be included in non-TECS celltype code.
 * Don not include in celltype code.
 * Mutiple *_cif.h files can be included non-TECS celltype code.
 */

/* include celltype definition header */
#ifndef TOPPERS_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY
#define TOPPERS_CB_TYPE_ONLY_defined_tArithmeticOperationSingleton_CIF_H
#endif

#include "tArithmeticOperationSingleton_tecsgen.h"

#ifdef TOPPERS_CB_TYPE_ONLY_defined_tArithmeticOperationSingleton_CIF_H
#undef TOPPERS_CB_TYPE_ONLY
#undef TOPPERS_CB_TYPE_ONLY_defined_tArithmeticOperationSingleton_CIF_H
#endif

/**/

/*** cell: IAOSingleton ***/
/** port: eIAO32 **/
/* funcition: add */
#define IAOSingleton_eIAO32_add( x, y ) \
        tArithmeticOperationSingleton_eIAO32_add( x, y )
/* funcition: sub */
#define IAOSingleton_eIAO32_sub( x, y ) \
        tArithmeticOperationSingleton_eIAO32_sub( x, y )
/* funcition: mul */
#define IAOSingleton_eIAO32_mul( x, y ) \
        tArithmeticOperationSingleton_eIAO32_mul( x, y )
/* funcition: div */
#define IAOSingleton_eIAO32_div( x, y ) \
        tArithmeticOperationSingleton_eIAO32_div( x, y )
/* funcition: rem */
#define IAOSingleton_eIAO32_rem( x, y ) \
        tArithmeticOperationSingleton_eIAO32_rem( x, y )

/** port: eIAO64 **/
/* funcition: add */
#define IAOSingleton_eIAO64_add( x, y ) \
        tArithmeticOperationSingleton_eIAO64_add( x, y )
/* funcition: sub */
#define IAOSingleton_eIAO64_sub( x, y ) \
        tArithmeticOperationSingleton_eIAO64_sub( x, y )
/* funcition: mul */
#define IAOSingleton_eIAO64_mul( x, y ) \
        tArithmeticOperationSingleton_eIAO64_mul( x, y )
/* funcition: div */
#define IAOSingleton_eIAO64_div( x, y ) \
        tArithmeticOperationSingleton_eIAO64_div( x, y )
/* funcition: rem */
#define IAOSingleton_eIAO64_rem( x, y ) \
        tArithmeticOperationSingleton_eIAO64_rem( x, y )

#endif /* TARITHMETICOPERATIONSINGLETON_H */
