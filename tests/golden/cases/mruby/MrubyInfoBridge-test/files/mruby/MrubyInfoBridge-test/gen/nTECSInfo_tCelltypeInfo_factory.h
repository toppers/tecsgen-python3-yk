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
#define tTask__sizeOfINIB                                  ((sizeof(tTask_INIB)))
#define tTask__NCELLINLINKUNIT         (2)

#include "tKernel_tecsgen.h"
#define tKernel__IDX_is_ID_act                             (false)
#define tKernel__sizeOfCB                                  ((0))
#define tKernel__sizeOfINIB                                ((0))
#define tKernel__NCELLINLINKUNIT       (1)

#include "tSysLog_tecsgen.h"
#define tSysLog__IDX_is_ID_act                             (false)
#define tSysLog__sizeOfCB                                  ((0))
#define tSysLog__sizeOfINIB                                ((0))
#define tSysLog__NCELLINLINKUNIT       (1)

#include "tSig_tecsgen.h"
#define tSig__IDX_is_ID_act                                (false)
#define tSig__sizeOfCB                                     ((0))
#define tSig__sizeOfINIB                                   ((0))
#define tSig__NCELLINLINKUNIT          (3)

#include "tTaskMain2PosixMain_tecsgen.h"
#define tTaskMain2PosixMain__IDX_is_ID_act                 (false)
#define tTaskMain2PosixMain__sizeOfCB                      ((0))
#define tTaskMain2PosixMain__sizeOfINIB                    ((sizeof(tTaskMain2PosixMain_INIB)))
#define tTaskMain2PosixMain__NCELLINLINKUNIT (2)

#include "tTracePlugin_sSig_tecsgen.h"
#define tTracePlugin_sSig__IDX_is_ID_act                   (false)
#define tTracePlugin_sSig__sizeOfCB                        ((0))
#define tTracePlugin_sSig__sizeOfINIB                      ((sizeof(tTracePlugin_sSig_INIB)))
#define tTracePlugin_sSig__NCELLINLINKUNIT (3)

#include "nMruby_tTECSInitializer_tecsgen.h"
#define nMruby_tTECSInitializer__IDX_is_ID_act             (false)
#define nMruby_tTECSInitializer__sizeOfCB                  ((sizeof(nMruby_tTECSInitializer_CB)))
#define nMruby_tTECSInitializer__sizeOfINIB                ((sizeof(nMruby_tTECSInitializer_INIB)))
#define nMruby_tTECSInitializer__NCELLINLINKUNIT (2)

#include "nMruby_tBoolPointer_tecsgen.h"
#define nMruby_tBoolPointer__IDX_is_ID_act                 (false)
#define nMruby_tBoolPointer__sizeOfCB                      ((0))
#define nMruby_tBoolPointer__sizeOfINIB                    ((0))
#define nMruby_tBoolPointer__NCELLINLINKUNIT (1)

#include "nMruby_tCharPointer_tecsgen.h"
#define nMruby_tCharPointer__IDX_is_ID_act                 (false)
#define nMruby_tCharPointer__sizeOfCB                      ((0))
#define nMruby_tCharPointer__sizeOfINIB                    ((0))
#define nMruby_tCharPointer__NCELLINLINKUNIT (1)

#include "nMruby_tSCharPointer_tecsgen.h"
#define nMruby_tSCharPointer__IDX_is_ID_act                (false)
#define nMruby_tSCharPointer__sizeOfCB                     ((0))
#define nMruby_tSCharPointer__sizeOfINIB                   ((0))
#define nMruby_tSCharPointer__NCELLINLINKUNIT (1)

#include "nMruby_tUCharPointer_tecsgen.h"
#define nMruby_tUCharPointer__IDX_is_ID_act                (false)
#define nMruby_tUCharPointer__sizeOfCB                     ((0))
#define nMruby_tUCharPointer__sizeOfINIB                   ((0))
#define nMruby_tUCharPointer__NCELLINLINKUNIT (1)

