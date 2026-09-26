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

#include "tSysLog_tecsgen.h"
#define tSysLog__IDX_is_ID_act                             (false)
#define tSysLog__sizeOfCB                                  ((0))
#define tSysLog__sizeOfINIB                                ((0))
#define tSysLog__NCELLINLINKUNIT       (1)

#include "tTask_tecsgen.h"
#define tTask__IDX_is_ID_act                               (false)
#define tTask__sizeOfCB                                    ((sizeof(tTask_CB)))
#define tTask__sizeOfINIB                                  ((sizeof(tTask_INIB)))
#define tTask__NCELLINLINKUNIT         (1)

#include "tKernel_tecsgen.h"
#define tKernel__IDX_is_ID_act                             (false)
#define tKernel__sizeOfCB                                  ((0))
#define tKernel__sizeOfINIB                                ((0))
#define tKernel__NCELLINLINKUNIT       (1)
#define tSemaphore__IDX_is_ID_act                          (false)
#define tSemaphore__sizeOfCB                               (0)
#define tSemaphore__sizeOfINIB                             (0)
#define tSemaphore__NCELLINLINKUNIT    (0)

#include "tNBOTDR_tecsgen.h"
#define tNBOTDR__IDX_is_ID_act                             (false)
#define tNBOTDR__sizeOfCB                                  ((sizeof(tNBOTDR_CB)))
#define tNBOTDR__sizeOfINIB                                ((0))
#define tNBOTDR__NCELLINLINKUNIT       (1)

#include "tRPCDedicatedTaskMainWithOpener_tecsgen.h"
#define tRPCDedicatedTaskMainWithOpener__IDX_is_ID_act     (false)
#define tRPCDedicatedTaskMainWithOpener__sizeOfCB          ((0))
#define tRPCDedicatedTaskMainWithOpener__sizeOfINIB        ((sizeof(tRPCDedicatedTaskMainWithOpener_INIB)))
#define tRPCDedicatedTaskMainWithOpener__NCELLINLINKUNIT (1)

#include "tPPAllocator_tecsgen.h"
#define tPPAllocator__IDX_is_ID_act                        (false)
#define tPPAllocator__sizeOfCB                             ((sizeof(tPPAllocator_CB)))
#define tPPAllocator__sizeOfINIB                           ((sizeof(tPPAllocator_INIB)))
#define tPPAllocator__NCELLINLINKUNIT  (1)
#define tSocketClient__IDX_is_ID_act                       (false)
#define tSocketClient__sizeOfCB                            (0)
#define tSocketClient__sizeOfINIB                          (0)
#define tSocketClient__NCELLINLINKUNIT (0)

#include "tSocketServer_tecsgen.h"
#define tSocketServer__IDX_is_ID_act                       (false)
#define tSocketServer__sizeOfCB                            ((sizeof(tSocketServer_CB)))
#define tSocketServer__sizeOfINIB                          ((sizeof(tSocketServer_INIB)))
#define tSocketServer__NCELLINLINKUNIT (1)

#include "tAlloc_tecsgen.h"
#define tAlloc__IDX_is_ID_act                              (false)
#define tAlloc__sizeOfCB                                   ((sizeof(tAlloc_CB)))
#define tAlloc__sizeOfINIB                                 ((sizeof(tAlloc_INIB)))
#define tAlloc__NCELLINLINKUNIT        (1)

#include "tSimpleServer_tecsgen.h"
#define tSimpleServer__IDX_is_ID_act                       (false)
#define tSimpleServer__sizeOfCB                            ((0))
#define tSimpleServer__sizeOfINIB                          ((0))
#define tSimpleServer__NCELLINLINKUNIT (1)
#define tSimpleClient__IDX_is_ID_act                       (false)
#define tSimpleClient__sizeOfCB                            (0)
#define tSimpleClient__sizeOfINIB                          (0)
#define tSimpleClient__NCELLINLINKUNIT (0)
#define tClientRPCErrorHandler__IDX_is_ID_act              (false)
#define tClientRPCErrorHandler__sizeOfCB                   (0)
#define tClientRPCErrorHandler__sizeOfINIB                 (0)
#define tClientRPCErrorHandler__NCELLINLINKUNIT (0)

