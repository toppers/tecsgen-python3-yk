#ifndef tCelltypeInfo_FACTORY_H
#define tCelltypeInfo_FACTORY_H
#undef N_CP_cEntryInfo
#undef NCP_cEntryInfo
#undef N_CP_cCallInfo
#undef NCP_cCallInfo
#undef N_CP_cAttrInfo
#undef NCP_cAttrInfo
#undef N_CP_cVarInfo
#undef NCP_cVarInfo
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef ATTR_name
#undef ATTR_b_singleton
#undef ATTR_b_IDX_is_ID_act
#undef ATTR_sizeOfCB
#undef ATTR_sizeOfINIB
#undef ATTR_n_cellInLinUnit
#undef ATTR_n_cellInSystem
#undef cEntryInfo_getName
#undef cEntryInfo_getNameLength
#undef cEntryInfo_getSignatureInfo
#undef cEntryInfo_getArraySize
#undef cEntryInfo_isInline
#undef cCallInfo_getName
#undef cCallInfo_getNameLength
#undef cCallInfo_getSignatureInfo
#undef cCallInfo_getArraySize
#undef cCallInfo_getSpecifierInfo
#undef cCallInfo_getInternalInfo
#undef cCallInfo_getLocationInfo
#undef cCallInfo_getOptimizeInfo
#undef cAttrInfo_getName
#undef cAttrInfo_getOffset
#undef cAttrInfo_getTypeInfo
#undef cAttrInfo_getSizeIsExpr
#undef cAttrInfo_getSizeIs
#undef cVarInfo_getName
#undef cVarInfo_getOffset
#undef cVarInfo_getTypeInfo
#undef cVarInfo_getSizeIsExpr
#undef cVarInfo_getSizeIs
#undef cEntryInfo_refer_to_descriptor
#undef cEntryInfo_ref_desc
#undef cCallInfo_refer_to_descriptor
#undef cCallInfo_ref_desc
#undef cAttrInfo_refer_to_descriptor
#undef cAttrInfo_ref_desc
#undef cVarInfo_refer_to_descriptor
#undef cVarInfo_ref_desc
#undef is_cEntryInfo_joined
#undef is_cCallInfo_joined
#undef is_cAttrInfo_joined
#undef is_cVarInfo_joined
#undef eCelltypeInfo_getName
#undef eCelltypeInfo_getNameLength
#undef eCelltypeInfo_getNAttr
#undef eCelltypeInfo_getAttrInfo
#undef eCelltypeInfo_getNVar
#undef eCelltypeInfo_getVarInfo
#undef eCelltypeInfo_getNCall
#undef eCelltypeInfo_getCallInfo
#undef eCelltypeInfo_getNEntry
#undef eCelltypeInfo_getEntryInfo
#undef eCelltypeInfo_isSingleton
#undef eCelltypeInfo_isIDX_is_ID
#undef eCelltypeInfo_hasCB
#undef eCelltypeInfo_hasINIB
#undef FOREACH_CELL
#undef END_FOREACH_CELL
#undef INITIALIZE_CB
#define TOPPERS_CB_TYPE_ONLY

#include "tTask_tecsgen.h"
#define tTask__IDX_is_ID_act                               (false)
#define tTask__sizeOfCB                                    ((sizeof(tTask_CB)))
#define tTask__sizeOfINIB                                  ((0))
#define tTask__NCELLINLINKUNIT         (1)

#include "tPutStringStdio_tecsgen.h"
#define tPutStringStdio__IDX_is_ID_act                     (false)
#define tPutStringStdio__sizeOfCB                          ((0))
#define tPutStringStdio__sizeOfINIB                        ((0))
#define tPutStringStdio__NCELLINLINKUNIT (1)

#include "tHelloWorld_tecsgen.h"
#define tHelloWorld__IDX_is_ID_act                         (false)
#define tHelloWorld__sizeOfCB                              ((sizeof(tHelloWorld_CB)))
#define tHelloWorld__sizeOfINIB                            ((0))
#define tHelloWorld__NCELLINLINKUNIT   (1)

#include "tTaskMain_tecsgen.h"
#define tTaskMain__IDX_is_ID_act                           (false)
#define tTaskMain__sizeOfCB                                ((sizeof(tTaskMain_CB)))
#define tTaskMain__sizeOfINIB                              ((0))
#define tTaskMain__NCELLINLINKUNIT     (1)

#include "nTECSInfo_tTECSInfo_tecsgen.h"
#define nTECSInfo_tTECSInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tTECSInfo__sizeOfCB                      ((0))
#define nTECSInfo_tTECSInfo__sizeOfINIB                    ((0))
#define nTECSInfo_tTECSInfo__NCELLINLINKUNIT (1)