#include "nMruby_tInt8Pointer_tecsgen.h"
#define nMruby_tInt8Pointer__IDX_is_ID_act                 (false)
#define nMruby_tInt8Pointer__sizeOfCB                      ((0))
#define nMruby_tInt8Pointer__sizeOfINIB                    ((0))
#define nMruby_tInt8Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tInt16Pointer_tecsgen.h"
#define nMruby_tInt16Pointer__IDX_is_ID_act                (false)
#define nMruby_tInt16Pointer__sizeOfCB                     ((0))
#define nMruby_tInt16Pointer__sizeOfINIB                   ((0))
#define nMruby_tInt16Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tInt32Pointer_tecsgen.h"
#define nMruby_tInt32Pointer__IDX_is_ID_act                (false)
#define nMruby_tInt32Pointer__sizeOfCB                     ((0))
#define nMruby_tInt32Pointer__sizeOfINIB                   ((0))
#define nMruby_tInt32Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tInt64Pointer_tecsgen.h"
#define nMruby_tInt64Pointer__IDX_is_ID_act                (false)
#define nMruby_tInt64Pointer__sizeOfCB                     ((0))
#define nMruby_tInt64Pointer__sizeOfINIB                   ((0))
#define nMruby_tInt64Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tUInt8Pointer_tecsgen.h"
#define nMruby_tUInt8Pointer__IDX_is_ID_act                (false)
#define nMruby_tUInt8Pointer__sizeOfCB                     ((0))
#define nMruby_tUInt8Pointer__sizeOfINIB                   ((0))
#define nMruby_tUInt8Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tUInt16Pointer_tecsgen.h"
#define nMruby_tUInt16Pointer__IDX_is_ID_act               (false)
#define nMruby_tUInt16Pointer__sizeOfCB                    ((0))
#define nMruby_tUInt16Pointer__sizeOfINIB                  ((0))
#define nMruby_tUInt16Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tUInt32Pointer_tecsgen.h"
#define nMruby_tUInt32Pointer__IDX_is_ID_act               (false)
#define nMruby_tUInt32Pointer__sizeOfCB                    ((0))
#define nMruby_tUInt32Pointer__sizeOfINIB                  ((0))
#define nMruby_tUInt32Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tUInt64Pointer_tecsgen.h"
#define nMruby_tUInt64Pointer__IDX_is_ID_act               (false)
#define nMruby_tUInt64Pointer__sizeOfCB                    ((0))
#define nMruby_tUInt64Pointer__sizeOfINIB                  ((0))
#define nMruby_tUInt64Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tFloat32Pointer_tecsgen.h"
#define nMruby_tFloat32Pointer__IDX_is_ID_act              (false)
#define nMruby_tFloat32Pointer__sizeOfCB                   ((0))
#define nMruby_tFloat32Pointer__sizeOfINIB                 ((0))
#define nMruby_tFloat32Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tDouble64Pointer_tecsgen.h"
#define nMruby_tDouble64Pointer__IDX_is_ID_act             (false)
#define nMruby_tDouble64Pointer__sizeOfCB                  ((0))
#define nMruby_tDouble64Pointer__sizeOfINIB                ((0))
#define nMruby_tDouble64Pointer__NCELLINLINKUNIT (1)

#include "nMruby_tIntPointer_tecsgen.h"
#define nMruby_tIntPointer__IDX_is_ID_act                  (false)
#define nMruby_tIntPointer__sizeOfCB                       ((0))
#define nMruby_tIntPointer__sizeOfINIB                     ((0))
#define nMruby_tIntPointer__NCELLINLINKUNIT (1)

#include "nMruby_tShortPointer_tecsgen.h"
#define nMruby_tShortPointer__IDX_is_ID_act                (false)
#define nMruby_tShortPointer__sizeOfCB                     ((0))
#define nMruby_tShortPointer__sizeOfINIB                   ((0))
#define nMruby_tShortPointer__NCELLINLINKUNIT (1)

#include "nMruby_tLongPointer_tecsgen.h"
#define nMruby_tLongPointer__IDX_is_ID_act                 (false)
#define nMruby_tLongPointer__sizeOfCB                      ((0))
#define nMruby_tLongPointer__sizeOfINIB                    ((0))
#define nMruby_tLongPointer__NCELLINLINKUNIT (1)