#include "tServerRPCErrorHandler_tecsgen.h"
#define tServerRPCErrorHandler__IDX_is_ID_act              (false)
#define tServerRPCErrorHandler__sizeOfCB                   ((0))
#define tServerRPCErrorHandler__sizeOfINIB                 ((0))
#define tServerRPCErrorHandler__NCELLINLINKUNIT (1)

#include "tTracePlugin_sSimple_tecsgen.h"
#define tTracePlugin_sSimple__IDX_is_ID_act                (false)
#define tTracePlugin_sSimple__sizeOfCB                     ((0))
#define tTracePlugin_sSimple__sizeOfINIB                   ((sizeof(tTracePlugin_sSimple_INIB)))
#define tTracePlugin_sSimple__NCELLINLINKUNIT (1)
#define tOpaqueMarshaler_sSimple__IDX_is_ID_act            (false)
#define tOpaqueMarshaler_sSimple__sizeOfCB                 (0)
#define tOpaqueMarshaler_sSimple__sizeOfINIB               (0)
#define tOpaqueMarshaler_sSimple__NCELLINLINKUNIT (0)

#include "tOpaqueUnmarshaler_sSimple_tecsgen.h"
#define tOpaqueUnmarshaler_sSimple__IDX_is_ID_act          (false)
#define tOpaqueUnmarshaler_sSimple__sizeOfCB               ((0))
#define tOpaqueUnmarshaler_sSimple__sizeOfINIB             ((0))
#define tOpaqueUnmarshaler_sSimple__NCELLINLINKUNIT (1)

#include "nTECSInfo_tTECSInfo_tecsgen.h"
#define nTECSInfo_tTECSInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tTECSInfo__sizeOfCB                      ((0))
#define nTECSInfo_tTECSInfo__sizeOfINIB                    ((0))
#define nTECSInfo_tTECSInfo__NCELLINLINKUNIT (1)

#include "nTECSInfo_tTECSInfoSub_tecsgen.h"
#define nTECSInfo_tTECSInfoSub__IDX_is_ID_act              (false)
#define nTECSInfo_tTECSInfoSub__sizeOfCB                   ((sizeof(nTECSInfo_tTECSInfoSub_CB)))
#define nTECSInfo_tTECSInfoSub__sizeOfINIB                 ((sizeof(nTECSInfo_tTECSInfoSub_INIB)))
#define nTECSInfo_tTECSInfoSub__NCELLINLINKUNIT (1)

#include "nTECSInfo_tNamespaceInfo_tecsgen.h"
#define nTECSInfo_tNamespaceInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tNamespaceInfo__sizeOfCB                 ((0))
#define nTECSInfo_tNamespaceInfo__sizeOfINIB               ((sizeof(nTECSInfo_tNamespaceInfo_INIB)))
#define nTECSInfo_tNamespaceInfo__NCELLINLINKUNIT (2)

#include "nTECSInfo_tSignatureInfo_tecsgen.h"
#define nTECSInfo_tSignatureInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tSignatureInfo__sizeOfCB                 ((0))
#define nTECSInfo_tSignatureInfo__sizeOfINIB               ((sizeof(nTECSInfo_tSignatureInfo_INIB)))
#define nTECSInfo_tSignatureInfo__NCELLINLINKUNIT (34)

#include "nTECSInfo_tFunctionInfo_tecsgen.h"
#define nTECSInfo_tFunctionInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tFunctionInfo__sizeOfCB                  ((0))
#define nTECSInfo_tFunctionInfo__sizeOfINIB                ((sizeof(nTECSInfo_tFunctionInfo_INIB)))
#define nTECSInfo_tFunctionInfo__NCELLINLINKUNIT (252)