#include "nTECSInfo_tTECSInfoSub_tecsgen.h"
#define nTECSInfo_tTECSInfoSub__IDX_is_ID_act              (false)
#define nTECSInfo_tTECSInfoSub__sizeOfCB                   ((sizeof(nTECSInfo_tTECSInfoSub_CB)))
#define nTECSInfo_tTECSInfoSub__sizeOfINIB                 ((0))
#define nTECSInfo_tTECSInfoSub__NCELLINLINKUNIT (1)

#include "nTECSInfo_tNamespaceInfo_tecsgen.h"
#define nTECSInfo_tNamespaceInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tNamespaceInfo__sizeOfCB                 ((sizeof(nTECSInfo_tNamespaceInfo_CB)))
#define nTECSInfo_tNamespaceInfo__sizeOfINIB               ((0))
#define nTECSInfo_tNamespaceInfo__NCELLINLINKUNIT (2)

#include "nTECSInfo_tSignatureInfo_tecsgen.h"
#define nTECSInfo_tSignatureInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tSignatureInfo__sizeOfCB                 ((sizeof(nTECSInfo_tSignatureInfo_CB)))
#define nTECSInfo_tSignatureInfo__sizeOfINIB               ((0))
#define nTECSInfo_tSignatureInfo__NCELLINLINKUNIT (26)

#include "nTECSInfo_tFunctionInfo_tecsgen.h"
#define nTECSInfo_tFunctionInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tFunctionInfo__sizeOfCB                  ((sizeof(nTECSInfo_tFunctionInfo_CB)))
#define nTECSInfo_tFunctionInfo__sizeOfINIB                ((0))
#define nTECSInfo_tFunctionInfo__NCELLINLINKUNIT (170)

#include "nTECSInfo_tParamInfo_tecsgen.h"
#define nTECSInfo_tParamInfo__IDX_is_ID_act                (false)
#define nTECSInfo_tParamInfo__sizeOfCB                     ((sizeof(nTECSInfo_tParamInfo_CB)))
#define nTECSInfo_tParamInfo__sizeOfINIB                   ((0))
#define nTECSInfo_tParamInfo__NCELLINLINKUNIT (205)

#include "nTECSInfo_tCelltypeInfo_tecsgen.h"
#define nTECSInfo_tCelltypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tCelltypeInfo__sizeOfCB                  ((sizeof(nTECSInfo_tCelltypeInfo_CB)))
#define nTECSInfo_tCelltypeInfo__sizeOfINIB                ((0))
#define nTECSInfo_tCelltypeInfo__NCELLINLINKUNIT (5)

#include "nTECSInfo_tCallInfo_tecsgen.h"
#define nTECSInfo_tCallInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tCallInfo__sizeOfCB                      ((sizeof(nTECSInfo_tCallInfo_CB)))
#define nTECSInfo_tCallInfo__sizeOfINIB                    ((0))
#define nTECSInfo_tCallInfo__NCELLINLINKUNIT (16)

#include "nTECSInfo_tEntryInfo_tecsgen.h"
#define nTECSInfo_tEntryInfo__IDX_is_ID_act                (false)
#define nTECSInfo_tEntryInfo__sizeOfCB                     ((sizeof(nTECSInfo_tEntryInfo_CB)))
#define nTECSInfo_tEntryInfo__sizeOfINIB                   ((0))
#define nTECSInfo_tEntryInfo__NCELLINLINKUNIT (5)

#include "nTECSInfo_tVarDeclInfo_tecsgen.h"
#define nTECSInfo_tVarDeclInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tVarDeclInfo__sizeOfCB                   ((sizeof(nTECSInfo_tVarDeclInfo_CB)))
#define nTECSInfo_tVarDeclInfo__sizeOfINIB                 ((0))
#define nTECSInfo_tVarDeclInfo__NCELLINLINKUNIT (19)

#include "nTECSInfo_tRegionInfo_tecsgen.h"
#define nTECSInfo_tRegionInfo__IDX_is_ID_act               (false)
#define nTECSInfo_tRegionInfo__sizeOfCB                    ((sizeof(nTECSInfo_tRegionInfo_CB)))
#define nTECSInfo_tRegionInfo__sizeOfINIB                  ((0))
#define nTECSInfo_tRegionInfo__NCELLINLINKUNIT (3)