#include "nMruby_tUIntPointer_tecsgen.h"
#define nMruby_tUIntPointer__IDX_is_ID_act                 (false)
#define nMruby_tUIntPointer__sizeOfCB                      ((0))
#define nMruby_tUIntPointer__sizeOfINIB                    ((0))
#define nMruby_tUIntPointer__NCELLINLINKUNIT (1)

#include "nMruby_tUShortPointer_tecsgen.h"
#define nMruby_tUShortPointer__IDX_is_ID_act               (false)
#define nMruby_tUShortPointer__sizeOfCB                    ((0))
#define nMruby_tUShortPointer__sizeOfINIB                  ((0))
#define nMruby_tUShortPointer__NCELLINLINKUNIT (1)

#include "nMruby_tULongPointer_tecsgen.h"
#define nMruby_tULongPointer__IDX_is_ID_act                (false)
#define nMruby_tULongPointer__sizeOfCB                     ((0))
#define nMruby_tULongPointer__sizeOfINIB                   ((0))
#define nMruby_tULongPointer__NCELLINLINKUNIT (1)

#include "nMruby_tMrubyProc_tecsgen.h"
#define nMruby_tMrubyProc__IDX_is_ID_act                   (false)
#define nMruby_tMrubyProc__sizeOfCB                        ((sizeof(nMruby_tMrubyProc_CB)))
#define nMruby_tMrubyProc__sizeOfINIB                      ((sizeof(nMruby_tMrubyProc_INIB)))
#define nMruby_tMrubyProc__NCELLINLINKUNIT (2)

#include "nMruby_tsSig_tecsgen.h"
#define nMruby_tsSig__IDX_is_ID_act                        (true)
#define nMruby_tsSig__sizeOfCB                             ((0))
#define nMruby_tsSig__sizeOfINIB                           ((sizeof(nMruby_tsSig_INIB)))
#define nMruby_tsSig__NCELLINLINKUNIT  (3)

#include "nMruby_tsSig_Initializer_tecsgen.h"
#define nMruby_tsSig_Initializer__IDX_is_ID_act            (false)
#define nMruby_tsSig_Initializer__sizeOfCB                 ((0))
#define nMruby_tsSig_Initializer__sizeOfINIB               ((0))
#define nMruby_tsSig_Initializer__NCELLINLINKUNIT (2)

#include "nMruby_tag_tecsgen.h"
#define nMruby_tag__IDX_is_ID_act                          (false)
#define nMruby_tag__sizeOfCB                               ((0))
#define nMruby_tag__sizeOfINIB                             ((0))
#define nMruby_tag__NCELLINLINKUNIT    (1)

#include "nMruby_tsTask_tecsgen.h"
#define nMruby_tsTask__IDX_is_ID_act                       (true)
#define nMruby_tsTask__sizeOfCB                            ((0))
#define nMruby_tsTask__sizeOfINIB                          ((sizeof(nMruby_tsTask_INIB)))
#define nMruby_tsTask__NCELLINLINKUNIT (2)

#include "nMruby_tsTask_Initializer_tecsgen.h"
#define nMruby_tsTask_Initializer__IDX_is_ID_act           (false)
#define nMruby_tsTask_Initializer__sizeOfCB                ((0))
#define nMruby_tsTask_Initializer__sizeOfINIB              ((0))
#define nMruby_tsTask_Initializer__NCELLINLINKUNIT (1)

#include "nMruby_tnTECSInfo_sAccessor_tecsgen.h"
#define nMruby_tnTECSInfo_sAccessor__IDX_is_ID_act         (true)
#define nMruby_tnTECSInfo_sAccessor__sizeOfCB              ((0))
#define nMruby_tnTECSInfo_sAccessor__sizeOfINIB            ((0))
#define nMruby_tnTECSInfo_sAccessor__NCELLINLINKUNIT (1)