#include "nTECSInfo_tParamInfo_tecsgen.h"
#define nTECSInfo_tParamInfo__IDX_is_ID_act                (false)
#define nTECSInfo_tParamInfo__sizeOfCB                     ((0))
#define nTECSInfo_tParamInfo__sizeOfINIB                   ((sizeof(nTECSInfo_tParamInfo_INIB)))
#define nTECSInfo_tParamInfo__NCELLINLINKUNIT (296)

#include "nTECSInfo_tCelltypeInfo_tecsgen.h"
#define nTECSInfo_tCelltypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tCelltypeInfo__sizeOfCB                  ((0))
#define nTECSInfo_tCelltypeInfo__sizeOfINIB                ((sizeof(nTECSInfo_tCelltypeInfo_INIB)))
#define nTECSInfo_tCelltypeInfo__NCELLINLINKUNIT (18)

#include "nTECSInfo_tCallInfo_tecsgen.h"
#define nTECSInfo_tCallInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tCallInfo__sizeOfCB                      ((0))
#define nTECSInfo_tCallInfo__sizeOfINIB                    ((sizeof(nTECSInfo_tCallInfo_INIB)))
#define nTECSInfo_tCallInfo__NCELLINLINKUNIT (156)

#include "nTECSInfo_tEntryInfo_tecsgen.h"
#define nTECSInfo_tEntryInfo__IDX_is_ID_act                (false)
#define nTECSInfo_tEntryInfo__sizeOfCB                     ((0))
#define nTECSInfo_tEntryInfo__sizeOfINIB                   ((sizeof(nTECSInfo_tEntryInfo_INIB)))
#define nTECSInfo_tEntryInfo__NCELLINLINKUNIT (23)

#include "nTECSInfo_tVarDeclInfo_tecsgen.h"
#define nTECSInfo_tVarDeclInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tVarDeclInfo__sizeOfCB                   ((0))
#define nTECSInfo_tVarDeclInfo__sizeOfINIB                 ((sizeof(nTECSInfo_tVarDeclInfo_INIB)))
#define nTECSInfo_tVarDeclInfo__NCELLINLINKUNIT (55)

#include "nTECSInfo_tRegionInfo_tecsgen.h"
#define nTECSInfo_tRegionInfo__IDX_is_ID_act               (false)
#define nTECSInfo_tRegionInfo__sizeOfCB                    ((0))
#define nTECSInfo_tRegionInfo__sizeOfINIB                  ((sizeof(nTECSInfo_tRegionInfo_INIB)))
#define nTECSInfo_tRegionInfo__NCELLINLINKUNIT (3)

#include "nTECSInfo_tCellInfo_tecsgen.h"
#define nTECSInfo_tCellInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tCellInfo__sizeOfCB                      ((0))
#define nTECSInfo_tCellInfo__sizeOfINIB                    ((sizeof(nTECSInfo_tCellInfo_INIB)))
#define nTECSInfo_tCellInfo__NCELLINLINKUNIT (13)

#include "nTECSInfo_tRawEntryDescriptorInfo_tecsgen.h"
#define nTECSInfo_tRawEntryDescriptorInfo__IDX_is_ID_act   (false)
#define nTECSInfo_tRawEntryDescriptorInfo__sizeOfCB        ((0))
#define nTECSInfo_tRawEntryDescriptorInfo__sizeOfINIB      ((sizeof(nTECSInfo_tRawEntryDescriptorInfo_INIB)))
#define nTECSInfo_tRawEntryDescriptorInfo__NCELLINLINKUNIT (15)

#include "nTECSInfo_tVoidTypeInfo_tecsgen.h"
#define nTECSInfo_tVoidTypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tVoidTypeInfo__sizeOfCB                  ((0))
#define nTECSInfo_tVoidTypeInfo__sizeOfINIB                ((sizeof(nTECSInfo_tVoidTypeInfo_INIB)))
#define nTECSInfo_tVoidTypeInfo__NCELLINLINKUNIT (2)

