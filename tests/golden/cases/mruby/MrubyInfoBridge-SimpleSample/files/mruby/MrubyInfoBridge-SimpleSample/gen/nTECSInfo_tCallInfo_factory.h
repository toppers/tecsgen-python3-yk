#ifndef tCallInfo_FACTORY_H
#define tCallInfo_FACTORY_H
#include "include_all_signature_header.h"

/***** Offset of attr & var of celltype  *****/
#define TOPPERS_CB_TYPE_ONLY

/* In case a celltype has 'inline' entry,
 * some macros are temporally defined
 * even if TOPPERS_CB_TYPE_ONLY is defined.
 * To avoid redefinition warning, undef these macros.
 */
#undef VALID_IDX
#undef GET_CELLCB
#undef CELLCB
#undef CELLIDX
#undef tCallInfo_IDX
#undef ATTR_name
#undef ATTR_offset
#undef ATTR_b_inCB
#undef ATTR_b_optional
#undef ATTR_b_omit
#undef ATTR_b_dynamic
#undef ATTR_b_ref_desc
#undef ATTR_b_allocator_port
#undef ATTR_b_require_port
#undef ATTR_b_VMT_useless
#undef ATTR_b_skelton_useless
#undef ATTR_b_cell_unique
#undef cSignatureInfo_getName
#undef cSignatureInfo_getNameLength
#undef cSignatureInfo_getNFunction
#undef cSignatureInfo_getFunctionInfo
#undef cSignatureInfo_refer_to_descriptor
#undef cSignatureInfo_ref_desc
#undef eCallInfo_getName
#undef eCallInfo_getNameLength
#undef eCallInfo_getSignatureInfo
#undef eCallInfo_getArraySize
#undef eCallInfo_isOptional
#undef eCallInfo_isDynamic
#undef eCallInfo_isRefDesc
#undef eCallInfo_isOmit
#undef FOREACH_CELL


#include "tSysLog_tecsgen.h"

#include "tSample_tecsgen.h"

#include "nTECSInfo_tTECSInfo_tecsgen.h"
#define nTECSInfo_tTECSInfo_cTECSInfo__offset              (0xffffffff)
#define nTECSInfo_tTECSInfo_cTECSInfo__array_size          (0)
#define nTECSInfo_tTECSInfo_cTECSInfo__place               (CALL_PLACE_NON)
#define nTECSInfo_tTECSInfo_cTECSInfo__b_VMT_useless       (true)
#define nTECSInfo_tTECSInfo_cTECSInfo__b_skelton_useless   (true)
#define nTECSInfo_tTECSInfo_cTECSInfo__b_cell_unique       (true)

#include "nTECSInfo_tTECSInfoSub_tecsgen.h"
#define nTECSInfo_tTECSInfoSub_cNamespaceInfo__offset      ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_INIB*)0)->cNamespaceInfo)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfo__array_size  (0)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfo__place       (CALL_PLACE_INIB_DES)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cRegionInfo__offset         ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_INIB*)0)->cRegionInfo)
#define nTECSInfo_tTECSInfoSub_cRegionInfo__array_size     (0)
#define nTECSInfo_tTECSInfoSub_cRegionInfo__place          (CALL_PLACE_INIB_DES)
#define nTECSInfo_tTECSInfoSub_cRegionInfo__b_VMT_useless  (false)
#define nTECSInfo_tTECSInfoSub_cRegionInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cRegionInfo__b_cell_unique  (false)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfoTemp__offset  ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cNamespaceInfoTemp)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfoTemp__array_size (0)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfoTemp__place   (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cNamespaceInfoTemp__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cRegionInfoTemp__offset     ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cRegionInfoTemp)
#define nTECSInfo_tTECSInfoSub_cRegionInfoTemp__array_size (0)
#define nTECSInfo_tTECSInfoSub_cRegionInfoTemp__place      (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cRegionInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cRegionInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cRegionInfoTemp__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cSignatureInfoTemp__offset  ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cSignatureInfoTemp)
#define nTECSInfo_tTECSInfoSub_cSignatureInfoTemp__array_size (0)
#define nTECSInfo_tTECSInfoSub_cSignatureInfoTemp__place   (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cSignatureInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cSignatureInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cSignatureInfoTemp__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cCelltypeInfoTemp__offset   ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cCelltypeInfoTemp)
#define nTECSInfo_tTECSInfoSub_cCelltypeInfoTemp__array_size (0)
#define nTECSInfo_tTECSInfoSub_cCelltypeInfoTemp__place    (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cCelltypeInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cCelltypeInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cCelltypeInfoTemp__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cCellInfoTemp__offset       ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cCellInfoTemp)
#define nTECSInfo_tTECSInfoSub_cCellInfoTemp__array_size   (0)
#define nTECSInfo_tTECSInfoSub_cCellInfoTemp__place        (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cCellInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cCellInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cCellInfoTemp__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cEntryInfoTemp__offset      ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cEntryInfoTemp)
#define nTECSInfo_tTECSInfoSub_cEntryInfoTemp__array_size  (0)
#define nTECSInfo_tTECSInfoSub_cEntryInfoTemp__place       (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cEntryInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cEntryInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cEntryInfoTemp__b_cell_unique (false)
#define nTECSInfo_tTECSInfoSub_cRawEntryDescriptorInfoTemp__offset ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoSub_CB*)0)->cRawEntryDescriptorInfoTemp)
#define nTECSInfo_tTECSInfoSub_cRawEntryDescriptorInfoTemp__array_size (0)
#define nTECSInfo_tTECSInfoSub_cRawEntryDescriptorInfoTemp__place (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoSub_cRawEntryDescriptorInfoTemp__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoSub_cRawEntryDescriptorInfoTemp__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoSub_cRawEntryDescriptorInfoTemp__b_cell_unique (false)