#include "nMruby_tnTECSInfo_sAccessor_Initializer_tecsgen.h"
#define nMruby_tnTECSInfo_sAccessor_Initializer__IDX_is_ID_act (false)
#define nMruby_tnTECSInfo_sAccessor_Initializer__sizeOfCB  ((0))
#define nMruby_tnTECSInfo_sAccessor_Initializer__sizeOfINIB ((0))
#define nMruby_tnTECSInfo_sAccessor_Initializer__NCELLINLINKUNIT (1)

#include "nMruby_t_rsem_tecsgen.h"
#define nMruby_t_rsem__IDX_is_ID_act                       (false)
#define nMruby_t_rsem__sizeOfCB                            ((0))
#define nMruby_t_rsem__sizeOfINIB                          ((0))
#define nMruby_t_rsem__NCELLINLINKUNIT (1)

#include "nMruby_t_rflg_tecsgen.h"
#define nMruby_t_rflg__IDX_is_ID_act                       (false)
#define nMruby_t_rflg__sizeOfCB                            ((0))
#define nMruby_t_rflg__sizeOfINIB                          ((0))
#define nMruby_t_rflg__NCELLINLINKUNIT (1)

#include "nMruby_t_rdtq_tecsgen.h"
#define nMruby_t_rdtq__IDX_is_ID_act                       (false)
#define nMruby_t_rdtq__sizeOfCB                            ((0))
#define nMruby_t_rdtq__sizeOfINIB                          ((0))
#define nMruby_t_rdtq__NCELLINLINKUNIT (1)

#include "nMruby_t_syslog_rlog_tecsgen.h"
#define nMruby_t_syslog_rlog__IDX_is_ID_act                (false)
#define nMruby_t_syslog_rlog__sizeOfCB                     ((0))
#define nMruby_t_syslog_rlog__sizeOfINIB                   ((0))
#define nMruby_t_syslog_rlog__NCELLINLINKUNIT (1)

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
#define nTECSInfo_tNamespaceInfo__NCELLINLINKUNIT (5)

#include "nTECSInfo_tSignatureInfo_tecsgen.h"
#define nTECSInfo_tSignatureInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tSignatureInfo__sizeOfCB                 ((0))
#define nTECSInfo_tSignatureInfo__sizeOfINIB               ((sizeof(nTECSInfo_tSignatureInfo_INIB)))
#define nTECSInfo_tSignatureInfo__NCELLINLINKUNIT (31)

#include "nTECSInfo_tFunctionInfo_tecsgen.h"
#define nTECSInfo_tFunctionInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tFunctionInfo__sizeOfCB                  ((0))
#define nTECSInfo_tFunctionInfo__sizeOfINIB                ((sizeof(nTECSInfo_tFunctionInfo_INIB)))
#define nTECSInfo_tFunctionInfo__NCELLINLINKUNIT (211)

#include "nTECSInfo_tParamInfo_tecsgen.h"
#define nTECSInfo_tParamInfo__IDX_is_ID_act                (false)
#define nTECSInfo_tParamInfo__sizeOfCB                     ((0))
#define nTECSInfo_tParamInfo__sizeOfINIB                   ((sizeof(nTECSInfo_tParamInfo_INIB)))
#define nTECSInfo_tParamInfo__NCELLINLINKUNIT (294)

#include "nTECSInfo_tCelltypeInfo_tecsgen.h"
#define nTECSInfo_tCelltypeInfo__IDX_is_ID_act             (false)
#define nTECSInfo_tCelltypeInfo__sizeOfCB                  ((0))
#define nTECSInfo_tCelltypeInfo__sizeOfINIB                ((sizeof(nTECSInfo_tCelltypeInfo_INIB)))
#define nTECSInfo_tCelltypeInfo__NCELLINLINKUNIT (73)

#include "nTECSInfo_tCallInfo_tecsgen.h"
#define nTECSInfo_tCallInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tCallInfo__sizeOfCB                      ((0))
#define nTECSInfo_tCallInfo__sizeOfINIB                    ((sizeof(nTECSInfo_tCallInfo_INIB)))
#define nTECSInfo_tCallInfo__NCELLINLINKUNIT (106)

