"""MrubyBridgeSignaturePlugin.rb の移植。mruby から TECS の受け口関数を呼ぶためのブリッジを生成する。

生成するもの:
  gen_cdl_file   … ブリッジ初期化セルタイプ・ブリッジセルタイプ（シグニチャごと）・構造体セルタイプ
  new_cell       … TECS 初期化セル（プロトタイプ宣言）
  gen_post_code  … 構造体初期化セル・ポインタ初期化セル・TECS 初期化セル
  ep_func        … signature・ポインタ・構造体の初期化受け口（mruby VM への登録）
  preamble       … ポインタ・構造体のアクセス用コード、ブリッジ関数のプロトタイプ宣言と定義
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.lib.MrubyBridgeSignaturePluginModule import (
    MrubyBridgeSignaturePluginModule,
)
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    rb_downcase,
    rb_print,
    sym,
    to_s,
    truthy,
)

M = MrubyBridgeSignaturePluginModule


class MrubyBridgeSignaturePlugin(MrubyBridgeSignaturePluginModule, SignaturePlugin):
    _b_no_banner: ClassVar[bool] = False
    # Ruby 版はこのファイルが require された時点で Makefile に追加する（プロセスごとに1回）
    _b_loaded: ClassVar[bool] = False

    @classmethod
    def reset(cls) -> None:
        """Ruby のクラス変数に当たる状態を初期化する（1プロセスで何度も実行するテスト用）。"""
        MrubyBridgeSignaturePlugin._b_no_banner = False
        MrubyBridgeSignaturePlugin._b_loaded = False
        MrubyBridgeSignaturePluginModule.reset_module()

    @classmethod
    def on_load(cls) -> None:
        """ロードされた時点で実行される処理（Makefile への追加）。実行ごとに1回だけ行う。"""
        from tecsgen.core.tecsgen import Makefile

        if MrubyBridgeSignaturePlugin._b_loaded:
            return
        MrubyBridgeSignaturePlugin._b_loaded = True
        # -I に $(TECSPATH)/mruby を追加
        Makefile.add_ldflag("-lmruby -L$(MRUBYPATH)/lib -lm")
        Makefile.add_search_path("$(MRUBYPATH)/include")
        Makefile.add_var("MRUBYPATH", "..", "CHANGE this to suitable path")

    def __init__(self, signature: Any, option: Any) -> None:
        """プラグインインスタンスの初期化。戻り値、引数の型が使用可能なものかチェックする。"""
        MrubyBridgeSignaturePlugin.on_load()
        super().__init__(signature, option)

        if not MrubyBridgeSignaturePlugin._b_no_banner:
            from tecsgen.cli import _stderr

            _stderr(
                "MrubyBridgePlugin: version 2.0.0 (Suitable for mruby above ver 1.2.0).\n"
            )
            MrubyBridgeSignaturePlugin._b_no_banner = True

        self._b_ignoreUnsigned = False
        self._includes: list[Any] = []
        self._excludes: list[Any] = []
        self._struct_list: dict[Any, Any] = {}
        self._ptr_list: dict[Any, Any] = {}
        self._auto_exclude_list: dict[Any, Any] = {}
        self._b_auto_exclude = True  # auto_exclude = true by default

        self._plugin_arg_check_proc_tab = M.MRUBY_BRIDGE_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

        gname = to_s(self._signature.get_global_name())
        self._celltype_name = sym(f"t{gname}")
        self._init_celltype_name = sym(f"{to_s(self._celltype_name)}_Initializer")
        self._class_name = sym(f"T{gname}")

        self._func_head_array: list[Any] = []
        fh_array: list[Any] = []
        if len(self._includes) > 0 and len(self._excludes) > 0:
            self.cdl_error("MRB1011 both include && exclude are specified")

        if signature.get_function_head_array() is None:
            return  # 以前に文法エラー発生

        for func_head in signature.get_function_head_array():
            if len(self._includes) > 0:
                if func_head.get_name() in self._includes:
                    fh_array.append(func_head)
            elif len(self._excludes) > 0:
                if func_head.get_name() not in self._excludes:
                    fh_array.append(func_head)
            else:
                fh_array.append(func_head)

        self.check_name_and_return_type(fh_array)
        self.check_parameter_type(fh_array)

        for fh in fh_array:
            if self._auto_exclude_list.get(fh.get_name()) is None:
                self._func_head_array.append(fh)

        if len(self._func_head_array) == 0:
            self.cdl_error(
                "MRB1012 '$1' no function remained by exclude",
                self._signature.get_name(),
            )

    def check_name_and_return_type(self, func_head_array: list[Any]) -> None:
        """関数名と戻り値の型をチェックする。"""
        from tecsgen.core.cdl_types import BoolType, FloatType, IntType, VoidType

        b_init = False
        b_init_cell = False
        for func_head in func_head_array:
            if func_head.get_name() == sym("initialize"):
                self.cdl_warning(
                    "MRW2001 initialize: internally defined. change to initialize_cell in ruby"
                )
                b_init = True
            elif func_head.get_name() == sym("initialize_cell"):
                b_init_cell = True
            rtype = func_head.get_return_type().get_original_type()
            if not isinstance(rtype, (BoolType, IntType, FloatType, VoidType)):
                if self._b_auto_exclude:
                    self.cdl_info(
                        "MRI0001 cannot return type $1, $2 automatcally excluded",
                        rtype.get_type_str(),
                        func_head.get_name(),
                    )
                    self._auto_exclude_list[func_head.get_name()] = func_head
                else:
                    self.cdl_error(
                        "MRB1001 cannot return type $1", rtype.get_type_str()
                    )
        if b_init and b_init_cell:
            self.cdl_warning(
                "MRB1002 initialize: internally defined. change to initialize_cell in ruby"
            )

    def check_parameter_type(self, func_head_array: list[Any]) -> None:
        """パラメータの型をチェックする。"""
        from tecsgen.core.cdl_types import (
            BoolType,
            FloatType,
            IntType,
            PtrType,
            StructType,
        )

        for fh in func_head_array:
            for param_decl in fh.get_paramlist().get_items():
                direction = param_decl.get_direction()
                if direction in (Y.SEND, Y.RECEIVE):
                    if self._b_auto_exclude:
                        self.cdl_info(
                            "MRI0002 $1: $2 parameter cannot be used in mruby Bridge, $3 automatcally excluded",
                            param_decl.get_name(),
                            rb_downcase(to_s(direction)),
                            fh.get_name(),
                        )
                        self._auto_exclude_list[fh.get_name()] = fh
                    else:
                        self.cdl_error(
                            "MRB1003 $1: $2 parameter cannot be used in mruby Bridge",
                            param_decl.get_name(),
                            rb_downcase(to_s(direction)),
                        )
                type_ = param_decl.get_type()
                type_org = type_.get_original_type()
                type_str = to_s(type_.get_type_str()) + to_s(type_.get_type_str_post())

                b_ng = False
                if isinstance(type_org, IntType):
                    if type_org.get_bit_size() not in (
                        8,
                        16,
                        32,
                        64,
                        -1,
                        -2,
                        -3,
                        -4,
                        -11,
                    ):
                        b_ng = True
                elif isinstance(type_org, (BoolType, FloatType)):
                    pass
                elif isinstance(type_org, PtrType):
                    ttype_org = type_org.get_type()  # ポインタの指している先の型
                    ttype = (
                        ttype_org.get_original_type()
                    )  # 上記が typedef されている場合、元の型
                    self.register_ptr_type(ttype_org, fh)

                    if to_s(type_org.get_string()) == "-1" and direction in (
                        Y.OUT,
                        Y.INOUT,
                    ):
                        if self._b_auto_exclude:
                            self.cdl_info(
                                "MRB9999 string specifier without length cannot be used for out & inout parameter, $1 automatcally excluded",
                                fh.get_name(),
                            )
                            self._auto_exclude_list[fh.get_name()] = fh
                        else:
                            self.cdl_error(
                                "MRB9999 string specifier without length cannot be used for out & inout parameter"
                            )

                    if isinstance(ttype, (IntType, FloatType, BoolType)):
                        pass
                    elif isinstance(ttype, StructType):
                        if (
                            truthy(type_org.get_size())
                            or truthy(type_org.get_string())
                            or truthy(type_org.get_count())
                        ):
                            if self._b_auto_exclude:
                                self.cdl_info(
                                    "MRI9999 $1: size_is, count_is, string cannot be specified for struct pointer, $2 automatcally excluded",
                                    param_decl.get_name(),
                                    fh.get_name(),
                                )
                                self._auto_exclude_list[fh.get_name()] = fh
                            else:
                                self.cdl_error(
                                    "MRB1004 $1: size_is, count_is, string cannot be specified for struct pointer",
                                    param_decl.get_name(),
                                )
                        self.check_struct_member(ttype_org, fh)
                    else:
                        b_ng = True
                elif isinstance(type_org, StructType):
                    self.check_struct_member(type_org, fh)
                else:  # ArrayType, FuncType, EnumType, VoidType
                    b_ng = True
                if b_ng:
                    if self._b_auto_exclude:
                        self.cdl_info(
                            "MRI9999 $1: type $2 cannot be used in mruby Bridge, $3 automatcally excluded",
                            param_decl.get_name(),
                            type_str,
                            fh.get_name(),
                        )
                        self._auto_exclude_list[fh.get_name()] = fh
                    else:
                        self.cdl_error(
                            "MRB1005 $1: type $2 cannot be used in mruby Bridge",
                            param_decl.get_name(),
                            type_str,
                        )

    def check_struct_member(self, struct_type: Any, fh: Any) -> None:
        """構造体のメンバーの型のチェック。"""
        from tecsgen.core.cdl_types import BoolType, FloatType, IntType

        sttype = struct_type.get_original_type()
        if sttype.get_name() is None:
            if self._b_auto_exclude:
                self.cdl_info(
                    "MRI9999 tagless-struct cannot be handled, $1 automatcally excluded",
                    fh.get_name(),
                )
                self._auto_exclude_list[fh.get_name()] = fh
                return  # 登録しないように打ち切る
            self.cdl_error("MRB10007 tagless-struct cannot be handled")
        for d in sttype.get_members_decl().get_items():
            t = d.get_type().get_original_type()
            if not isinstance(t, (IntType, FloatType, BoolType)):
                t_str = to_s(d.get_type().get_type_str()) + to_s(
                    d.get_type().get_type_str_post()
                )
                if self._b_auto_exclude:
                    self.cdl_info(
                        "MRI9999 $1: type '$2' not allowed for struct member, '$3' automatcally excluded",
                        d.get_name(),
                        t_str,
                        fh.get_name(),
                    )
                    self._auto_exclude_list[fh.get_name()] = fh
                    return  # 登録しないように打ち切る
                self.cdl_error(
                    "MRB1006 $1: type '$2' not allowed for struct member",
                    d.get_name(),
                    t_str,
                )
        if self._struct_list.get(sttype.get_name()) is None:
            rb_print(
                f"  MrubyBridgePlugin: [struct]   {to_s(struct_type.get_type_str())} => "
                f"[class] TECS::Struct{to_s(sttype.get_name())}\n"
            )
            self._struct_list[sttype.get_name()] = sttype

    def register_ptr_type(self, ttype: Any, fh: Any) -> None:
        t_org = ttype.get_original_type()
        tment = self.get_type_map_ent(t_org)
        if tment is None:
            return
        ptr_celltype_name = sym(f"t{tment[1]}Pointer")
        if M._ptr_list.get(ptr_celltype_name) is None:
            rb_print(
                f"  MrubyBridgePlugin: [pointer]  {to_s(ttype.get_type_str())}* => "
                f"[class] TECS::{tment[1]}Pointer\n"
            )
            M._ptr_list[ptr_celltype_name] = tment
        if self._ptr_list.get(ptr_celltype_name) is None:
            self._ptr_list[ptr_celltype_name] = tment

    def get_type_map_ent(self, ttype: Any) -> list[str] | None:
        """構造体は check_struct_member で登録するので nil を返す。"""
        from tecsgen.core.cdl_types import StructType

        if isinstance(ttype, StructType):
            return None
        tstr = re.sub(
            r"const ", "", to_s(ttype.get_type_str()), count=1
        )  # const は無視
        tstr = re.sub(r"volatile ", "", tstr, count=1)  # volatile も無視
        if self._b_ignoreUnsigned:
            tstr = re.sub(r"unsigned ", "", tstr, count=1)
            tstr = re.sub(r"uint", "int", tstr, count=1)
            tstr = re.sub(r"[cs]char", "char", tstr, count=1)
        return M.TYPE_MAP.get(tstr)

    def gen_cdl_file(self, file: Any) -> None:
        """CDL ファイルの生成（typedef, signature, celltype, cell）。"""
        # ブリッジセルタイプの生成
        if M._celltypes.get(self._celltype_name) is None:
            M._celltypes[self._celltype_name] = [self]
            M._init_celltypes[self._init_celltype_name] = True
            nsp = to_s(self._signature.get_namespace_path())
            ct = to_s(self._celltype_name)
            ict = to_s(self._init_celltype_name)
            cls_name = to_s(self._class_name)
            self.print_msg(
                f"  MrubyBridgePlugin: [signature] {nsp} => [celltype] nMruby::{ct} => [class] TECS::{cls_name}\n"
            )
            file.print(
                "/*\n"
                " * MrubyBridgeSignaturePlugin:\n"
                f" *     signature={nsp}\n"
                " *\n"
                f" *   => celltype=nMruby::{ct}\n"
                " *      (bridge cell's celltype; generated in this file)\n"
                f" *      cell nMruby::{ct} BridgeCellName {{ cTECS = CellName.eEntry; }};\n"
                f" *        where eEntry's signature must be {nsp}.\n"
                f" *      => class=TECS::{cls_name}\n"
                " *         (mruby's class; accessible from your script)\n"
                f' *          bridge = TECS::{cls_name}.new("BridgeCellName")\n'
                " */\n"
                "import( <mruby.cdl> );\n"
                "\n"
                "/****  Ruby => TECS Bridge Celltype (MBP500) ****/\n"
                "namespace nMruby{\n"
                "    // bridge celltype\n"
                "    [idx_is_id,active]   // not actually active, to avoid warning W1002, W1007\n"
                f"    celltype {ct} {{\n"
                f"        call {nsp} cTECS;\n"
                "        attr {\n"
                "            [omit]\n"
                '            char_t *VMname = "VM";\n'
                "            [omit]\n"
                '            char_t *bridgeName = C_EXP( "$cell$" );\n'
                "        };\n"
                "    };\n"
                "    // bridge initializer celltype\n"
                f"    celltype {ict} {{\n"
                "        entry sInitializeTECSBridge eInitialize;\n"
                "    };\n"
                "};\n"
            )

            # 構造体セルタイプの生成
            for name, sttype in self._struct_list.items():
                if M._struct_list.get(name) is None:
                    file.print(
                        "namespace nMruby{\n"
                        "    [singleton]\n"
                        f"    celltype {to_s(name)} {{\n"
                        "        entry sInitializeTECSBridge eInitialize;\n"
                        "    };\n"
                        "};\n"
                    )
                    M._struct_list[name] = sttype
        else:
            self.cdl_info(
                "MRBW001 MrubyBridgePlugin: signature '$1' duplicate. ignored current one",
                self._signature.get_namespace_path(),
            )
            M._celltypes[self._celltype_name].append(self)

    def new_cell(self, cell: Any) -> None:
        """gen_cdl_file で定義したセルタイプ（名前は @celltype_name）に新しいセルが定義された。"""
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile
        from tecsgen.core.syntaxobj.cdlstring import CDLString
        from tecsgen.syntax.cdl_parser import CdlParser

        if cell.get_celltype().get_name() != self._celltype_name:
            return

        join = cell.get_join_list().get_item(sym("VMname"))
        if join is not None:
            vm_name = sym(CDLString.remove_dquote(to_s(join.get_rhs())))
        else:
            vm_name = sym("VM")

        if M._VM_list.get(vm_name) is None:
            M._VM_list[vm_name] = True
            initializer_celltype_cdl = (
                f"{get_context().gen}/{to_s(cell.get_name())}Initializer.cdl"
            )
            f = CFile.open(initializer_celltype_cdl, "w")
            # TECS 初期化セル（プロトタイプ宣言）
            self.print_msg(
                f"  MrubyBridgePlugin: join your VM's cInitialize to {to_s(vm_name)}_TECSInitializer.eInitialize\n"
            )
            f.print(
                "\n"
                "  // prototype of TECSInitializer (MBP510)\n"
                f"  cell nMruby::tTECSInitializer {to_s(vm_name)}_TECSInitializer;\n"
            )
            f.close()
            CdlParser.parse_file(initializer_celltype_cdl, self)

        vma = M._VM_celltypes.get(vm_name)
        if vma is not None:
            if vma.get(self._celltype_name) is not None:
                vma[self._celltype_name].append(cell)
            else:
                vma[self._celltype_name] = [cell]
        else:
            M._VM_celltypes[vm_name] = {self._celltype_name: [cell]}

        for sttype in self._struct_list.values():
            if M._VM_struct_list.get(vm_name) is not None:
                M._VM_struct_list[vm_name][sttype.get_name()] = sttype
            else:
                M._VM_struct_list[vm_name] = {sttype.get_name(): sttype}
        for ptr_celltype_name, tment in self._ptr_list.items():
            if M._VM_ptr_list.get(vm_name) is not None:
                M._VM_ptr_list[vm_name][ptr_celltype_name] = tment
            else:
                M._VM_ptr_list[vm_name] = {ptr_celltype_name: tment}

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """プラグインが CDL の POST コードを生成（tmp_plugin_post_code.cdl への出力）。"""
        cls.gen_post_code_body(file)

    @classmethod
    def gen_post_code_body(cls, file: Any) -> None:
        if M._b_post_coded is False:
            M._b_post_coded = True
        else:
            return

        file.print("\n  // MrubyBridgeSignaturePlugin: MBP601\n")
        for vm_name, instance_list in M._VM_celltypes.items():
            for array in instance_list.values():
                cell = array[0]
                if truthy(cell.get_celltype()):
                    ct_name = to_s(cell.get_celltype().get_name())
                    info = "Info" if ct_name.startswith("tInfo") else ""
                    file.print(
                        f"  cell nMruby{info}::{ct_name}_Initializer {to_s(vm_name)}_{ct_name}_Initializer{{ }};\n"
                    )

        file.print("  // MBP602\n")
        for name in M._ptr_list:
            file.print(f"  cell nMruby::{to_s(name)} C{to_s(name)} {{ }};\n")

        file.print("  // MBP603\n")
        for name in M._struct_list:
            file.print(f"  cell nMruby::{to_s(name)} C{to_s(name)} {{ }};\n")

        for vm_name, instance_list in M._VM_celltypes.items():
            file.print(f"  /* === VM name is '{to_s(vm_name)}' === (MBP610) */\n")
            init_cell_name = f"{to_s(vm_name)}_TECSInitializer"
            file.print(f"  cell nMruby::tTECSInitializer {init_cell_name} {{\n")
            for celltype_name in instance_list:
                file.print(
                    f"    cInitialize[] = {to_s(vm_name)}_{to_s(celltype_name)}_Initializer.eInitialize;\n"
                )
            if M._VM_ptr_list.get(vm_name) is not None:
                for name in M._VM_ptr_list[vm_name]:
                    file.print(f"    cInitialize[] = C{to_s(name)}.eInitialize;\n")
            if M._VM_struct_list.get(vm_name) is not None:
                for name in M._VM_struct_list[vm_name]:
                    file.print(f"    cInitialize[] = C{to_s(name)}.eInitialize;\n")
            file.print("  };")

    ####### 以下コード生成段階 ######

    def gen_ep_func_body(
        self,
        file: Any,
        b_singleton: bool,
        ct_name: Any,
        global_ct_name: Any,
        sig_name: Any,
        ep_name: Any,
        func_name: Any,
        func_global_name: Any,
        func_type: Any,
        params: Any,
    ) -> None:
        """受け口関数の本体コードを生成（頭部と末尾は別途出力）。ct_name は Symbol。"""
        args = (
            file,
            b_singleton,
            ct_name,
            global_ct_name,
            sig_name,
            ep_name,
            func_name,
            func_global_name,
            func_type,
            params,
        )
        if M._celltypes.get(ct_name) is not None:
            raise RubyRuntimeError("MrubyBridgeSignaturePlugin: unexpected ")
        if M._init_celltypes.get(ct_name) is not None:
            self.gen_ep_func_body_bridge_init(*args)
        elif M._ptr_list.get(ct_name) is not None:
            self.gen_ep_func_body_ptr(*args)
        elif M._struct_list.get(ct_name) is not None:
            self.gen_ep_func_body_struct(*args)
        else:
            raise RubyRuntimeError(
                f"MrubyBridgeSignaturePlugin: Unknown {to_s(ct_name)}"
            )

    def _bridge_func_name(self, f: Any) -> str:
        return (
            to_s(f.get_name())
            if f.get_name() != sym("initialize")
            else "initialize_cell"
        )

    def gen_ep_func_body_bridge_init(
        self,
        file: Any,
        b_singleton: bool,
        ct_name: Any,
        global_ct_name: Any,
        sig_name: Any,
        ep_name: Any,
        func_name: Any,
        func_global_name: Any,
        func_type: Any,
        params: Any,
    ) -> None:
        ct = to_s(self._celltype_name)
        file.print(
            "    // CELLCB *p_cellcb = GET_CELLCB( idx );  /* no error check */     /* MBP700 */\n"
            "    struct RClass\t*rc;\n"
            "\n"
            f'    rc = mrb_define_class_under( mrb, TECS, "{to_s(self._class_name)}", mrb->object_class );\n'
            f'    mrb_define_method( mrb, rc, "initialize", MrubyBridge_{ct}_initialize, MRB_ARGS_REQ(1) );\n'
            "    MRB_SET_INSTANCE_TT(rc, MRB_TT_DATA);\n"
        )
        for f in self._func_head_array:
            if not f.is_function():
                continue
            fn = self._bridge_func_name(f)
            n_param = 0
            for param in f.get_paramlist().get_items():
                d = param.get_direction()
                if d in (Y.IN, Y.INOUT, Y.OUT):
                    n_param += 1
                elif d in (Y.SEND, Y.RECEIVE):
                    raise RubyRuntimeError("MrubyBridgeSignaturePlugin: send, receive")
            p_str = f"MRB_ARGS_REQ( {n_param} )" if n_param > 0 else "MRB_ARGS_NONE()"
            file.print(
                f'\tmrb_define_method( mrb, rc, "{fn}", MrubyBridge_{ct}_{fn}, {p_str} );\n'
            )

    def gen_preamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """受け口関数の preamble（C 言語）を生成する。"""
        if M._celltypes.get(ct_name) is not None:
            self.gen_preamble_mruby(file, b_singleton, ct_name, global_ct_name)
            self.gen_preamble_instance(file, b_singleton, ct_name, global_ct_name)
            self.gen_preamble_instance_initialize(
                file, b_singleton, ct_name, global_ct_name
            )
            self.gen_preamble_bridge_func(file, b_singleton, ct_name, global_ct_name)
        elif M._init_celltypes.get(ct_name) is not None:
            self.gen_preamble_mruby(file, b_singleton, ct_name, global_ct_name)
            self.gen_preamble_instance_proto(file, b_singleton, ct_name, global_ct_name)
        elif M._ptr_list.get(ct_name) is not None:
            self.gen_preamble_ptr(file, b_singleton, ct_name, global_ct_name)
        elif M._struct_list.get(ct_name) is not None:
            self.gen_preamble_struct(file, b_singleton, ct_name, global_ct_name)
        else:
            raise RubyRuntimeError(
                f"MrubyBridgeSignaturePlugin: MrubyBridgeSignaturePlugin: Unknown {to_s(ct_name)}"
            )

    def gen_preamble_mruby(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        file.print(
            "/* MBP: MrubyBridgePlugin: MBP000 */\n"
            "#ifndef TECSGEN\n"
            '#include "mruby.h"\n'
            '#include "mruby/class.h"\n'
            '#include "mruby/data.h"\n'
            '#include "mruby/string.h"\n'
            "#endif /* TECSGEN */\n"
            '#include "TECSPointer.h"\n'
            '#include "TECSStruct.h"\n'
            "\n"
            "#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)\n"
            "#define DLLEXPORT __declspec(dllexport)\n"
            "#else\n"
            "#define DLLEXPORT\n"
            "#endif\n"
            "\n"
            "#ifndef NULL\n"
            "#define NULL 0\n"
            "#endif\n"
        )

    def _find_nmruby_celltype(self, ct_name: Any) -> Any:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        nsp = NamespacePath(sym("nMruby"), True)
        nsp.append_bang(ct_name)
        return Namespace.find(nsp)

    def gen_preamble_instance(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        # 「#1005 MrubyBridgePlugin-test のビルドに失敗」にて追加
        ct = self._find_nmruby_celltype(ct_name)
        if ct.idx_is_id_act():
            if ct.has_CB():
                inib_cb: str | None = "CB"
            elif ct.has_INIB():
                inib_cb = "INIB"
            else:
                inib_cb = None
            if inib_cb is not None:
                for cell in ct.get_cell_list():
                    if cell.is_generate():
                        # Ruby 版は INIB の場合も型名に _CB を使う（そのまま再現する）
                        file.print(
                            f"extern {to_s(ct.get_global_name())}_CB  "
                            f"{to_s(cell.get_global_name())}_{inib_cb};\n"
                        )

        c = to_s(self._celltype_name)
        file.print(
            "\n"
            "/* RData MBP001 */\n"
            "static void \n"
            f"{c}_free( mrb_state *mrb, void *p )\n"
            "{\n"
            "\tif( p )\n"
            "\t\t(void)mrb_free( mrb, p );\n"
            "}\n"
            "\n"
            "/* RData MBP002 */\n"
            f"struct mrb_data_type data_type_{c} =\n"
            "{\n"
            f'\t"{c}",\n'
            f"\t{c}_free\n"
            "};\n"
            "\n"
            "/* RData MBP003 */\n"
            f"struct tecs_{c} {{\n"
            "    CELLCB  *cbp;\n"
            "};\n"
            "\n"
            "/* name_to_cbp MBP010 */\n"
            f"const struct name_to_cbp_{c} {{\n"
            "    char   *name;    /* Cell Name */\n"
            "    CELLCB *cbp;\n"
            f"}} Name_to_cbp_{c}[] = {{\n"
        )

        ct = self._find_nmruby_celltype(ct_name)
        for cell in ct.get_cell_list():
            if cell.is_generate():
                join_list = cell.get_join_list()
                join = join_list.get_item(sym("bridgeName"))
                if join is None:
                    name = f'"{to_s(cell.get_name())}"'
                else:
                    attr_list = cell.get_celltype().get_attribute_list()
                    name = to_s(join.get_rhs().eval_const(join_list, attr_list))
                name_array = ct.get_name_array(cell)
                file.print(f"\t{{ {name}, {to_s(name_array[8])} }},\n")

        file.print("\t{ 0, 0 },\n};\n\n")

    def gen_preamble_instance_proto(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        c = to_s(self._celltype_name)
        file.print(
            "//  Prototype MBP400\n"
            f"mrb_value  MrubyBridge_{c}_initialize( mrb_state *mrb, mrb_value self);\n"
        )
        for f in self._func_head_array:
            if not f.is_function():
                continue
            fn = self._bridge_func_name(f)
            file.print(
                f"mrb_value  MrubyBridge_{c}_{fn}( mrb_state *mrb, mrb_value self );\n"
            )

    def gen_preamble_instance_initialize(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        c = to_s(self._celltype_name)
        file.print(
            "\n"
            "/* MBP100 */\n"
            "mrb_value\n"
            f"MrubyBridge_{c}_initialize( mrb_state *mrb, mrb_value self)\n"
            "{\n"
            "\tmrb_value\tname;\n"
            f"\tstruct tecs_{c} *tecs_cb;\n"
            f"\tconst struct name_to_cbp_{c} *ntc;\n"
            "\n"
            "\t/* set DATA_TYPE earlier to avoid SEGV */\n"
            f"\tDATA_TYPE( self ) = &data_type_{c};\n"
            "\n"
            '\tmrb_get_args(mrb, "o", &name );\n'
            "\tif( mrb_type( name ) != MRB_TT_STRING ){\n"
            '\t\tmrb_raise(mrb, E_NAME_ERROR, "cell name not string");\n'
            "\t}\n"
            f"\tfor( ntc = &Name_to_cbp_{c}[0]; ntc->name != NULL; ntc++ ){{\n"
            "\t\tif( strcmp( ntc->name, RSTRING_PTR( name ) ) == 0 )\n"
            "\t\t\tbreak;\n"
            "\t}\n"
            "\tif( ntc->name == 0 ){\n"
            '\t\tmrb_raise(mrb, E_ARGUMENT_ERROR, "cell not found");\n'
            "\t}\n"
            f"\ttecs_cb = (struct tecs_{c} *)mrb_malloc(mrb, sizeof(struct tecs_{c}) );\n"
            "\ttecs_cb->cbp = ntc->cbp;\n"
            "\tDATA_PTR( self ) = (void *)tecs_cb;\n"
            "\n"
            "\treturn self;\n"
            "}\n"
        )

    def gen_preamble_bridge_func(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        from tecsgen.core.cdl_types import (
            BoolType,
            FloatType,
            IntType,
            PtrType,
            StructType,
            VoidType,
        )

        c = to_s(self._celltype_name)
        for f in self._func_head_array:
            if not f.is_function():
                continue
            fn = self._bridge_func_name(f)
            ret_type = f.get_return_type()
            ret_type0 = ret_type.get_original_type()
            b_void = ret_type0.is_void()
            plist = f.get_paramlist().get_items()

            file.print(
                "\n"
                "/* bridge function (MBP101) */\n"
                "mrb_value\n"
                f"MrubyBridge_{to_s(ct_name)}_{fn}( mrb_state *mrb, mrb_value self )\n"
                "{\n"
                "\t/* cellcbp (MBP105) */\n"
                f"\tCELLCB\t*p_cellcb = ((struct tecs_{c} *)DATA_PTR(self))->cbp;\n"
            )
            file.print("\t/* variables for return & parameter (MBP110) */\n")
            if not b_void:
                file.print(
                    f"\t{ret_type.get_type_str()}\tret_val{ret_type.get_type_str_post()};\n"
                )

            def in_dir(param: Any) -> bool:
                return param.get_direction() in (Y.IN, Y.INOUT, Y.OUT)

            arg_str = ""
            n_param = 0
            n_scalar = 0
            n_ptr = 0
            n_struct = 0
            for param in plist:
                if not in_dir(param):
                    continue
                pn = to_s(param.get_name())
                pt = param.get_type()
                decl = f"\t{pt.get_type_str()}\t{pn}{pt.get_type_str_post()};\n"
                type_ = pt.get_original_type()
                if isinstance(type_, IntType):
                    file.print(f"\tmrb_int\tmrb_{pn};\n" + decl)
                    arg_str += "i"
                    n_scalar += 1
                elif isinstance(type_, FloatType):
                    file.print(f"\tmrb_float\tmrb_{pn};\n" + decl)
                    arg_str += "f"
                    n_scalar += 1
                elif isinstance(type_, BoolType):
                    file.print(f"\tmrb_value\tmrb_{pn};\n" + decl)
                    arg_str += "o"
                    n_scalar += 1
                elif isinstance(type_, PtrType):
                    file.print(f"\tmrb_value\tmrb_{pn};\n" + decl)
                    arg_str += "o"
                    n_ptr += 1
                elif isinstance(type_, StructType):
                    file.print(
                        f"\tmrb_value\tmrb_{pn};\n"
                        f"\t{pt.get_type_str()}\t*{pn}{pt.get_type_str_post()};\n"
                    )
                    arg_str += "o"
                    n_struct += 1
                else:
                    raise RubyRuntimeError("MrubyBridgeSignaturePlugin: Unknown type")
                n_param += 1

            if n_param > 0:
                file.print("\t/* retrieve arguments (MBP111) */\n")
                file.print(f'\tmrb_get_args(mrb, "{arg_str}"')
                for param in plist:
                    if in_dir(param):
                        type_ = param.get_type().get_original_type()
                        if isinstance(
                            type_, (IntType, FloatType, BoolType, PtrType, StructType)
                        ):
                            file.print(f", &mrb_{to_s(param.get_name())}")
                        else:
                            raise RubyRuntimeError(
                                "MrubyBridgeSignaturePlugin: Unknown type"
                            )
                file.print(" );\n")

                if n_scalar > 0 or n_struct > 0:
                    file.print("\t/* convert mrb to C (MBP112) */\n")
                for param in plist:
                    if not in_dir(param):
                        continue
                    pn = to_s(param.get_name())
                    type_ = param.get_type().get_original_type()
                    if isinstance(type_, IntType):
                        tment: Any = self.get_type_map_ent(type_.get_original_type())
                        file.print(f"\tVALCHECK_{tment[1]}( mrb, mrb_{pn} );\n")
                        file.print(
                            f"\t{pn} = ({param.get_type().get_type_str()})mrb_{pn};\n"
                        )
                    elif isinstance(type_, FloatType):
                        file.print(
                            f"\t{pn} = ({param.get_type().get_type_str()})mrb_{pn};\n"
                        )
                    elif isinstance(type_, BoolType):
                        file.print(f"\t{pn} = mrb_test( mrb_{pn} );\n")
                    elif isinstance(type_, PtrType):
                        ttype = type_.get_type().get_original_type()
                        if isinstance(ttype, StructType):
                            tn = to_s(ttype.get_name())
                            file.print(f"\tCHECK_STRUCT( {tn}, mrb_{pn} );\n")
                            file.print(f"\t{pn} = (struct {tn}*)DATA_PTR(mrb_{pn});\n")
                        elif not isinstance(ttype, (IntType, FloatType, BoolType)):
                            raise RubyRuntimeError(
                                "MrubyBridgeSignaturePlugin: cannot handle type"
                            )
                    elif isinstance(type_, StructType):
                        tn = to_s(type_.get_name())
                        file.print(f"\tCHECK_STRUCT( {tn}, mrb_{pn} );\n")
                        file.print(f"\t{pn} = (struct {tn}*)DATA_PTR(mrb_{pn});\n")
                    else:
                        raise RubyRuntimeError(
                            "MrubyBridgeSignaturePlugin: canot treat class"
                        )

                if n_ptr > 0:
                    file.print("\t/* convert mrb to C for pointer types (MBP113) */\n")
                for param in plist:
                    if not in_dir(param):
                        continue
                    type_ = param.get_type().get_original_type()
                    if isinstance(type_, (IntType, FloatType, BoolType, StructType)):
                        pass
                    elif isinstance(type_, PtrType):
                        ttype = type_.get_type().get_original_type()
                        if isinstance(ttype, StructType):
                            pass
                        elif isinstance(ttype, (IntType, FloatType, BoolType)):
                            self.ptrMrb2C(file, type_, param)
                        else:
                            raise RubyRuntimeError(
                                "MrubyBridgeSignaturePlugin: cannot handle type"
                            )
                    else:
                        raise RubyRuntimeError(
                            "MrubyBridgeSignaturePlugin: canot treat class"
                        )

            file.print("\t/* calling target (MBP120) */\n")
            file.print("\tret_val = " if not b_void else "\t")
            delim = ""
            file.print(f"cTECS_{to_s(f.get_name())}( ")
            for param in plist:
                aster = (
                    "*"
                    if isinstance(param.get_type().get_original_type(), StructType)
                    else ""
                )
                file.print(f"{delim}{aster}{to_s(param.get_name())}")
                delim = ", "
            file.print(" );\n")

            file.print("\t/* return (MBP130) */\n")
            if isinstance(ret_type0, BoolType):
                file.print("\treturn ret_val ? mrb_true_value() : mrb_false_value();\n")
            elif isinstance(ret_type0, IntType):
                file.print("\treturn mrb_fixnum_value( ret_val );\n")
            elif isinstance(ret_type0, FloatType):
                file.print("\treturn mrb_float_value( mrb, ret_val );\n")
            elif isinstance(ret_type0, VoidType):
                file.print("\treturn  mrb_nil_value();\n")
            else:
                raise RubyRuntimeError("MrubyBridgeSignaturePlugin: unknown type")

            file.print("}\n")