#include "nTECSInfo_tNamespaceInfo_tecsgen.h"
#define nTECSInfo_tNamespaceInfo_cSignatureInfo__offset    ((uint32_t)(intptr_t)&((nTECSInfo_tNamespaceInfo_INIB*)0)->cSignatureInfo)
#define nTECSInfo_tNamespaceInfo_cSignatureInfo__array_size (0xffffffff)
#define nTECSInfo_tNamespaceInfo_cSignatureInfo__place     (CALL_PLACE_INIB_DES)
#define nTECSInfo_tNamespaceInfo_cSignatureInfo__b_VMT_useless (false)
#define nTECSInfo_tNamespaceInfo_cSignatureInfo__b_skelton_useless (false)
#define nTECSInfo_tNamespaceInfo_cSignatureInfo__b_cell_unique (false)
#define nTECSInfo_tNamespaceInfo_cCelltypeInfo__offset     ((uint32_t)(intptr_t)&((nTECSInfo_tNamespaceInfo_INIB*)0)->cCelltypeInfo)
#define nTECSInfo_tNamespaceInfo_cCelltypeInfo__array_size (0xffffffff)
#define nTECSInfo_tNamespaceInfo_cCelltypeInfo__place      (CALL_PLACE_INIB_DES)
#define nTECSInfo_tNamespaceInfo_cCelltypeInfo__b_VMT_useless (false)
#define nTECSInfo_tNamespaceInfo_cCelltypeInfo__b_skelton_useless (false)
#define nTECSInfo_tNamespaceInfo_cCelltypeInfo__b_cell_unique (false)
#define nTECSInfo_tNamespaceInfo_cNamespaceInfo__offset    ((uint32_t)(intptr_t)&((nTECSInfo_tNamespaceInfo_INIB*)0)->cNamespaceInfo)
#define nTECSInfo_tNamespaceInfo_cNamespaceInfo__array_size (0xffffffff)
#define nTECSInfo_tNamespaceInfo_cNamespaceInfo__place     (CALL_PLACE_INIB_DES)
#define nTECSInfo_tNamespaceInfo_cNamespaceInfo__b_VMT_useless (false)
#define nTECSInfo_tNamespaceInfo_cNamespaceInfo__b_skelton_useless (false)
#define nTECSInfo_tNamespaceInfo_cNamespaceInfo__b_cell_unique (false)

#include "nTECSInfo_tSignatureInfo_tecsgen.h"
#define nTECSInfo_tSignatureInfo_cFunctionInfo__offset     ((uint32_t)(intptr_t)&((nTECSInfo_tSignatureInfo_INIB*)0)->cFunctionInfo)
#define nTECSInfo_tSignatureInfo_cFunctionInfo__array_size (0xffffffff)
#define nTECSInfo_tSignatureInfo_cFunctionInfo__place      (CALL_PLACE_INIB_DES)
#define nTECSInfo_tSignatureInfo_cFunctionInfo__b_VMT_useless (false)
#define nTECSInfo_tSignatureInfo_cFunctionInfo__b_skelton_useless (false)
#define nTECSInfo_tSignatureInfo_cFunctionInfo__b_cell_unique (false)

#include "nTECSInfo_tFunctionInfo_tecsgen.h"
#define nTECSInfo_tFunctionInfo_cParamInfo__offset         ((uint32_t)(intptr_t)&((nTECSInfo_tFunctionInfo_INIB*)0)->cParamInfo)
#define nTECSInfo_tFunctionInfo_cParamInfo__array_size     (0xffffffff)
#define nTECSInfo_tFunctionInfo_cParamInfo__place          (CALL_PLACE_INIB_DES)
#define nTECSInfo_tFunctionInfo_cParamInfo__b_VMT_useless  (false)
#define nTECSInfo_tFunctionInfo_cParamInfo__b_skelton_useless (false)
#define nTECSInfo_tFunctionInfo_cParamInfo__b_cell_unique  (false)
#define nTECSInfo_tFunctionInfo_cReturnTypeInfo__offset    ((uint32_t)(intptr_t)&((nTECSInfo_tFunctionInfo_INIB*)0)->cReturnTypeInfo)
#define nTECSInfo_tFunctionInfo_cReturnTypeInfo__array_size (0)
#define nTECSInfo_tFunctionInfo_cReturnTypeInfo__place     (CALL_PLACE_INIB_DES)
#define nTECSInfo_tFunctionInfo_cReturnTypeInfo__b_VMT_useless (false)
#define nTECSInfo_tFunctionInfo_cReturnTypeInfo__b_skelton_useless (false)
#define nTECSInfo_tFunctionInfo_cReturnTypeInfo__b_cell_unique (false)

#include "nTECSInfo_tParamInfo_tecsgen.h"
#define nTECSInfo_tParamInfo_cTypeInfo__offset             ((uint32_t)(intptr_t)&((nTECSInfo_tParamInfo_INIB*)0)->cTypeInfo)
#define nTECSInfo_tParamInfo_cTypeInfo__array_size         (0)
#define nTECSInfo_tParamInfo_cTypeInfo__place              (CALL_PLACE_INIB_DES)
#define nTECSInfo_tParamInfo_cTypeInfo__b_VMT_useless      (false)
#define nTECSInfo_tParamInfo_cTypeInfo__b_skelton_useless  (false)
#define nTECSInfo_tParamInfo_cTypeInfo__b_cell_unique      (false)

#include "nTECSInfo_tCelltypeInfo_tecsgen.h"
#define nTECSInfo_tCelltypeInfo_cEntryInfo__offset         ((uint32_t)(intptr_t)&((nTECSInfo_tCelltypeInfo_INIB*)0)->cEntryInfo)
#define nTECSInfo_tCelltypeInfo_cEntryInfo__array_size     (0xffffffff)
#define nTECSInfo_tCelltypeInfo_cEntryInfo__place          (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCelltypeInfo_cEntryInfo__b_VMT_useless  (false)
#define nTECSInfo_tCelltypeInfo_cEntryInfo__b_skelton_useless (false)
#define nTECSInfo_tCelltypeInfo_cEntryInfo__b_cell_unique  (false)
#define nTECSInfo_tCelltypeInfo_cCallInfo__offset          ((uint32_t)(intptr_t)&((nTECSInfo_tCelltypeInfo_INIB*)0)->cCallInfo)
#define nTECSInfo_tCelltypeInfo_cCallInfo__array_size      (0xffffffff)
#define nTECSInfo_tCelltypeInfo_cCallInfo__place           (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCelltypeInfo_cCallInfo__b_VMT_useless   (false)
#define nTECSInfo_tCelltypeInfo_cCallInfo__b_skelton_useless (false)
#define nTECSInfo_tCelltypeInfo_cCallInfo__b_cell_unique   (false)
#define nTECSInfo_tCelltypeInfo_cAttrInfo__offset          ((uint32_t)(intptr_t)&((nTECSInfo_tCelltypeInfo_INIB*)0)->cAttrInfo)
#define nTECSInfo_tCelltypeInfo_cAttrInfo__array_size      (0xffffffff)
#define nTECSInfo_tCelltypeInfo_cAttrInfo__place           (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCelltypeInfo_cAttrInfo__b_VMT_useless   (false)
#define nTECSInfo_tCelltypeInfo_cAttrInfo__b_skelton_useless (false)
#define nTECSInfo_tCelltypeInfo_cAttrInfo__b_cell_unique   (false)
#define nTECSInfo_tCelltypeInfo_cVarInfo__offset           ((uint32_t)(intptr_t)&((nTECSInfo_tCelltypeInfo_INIB*)0)->cVarInfo)
#define nTECSInfo_tCelltypeInfo_cVarInfo__array_size       (0xffffffff)
#define nTECSInfo_tCelltypeInfo_cVarInfo__place            (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCelltypeInfo_cVarInfo__b_VMT_useless    (false)
#define nTECSInfo_tCelltypeInfo_cVarInfo__b_skelton_useless (false)
#define nTECSInfo_tCelltypeInfo_cVarInfo__b_cell_unique    (false)