#include "nTECSInfo_tEntryInfo_tecsgen.h"
#define nTECSInfo_tEntryInfo__IDX_is_ID_act                (false)
#define nTECSInfo_tEntryInfo__sizeOfCB                     ((0))
#define nTECSInfo_tEntryInfo__sizeOfINIB                   ((sizeof(nTECSInfo_tEntryInfo_INIB)))
#define nTECSInfo_tEntryInfo__NCELLINLINKUNIT (56)

#include "nTECSInfo_tVarDeclInfo_tecsgen.h"
#define nTECSInfo_tVarDeclInfo__IDX_is_ID_act              (false)
#define nTECSInfo_tVarDeclInfo__sizeOfCB                   ((0))
#define nTECSInfo_tVarDeclInfo__sizeOfINIB                 ((sizeof(nTECSInfo_tVarDeclInfo_INIB)))
#define nTECSInfo_tVarDeclInfo__NCELLINLINKUNIT (75)

#include "nTECSInfo_tRegionInfo_tecsgen.h"
#define nTECSInfo_tRegionInfo__IDX_is_ID_act               (false)
#define nTECSInfo_tRegionInfo__sizeOfCB                    ((0))
#define nTECSInfo_tRegionInfo__sizeOfINIB                  ((sizeof(nTECSInfo_tRegionInfo_INIB)))
#define nTECSInfo_tRegionInfo__NCELLINLINKUNIT (2)

#include "nTECSInfo_tCellInfo_tecsgen.h"
#define nTECSInfo_tCellInfo__IDX_is_ID_act                 (false)
#define nTECSInfo_tCellInfo__sizeOfCB                      ((0))
#define nTECSInfo_tCellInfo__sizeOfINIB                    ((sizeof(nTECSInfo_tCellInfo_INIB)))
#define nTECSInfo_tCellInfo__NCELLINLINKUNIT (22)

#include "nTECSInfo_tRawEntryDescriptorInfo_tecsgen.h"
#define nTECSInfo_tRawEntryDescriptorInfo__IDX_is_ID_act   (false)
#define nTECSInfo_tRawEntryDescriptorInfo__sizeOfCB        ((0))
#define nTECSInfo_tRawEntryDescriptorInfo__sizeOfINIB      ((sizeof(nTECSInfo_tRawEntryDescriptorInfo_INIB)))
#define nTECSInfo_tRawEntryDescriptorInfo__NCELLINLINKUNIT (20)

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
#define nTECSInfo_tIntTypeInfo__NCELLINLINKUNIT (24)

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
#define nTECSInfo_tPtrTypeInfo__NCELLINLINKUNIT (58)

#include "nTECSInfo_tArrayTypeInfo_tecsgen.h"
#define nTECSInfo_tArrayTypeInfo__IDX_is_ID_act            (false)
#define nTECSInfo_tArrayTypeInfo__sizeOfCB                 ((0))
#define nTECSInfo_tArrayTypeInfo__sizeOfINIB               ((sizeof(nTECSInfo_tArrayTypeInfo_INIB)))
#define nTECSInfo_tArrayTypeInfo__NCELLINLINKUNIT (1)

#include "nTECSInfo_tDefinedTypeInfo_tecsgen.h"
#define nTECSInfo_tDefinedTypeInfo__IDX_is_ID_act          (false)
#define nTECSInfo_tDefinedTypeInfo__sizeOfCB               ((0))
#define nTECSInfo_tDefinedTypeInfo__sizeOfINIB             ((sizeof(nTECSInfo_tDefinedTypeInfo_INIB)))
#define nTECSInfo_tDefinedTypeInfo__NCELLINLINKUNIT (32)

#include "nTECSInfo_tDescriptorTypeInfo_tecsgen.h"
#define nTECSInfo_tDescriptorTypeInfo__IDX_is_ID_act       (false)
#define nTECSInfo_tDescriptorTypeInfo__sizeOfCB            ((0))
#define nTECSInfo_tDescriptorTypeInfo__sizeOfINIB          ((sizeof(nTECSInfo_tDescriptorTypeInfo_INIB)))
#define nTECSInfo_tDescriptorTypeInfo__NCELLINLINKUNIT (12)