#include "nTECSInfo_tCellInfo_tecsgen.h"
#define nTECSInfo_tCellInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tCellInfo__sizeOfCB                      ((sizeof(nTECSInfo_tCellInfo_CB)))
#define nTECSInfo_tCellInfo__sizeOfINIB                    ((0))
#define nTECSInfo_tCellInfo__NCELLINLINKUNIT (5)

#include "nTECSInfo_tRawEntryDescriptorInfo_tecsgen.h"
#define nTECSInfo_tRawEntryDescriptorInfo__IDX_is_ID_act   (false)
#define nTECSInfo_tRawEntryDescriptorInfo__sizeOfCB        ((sizeof(nTECSInfo_tRawEntryDescriptorInfo_CB)))
#define nTECSInfo_tRawEntryDescriptorInfo__sizeOfINIB      ((0))
#define nTECSInfo_tRawEntryDescriptorInfo__NCELLINLINKUNIT (5)

#include "nTECSInfo_tVoidTypeInfo_tecsgen.h"
#define nTECSInfo_tVoidTypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tVoidTypeInfo__sizeOfCB                  ((sizeof(nTECSInfo_tVoidTypeInfo_CB)))
#define nTECSInfo_tVoidTypeInfo__sizeOfINIB                ((0))
#define nTECSInfo_tVoidTypeInfo__NCELLINLINKUNIT (2)

#include "nTECSInfo_tBoolTypeInfo_tecsgen.h"
#define nTECSInfo_tBoolTypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tBoolTypeInfo__sizeOfCB                  ((sizeof(nTECSInfo_tBoolTypeInfo_CB)))
#define nTECSInfo_tBoolTypeInfo__sizeOfINIB                ((0))
#define nTECSInfo_tBoolTypeInfo__NCELLINLINKUNIT (1)

#include "nTECSInfo_tIntTypeInfo_tecsgen.h"
#define nTECSInfo_tIntTypeInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tIntTypeInfo__sizeOfCB                   ((sizeof(nTECSInfo_tIntTypeInfo_CB)))
#define nTECSInfo_tIntTypeInfo__sizeOfINIB                 ((0))
#define nTECSInfo_tIntTypeInfo__NCELLINLINKUNIT (11)

#include "nTECSInfo_tStructTypeInfo_tecsgen.h"
#define nTECSInfo_tStructTypeInfo__IDX_is_ID_act           (false)
#define nTECSInfo_tStructTypeInfo__sizeOfCB                ((sizeof(nTECSInfo_tStructTypeInfo_CB)))
#define nTECSInfo_tStructTypeInfo__sizeOfINIB              ((0))
#define nTECSInfo_tStructTypeInfo__NCELLINLINKUNIT (3)

#include "nTECSInfo_tPtrTypeInfo_tecsgen.h"
#define nTECSInfo_tPtrTypeInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tPtrTypeInfo__sizeOfCB                   ((sizeof(nTECSInfo_tPtrTypeInfo_CB)))
#define nTECSInfo_tPtrTypeInfo__sizeOfINIB                 ((0))
#define nTECSInfo_tPtrTypeInfo__NCELLINLINKUNIT (28)

#include "nTECSInfo_tDefinedTypeInfo_tecsgen.h"
#define nTECSInfo_tDefinedTypeInfo__IDX_is_ID_act          (false)
#define nTECSInfo_tDefinedTypeInfo__sizeOfCB               ((sizeof(nTECSInfo_tDefinedTypeInfo_CB)))
#define nTECSInfo_tDefinedTypeInfo__sizeOfINIB             ((0))
#define nTECSInfo_tDefinedTypeInfo__NCELLINLINKUNIT (22)

#include "nTECSInfo_tDescriptorTypeInfo_tecsgen.h"
#define nTECSInfo_tDescriptorTypeInfo__IDX_is_ID_act       (false)
#define nTECSInfo_tDescriptorTypeInfo__sizeOfCB            ((sizeof(nTECSInfo_tDescriptorTypeInfo_CB)))
#define nTECSInfo_tDescriptorTypeInfo__sizeOfINIB          ((0))
#define nTECSInfo_tDescriptorTypeInfo__NCELLINLINKUNIT (12)
/* iteration code (FOREACH_CELL) #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nTECSInfo_tCelltypeInfo_N_CELL; (i)++ ){ \
       (p_cb) = &nTECSInfo_tCelltypeInfo_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB initialize macro #_CIM_# */
#define INITIALIZE_CB(p_that)	(void)(p_that);
#define SET_CB_INIB_POINTER(i,p_that)\
	/* empty */

#endif /* tCelltypeInfo_FACTORY_H */