#include "nTECSInfo_tCallInfo_tecsgen.h"
#define nTECSInfo_tCallInfo_cSignatureInfo__offset         ((uint32_t)(intptr_t)&((nTECSInfo_tCallInfo_INIB*)0)->cSignatureInfo)
#define nTECSInfo_tCallInfo_cSignatureInfo__array_size     (0)
#define nTECSInfo_tCallInfo_cSignatureInfo__place          (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCallInfo_cSignatureInfo__b_VMT_useless  (false)
#define nTECSInfo_tCallInfo_cSignatureInfo__b_skelton_useless (false)
#define nTECSInfo_tCallInfo_cSignatureInfo__b_cell_unique  (false)

#include "nTECSInfo_tEntryInfo_tecsgen.h"
#define nTECSInfo_tEntryInfo_cSignatureInfo__offset        ((uint32_t)(intptr_t)&((nTECSInfo_tEntryInfo_INIB*)0)->cSignatureInfo)
#define nTECSInfo_tEntryInfo_cSignatureInfo__array_size    (0)
#define nTECSInfo_tEntryInfo_cSignatureInfo__place         (CALL_PLACE_INIB_DES)
#define nTECSInfo_tEntryInfo_cSignatureInfo__b_VMT_useless (false)
#define nTECSInfo_tEntryInfo_cSignatureInfo__b_skelton_useless (false)
#define nTECSInfo_tEntryInfo_cSignatureInfo__b_cell_unique (false)

#include "nTECSInfo_tVarDeclInfo_tecsgen.h"
#define nTECSInfo_tVarDeclInfo_cTypeInfo__offset           ((uint32_t)(intptr_t)&((nTECSInfo_tVarDeclInfo_INIB*)0)->cTypeInfo)
#define nTECSInfo_tVarDeclInfo_cTypeInfo__array_size       (0)
#define nTECSInfo_tVarDeclInfo_cTypeInfo__place            (CALL_PLACE_INIB_DES)
#define nTECSInfo_tVarDeclInfo_cTypeInfo__b_VMT_useless    (false)
#define nTECSInfo_tVarDeclInfo_cTypeInfo__b_skelton_useless (false)
#define nTECSInfo_tVarDeclInfo_cTypeInfo__b_cell_unique    (false)

#include "nTECSInfo_tRegionInfo_tecsgen.h"
#define nTECSInfo_tRegionInfo_cCellInfo__offset            ((uint32_t)(intptr_t)&((nTECSInfo_tRegionInfo_INIB*)0)->cCellInfo)
#define nTECSInfo_tRegionInfo_cCellInfo__array_size        (0xffffffff)
#define nTECSInfo_tRegionInfo_cCellInfo__place             (CALL_PLACE_INIB_DES)
#define nTECSInfo_tRegionInfo_cCellInfo__b_VMT_useless     (false)
#define nTECSInfo_tRegionInfo_cCellInfo__b_skelton_useless (false)
#define nTECSInfo_tRegionInfo_cCellInfo__b_cell_unique     (false)
#define nTECSInfo_tRegionInfo_cRegionInfo__offset          ((uint32_t)(intptr_t)&((nTECSInfo_tRegionInfo_INIB*)0)->cRegionInfo)
#define nTECSInfo_tRegionInfo_cRegionInfo__array_size      (0xffffffff)
#define nTECSInfo_tRegionInfo_cRegionInfo__place           (CALL_PLACE_INIB_DES)
#define nTECSInfo_tRegionInfo_cRegionInfo__b_VMT_useless   (false)
#define nTECSInfo_tRegionInfo_cRegionInfo__b_skelton_useless (false)
#define nTECSInfo_tRegionInfo_cRegionInfo__b_cell_unique   (false)

#include "nTECSInfo_tCellInfo_tecsgen.h"
#define nTECSInfo_tCellInfo_cCelltypeInfo__offset          ((uint32_t)(intptr_t)&((nTECSInfo_tCellInfo_INIB*)0)->cCelltypeInfo)
#define nTECSInfo_tCellInfo_cCelltypeInfo__array_size      (0)
#define nTECSInfo_tCellInfo_cCelltypeInfo__place           (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCellInfo_cCelltypeInfo__b_VMT_useless   (false)
#define nTECSInfo_tCellInfo_cCelltypeInfo__b_skelton_useless (false)
#define nTECSInfo_tCellInfo_cCelltypeInfo__b_cell_unique   (false)
#define nTECSInfo_tCellInfo_cRawEntryDescriptor__offset    ((uint32_t)(intptr_t)&((nTECSInfo_tCellInfo_INIB*)0)->cRawEntryDescriptor)
#define nTECSInfo_tCellInfo_cRawEntryDescriptor__array_size (0xffffffff)
#define nTECSInfo_tCellInfo_cRawEntryDescriptor__place     (CALL_PLACE_INIB_DES)
#define nTECSInfo_tCellInfo_cRawEntryDescriptor__b_VMT_useless (false)
#define nTECSInfo_tCellInfo_cRawEntryDescriptor__b_skelton_useless (false)
#define nTECSInfo_tCellInfo_cRawEntryDescriptor__b_cell_unique (false)

#include "nTECSInfo_tRawEntryDescriptorInfo_tecsgen.h"

#include "nTECSInfo_tVoidTypeInfo_tecsgen.h"

#include "nTECSInfo_tBoolTypeInfo_tecsgen.h"

#include "nTECSInfo_tIntTypeInfo_tecsgen.h"

#include "nTECSInfo_tStructTypeInfo_tecsgen.h"
#define nTECSInfo_tStructTypeInfo_cVarDeclInfo__offset     ((uint32_t)(intptr_t)&((nTECSInfo_tStructTypeInfo_INIB*)0)->cVarDeclInfo)
#define nTECSInfo_tStructTypeInfo_cVarDeclInfo__array_size (0xffffffff)
#define nTECSInfo_tStructTypeInfo_cVarDeclInfo__place      (CALL_PLACE_INIB_DES)
#define nTECSInfo_tStructTypeInfo_cVarDeclInfo__b_VMT_useless (false)
#define nTECSInfo_tStructTypeInfo_cVarDeclInfo__b_skelton_useless (false)
#define nTECSInfo_tStructTypeInfo_cVarDeclInfo__b_cell_unique (false)

#include "nTECSInfo_tPtrTypeInfo_tecsgen.h"
#define nTECSInfo_tPtrTypeInfo_cTypeInfo__offset           ((uint32_t)(intptr_t)&((nTECSInfo_tPtrTypeInfo_INIB*)0)->cTypeInfo)
#define nTECSInfo_tPtrTypeInfo_cTypeInfo__array_size       (0)
#define nTECSInfo_tPtrTypeInfo_cTypeInfo__place            (CALL_PLACE_INIB_DES)
#define nTECSInfo_tPtrTypeInfo_cTypeInfo__b_VMT_useless    (false)
#define nTECSInfo_tPtrTypeInfo_cTypeInfo__b_skelton_useless (false)
#define nTECSInfo_tPtrTypeInfo_cTypeInfo__b_cell_unique    (false)

