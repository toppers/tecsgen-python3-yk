"""MrubyInfoBridgeSignaturePlugin.rb の移植。mruby から TECSInfo 経由で受け口関数を呼ぶためのブリッジを生成する。

`MrubyBridgeSignaturePlugin` の派生で、セル名のかわりに TECSInfo の経路（"::cell.eEntry"）から
受け口のディスクリプタを得る。Ruby 版も同じ `MrubyBridgeSignaturePluginModule` を include するので、
クラス変数（`@@celltypes` など）はモジュールにあって `MrubyBridgeSignaturePlugin` と共有する。
`check_name_and_return_type`・`check_parameter_type`・`get_type_map_ent` とコードを出す
`gen_preamble_bridge_func` の大部分は、Ruby 版でも `MrubyBridgeSignaturePlugin` と同じ内容なので
共有する（メッセージの文言が違うものは別に書く）。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.lib.MrubyBridgeSignaturePluginModule import (
    MrubyBridgeSignaturePluginModule,
)
from tecsgen.plugin.MrubyBridgeSignaturePlugin import MrubyBridgeSignaturePlugin
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    rb_print,
    sym,
    to_s,
    truthy,
    utf8_literal,
)

M = MrubyBridgeSignaturePluginModule

_RX_TECSINFO_SIG = re.compile(r"\A::nTECSInfo::")


class MrubyInfoBridgeSignaturePlugin(MrubyBridgeSignaturePluginModule, SignaturePlugin):
    _b_no_banner: ClassVar[bool] = False
    # Ruby 版はこのファイルが require された時点で Makefile に追加する（プロセスごとに1回）
    _b_loaded: ClassVar[bool] = False

    @classmethod
    def reset(cls) -> None:
        """Ruby のクラス変数に当たる状態を初期化する（1プロセスで何度も実行するテスト用）。"""
        MrubyInfoBridgeSignaturePlugin._b_no_banner = False
        MrubyInfoBridgeSignaturePlugin._b_loaded = False

    @classmethod
    def on_load(cls) -> None:
        """ロードされた時点で実行される処理（Makefile への追加）。実行ごとに1回だけ行う。"""
        from tecsgen.core.tecsgen import Makefile

        if MrubyInfoBridgeSignaturePlugin._b_loaded:
            return
        MrubyInfoBridgeSignaturePlugin._b_loaded = True
        # -I に $(TECSPATH)/mruby を追加
        Makefile.add_ldflag("-lmruby -L$(MRUBYPATH)/lib -lm")
        Makefile.add_search_path("$(MRUBYPATH)/include")
        Makefile.add_var("MRUBYPATH", "..", "CHANGE this to suitable path")

    def __init__(self, signature: Any, option: Any) -> None:
        """プラグインインスタンスの初期化。戻り値、引数の型が使用可能なものかチェックする。"""
        MrubyInfoBridgeSignaturePlugin.on_load()
        super().__init__(signature, option)

        if not MrubyInfoBridgeSignaturePlugin._b_no_banner:
            from tecsgen.cli import _stderr

            _stderr(
                "MrubyInfoBridgeSignaturePlugin: version 2.0.0 (Suitable for mruby above ver 1.2.0). \n"
            )
            MrubyInfoBridgeSignaturePlugin._b_no_banner = True

        self._b_ignoreUnsigned = False
        self._includes: list[Any] = []  # function name list
        self._excludes: list[Any] = []  # function name list
        self._struct_list: dict[Any, Any] = {}
        self._ptr_list: dict[Any, Any] = {}
        self._auto_exclude_list: dict[Any, Any] = {}  # function name list
        self._b_auto_exclude = True  # auto_exclude = true by default
        # exclude TECSInfo & mruby: sInitializeBridge, sInitializeTECSBridge
        self._b_refused_signature = False

        self._plugin_arg_check_proc_tab = M.MRUBY_BRIDGE_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

        gname = to_s(self._signature.get_global_name())
        self._celltype_name = sym(f"tInfo{gname}")
        self._init_celltype_name = sym(f"{to_s(self._celltype_name)}_Initializer")
        self._class_name = sym(f"Info{gname}")

        self._func_head_array: list[Any] = []
        fh_array: list[Any] = []
        if len(self._includes) > 0 and len(self._excludes) > 0:
            self.cdl_error("MRB1011 both include && exclude are specified")

        sig_path = to_s(signature.get_namespace_path())
        if sig_path == "::nTECSInfo::sAccessor":
            pass  # accept
        elif sig_path in (
            "::nMruby::sInitializeBridge",
            "::nMruby::sInitializeTECSBridge",
        ) or _RX_TECSINFO_SIG.match(sig_path):
            # refuse
            self._b_refused_signature = True
            return

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
            self.cdl_warning(
                "MRB1012 '$1' no function remained by exclude",
                self._signature.get_name(),
            )

    # Ruby 版でも MrubyBridgeSignaturePlugin と同じ内容
    check_name_and_return_type = MrubyBridgeSignaturePlugin.check_name_and_return_type
    check_parameter_type = MrubyBridgeSignaturePlugin.check_parameter_type
    get_type_map_ent = MrubyBridgeSignaturePlugin.get_type_map_ent
    _bridge_func_name = MrubyBridgeSignaturePlugin._bridge_func_name
    _find_nmruby_celltype = MrubyBridgeSignaturePlugin._find_nmruby_celltype

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
                f"  MrubyInfoBridgePlugin: [struct]   {to_s(struct_type.get_type_str())} => "
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
                f"  MrubyInfoBridgePlugin: [pointer]  {to_s(ttype.get_type_str())}* => "
                f"[class] TECS::{tment[1]}Pointer\n"
            )
            M._ptr_list[ptr_celltype_name] = tment
        if self._ptr_list.get(ptr_celltype_name) is None:
            self._ptr_list[ptr_celltype_name] = tment

    def gen_cdl_file(self, file: Any) -> None:
        """CDL ファイルの生成（typedef, signature, celltype, cell）。"""
        if self._b_refused_signature:
            return

        # ブリッジセルタイプの生成
        if M._celltypes.get(self._celltype_name) is None:
            M._celltypes[self._celltype_name] = [self]
            M._init_celltypes[self._init_celltype_name] = True
            nsp = to_s(self._signature.get_namespace_path())
            ct = to_s(self._celltype_name)
            ict = to_s(self._init_celltype_name)
            cls_name = to_s(self._class_name)
            gname = to_s(self._signature.get_global_name())
            self.print_msg(
                f"  MrubyInfoBridgePlugin: [signature] {nsp} => [class] TECS::{cls_name}\n"
            )

            file.print(
                " /*\n"
                "  * MrubyInfoBridgeSignaturePlugin:\n"
                f"  *     signature={nsp}\n"
                "  *\n"
                f"  *   => celltype=nMrubyInfo::{ct}\n"
                "  *      (bridge cell 's celltype; generated in this file)\n"
                f"  *      cell nMrubyInfo::{ct} BridgeCellName {{ cTECS = CellName.eEntry; }};\n"
                f"  *        where eEntry's signature must be {nsp}.\n"
                f"  *      => class=TECS::{cls_name}\n"
                + utf8_literal(
                    "  *         (mruby’s class; accessible from your script)\n"
                )
                + f'  *          bridge = TECS::{cls_name}.new("BridgeCellName")\n'
                "  */\n"
                "import( <mruby.cdl> );\n"
                "\n"
                "/****  Ruby => TECS Bridge Celltype (MBP500) ****/\n"
                "namespace nMrubyInfo{\n"
                "    // bridge celltype\n"
                "    [singleton, idx_is_id,active]   // not actually active, to avoid warning W1002, W1007\n"
                f"    celltype {ct} {{\n"
                "        [dynamic,optional]\n"
                f"            call {nsp} cTECS;\n"
                "        call nTECSInfo::sTECSInfo cTECSInfo;\n"
                "        [dynamic,optional]\n"
                "            call nTECSInfo::sEntryInfo cEntryInfo;\n"
                "        [dynamic,optional]\n"
                "            call nTECSInfo::sSignatureInfo cSignatureInfo;\n"
                "        [dynamic,optional]\n"
                "            call nTECSInfo::sRawEntryDescriptorInfo cRawEntryDescriptorInfo;\n"
                "        attr {\n"
                "            [omit]\n"
                '            char_t *VMname = "VM";\n'
                "            [omit]\n"
                '            char_t *bridgeName = C_EXP( "$cell$" );\n'
                "        };\n"
                "    };\n"
                "    // bridge initializer celltype\n"
                f"    celltype {ict} {{\n"
                "        entry nMruby::sInitializeTECSBridge eInitialize;\n"
                "    };\n"
                "};\n"
                "\n"
                "// Bridge Cell\n"
                f"cell nMrubyInfo::{ct} MrubyInfoBridge_{gname} {{\n"
                "  // cTECS = Sample.eEnt;\n"
                "  cTECSInfo = TECSInfo.eTECSInfo;\n"
                '  // bridgeName = "Simple";\n'
                "};\n"
            )

            # 構造体セルタイプの生成
            for name, sttype in self._struct_list.items():
                if M._struct_list.get(name) is None:
                    file.print(
                        "namespace nMruby{\n"
                        "    [singleton]\n"
                        f"    celltype {to_s(name)} {{\n"
                        "        entry nMruby::sInitializeTECSBridge eInitialize;\n"
                        "    };\n"
                        "};\n"
                    )
                    M._struct_list[name] = sttype
        else:
            self.cdl_info(
                "MRBW001 MrubyInfoBridgePlugin: signature '$1' duplicate. ignored current one",
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
                f"  MrubyInfoBridgePlugin: join your VM's cInitialize to {to_s(vm_name)}_TECSInitializer.eInitialize\n"
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

        file.print("\n  // MrubyInfoBridgeSignaturePlugin: MBP601\n")
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
            raise RubyRuntimeError("MrubyInfoBridgeSignaturePlugin: unexpected ")
        if M._init_celltypes.get(ct_name) is not None:
            self.gen_ep_func_body_bridge_init(*args)
        elif M._ptr_list.get(ct_name) is not None:
            self.gen_ep_func_body_ptr(*args)
        elif M._struct_list.get(ct_name) is not None:
            self.gen_ep_func_body_struct(*args)
        else:
            raise RubyRuntimeError(
                f"MrubyInfoBridgeSignaturePlugin: Unknown {to_s(ct_name)}"
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
            f'    mrb_define_method( mrb, rc, "initialize", MrubyInfoBridge_{ct}_initialize, MRB_ARGS_REQ(1) );\n'
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
                    raise RubyRuntimeError(
                        "MrubyInfoBridgeSignaturePlugin: send, receive"
                    )
            p_str = f"MRB_ARGS_REQ( {n_param} )" if n_param > 0 else "MRB_ARGS_NONE()"
            file.print(
                f'    mrb_define_method( mrb, rc, "{fn}", MrubyInfoBridge_{ct}_{fn}, {p_str} );\n'
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
                f"MrubyInfoBridgeSignaturePlugin: MrubyInfoBridgeSignaturePlugin: Unknown {to_s(ct_name)}"
            )

    def gen_preamble_mruby(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        file.print(
            "/* MBP: MrubyInfoBridgePlugin: MBP000 */\n"
            '#include "mruby.h"\n'
            '#include "mruby/class.h"\n'
            '#include "mruby/data.h"\n'
            '#include "mruby/string.h"\n'
            '#include "TECSPointer.h"\n'
            '#include "TECSStruct.h"\n'
            '#include "t_syslog.h"\n'
            '#include "stdlib.h"\n'
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

    def gen_preamble_instance(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        # 「#1005  MrubyBridgePlugin-test のビルドに失敗」にて追加
        nsp = NamespacePath(sym("nMrubyInfo"), True)
        nsp.append_bang(ct_name)
        ct = Namespace.find(nsp)
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
            "    if( p )\n"
            "        (void)mrb_free( mrb, p );\n"
            "}\n"
            "\n"
            "/* RData MBP002 */\n"
            f"struct mrb_data_type data_type_{c} =\n"
            "{\n"
            f'    "{c}",\n'
            f"    {c}_free\n"
            "};\n"
            "\n"
            "/* RData MBP003 */\n"
            f"struct tecs_{c} {{\n"
            f"    Descriptor( {to_s(self._signature.get_global_name())} ) desc;\n"
            "};\n"
            "\n"
            "#ifndef MRUBYINFOBRIDGE_NAME_LEN\n"
            "#define MRUBYINFOBRIDGE_NAME_LEN  256\n"
            "#endif\n"
        )

    def gen_preamble_instance_proto(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        c = to_s(self._celltype_name)
        file.print(
            "//  Prototype MBP400\n"
            f"mrb_value  MrubyInfoBridge_{c}_initialize( mrb_state *mrb, mrb_value self);\n"
        )
        for f in self._func_head_array:
            if not f.is_function():
                continue
            fn = self._bridge_func_name(f)
            file.print(
                f"mrb_value  MrubyInfoBridge_{c}_{fn}( mrb_state *mrb, mrb_value self );\n"
            )

    def gen_preamble_instance_initialize(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        c = to_s(self._celltype_name)
        sig_name = to_s(self._signature.get_name())
        sig_gname = to_s(self._signature.get_global_name())
        file.print(
            "\n"
            "/* MBP100 */\n"
            "mrb_value\n"
            f"MrubyInfoBridge_{c}_initialize( mrb_state *mrb, mrb_value self)\n"
            "{\n"
            "    mrb_value\tname;\n"
            f"    struct tecs_{c} *tecs_desc;\n"
            "    Descriptor( nTECSInfo_sRawEntryDescriptorInfo ) rawEntryDescDesc;\n"
            "    Descriptor( nTECSInfo_sEntryInfo ) entryDesc;\n"
            "    Descriptor( nTECSInfo_sSignatureInfo ) signatureDesc;\n"
            f"    Descriptor( {sig_gname} ) cellEntryDesc;\n"
            "    char_t   tecs_name[ MRUBYINFOBRIDGE_NAME_LEN ];\n"
            "    void     *rawDesc;\n"
            "    char     *p;\n"
            "    int      subsc;\n"
            "\n"
            "    /* set DATA_TYPE earlier to avoid SEGV */\n"
            f"    DATA_TYPE( self ) = &data_type_{c};\n"
            "\n"
            '    mrb_get_args(mrb, "o", &name );\n'
            "    if( mrb_type( name ) != MRB_TT_STRING ){\n"
            '        mrb_raise(mrb, E_NAME_ERROR, "cell name not string");\n'
            "    }\n"
            "    if( cTECSInfo_findRawEntryDescriptor( RSTRING_PTR( name ), &rawEntryDescDesc, &entryDesc ) != E_OK ){\n"
            '         mrb_raise( mrb, E_ARGUMENT_ERROR, "MrubyInfoBridgeSignaturePlugin: path not found" );\n'
            "    }\n"
            "    else{\n"
            "#ifdef MRUBYINFOBRIDGEPLUGIN_VERBOSE\n"
            '         syslog( LOG_NOTICE, "MrubyInfoBridgePlugin: %s: found", RSTRING_PTR( name ) );\n'
            "#endif /* MRUBYINFOBRIDGEPLUGIN_VERBOSE */\n"
            "    }\n"
            "\n"
            "    // retrieve Signature Name from EntryInfo to check\n"
            "    cEntryInfo_set_descriptor( entryDesc );\n"
            "    cEntryInfo_getSignatureInfo( &signatureDesc );\n"
            "    cSignatureInfo_set_descriptor( signatureDesc );\n"
            "    cSignatureInfo_getName( tecs_name, MRUBYINFOBRIDGE_NAME_LEN );\n"
            f'    if( strncmp( tecs_name, "{sig_name}", MRUBYINFOBRIDGE_NAME_LEN ) != 0 ){{\n'
            '         mrb_raise( mrb, E_ARGUMENT_ERROR, "MrubyInfoBridgeSignaturePlugin: signature name mismatch" );\n'
            "    }\n"
            "    else{\n"
            "#ifdef MRUBYINFOBRIDGEPLUGIN_VERBOSE\n"
            f'         syslog( LOG_NOTICE, "MrubyInfoBridgePlugin: signature name matched: %s", "{sig_name}" );\n'
            "#endif /* MRUBYINFOBRIDGEPLUGIN_VERBOSE */\n"
            "    }\n"
            "\n"
            "    /* retrieve entry array suscript if exist */\n"
            "    for( p = RSTRING_PTR( name ), subsc = 0; *p != 0; p++ ){\n"
            "        if( *p == '[' ){\n"
            "            p++;\n"
            "            subsc = atoi( p );\n"
            "            break;\n"
            "        }\n"
            "    }\n"
            "\n"
            "    // retrieve Cell's Entry Descriptor\n"
            "    cRawEntryDescriptorInfo_set_descriptor( rawEntryDescDesc );\n"
            "    if( cRawEntryDescriptorInfo_getRawDescriptor( subsc, &rawDesc ) != E_OK ){\n"
            '         mrb_raise( mrb, E_ARGUMENT_ERROR, "MrubyInfoBridgeSignaturePlugin: cannot get RawDescriptor (maybe subscript out of range)" );\n'
            "    }\n"
            "    else{\n"
            "#ifdef MRUBYINFOBRIDGEPLUGIN_VERBOSE\n"
            f'         syslog( LOG_NOTICE, "MrubyInfoBridgePlugin: got RawDescriptor: %s %d", "{sig_name}", subsc );\n'
            "#endif /* MRUBYINFOBRIDGEPLUGIN_VERBOSE */\n"
            "    }\n"
            f"    cellEntryDesc.vdes = (struct tag_{sig_gname}_VDES *)rawDesc;\n"
            "  \n"
            f"    tecs_desc = (struct tecs_{c} *)mrb_malloc(mrb, sizeof(struct tecs_{c}) );\n"
            "    tecs_desc->desc = cellEntryDesc;\n"
            "    DATA_PTR( self ) = (void *)tecs_desc;\n"
            "\n"
            "    return self;\n"
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
                f"MrubyInfoBridge_{to_s(ct_name)}_{fn}( mrb_state *mrb, mrb_value self )\n"
                "{\n"
                "  /* cellcbp (MBP105) */\n"
                f"  // CELLCB\t*p_cellcb = ((struct tecs_{c} *)DATA_PTR(self))->cbp;\n"
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
                    raise RubyRuntimeError(
                        "MrubyInfoBridgeSignaturePlugin: Unknown type"
                    )
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
                                "MrubyInfoBridgeSignaturePlugin: Unknown type"
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
                                "MrubyInfoBridgeSignaturePlugin: cannot handle type"
                            )
                    elif isinstance(type_, StructType):
                        tn = to_s(type_.get_name())
                        file.print(f"\tCHECK_STRUCT( {tn}, mrb_{pn} );\n")
                        file.print(f"\t{pn} = (struct {tn}*)DATA_PTR(mrb_{pn});\n")
                    else:
                        raise RubyRuntimeError(
                            "MrubyInfoBridgeSignaturePlugin: canot treat class"
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
                                "MrubyInfoBridgeSignaturePlugin: cannot handle type"
                            )
                    else:
                        raise RubyRuntimeError(
                            "MrubyInfoBridgeSignaturePlugin: canot treat class"
                        )

            file.print(
                "\t/* calling target (MBP120) */\n"
                f"  cTECS_set_descriptor( ((struct tecs_{c} *)DATA_PTR(self))->desc );\n"
            )
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
                raise RubyRuntimeError("MrubyInfoBridgeSignaturePlugin: unknown type")

            file.print("}\n")