#include "nTECSInfo_tBoolTypeInfo_tecsgen.h"
#define nTECSInfo_tBoolTypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tBoolTypeInfo__sizeOfCB                  ((0))
#define nTECSInfo_tBoolTypeInfo__sizeOfINIB                ((sizeof(nTECSInfo_tBoolTypeInfo_INIB)))
#define nTECSInfo_tBoolTypeInfo__NCELLINLINKUNIT (1)

#include "nTECSInfo_tIntTypeInfo_tecsgen.h"
#define nTECSInfo_tIntTypeInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tIntTypeInfo__sizeOfCB                   ((0))
#define nTECSInfo_tIntTypeInfo__sizeOfINIB                 ((sizeof(nTECSInfo_tIntTypeInfo_INIB)))
#define nTECSInfo_tIntTypeInfo__NCELLINLINKUNIT (26)

#include "nTECSInfo_tFloatTypeInfo_tecsgen.h"
#define nTECSInfo_tFloatTypeInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tFloatTypeInfo__sizeOfCB                 ((0))
#define nTECSInfo_tFloatTypeInfo__sizeOfINIB               ((sizeof(nTECSInfo_tFloatTypeInfo_INIB)))
#define nTECSInfo_tFloatTypeInfo__NCELLINLINKUNIT (2)

#include "nTECSInfo_tStructTypeInfo_tecsgen.h"
#define nTECSInfo_tStructTypeInfo__IDX_is_ID_act           (false)
#define nTECSInfo_tStructTypeInfo__sizeOfCB                ((0))
#define nTECSInfo_tStructTypeInfo__sizeOfINIB              ((sizeof(nTECSInfo_tStructTypeInfo_INIB)))
#define nTECSInfo_tStructTypeInfo__NCELLINLINKUNIT (7)

#include "nTECSInfo_tPtrTypeInfo_tecsgen.h"
#define nTECSInfo_tPtrTypeInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tPtrTypeInfo__sizeOfCB                   ((0))
#define nTECSInfo_tPtrTypeInfo__sizeOfINIB                 ((sizeof(nTECSInfo_tPtrTypeInfo_INIB)))
#define nTECSInfo_tPtrTypeInfo__NCELLINLINKUNIT (66)

#include "nTECSInfo_tArrayTypeInfo_tecsgen.h"
#define nTECSInfo_tArrayTypeInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tArrayTypeInfo__sizeOfCB                 ((0))
#define nTECSInfo_tArrayTypeInfo__sizeOfINIB               ((sizeof(nTECSInfo_tArrayTypeInfo_INIB)))
#define nTECSInfo_tArrayTypeInfo__NCELLINLINKUNIT (9)

#include "nTECSInfo_tDefinedTypeInfo_tecsgen.h"
#define nTECSInfo_tDefinedTypeInfo__IDX_is_ID_act          (false)
#define nTECSInfo_tDefinedTypeInfo__sizeOfCB               ((0))
#define nTECSInfo_tDefinedTypeInfo__sizeOfINIB             ((sizeof(nTECSInfo_tDefinedTypeInfo_INIB)))
#define nTECSInfo_tDefinedTypeInfo__NCELLINLINKUNIT (34)

#include "nTECSInfo_tDescriptorTypeInfo_tecsgen.h"
#define nTECSInfo_tDescriptorTypeInfo__IDX_is_ID_act       (false)
#define nTECSInfo_tDescriptorTypeInfo__sizeOfCB            ((0))
#define nTECSInfo_tDescriptorTypeInfo__sizeOfINIB          ((sizeof(nTECSInfo_tDescriptorTypeInfo_INIB)))
#define nTECSInfo_tDescriptorTypeInfo__NCELLINLINKUNIT (12)
/* iteration code (FOREACH_CELL) #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nTECSInfo_tCelltypeInfo_N_CELL; (i)++ ){ \
       //(p_cb) = &nTECSInfo_tCelltypeInfo_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB initialize macro #_CIM_# */

#endif /* tCelltypeInfo_FACTORY_H */