#include "nTECSInfo_tArrayTypeInfo_tecsgen.h"
#define nTECSInfo_tArrayTypeInfo_cTypeInfo__offset         ((uint32_t)(intptr_t)&((nTECSInfo_tArrayTypeInfo_INIB*)0)->cTypeInfo)
#define nTECSInfo_tArrayTypeInfo_cTypeInfo__array_size     (0)
#define nTECSInfo_tArrayTypeInfo_cTypeInfo__place          (CALL_PLACE_INIB_DES)
#define nTECSInfo_tArrayTypeInfo_cTypeInfo__b_VMT_useless  (false)
#define nTECSInfo_tArrayTypeInfo_cTypeInfo__b_skelton_useless (false)
#define nTECSInfo_tArrayTypeInfo_cTypeInfo__b_cell_unique  (false)

#include "nTECSInfo_tDefinedTypeInfo_tecsgen.h"
#define nTECSInfo_tDefinedTypeInfo_cTypeInfo__offset       ((uint32_t)(intptr_t)&((nTECSInfo_tDefinedTypeInfo_INIB*)0)->cTypeInfo)
#define nTECSInfo_tDefinedTypeInfo_cTypeInfo__array_size   (0)
#define nTECSInfo_tDefinedTypeInfo_cTypeInfo__place        (CALL_PLACE_INIB_DES)
#define nTECSInfo_tDefinedTypeInfo_cTypeInfo__b_VMT_useless (false)
#define nTECSInfo_tDefinedTypeInfo_cTypeInfo__b_skelton_useless (false)
#define nTECSInfo_tDefinedTypeInfo_cTypeInfo__b_cell_unique (false)

#include "nTECSInfo_tDescriptorTypeInfo_tecsgen.h"
#define nTECSInfo_tDescriptorTypeInfo_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nTECSInfo_tDescriptorTypeInfo_INIB*)0)->cSignatureInfo)
#define nTECSInfo_tDescriptorTypeInfo_cSignatureInfo__array_size (0)
#define nTECSInfo_tDescriptorTypeInfo_cSignatureInfo__place (CALL_PLACE_INIB_DES)
#define nTECSInfo_tDescriptorTypeInfo_cSignatureInfo__b_VMT_useless (false)
#define nTECSInfo_tDescriptorTypeInfo_cSignatureInfo__b_skelton_useless (false)
#define nTECSInfo_tDescriptorTypeInfo_cSignatureInfo__b_cell_unique (false)

#include "nTECSInfo_tTECSInfoAccessor_tecsgen.h"
#define nTECSInfo_tTECSInfoAccessor_cTECSInfo__offset      (0xffffffff)
#define nTECSInfo_tTECSInfoAccessor_cTECSInfo__array_size  (0)
#define nTECSInfo_tTECSInfoAccessor_cTECSInfo__place       (CALL_PLACE_NON)
#define nTECSInfo_tTECSInfoAccessor_cTECSInfo__b_VMT_useless (true)
#define nTECSInfo_tTECSInfoAccessor_cTECSInfo__b_skelton_useless (true)
#define nTECSInfo_tTECSInfoAccessor_cTECSInfo__b_cell_unique (true)
#define nTECSInfo_tTECSInfoAccessor_cNSInfo__offset        ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cNSInfo)
#define nTECSInfo_tTECSInfoAccessor_cNSInfo__array_size    (0)
#define nTECSInfo_tTECSInfoAccessor_cNSInfo__place         (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cNSInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cNSInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cNSInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cCelltypeInfo__offset  ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cCelltypeInfo)
#define nTECSInfo_tTECSInfoAccessor_cCelltypeInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cCelltypeInfo__place   (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cCelltypeInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cCelltypeInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cCelltypeInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cSignatureInfo)
#define nTECSInfo_tTECSInfoAccessor_cSignatureInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cSignatureInfo__place  (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cSignatureInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cSignatureInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cSignatureInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cFunctionInfo__offset  ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cFunctionInfo)
#define nTECSInfo_tTECSInfoAccessor_cFunctionInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cFunctionInfo__place   (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cFunctionInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cFunctionInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cFunctionInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cParamInfo__offset     ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cParamInfo)
#define nTECSInfo_tTECSInfoAccessor_cParamInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cParamInfo__place      (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cParamInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cParamInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cParamInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cCallInfo__offset      ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cCallInfo)
#define nTECSInfo_tTECSInfoAccessor_cCallInfo__array_size  (0)
#define nTECSInfo_tTECSInfoAccessor_cCallInfo__place       (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cCallInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cCallInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cCallInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cEntryInfo__offset     ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cEntryInfo)
#define nTECSInfo_tTECSInfoAccessor_cEntryInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cEntryInfo__place      (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cEntryInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cEntryInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cEntryInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cAttrInfo__offset      ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cAttrInfo)
#define nTECSInfo_tTECSInfoAccessor_cAttrInfo__array_size  (0)
#define nTECSInfo_tTECSInfoAccessor_cAttrInfo__place       (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cAttrInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cAttrInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cAttrInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cVarInfo__offset       ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cVarInfo)
#define nTECSInfo_tTECSInfoAccessor_cVarInfo__array_size   (0)
#define nTECSInfo_tTECSInfoAccessor_cVarInfo__place        (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cVarInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cVarInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cVarInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cVarDeclInfo__offset   ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cVarDeclInfo)
#define nTECSInfo_tTECSInfoAccessor_cVarDeclInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cVarDeclInfo__place    (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cVarDeclInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cVarDeclInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cVarDeclInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cTypeInfo__offset      ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cTypeInfo)
#define nTECSInfo_tTECSInfoAccessor_cTypeInfo__array_size  (0)
#define nTECSInfo_tTECSInfoAccessor_cTypeInfo__place       (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cTypeInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cTypeInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cTypeInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cRegionInfo__offset    ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cRegionInfo)
#define nTECSInfo_tTECSInfoAccessor_cRegionInfo__array_size (0)
#define nTECSInfo_tTECSInfoAccessor_cRegionInfo__place     (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cRegionInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cRegionInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cRegionInfo__b_cell_unique (false)
#define nTECSInfo_tTECSInfoAccessor_cCellInfo__offset      ((uint32_t)(intptr_t)&((nTECSInfo_tTECSInfoAccessor_CB*)0)->cCellInfo)
#define nTECSInfo_tTECSInfoAccessor_cCellInfo__array_size  (0)
#define nTECSInfo_tTECSInfoAccessor_cCellInfo__place       (CALL_PLACE_CB_DES)
#define nTECSInfo_tTECSInfoAccessor_cCellInfo__b_VMT_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cCellInfo__b_skelton_useless (false)
#define nTECSInfo_tTECSInfoAccessor_cCellInfo__b_cell_unique (false)