#include "nTECSInfo_tTECSInfoAccessor_tecsgen.h"
#define nTECSInfo_tTECSInfoAccessor__IDX_is_ID_act         (false)
#define nTECSInfo_tTECSInfoAccessor__sizeOfCB              ((sizeof(nTECSInfo_tTECSInfoAccessor_CB)))
#define nTECSInfo_tTECSInfoAccessor__sizeOfINIB            ((sizeof(nTECSInfo_tTECSInfoAccessor_INIB)))
#define nTECSInfo_tTECSInfoAccessor__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosTaskBody_tecsgen.h"
#define nMrubyInfo_tInfosTaskBody__IDX_is_ID_act           (false)
#define nMrubyInfo_tInfosTaskBody__sizeOfCB                ((sizeof(nMrubyInfo_tInfosTaskBody_CB)))
#define nMrubyInfo_tInfosTaskBody__sizeOfINIB              ((0))
#define nMrubyInfo_tInfosTaskBody__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosTaskBody_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosTaskBody_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosTaskBody_Initializer__sizeOfCB    ((0))
#define nMrubyInfo_tInfosTaskBody_Initializer__sizeOfINIB  ((0))
#define nMrubyInfo_tInfosTaskBody_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosTaskExceptionBody_tecsgen.h"
#define nMrubyInfo_tInfosTaskExceptionBody__IDX_is_ID_act  (false)
#define nMrubyInfo_tInfosTaskExceptionBody__sizeOfCB       ((sizeof(nMrubyInfo_tInfosTaskExceptionBody_CB)))
#define nMrubyInfo_tInfosTaskExceptionBody__sizeOfINIB     ((0))
#define nMrubyInfo_tInfosTaskExceptionBody__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosTaskExceptionBody_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosTaskExceptionBody_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosTaskExceptionBody_Initializer__sizeOfCB ((0))
#define nMrubyInfo_tInfosTaskExceptionBody_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosTaskExceptionBody_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosTask_tecsgen.h"
#define nMrubyInfo_tInfosTask__IDX_is_ID_act               (false)
#define nMrubyInfo_tInfosTask__sizeOfCB                    ((sizeof(nMrubyInfo_tInfosTask_CB)))
#define nMrubyInfo_tInfosTask__sizeOfINIB                  ((0))
#define nMrubyInfo_tInfosTask__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosTask_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosTask_Initializer__IDX_is_ID_act   (false)
#define nMrubyInfo_tInfosTask_Initializer__sizeOfCB        ((0))
#define nMrubyInfo_tInfosTask_Initializer__sizeOfINIB      ((0))
#define nMrubyInfo_tInfosTask_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosKernel_tecsgen.h"
#define nMrubyInfo_tInfosKernel__IDX_is_ID_act             (false)
#define nMrubyInfo_tInfosKernel__sizeOfCB                  ((sizeof(nMrubyInfo_tInfosKernel_CB)))
#define nMrubyInfo_tInfosKernel__sizeOfINIB                ((0))
#define nMrubyInfo_tInfosKernel__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosKernel_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosKernel_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosKernel_Initializer__sizeOfCB      ((0))
#define nMrubyInfo_tInfosKernel_Initializer__sizeOfINIB    ((0))
#define nMrubyInfo_tInfosKernel_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiKernel_tecsgen.h"
#define nMrubyInfo_tInfosiKernel__IDX_is_ID_act            (false)
#define nMrubyInfo_tInfosiKernel__sizeOfCB                 ((sizeof(nMrubyInfo_tInfosiKernel_CB)))
#define nMrubyInfo_tInfosiKernel__sizeOfINIB               ((0))
#define nMrubyInfo_tInfosiKernel__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiKernel_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosiKernel_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosiKernel_Initializer__sizeOfCB     ((0))
#define nMrubyInfo_tInfosiKernel_Initializer__sizeOfINIB   ((0))
#define nMrubyInfo_tInfosiKernel_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosSemaphore_tecsgen.h"
#define nMrubyInfo_tInfosSemaphore__IDX_is_ID_act          (false)
#define nMrubyInfo_tInfosSemaphore__sizeOfCB               ((sizeof(nMrubyInfo_tInfosSemaphore_CB)))
#define nMrubyInfo_tInfosSemaphore__sizeOfINIB             ((0))
#define nMrubyInfo_tInfosSemaphore__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosSemaphore_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosSemaphore_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosSemaphore_Initializer__sizeOfCB   ((0))
#define nMrubyInfo_tInfosSemaphore_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosSemaphore_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiSemaphore_tecsgen.h"
#define nMrubyInfo_tInfosiSemaphore__IDX_is_ID_act         (false)
#define nMrubyInfo_tInfosiSemaphore__sizeOfCB              ((sizeof(nMrubyInfo_tInfosiSemaphore_CB)))
#define nMrubyInfo_tInfosiSemaphore__sizeOfINIB            ((0))
#define nMrubyInfo_tInfosiSemaphore__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiSemaphore_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosiSemaphore_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosiSemaphore_Initializer__sizeOfCB  ((0))
#define nMrubyInfo_tInfosiSemaphore_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosiSemaphore_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosEventflag_tecsgen.h"
#define nMrubyInfo_tInfosEventflag__IDX_is_ID_act          (false)
#define nMrubyInfo_tInfosEventflag__sizeOfCB               ((sizeof(nMrubyInfo_tInfosEventflag_CB)))
#define nMrubyInfo_tInfosEventflag__sizeOfINIB             ((0))
#define nMrubyInfo_tInfosEventflag__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosEventflag_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosEventflag_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosEventflag_Initializer__sizeOfCB   ((0))
#define nMrubyInfo_tInfosEventflag_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosEventflag_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiEventflag_tecsgen.h"
#define nMrubyInfo_tInfosiEventflag__IDX_is_ID_act         (false)
#define nMrubyInfo_tInfosiEventflag__sizeOfCB              ((sizeof(nMrubyInfo_tInfosiEventflag_CB)))
#define nMrubyInfo_tInfosiEventflag__sizeOfINIB            ((0))
#define nMrubyInfo_tInfosiEventflag__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiEventflag_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosiEventflag_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosiEventflag_Initializer__sizeOfCB  ((0))
#define nMrubyInfo_tInfosiEventflag_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosiEventflag_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosDataqueue_tecsgen.h"
#define nMrubyInfo_tInfosDataqueue__IDX_is_ID_act          (false)
#define nMrubyInfo_tInfosDataqueue__sizeOfCB               ((sizeof(nMrubyInfo_tInfosDataqueue_CB)))
#define nMrubyInfo_tInfosDataqueue__sizeOfINIB             ((0))
#define nMrubyInfo_tInfosDataqueue__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosDataqueue_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosDataqueue_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosDataqueue_Initializer__sizeOfCB   ((0))
#define nMrubyInfo_tInfosDataqueue_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosDataqueue_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiDataqueue_tecsgen.h"
#define nMrubyInfo_tInfosiDataqueue__IDX_is_ID_act         (false)
#define nMrubyInfo_tInfosiDataqueue__sizeOfCB              ((sizeof(nMrubyInfo_tInfosiDataqueue_CB)))
#define nMrubyInfo_tInfosiDataqueue__sizeOfINIB            ((0))
#define nMrubyInfo_tInfosiDataqueue__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosiDataqueue_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosiDataqueue_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosiDataqueue_Initializer__sizeOfCB  ((0))
#define nMrubyInfo_tInfosiDataqueue_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfosiDataqueue_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosSysLog_tecsgen.h"
#define nMrubyInfo_tInfosSysLog__IDX_is_ID_act             (false)
#define nMrubyInfo_tInfosSysLog__sizeOfCB                  ((sizeof(nMrubyInfo_tInfosSysLog_CB)))
#define nMrubyInfo_tInfosSysLog__sizeOfINIB                ((0))
#define nMrubyInfo_tInfosSysLog__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosSysLog_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosSysLog_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfosSysLog_Initializer__sizeOfCB      ((0))
#define nMrubyInfo_tInfosSysLog_Initializer__sizeOfINIB    ((0))
#define nMrubyInfo_tInfosSysLog_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosSig_tecsgen.h"
#define nMrubyInfo_tInfosSig__IDX_is_ID_act                (false)
#define nMrubyInfo_tInfosSig__sizeOfCB                     ((sizeof(nMrubyInfo_tInfosSig_CB)))
#define nMrubyInfo_tInfosSig__sizeOfINIB                   ((0))
#define nMrubyInfo_tInfosSig__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosSig_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosSig_Initializer__IDX_is_ID_act    (false)
#define nMrubyInfo_tInfosSig_Initializer__sizeOfCB         ((0))
#define nMrubyInfo_tInfosSig_Initializer__sizeOfINIB       ((0))
#define nMrubyInfo_tInfosSig_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosHello_tecsgen.h"
#define nMrubyInfo_tInfosHello__IDX_is_ID_act              (false)
#define nMrubyInfo_tInfosHello__sizeOfCB                   ((sizeof(nMrubyInfo_tInfosHello_CB)))
#define nMrubyInfo_tInfosHello__sizeOfINIB                 ((0))
#define nMrubyInfo_tInfosHello__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfosHello_Initializer_tecsgen.h"
#define nMrubyInfo_tInfosHello_Initializer__IDX_is_ID_act  (false)
#define nMrubyInfo_tInfosHello_Initializer__sizeOfCB       ((0))
#define nMrubyInfo_tInfosHello_Initializer__sizeOfINIB     ((0))
#define nMrubyInfo_tInfosHello_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfonPosix_sMain_tecsgen.h"
#define nMrubyInfo_tInfonPosix_sMain__IDX_is_ID_act        (false)
#define nMrubyInfo_tInfonPosix_sMain__sizeOfCB             ((sizeof(nMrubyInfo_tInfonPosix_sMain_CB)))
#define nMrubyInfo_tInfonPosix_sMain__sizeOfINIB           ((0))
#define nMrubyInfo_tInfonPosix_sMain__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfonPosix_sMain_Initializer_tecsgen.h"
#define nMrubyInfo_tInfonPosix_sMain_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfonPosix_sMain_Initializer__sizeOfCB ((0))
#define nMrubyInfo_tInfonPosix_sMain_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfonPosix_sMain_Initializer__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfonTECSInfo_sAccessor_tecsgen.h"
#define nMrubyInfo_tInfonTECSInfo_sAccessor__IDX_is_ID_act (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor__sizeOfCB      ((sizeof(nMrubyInfo_tInfonTECSInfo_sAccessor_CB)))
#define nMrubyInfo_tInfonTECSInfo_sAccessor__sizeOfINIB    ((0))
#define nMrubyInfo_tInfonTECSInfo_sAccessor__NCELLINLINKUNIT (1)

#include "nMrubyInfo_tInfonTECSInfo_sAccessor_Initializer_tecsgen.h"
#define nMrubyInfo_tInfonTECSInfo_sAccessor_Initializer__IDX_is_ID_act (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_Initializer__sizeOfCB ((0))
#define nMrubyInfo_tInfonTECSInfo_sAccessor_Initializer__sizeOfINIB ((0))
#define nMrubyInfo_tInfonTECSInfo_sAccessor_Initializer__NCELLINLINKUNIT (1)
/* iteration code (FOREACH_CELL) #_FEC_# */
#define FOREACH_CELL(i,p_cb)   \
    for( (i) = 0; (i) < nTECSInfo_tCelltypeInfo_N_CELL; (i)++ ){ \
       //(p_cb) = &nTECSInfo_tCelltypeInfo_CB_tab[i];

#define END_FOREACH_CELL   }

/* CB initialize macro #_CIM_# */

#endif /* tCelltypeInfo_FACTORY_H */