#include "nMruby_tTECSInitializer_tecsgen.h"
#define nMruby_tTECSInitializer_cInitialize__offset        ((uint32_t)(intptr_t)&((nMruby_tTECSInitializer_INIB*)0)->cInitialize)
#define nMruby_tTECSInitializer_cInitialize__array_size    (0xffffffff)
#define nMruby_tTECSInitializer_cInitialize__place         (CALL_PLACE_INIB_DES)
#define nMruby_tTECSInitializer_cInitialize__b_VMT_useless (false)
#define nMruby_tTECSInitializer_cInitialize__b_skelton_useless (false)
#define nMruby_tTECSInitializer_cInitialize__b_cell_unique (false)

#include "nMruby_tBoolPointer_tecsgen.h"

#include "nMruby_tCharPointer_tecsgen.h"

#include "nMruby_tInt8Pointer_tecsgen.h"

#include "nMruby_tUInt32Pointer_tecsgen.h"

#include "nMruby_tIntPointer_tecsgen.h"

#include "nMruby_tLongPointer_tecsgen.h"

#include "nMruby_tUIntPointer_tecsgen.h"

#include "nMruby_tULongPointer_tecsgen.h"

#include "nMruby_tMrubyProc_tecsgen.h"
#define nMruby_tMrubyProc_cInit__offset                    (0xffffffff)
#define nMruby_tMrubyProc_cInit__array_size                (0)
#define nMruby_tMrubyProc_cInit__place                     (CALL_PLACE_NON)
#define nMruby_tMrubyProc_cInit__b_VMT_useless             (true)
#define nMruby_tMrubyProc_cInit__b_skelton_useless         (true)
#define nMruby_tMrubyProc_cInit__b_cell_unique             (true)

#include "nMruby_tnTECSInfo_sAccessor_tecsgen.h"
#define nMruby_tnTECSInfo_sAccessor_cTECS__offset          (0xffffffff)
#define nMruby_tnTECSInfo_sAccessor_cTECS__array_size      (0)
#define nMruby_tnTECSInfo_sAccessor_cTECS__place           (CALL_PLACE_NON)
#define nMruby_tnTECSInfo_sAccessor_cTECS__b_VMT_useless   (true)
#define nMruby_tnTECSInfo_sAccessor_cTECS__b_skelton_useless (true)
#define nMruby_tnTECSInfo_sAccessor_cTECS__b_cell_unique   (true)

#include "nMruby_tnTECSInfo_sAccessor_Initializer_tecsgen.h"

#include "nMruby_t_syslog_rlog_tecsgen.h"

#include "nMruby_t_rsem_tecsgen.h"

#include "nMruby_t_rflg_tecsgen.h"

#include "nMruby_t_rdtq_tecsgen.h"

#include "nC2TECS_tnPosix_sMain_tecsgen.h"
#define nC2TECS_tnPosix_sMain_cCall__offset                (0xffffffff)
#define nC2TECS_tnPosix_sMain_cCall__array_size            (0)
#define nC2TECS_tnPosix_sMain_cCall__place                 (CALL_PLACE_NON)
#define nC2TECS_tnPosix_sMain_cCall__b_VMT_useless         (true)
#define nC2TECS_tnPosix_sMain_cCall__b_skelton_useless     (true)
#define nC2TECS_tnPosix_sMain_cCall__b_cell_unique         (true)

#include "nMrubyInfo_tInfosSysLog_tecsgen.h"
#define nMrubyInfo_tInfosSysLog_cTECS__offset              ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSysLog_CB*)0)->cTECS)
#define nMrubyInfo_tInfosSysLog_cTECS__array_size          (0)
#define nMrubyInfo_tInfosSysLog_cTECS__place               (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSysLog_cTECS__b_VMT_useless       (false)
#define nMrubyInfo_tInfosSysLog_cTECS__b_skelton_useless   (false)
#define nMrubyInfo_tInfosSysLog_cTECS__b_cell_unique       (false)
#define nMrubyInfo_tInfosSysLog_cTECSInfo__offset          (0xffffffff)
#define nMrubyInfo_tInfosSysLog_cTECSInfo__array_size      (0)
#define nMrubyInfo_tInfosSysLog_cTECSInfo__place           (CALL_PLACE_NON)
#define nMrubyInfo_tInfosSysLog_cTECSInfo__b_VMT_useless   (true)
#define nMrubyInfo_tInfosSysLog_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosSysLog_cTECSInfo__b_cell_unique   (true)
#define nMrubyInfo_tInfosSysLog_cEntryInfo__offset         ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSysLog_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosSysLog_cEntryInfo__array_size     (0)
#define nMrubyInfo_tInfosSysLog_cEntryInfo__place          (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSysLog_cEntryInfo__b_VMT_useless  (false)
#define nMrubyInfo_tInfosSysLog_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSysLog_cEntryInfo__b_cell_unique  (false)
#define nMrubyInfo_tInfosSysLog_cSignatureInfo__offset     ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSysLog_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosSysLog_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosSysLog_cSignatureInfo__place      (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSysLog_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSysLog_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSysLog_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosSysLog_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSysLog_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosSysLog_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosSysLog_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSysLog_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSysLog_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSysLog_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosSysLog_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosTaskBody_tecsgen.h"
#define nMrubyInfo_tInfosTaskBody_cTECS__offset            ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskBody_CB*)0)->cTECS)
#define nMrubyInfo_tInfosTaskBody_cTECS__array_size        (0)
#define nMrubyInfo_tInfosTaskBody_cTECS__place             (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskBody_cTECS__b_VMT_useless     (false)
#define nMrubyInfo_tInfosTaskBody_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskBody_cTECS__b_cell_unique     (false)
#define nMrubyInfo_tInfosTaskBody_cTECSInfo__offset        (0xffffffff)
#define nMrubyInfo_tInfosTaskBody_cTECSInfo__array_size    (0)
#define nMrubyInfo_tInfosTaskBody_cTECSInfo__place         (CALL_PLACE_NON)
#define nMrubyInfo_tInfosTaskBody_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosTaskBody_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosTaskBody_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosTaskBody_cEntryInfo__offset       ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskBody_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosTaskBody_cEntryInfo__array_size   (0)
#define nMrubyInfo_tInfosTaskBody_cEntryInfo__place        (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskBody_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskBody_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskBody_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosTaskBody_cSignatureInfo__offset   ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskBody_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosTaskBody_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosTaskBody_cSignatureInfo__place    (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskBody_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskBody_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskBody_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosTaskBody_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskBody_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosTaskBody_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosTaskBody_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskBody_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskBody_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskBody_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosTaskBody_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosTaskExceptionBody_tecsgen.h"
#define nMrubyInfo_tInfosTaskExceptionBody_cTECS__offset   ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskExceptionBody_CB*)0)->cTECS)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECS__array_size (0)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECS__place    (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECS__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECS__b_cell_unique (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECSInfo__offset (0xffffffff)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECSInfo__array_size (0)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECSInfo__place (CALL_PLACE_NON)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosTaskExceptionBody_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosTaskExceptionBody_cEntryInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskExceptionBody_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosTaskExceptionBody_cEntryInfo__array_size (0)
#define nMrubyInfo_tInfosTaskExceptionBody_cEntryInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskExceptionBody_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskExceptionBody_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosTaskExceptionBody_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosTaskExceptionBody_cSignatureInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskExceptionBody_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTaskExceptionBody_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosTaskExceptionBody_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosTaskExceptionBody_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTaskExceptionBody_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTaskExceptionBody_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosTaskExceptionBody_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosTask_tecsgen.h"
#define nMrubyInfo_tInfosTask_cTECS__offset                ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTask_CB*)0)->cTECS)
#define nMrubyInfo_tInfosTask_cTECS__array_size            (0)
#define nMrubyInfo_tInfosTask_cTECS__place                 (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTask_cTECS__b_VMT_useless         (false)
#define nMrubyInfo_tInfosTask_cTECS__b_skelton_useless     (false)
#define nMrubyInfo_tInfosTask_cTECS__b_cell_unique         (false)
#define nMrubyInfo_tInfosTask_cTECSInfo__offset            (0xffffffff)
#define nMrubyInfo_tInfosTask_cTECSInfo__array_size        (0)
#define nMrubyInfo_tInfosTask_cTECSInfo__place             (CALL_PLACE_NON)
#define nMrubyInfo_tInfosTask_cTECSInfo__b_VMT_useless     (true)
#define nMrubyInfo_tInfosTask_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosTask_cTECSInfo__b_cell_unique     (true)
#define nMrubyInfo_tInfosTask_cEntryInfo__offset           ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTask_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosTask_cEntryInfo__array_size       (0)
#define nMrubyInfo_tInfosTask_cEntryInfo__place            (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTask_cEntryInfo__b_VMT_useless    (false)
#define nMrubyInfo_tInfosTask_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTask_cEntryInfo__b_cell_unique    (false)
#define nMrubyInfo_tInfosTask_cSignatureInfo__offset       ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTask_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosTask_cSignatureInfo__array_size   (0)
#define nMrubyInfo_tInfosTask_cSignatureInfo__place        (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTask_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTask_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTask_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosTask_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosTask_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosTask_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosTask_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosTask_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosTask_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosTask_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosTask_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosKernel_tecsgen.h"
#define nMrubyInfo_tInfosKernel_cTECS__offset              ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosKernel_CB*)0)->cTECS)
#define nMrubyInfo_tInfosKernel_cTECS__array_size          (0)
#define nMrubyInfo_tInfosKernel_cTECS__place               (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosKernel_cTECS__b_VMT_useless       (false)
#define nMrubyInfo_tInfosKernel_cTECS__b_skelton_useless   (false)
#define nMrubyInfo_tInfosKernel_cTECS__b_cell_unique       (false)
#define nMrubyInfo_tInfosKernel_cTECSInfo__offset          (0xffffffff)
#define nMrubyInfo_tInfosKernel_cTECSInfo__array_size      (0)
#define nMrubyInfo_tInfosKernel_cTECSInfo__place           (CALL_PLACE_NON)
#define nMrubyInfo_tInfosKernel_cTECSInfo__b_VMT_useless   (true)
#define nMrubyInfo_tInfosKernel_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosKernel_cTECSInfo__b_cell_unique   (true)
#define nMrubyInfo_tInfosKernel_cEntryInfo__offset         ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosKernel_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosKernel_cEntryInfo__array_size     (0)
#define nMrubyInfo_tInfosKernel_cEntryInfo__place          (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosKernel_cEntryInfo__b_VMT_useless  (false)
#define nMrubyInfo_tInfosKernel_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosKernel_cEntryInfo__b_cell_unique  (false)
#define nMrubyInfo_tInfosKernel_cSignatureInfo__offset     ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosKernel_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosKernel_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosKernel_cSignatureInfo__place      (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosKernel_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosKernel_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosKernel_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosKernel_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosKernel_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosKernel_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosKernel_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosKernel_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosKernel_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosKernel_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosKernel_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosiKernel_tecsgen.h"
#define nMrubyInfo_tInfosiKernel_cTECS__offset             ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiKernel_CB*)0)->cTECS)
#define nMrubyInfo_tInfosiKernel_cTECS__array_size         (0)
#define nMrubyInfo_tInfosiKernel_cTECS__place              (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiKernel_cTECS__b_VMT_useless      (false)
#define nMrubyInfo_tInfosiKernel_cTECS__b_skelton_useless  (false)
#define nMrubyInfo_tInfosiKernel_cTECS__b_cell_unique      (false)
#define nMrubyInfo_tInfosiKernel_cTECSInfo__offset         (0xffffffff)
#define nMrubyInfo_tInfosiKernel_cTECSInfo__array_size     (0)
#define nMrubyInfo_tInfosiKernel_cTECSInfo__place          (CALL_PLACE_NON)
#define nMrubyInfo_tInfosiKernel_cTECSInfo__b_VMT_useless  (true)
#define nMrubyInfo_tInfosiKernel_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosiKernel_cTECSInfo__b_cell_unique  (true)
#define nMrubyInfo_tInfosiKernel_cEntryInfo__offset        ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiKernel_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosiKernel_cEntryInfo__array_size    (0)
#define nMrubyInfo_tInfosiKernel_cEntryInfo__place         (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiKernel_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiKernel_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiKernel_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiKernel_cSignatureInfo__offset    ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiKernel_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosiKernel_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosiKernel_cSignatureInfo__place     (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiKernel_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiKernel_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiKernel_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiKernel_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiKernel_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosiKernel_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosiKernel_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiKernel_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiKernel_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiKernel_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosiKernel_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosSemaphore_tecsgen.h"
#define nMrubyInfo_tInfosSemaphore_cTECS__offset           ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSemaphore_CB*)0)->cTECS)
#define nMrubyInfo_tInfosSemaphore_cTECS__array_size       (0)
#define nMrubyInfo_tInfosSemaphore_cTECS__place            (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSemaphore_cTECS__b_VMT_useless    (false)
#define nMrubyInfo_tInfosSemaphore_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosSemaphore_cTECS__b_cell_unique    (false)
#define nMrubyInfo_tInfosSemaphore_cTECSInfo__offset       (0xffffffff)
#define nMrubyInfo_tInfosSemaphore_cTECSInfo__array_size   (0)
#define nMrubyInfo_tInfosSemaphore_cTECSInfo__place        (CALL_PLACE_NON)
#define nMrubyInfo_tInfosSemaphore_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosSemaphore_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosSemaphore_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosSemaphore_cEntryInfo__offset      ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSemaphore_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosSemaphore_cEntryInfo__array_size  (0)
#define nMrubyInfo_tInfosSemaphore_cEntryInfo__place       (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSemaphore_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSemaphore_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSemaphore_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosSemaphore_cSignatureInfo__offset  ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSemaphore_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosSemaphore_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosSemaphore_cSignatureInfo__place   (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSemaphore_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSemaphore_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSemaphore_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosSemaphore_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSemaphore_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosSemaphore_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosSemaphore_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSemaphore_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSemaphore_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSemaphore_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosSemaphore_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosiSemaphore_tecsgen.h"
#define nMrubyInfo_tInfosiSemaphore_cTECS__offset          ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiSemaphore_CB*)0)->cTECS)
#define nMrubyInfo_tInfosiSemaphore_cTECS__array_size      (0)
#define nMrubyInfo_tInfosiSemaphore_cTECS__place           (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiSemaphore_cTECS__b_VMT_useless   (false)
#define nMrubyInfo_tInfosiSemaphore_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cTECS__b_cell_unique   (false)
#define nMrubyInfo_tInfosiSemaphore_cTECSInfo__offset      (0xffffffff)
#define nMrubyInfo_tInfosiSemaphore_cTECSInfo__array_size  (0)
#define nMrubyInfo_tInfosiSemaphore_cTECSInfo__place       (CALL_PLACE_NON)
#define nMrubyInfo_tInfosiSemaphore_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosiSemaphore_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosiSemaphore_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosiSemaphore_cEntryInfo__offset     ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiSemaphore_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosiSemaphore_cEntryInfo__array_size (0)
#define nMrubyInfo_tInfosiSemaphore_cEntryInfo__place      (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiSemaphore_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiSemaphore_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiSemaphore_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosiSemaphore_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosiSemaphore_cSignatureInfo__place  (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiSemaphore_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiSemaphore_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiSemaphore_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosiSemaphore_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosiSemaphore_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiSemaphore_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiSemaphore_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosiSemaphore_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosEventflag_tecsgen.h"
#define nMrubyInfo_tInfosEventflag_cTECS__offset           ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosEventflag_CB*)0)->cTECS)
#define nMrubyInfo_tInfosEventflag_cTECS__array_size       (0)
#define nMrubyInfo_tInfosEventflag_cTECS__place            (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosEventflag_cTECS__b_VMT_useless    (false)
#define nMrubyInfo_tInfosEventflag_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosEventflag_cTECS__b_cell_unique    (false)
#define nMrubyInfo_tInfosEventflag_cTECSInfo__offset       (0xffffffff)
#define nMrubyInfo_tInfosEventflag_cTECSInfo__array_size   (0)
#define nMrubyInfo_tInfosEventflag_cTECSInfo__place        (CALL_PLACE_NON)
#define nMrubyInfo_tInfosEventflag_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosEventflag_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosEventflag_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosEventflag_cEntryInfo__offset      ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosEventflag_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosEventflag_cEntryInfo__array_size  (0)
#define nMrubyInfo_tInfosEventflag_cEntryInfo__place       (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosEventflag_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosEventflag_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosEventflag_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosEventflag_cSignatureInfo__offset  ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosEventflag_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosEventflag_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosEventflag_cSignatureInfo__place   (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosEventflag_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosEventflag_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosEventflag_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosEventflag_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosEventflag_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosEventflag_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosEventflag_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosEventflag_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosEventflag_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosEventflag_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosEventflag_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosiEventflag_tecsgen.h"
#define nMrubyInfo_tInfosiEventflag_cTECS__offset          ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiEventflag_CB*)0)->cTECS)
#define nMrubyInfo_tInfosiEventflag_cTECS__array_size      (0)
#define nMrubyInfo_tInfosiEventflag_cTECS__place           (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiEventflag_cTECS__b_VMT_useless   (false)
#define nMrubyInfo_tInfosiEventflag_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosiEventflag_cTECS__b_cell_unique   (false)
#define nMrubyInfo_tInfosiEventflag_cTECSInfo__offset      (0xffffffff)
#define nMrubyInfo_tInfosiEventflag_cTECSInfo__array_size  (0)
#define nMrubyInfo_tInfosiEventflag_cTECSInfo__place       (CALL_PLACE_NON)
#define nMrubyInfo_tInfosiEventflag_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosiEventflag_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosiEventflag_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosiEventflag_cEntryInfo__offset     ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiEventflag_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosiEventflag_cEntryInfo__array_size (0)
#define nMrubyInfo_tInfosiEventflag_cEntryInfo__place      (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiEventflag_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiEventflag_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiEventflag_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiEventflag_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiEventflag_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosiEventflag_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosiEventflag_cSignatureInfo__place  (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiEventflag_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiEventflag_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiEventflag_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiEventflag_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiEventflag_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosiEventflag_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosiEventflag_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiEventflag_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiEventflag_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiEventflag_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosiEventflag_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosDataqueue_tecsgen.h"
#define nMrubyInfo_tInfosDataqueue_cTECS__offset           ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosDataqueue_CB*)0)->cTECS)
#define nMrubyInfo_tInfosDataqueue_cTECS__array_size       (0)
#define nMrubyInfo_tInfosDataqueue_cTECS__place            (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosDataqueue_cTECS__b_VMT_useless    (false)
#define nMrubyInfo_tInfosDataqueue_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosDataqueue_cTECS__b_cell_unique    (false)
#define nMrubyInfo_tInfosDataqueue_cTECSInfo__offset       (0xffffffff)
#define nMrubyInfo_tInfosDataqueue_cTECSInfo__array_size   (0)
#define nMrubyInfo_tInfosDataqueue_cTECSInfo__place        (CALL_PLACE_NON)
#define nMrubyInfo_tInfosDataqueue_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosDataqueue_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosDataqueue_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosDataqueue_cEntryInfo__offset      ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosDataqueue_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosDataqueue_cEntryInfo__array_size  (0)
#define nMrubyInfo_tInfosDataqueue_cEntryInfo__place       (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosDataqueue_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosDataqueue_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosDataqueue_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosDataqueue_cSignatureInfo__offset  ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosDataqueue_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosDataqueue_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosDataqueue_cSignatureInfo__place   (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosDataqueue_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosDataqueue_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosDataqueue_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosDataqueue_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosDataqueue_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosDataqueue_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosDataqueue_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosDataqueue_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosDataqueue_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosDataqueue_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosDataqueue_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosiDataqueue_tecsgen.h"
#define nMrubyInfo_tInfosiDataqueue_cTECS__offset          ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiDataqueue_CB*)0)->cTECS)
#define nMrubyInfo_tInfosiDataqueue_cTECS__array_size      (0)
#define nMrubyInfo_tInfosiDataqueue_cTECS__place           (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiDataqueue_cTECS__b_VMT_useless   (false)
#define nMrubyInfo_tInfosiDataqueue_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cTECS__b_cell_unique   (false)
#define nMrubyInfo_tInfosiDataqueue_cTECSInfo__offset      (0xffffffff)
#define nMrubyInfo_tInfosiDataqueue_cTECSInfo__array_size  (0)
#define nMrubyInfo_tInfosiDataqueue_cTECSInfo__place       (CALL_PLACE_NON)
#define nMrubyInfo_tInfosiDataqueue_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfosiDataqueue_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosiDataqueue_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfosiDataqueue_cEntryInfo__offset     ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiDataqueue_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosiDataqueue_cEntryInfo__array_size (0)
#define nMrubyInfo_tInfosiDataqueue_cEntryInfo__place      (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiDataqueue_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiDataqueue_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiDataqueue_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosiDataqueue_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosiDataqueue_cSignatureInfo__place  (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiDataqueue_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosiDataqueue_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosiDataqueue_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosiDataqueue_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosiDataqueue_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosiDataqueue_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosiDataqueue_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosiDataqueue_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfosSample_tecsgen.h"
#define nMrubyInfo_tInfosSample_cTECS__offset              ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSample_CB*)0)->cTECS)
#define nMrubyInfo_tInfosSample_cTECS__array_size          (0)
#define nMrubyInfo_tInfosSample_cTECS__place               (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSample_cTECS__b_VMT_useless       (false)
#define nMrubyInfo_tInfosSample_cTECS__b_skelton_useless   (false)
#define nMrubyInfo_tInfosSample_cTECS__b_cell_unique       (false)
#define nMrubyInfo_tInfosSample_cTECSInfo__offset          (0xffffffff)
#define nMrubyInfo_tInfosSample_cTECSInfo__array_size      (0)
#define nMrubyInfo_tInfosSample_cTECSInfo__place           (CALL_PLACE_NON)
#define nMrubyInfo_tInfosSample_cTECSInfo__b_VMT_useless   (true)
#define nMrubyInfo_tInfosSample_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfosSample_cTECSInfo__b_cell_unique   (true)
#define nMrubyInfo_tInfosSample_cEntryInfo__offset         ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSample_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfosSample_cEntryInfo__array_size     (0)
#define nMrubyInfo_tInfosSample_cEntryInfo__place          (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSample_cEntryInfo__b_VMT_useless  (false)
#define nMrubyInfo_tInfosSample_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSample_cEntryInfo__b_cell_unique  (false)
#define nMrubyInfo_tInfosSample_cSignatureInfo__offset     ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSample_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfosSample_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfosSample_cSignatureInfo__place      (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSample_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSample_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSample_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfosSample_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfosSample_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfosSample_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfosSample_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfosSample_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfosSample_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfosSample_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfosSample_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfonTECSInfo_sAccessor_tecsgen.h"
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECS__offset  ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonTECSInfo_sAccessor_CB*)0)->cTECS)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECS__array_size (0)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECS__place   (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECS__b_VMT_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECS__b_cell_unique (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECSInfo__offset (0xffffffff)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECSInfo__array_size (0)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECSInfo__place (CALL_PLACE_NON)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cEntryInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonTECSInfo_sAccessor_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cEntryInfo__array_size (0)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cEntryInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonTECSInfo_sAccessor_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cSignatureInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonTECSInfo_sAccessor_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfonTECSInfo_sAccessor_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfonTECSInfo_sAccessor_Initializer_tecsgen.h"

#include "nMrubyInfo_tInfonPosix_sMain_tecsgen.h"
#define nMrubyInfo_tInfonPosix_sMain_cTECS__offset         ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonPosix_sMain_CB*)0)->cTECS)
#define nMrubyInfo_tInfonPosix_sMain_cTECS__array_size     (0)
#define nMrubyInfo_tInfonPosix_sMain_cTECS__place          (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonPosix_sMain_cTECS__b_VMT_useless  (false)
#define nMrubyInfo_tInfonPosix_sMain_cTECS__b_skelton_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cTECS__b_cell_unique  (false)
#define nMrubyInfo_tInfonPosix_sMain_cTECSInfo__offset     (0xffffffff)
#define nMrubyInfo_tInfonPosix_sMain_cTECSInfo__array_size (0)
#define nMrubyInfo_tInfonPosix_sMain_cTECSInfo__place      (CALL_PLACE_NON)
#define nMrubyInfo_tInfonPosix_sMain_cTECSInfo__b_VMT_useless (true)
#define nMrubyInfo_tInfonPosix_sMain_cTECSInfo__b_skelton_useless (true)
#define nMrubyInfo_tInfonPosix_sMain_cTECSInfo__b_cell_unique (true)
#define nMrubyInfo_tInfonPosix_sMain_cEntryInfo__offset    ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonPosix_sMain_CB*)0)->cEntryInfo)
#define nMrubyInfo_tInfonPosix_sMain_cEntryInfo__array_size (0)
#define nMrubyInfo_tInfonPosix_sMain_cEntryInfo__place     (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonPosix_sMain_cEntryInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cEntryInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cEntryInfo__b_cell_unique (false)
#define nMrubyInfo_tInfonPosix_sMain_cSignatureInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonPosix_sMain_CB*)0)->cSignatureInfo)
#define nMrubyInfo_tInfonPosix_sMain_cSignatureInfo__array_size (0)
#define nMrubyInfo_tInfonPosix_sMain_cSignatureInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonPosix_sMain_cSignatureInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cSignatureInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cSignatureInfo__b_cell_unique (false)
#define nMrubyInfo_tInfonPosix_sMain_cRawEntryDescriptorInfo__offset ((uint32_t)(intptr_t)&((nMrubyInfo_tInfonPosix_sMain_CB*)0)->cRawEntryDescriptorInfo)
#define nMrubyInfo_tInfonPosix_sMain_cRawEntryDescriptorInfo__array_size (0)
#define nMrubyInfo_tInfonPosix_sMain_cRawEntryDescriptorInfo__place (CALL_PLACE_CB_DES)
#define nMrubyInfo_tInfonPosix_sMain_cRawEntryDescriptorInfo__b_VMT_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cRawEntryDescriptorInfo__b_skelton_useless (false)
#define nMrubyInfo_tInfonPosix_sMain_cRawEntryDescriptorInfo__b_cell_unique (false)

#include "nMrubyInfo_tInfonPosix_sMain_Initializer_tecsgen.h"

/* redefine macros */
#define tCallInfo_IDX  nTECSInfo_tCallInfo_IDX

#endif /* tCallInfo_FACTORY_H */
