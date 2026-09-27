"""generate.rb の移植（内部仕様8章・10章）。コード生成。

Ruby 版は `Namespace`・`Signature`・`Celltype` などのモデルクラスを再オープンして `generate`・
`gen_*` を足している。Python 版はクラスごとの mixin にし、各モデルクラスの基底に入れる。
Celltype の部分は大きいので `generate_celltype*.py` に分けた。

ヒアドキュメントは f 文字列でそのまま写す（C のコードの `{`・`}` は `{{`・`}}` と書く）。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context, print_exception
from tecsgen.core.generator import _get_at
from tecsgen.host import get_host
from tecsgen.ruby_compat import RubyIO, Y, rb_print, to_s, truthy


def ifdef_macro_only(f: Any) -> None:
    # Ruby 版も #ifndef を出力する（名前と違うが、移植元のとおり）
    f.print("#ifndef TOPPERS_MACRO_ONLY\n\n")


def ifndef_macro_only(f: Any) -> None:
    f.print("#ifndef TOPPERS_MACRO_ONLY\n\n")


def endif_macro_only(f: Any) -> None:
    f.print("#endif /* TOPPERS_MACRO_ONLY */\n\n")


def ifndef_cb_type_only(f: Any) -> None:
    f.print("#ifndef TOPPERS_CB_TYPE_ONLY\n\n")


def ifdef_cb_type_only(f: Any) -> None:
    f.print("#ifdef TOPPERS_CB_TYPE_ONLY\n\n")


def endif_cb_type_only(f: Any) -> None:
    f.print("#endif /* TOPPERS_CB_TYPE_ONLY */\n\n")


def begin_extern_C(f: Any) -> None:
    f.print('#ifdef __cplusplus\nextern "C" {\n#endif /* __cplusplus */\n')


def end_extern_C(f: Any) -> None:
    f.print("#ifdef __cplusplus\n}\n#endif /* __cplusplus */\n")


def print_note(f: Any, b_complete: bool = True) -> None:
    from tecsgen.core.messages import TECSMsg

    f.print("/*\n" if b_complete else " *\n")
    f.print(TECSMsg.get("note"))
    f.print(" */\n" if b_complete else " *\n")


def print_Makefile_note(f: Any) -> None:
    from tecsgen.core.messages import TECSMsg

    f.print(TECSMsg.get("Makefile_note"))


def print_indent(f: Any, n: int) -> None:
    f.print("    " * n)


class AppFile:
    """Appendable File（追記可能ファイル）。

    同じ名前で2回目以降に開くと追記モードになる。`--force-overwrite` でなければ `<name>.tmp` に
    書き、`update()` で既存ファイルと比べて、内容が変わったときだけ置き換える
    （make の依存関係で不要な再コンパイルが起きないようにするため）。
    """

    # 開いたファイルのリスト（挿入順を保つ。Ruby の Hash と同じ）
    _file_name_list: ClassVar[dict[str, bool]] = {}

    @classmethod
    def reset(cls) -> None:
        """開いたファイルのリストを空にする（Ruby 版には無い。テスト用）。"""
        cls._file_name_list = {}

    @classmethod
    def open(cls, name: str) -> RubyIO:
        ctx = get_context()
        real_name = name if ctx.force_overwrite else name + ".tmp"

        if cls._file_name_list.get(name):
            # 既に開いている: 追記モードで開く
            return RubyIO(real_name, "a", ctx.file_codec)
        # 新規モードで開く（既にあれば、サイズを０にする）
        f = RubyIO(real_name, "w", ctx.file_codec)
        cls._file_name_list[name] = True
        return f

    @classmethod
    def update(cls) -> None:
        ctx = get_context()
        if ctx.force_overwrite:
            return

        host = get_host()
        for name in cls._file_name_list:
            tmp = name + ".tmp"
            b_identical = False
            if host.is_readable(name):
                old_lines = host.read_bytes(name).splitlines(keepends=True)
                new_lines = host.read_bytes(tmp).splitlines(keepends=True)
                b_identical = old_lines == new_lines
            if not b_identical:
                if ctx.verbose:
                    rb_print(f"{name} changed\n")
                    rb_print(f"renaming '{name}.tmp' => '{name}'\n")
                host.rename(tmp, name)
            else:
                if ctx.verbose:
                    rb_print(f"{name} not changed\n")
                host.remove(tmp)


class MemFile:
    """文字列に書き溜める出力先（File と同じ print を持つ）。"""

    def __init__(self) -> None:
        self._string = ""

    def print(self, s: Any) -> None:
        self._string += to_s(s)

    def get_string(self) -> str:
        return self._string


class NamespaceGenerate:
    """generate.rb の Namespace 再オープン部分（mixin）。

    クラス変数 `@@domain_gen_factory_list`・`@@class_gen_factory_list` は Namespace 本体にある。
    """

    _name: Any
    _signature_list: list[Any]
    _celltype_list: list[Any]
    _namespace_list: list[Any]
    _decl_list: list[Any]
    _const_decl_list: list[Any]

    def generate(self) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.region import Region

        ctx = get_context()
        s: Any = self
        dbg_print(
            f"Namespace#generate: generating_region={to_s(ctx.generating_region.get_name())} "
            f"namespace={to_s(self._name)} gen_dir={ctx.gen}\n"
        )
        try:
            # root namespace ならば makefile を出力する(全セルタイプに関わるものだけ)
            # 先に出力する
            if self._name == "::":
                self.gen_makefile_template()
                self.gen_makefile_tecsgen()
                if ctx.generating_region.get_n_cells() == 0:
                    dbg_print(f"only makefile_template {to_s(self._name)}\n")
                    return

            # global_tecsgen.h (typedef, struct, const) の生成
            self.gen_global_header()

            # signature のコードを生成
            for sig in self._signature_list:
                sig.generate()

            # celltype のコードを生成
            for t in self._celltype_list:
                t.generate()

            # サブネームスペースのコードを生成
            for n in self._namespace_list:
                n.generate()

            # ドメインプラグインの gen_factory は、諸々のコードの出た後で呼び出す V1.8
            if type(self) is Region:
                gr = ctx.generating_region
                if (
                    s.get_domain_type() is not None
                    and Namespace._domain_gen_factory_list.get(gr) is None
                ):
                    Namespace._domain_gen_factory_list[gr] = self
                    s.get_domain_type().gen_factory(gr)
                if (
                    s.get_class_type() is not None
                    and Namespace._class_gen_factory_list.get(gr) is None
                ):
                    Namespace._class_gen_factory_list[gr] = self
                    s.get_class_type().gen_factory(gr)
        except Exception as evar:  # noqa: BLE001  Ruby の rescue => evar
            reraise_if_not_standard_error(evar)
            s.cdl_error("H1001 tecsgen: fatal internal error during code generation")
            print_exception(evar)

    def generate_post(self) -> None:
        ctx = get_context()
        s: Any = self
        if ctx.generating_region.get_n_cells() == 0:
            return

        try:
            # global_tecsgen.h (typedef, struct, const) の終わりのガードコード生成
            self.gen_global_header_post()

            for sig in self._signature_list:
                sig.generate_post()
            for t in self._celltype_list:
                t.generate_post()
            for n in self._namespace_list:
                n.generate_post()
        except Exception as evar:  # noqa: BLE001
            reraise_if_not_standard_error(evar)
            s.cdl_error(
                "H1002 tecsgen: fatal internal error during post code generation"
            )
            print_exception(evar)

    def gen_global_header(self) -> None:
        from tecsgen.core.c_types import CType
        from tecsgen.core.componentobj.import_c import Import_C
        from tecsgen.core.messages import TECSMsg
        from tecsgen.core.syntaxobj.typedef import Typedef

        ctx = get_context()
        dbg_print(
            f"gen_global_header region={to_s(self._name)} "
            f"$generating_region={to_s(ctx.generating_region.get_name())}\n"
        )
        # global_tecs.h の生成
        f = AppFile.open(f"{ctx.gen}/global_tecsgen.{ctx.h_suffix}")

        if self._name == "::":
            print_note(f)

            # ガードコードを出力
            f.print("#ifndef GLOBAL_TECSGEN_H\n#define GLOBAL_TECSGEN_H\n\n")

            # import_C で指定されたヘッダファイルの #include を出力
            if len(Import_C.get_header_list2()) > 0:
                # ヘッダ include の出力
                f.printf(TECSMsg.get("IMP_comment"), "#_IMP_#")
                for h in Import_C.get_header_list2():
                    f.printf(f'#include "{to_s(h)}"\n')
                f.printf("/**/\n\n")

            ifndef_macro_only(f)

        # typedef, struct, enum を生成
        for d in self._decl_list:
            # d は Typedef, StructType, EnumType のいずれか
            if type(d) is Typedef:
                # Typedef の場合、declarator の @type が　CType でないか
                if not isinstance(d.get_declarator().get_type(), CType):
                    d.gen_gh(f)
            elif not isinstance(d, CType):
                # CType ではない (StructType または EnumType)
                d.gen_gh(f)

        if self._name == "::":
            if ctx.ram_initializer:
                # Proc to judge the necessity of CB initializer
                def b_inline_only_or_proc(ct: Any) -> Any:
                    return ct.need_CB_initializer()

                self.gen_celltype_names(
                    f,
                    "extern void ",
                    "_CB_initialize();\n",
                    True,
                    b_inline_only_or_proc,
                )
                self.gen_celltype_names(
                    f,
                    "extern void ",
                    "_CB_initialize();\n",
                    False,
                    b_inline_only_or_proc,
                )
                f.print("\n#define INITIALIZE_TECS() \\\n")
                self.gen_celltype_names(
                    f, "\t", "_CB_initialize();\\\n", True, b_inline_only_or_proc
                )
                self.gen_celltype_names(
                    f, "\t", "_CB_initialize();\\\n", False, b_inline_only_or_proc
                )
                f.print("/* INITIALIZE_TECS terminator */\n\n")
            else:
                f.print("\n#define INITIALIZE_TECS() \n")
            f.print(
                "#define INITIALZE_TECSGEN() INITIALIZE_TECS()  /* for backward compatibility */\n\n"
            )

            f.print("/* Descriptor for dynamic join */\n")
            f.print(
                "#define Descriptor( signature_global_name )  DynDesc__ ## signature_global_name\n"
            )
            f.print("#define is_descriptor_unjoined( desc )  ((desc).vdes==NULL)\n\n")
            endif_macro_only(f)

        # const を生成  mikan
        for d in self._const_decl_list:
            f.printf(
                "#define %-14s ((%s%s)%s)\n",
                d.get_global_name(),
                d.get_type().get_type_str(),
                d.get_type().get_type_str_post(),
                d.get_initializer().eval_const2(None),
            )

        f.close()

    def gen_global_header_post(self) -> None:
        ctx = get_context()
        # global_tecs.h を開く
        f = AppFile.open(f"{ctx.gen}/global_tecsgen.{ctx.h_suffix}")
        if self._name == "::":
            f.print("\n#endif /* GLOBAL_TECSGEN_H */\n")
        f.close()

    def gen_makefile(self) -> None:
        """Makefile.tecsgen, Makefile.templ の出力。

        全セルタイプ名を出力する部分を出力（本メソッドは root namespace に対して呼出す）。
        個々のセルタイプのメークルールは Celltype クラスで出力。
        """
        self.gen_makefile_template()
        self.gen_makefile_tecsgen()

    def gen_makefile_template(self) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.region import Region
        from tecsgen.core.messages import TECSMsg
        from tecsgen.core.tecsgen import TECSGEN, Makefile

        ctx = get_context()
        gr = ctx.generating_region
        root = Namespace._root_namespace
        dbg_print(
            f"gen_makefile_template: region={to_s(self._name)} "
            f"$generating_region={to_s(gr.get_name())} $gen={ctx.gen}\n"
        )

        if ctx.generate_no_template:
            return

        ### Makefile.templ の生成
        f = AppFile.open(f"{ctx.gen}/Makefile.templ")

        print_Makefile_note(f)

        # Makefile の変数の出力
        f.printf(TECSMsg.get("MVAR_comment"), "#_MVAR_#")
        f.printf("# fixed variable (unchangeable by config or plugin)\n")

        # TARGET の出力 (第一引数 $target に region 名および .exe を付加)
        target = ctx.target
        if gr is not root:
            # 子 region のリンクターゲットの場合
            target += f"-{to_s(gr.get_global_name())}"
        f.print(f"TARGET_BASE = {target}\n")

        if gr is root:
            f.print("BASE_DIR = .\n")
            vpath_lead = ""
        else:
            f.print("BASE_DIR = ..\n")
            vpath_lead = "../"

        f.print(f"GEN_DIR = $(BASE_DIR)/{ctx.gen}\n")

        f.print("INCLUDES =")
        search_path = ctx.import_path + Makefile.get_search_path()
        for path in search_path:
            if TECSGEN.is_absolute_path(path):
                f.print(TECSGEN.subst_tecspath(f" -I {to_s(path)}"))
            else:
                f.print(f" -I $(BASE_DIR)/{to_s(path)}")
        f.print(" -I $(GEN_DIR)\n")
        f.print("DEFINES =")
        for define in ctx.define:
            f.print(f" -D {to_s(define)}")
        f.print("\n\n")
        f.printf("# end of fixed variable (unchangeable by config or plugin)\n")

        vpath_add = ""
        for path in search_path:
            if path != ".":
                if TECSGEN.is_absolute_path(path):
                    vpath_add += " " + TECSGEN.subst_tecspath(path)
                else:
                    vpath_add += " " + vpath_lead + path
        objs_add = ""
        for obj in Makefile.get_objs():
            objs_add += " " + obj
        var_add = ""
        for var in Makefile.get_vars():
            var_add += "#" + Makefile.get_var_comment(var) + "\n"
            var_add += to_s(var) + " =" + " " + to_s(Makefile.get_var_val(var)) + "\n\n"
        # Ruby 版は get_pre_tecsgen_target にブロックを渡しているが、メソッドが yield しないので
        # 常に空になる（そのまま再現する）
        pre_tecsgen_target = ""
        post_tecsgen_target = ""

        c = ctx.c_suffix
        h = ctx.h_suffix
        f.print(
            f"""{var_add}

# Pre-tecsgen target
PRE_TECSGEN_TARGET ={pre_tecsgen_target}

# Post-tecsgen target
POST_TECSGEN_TARGET ={post_tecsgen_target}

# vpath for C sources and headers
vpath %.{c} $(SRC_DIR) $(GEN_DIR) {vpath_add}
vpath %.{h} $(SRC_DIR) $(GEN_DIR) {vpath_add}

# Other objects (out of tecsgen)
OTHER_OBJS ={objs_add}                      # Add objects out of tecs care.
# OTHER_OBJS = $(_TECS_OBJ_DIR)vasyslog.o
"""
        )

        # make ルールの出力
        f.printf(TECSMsg.get("MRUL_comment"), "#_MRUL_#")

        f.print(
            "allall: tecs\n"
            "\tmake all     # in order to include generated Makefile.tecsgen & Makefile.depend\n"
            "\n"
        )

        all_target = "$(TARGET)" if gr.get_n_cells() != 0 else ""

        if gr is root:
            if len(Region.get_link_roots()) > 1:
                all_target += " sub_regions"
            timestamp = " $(TIMESTAMP)"
        else:
            timestamp = ""

        f.print(f"all : {all_target}\n\n")
        f.printf(TECSMsg.get("MDEP_comment"), "#_MDEP_#")
        f.print("-include $(GEN_DIR)/Makefile.tecsgen\n")
        if gr.get_n_cells() != 0:
            # Makefile.depend の include
            f.print("-include $(GEN_DIR)/Makefile.depend\n\n")

            f.print(
                f"$(TARGET) :{timestamp} $(CELLTYPE_COBJS) $(TECSGEN_COBJS) $(PLUGIN_COBJS) $(OTHER_OBJS)\n"
            )
            f.print(
                "\t$(LD) -o $(TARGET) $(TECSGEN_COBJS) $(CELLTYPE_COBJS) $(PLUGIN_COBJS) $(OTHER_OBJS) $(LDFLAGS)\n\n"
            )

        if len(Region.get_link_roots()) > 1 and gr is root:
            f.print("\nsub_regions:$(TIMESTAMP)\n")
            for region in Region.get_link_roots():
                if region.get_global_name() != "":  # Root region: この Makefile 自身
                    f.print(f"\tcd {to_s(region.get_global_name())}; make all\n")
            f.print("\n")

        # clean: ターゲット
        f.print("clean :\n")
        if gr is root:
            for region in Region.get_link_roots():
                if region.get_global_name() != "":  # Root region: この Makefile 自身
                    f.print(f"\tcd {to_s(region.get_global_name())}; make clean\n")
        f.print(
            f"\trm -f $(CELLTYPE_COBJS) $(TECSGEN_COBJS) $(PLUGIN_COBJS) $(OTHER_OBJS) $(TARGET) {timestamp}\n"
        )
        if gr is root:
            f.print("\trm -rf $(GEN_DIR)\n")
        f.print("\n")

        # tecs: ターゲット
        if gr is root:
            f.print(
                "tecs : $(PRE_TECSGEN_TARGET) $(TIMESTAMP) $(POST_TECSGEN_TARGET)\n\n"
            )
            f.print("$(TIMESTAMP) : $(TECS_IMPORTS)\n")
            f.print(f"\t$(TECSGEN) {TECSGEN.subst_tecspath(ctx.arguments, True)}\n\n")
        else:
            f.print("tecs:\n")
            f.print("\t@echo \"run 'make tecs' in root region\"\n\n")

        # tecsflow:, tcflow ターゲット
        if gr.get_n_cells() != 0 or gr is root:
            f.print("#####  TECSFlow targets  #####\n")

        if len(Region.get_link_roots()) > 1 and gr is root:
            tecsflow_target = "tecsflow_sub"
            if gr.get_n_cells() > 0:
                f.print("tecsflow: tecs tecsflow_sub\n")
            else:
                f.print("tecsflow:\n")
            for region in Region.get_link_roots():
                if region.get_n_cells() > 0:
                    f.print(f"\tcd {to_s(region.get_global_name())}; make tecsflow\n")
            f.print("\n")
        else:
            tecsflow_target = "tecsflow"

        if gr.get_n_cells() != 0:
            f.print(f"{tecsflow_target} : $(GEN_DIR)/tecsgen.rbdmp tcflow\n")
            f.print("\ttecsflow -g $(GEN_DIR)\n\n")
            f.print("tecsflow_u : $(GEN_DIR)/tecsgen.rbdmp tcflow\n")
            f.print("\ttecsflow -g $(GEN_DIR) -U\n\n")
            f.print("$(GEN_DIR)/tecsgen.rbdmp : tecs\n\n")
            f.print("tcflow : tecs\n")
            f.print("\tmake tcflow_exec\n\n")
            f.print("tcflow_exec : $(GEN_DIR)/tcflow.rbdmp\n")
            f.print(
                "$(GEN_DIR)/tcflow.rbdmp : $(CELLTYPE_SRCS) $(PLUGIN_CELLTYPE_SRCS)\n"
            )
            f.print(
                "\ttcflow -g $(GEN_DIR) -c '$(CC) -E -DTECSFLOW $(CFLAGS) -I ./' $^\n"
            )
            f.print(
                "\t# add -DTECSGEN if many errors occur, especially in case using cygwin, linux\n"
            )

        if gr.get_n_cells() != 0 or gr is root:
            f.print("#####  end TECSFlow targets  #####\n\n")

        # generic %.o : %.c
        f.print("# generic target for objs\n")
        f.print(f"$(_TECS_OBJ_DIR)%.o : %.{c}\n")
        f.print("\t$(CC) -c $(CFLAGS) -o $@ $<\n\n")

        lines = Makefile.get_lines()
        if len(lines) > 0:
            f.print("# additional lines\n")
            for line in lines:
                f.print(line, "\n")
            f.print("# end additional lines\n\n")

        f.close()

    def gen_makefile_tecsgen(self) -> None:
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.import_c import Import_C
        from tecsgen.core.componentobj.import_cdl import Import
        from tecsgen.core.tecsgen import TECSGEN

        ctx = get_context()
        gr = ctx.generating_region
        c = ctx.c_suffix
        h = ctx.h_suffix
        ### Makefile.tecsgen の生成
        f = AppFile.open(f"{ctx.gen}/Makefile.tecsgen")

        f.print(_MAKEFILE_TECSGEN_HEAD)

        f.print("TECS_IMPORT_CDLS =")
        for imp in Import.get_list().values():
            path = imp.get_cdl_path()
            if TECSGEN.is_absolute_path(path):
                path = TECSGEN.subst_tecspath(path)
            f.print(" ")
            f.print(path)
        f.print("\n")
        f.print("TECS_IMPORT_HEADERS =")
        for path in Import_C.get_header_list().values():
            if TECSGEN.is_absolute_path(path):
                path = TECSGEN.subst_tecspath(path)
            f.print(" ")
            f.print(path)
        f.print("\n")
        f.print("TECS_IMPORTS = $(TECS_IMPORT_CDLS) $(TECS_IMPORT_HEADERS)\n\n")

        f.print("SIGNATURE_HEADERS = \\\n")
        if gr.get_n_cells() != 0:
            for sig in self._signature_list:
                f.print(f"\t$(GEN_DIR)/{to_s(sig.get_global_name())}_tecsgen.{h} \\\n")
        f.print("# SIGNATURE_HEADERS terminator\n\n")

        def always(ct: Any) -> bool:
            return True

        f.print("CELLTYPE_TECSGEN_HEADERS = \\\n")
        self.gen_celltype_names(f, "\t$(GEN_DIR)/", "_tecsgen.h \\\n", True, always)
        self.gen_celltype_names(f, "\t$(GEN_DIR)/", "_tecsgen.h \\\n", False, always)
        f.print("# CELLTYPE_TECSGEN_HEADERS terminator\n\n")
        f.print("CELLTYPE_FACTORY_HEADERS = \\\n")
        self.gen_celltype_names(f, "\t$(GEN_DIR)/", "_factory.h \\\n", True, always)
        self.gen_celltype_names(f, "\t$(GEN_DIR)/", "_factory.h \\\n", False, always)
        f.print("# CELLTYPE_FACTORY_HEADERS terminator\n\n")
        f.print("# TECS_HEADERS:  headers generated by tecsgen\n")
        f.print(
            "TECS_HEADERS = $(SIGNATURE_HEADERS) $(CELLTYPE_TECSGEN_HEADERS) $(CELLTYPE_FACTORY_HEADERS)\n\n"
        )
        f.print("TECS_INLINE_HEADERS = \\\n")
        self.gen_celltype_names(f, "\t", "_tecsgen.h \\\n", False, True)
        f.print("# TECS_INLINE_HEADERS terminator\n\n")
        f.print("PLUGIN_INLINE_HEADERS = \\\n")
        self.gen_celltype_names(f, "\t", "_tecsgen.h \\\n", True, True)
        f.print("# PLUGIN_INLINE_HEADERS terminator\n\n")

        ### set domain variables ###
        domain_type = None
        domain_regions: list[Any] = list(Celltype.get_domain_class_roots_total().keys())
        if ctx.debug:
            dbg_print("domain_regions: ")
            for dr in domain_regions:
                rb_print(dr.get_name(), " ")
            rb_print("\n")

        def has_domain() -> bool:
            # Ruby の [][0] は nil なので、domain_regions が空でも真になる
            return len(domain_regions) > 1 or _get_at(domain_regions, 0) is not gr

        def decide_domain_name(region: Any) -> str:
            if region.is_root():
                return "_Root_" if has_domain() else ""
            if has_domain():
                return f"_{to_s(region.get_namespace_path().get_global_name())}"
            return ""

        f.print(
            "# TECS_COBJS: all objects of TECS, include both user written code and tecsgen automatically generated code\n"
        )
        f.print("TECS_COBJS = $(TECSGEN_COBJS) $(PLUGIN_COBJS) $(CELLTYPE_COBJS)\n\n")

        ### in case domain is used ###
        if has_domain():
            f.print(
                "# TECS_DOMAINS: list of domain names (names of 'domain' spacified region)\n"
            )
            f.print("TECS_DOMAINS = ")
            for r in domain_regions:
                dt = r.get_domain_root().get_domain_type()
                if truthy(dt) and dt.get_option() != "OutOfDomain":
                    f.print(f" {to_s(r.get_namespace_path().get_global_name())}")
            f.print("\n")
            f.print("TECS_CLASS = ")
            for r in domain_regions:
                ct = r.get_class_root().get_class_type()
                if truthy(ct) and ct.get_option() != "OutOfDomain":
                    f.print(f" {to_s(r.get_namespace_path().get_global_name())}")
            f.print("\n\n")

            for label, kind in (
                ("KERNEL", Y.kernel),
                ("USER", Y.user),
                ("OUTOFDOMAIN", Y.OutOfDomain),
            ):
                desc = {
                    "KERNEL": "objects belong to kernel domain",
                    "USER": "objects belong to user domain",
                    "OUTOFDOMAIN": "objects belong to OutOfDomain",
                }[label]
                f.print(f"# TECS_{label}_COBJS: {desc}\n")
                f.print(f"TECS_{label}_COBJS = \\\n")
                for r in domain_regions:
                    dt = r.get_domain_root().get_domain_type()
                    if truthy(dt) and dt.get_kind() == kind:
                        dn = decide_domain_name(r)
                        f.print(f"\t$(TECSGEN{dn}_COBJS) \\\n")
                        f.print(f"\t$(PLUGIN{dn}_COBJS) \\\n")
                        f.print(f"\t$(CELLTYPE{dn}_COBJS) \\\n")
                f.print(f"# TECS_{label}_COBJS terminator\n\n")

            f.print(
                "# TECSGEN_COBJS: objects from sources which are automatically generated by tecsgen\n"
            )
            f.print("TECSGEN_COBJS = \\\n")
            for r in domain_regions:
                f.print(f"\t$(TECSGEN{decide_domain_name(r)}_COBJS) \\\n")
            f.print("# TECSGEN_COBJS terminator\n\n")

            f.print(
                "# PLUGIN_COBJS: objects from sources which are automatically generated by plugin(s)\n"
            )
            f.print("PLUGIN_COBJS = \\\n")
            for r in domain_regions:
                f.print(f"\t$(PLUGIN{decide_domain_name(r)}_COBJS) \\\n")
            f.print("# PLUGIN_COBJS terminator\n\n")

            f.print("CELLTYPE_COBJS = \\\n")
            for r in domain_regions:
                f.print(f"\t$(CELLTYPE{decide_domain_name(r)}_COBJS) \\\n")
            f.print("# CELLTYPE_COBJS terminator\n\n")

            f.print("TECSGEN_SRCS = \\\n")
            for r in domain_regions:
                f.print(f"\t$(TECSGEN{decide_domain_name(r)}_SRCS) \\\n")
            f.print("# TECSGEN_SRCS terminator\n\n")

            f.print("PLUGIN_SRCS = \\\n")
            for r in domain_regions:
                f.print(f"\t$(PLUGIN{decide_domain_name(r)}_SRCS) \\\n")
            f.print("# PLUGIN#_SRCS terminator\n\n")

        ###
        f.print(
            "# TECSGEN_COBJS: objects from sources which are automatically generated by tecsgen\n"
        )
        for r in domain_regions:
            nsp = decide_domain_name(r)
            f.print(f"TECSGEN{nsp}_COBJS = \\\n")
            self.gen_celltype_names_domain(
                f, "\t$(_TECS_OBJ_DIR)", "_tecsgen.o \\\n", domain_type, r, False
            )
            f.print(f"# TECSGEN{nsp}_COBJS terminator\n\n")

        f.print(
            "# PLUGIN_COBJS: objects from sources which are automatically generated by plugin(s)\n"
        )
        for r in domain_regions:
            nsp = decide_domain_name(r)
            f.print(f"PLUGIN{nsp}_COBJS = \\\n")
            self.gen_celltype_names_domain(
                f, "\t$(_TECS_OBJ_DIR)", "_tecsgen.o \\\n", domain_type, r, True
            )
            self.gen_celltype_names_domain2(
                f, "\t$(_TECS_OBJ_DIR)", ".o \\\n", domain_type, r, True, False
            )
            f.print(f"# PLUGIN{nsp}_COBJS terminator\n\n")

        f.print("# CELLTYPE_COBJS: objects of celltype code written by user\n")
        for r in domain_regions:
            nsp = decide_domain_name(r)
            f.print(f"CELLTYPE{nsp}_COBJS = \\\n")
            self.gen_celltype_names_domain2(
                f, "\t$(_TECS_OBJ_DIR)", ".o \\\n", domain_type, r, False, False
            )
            f.print(f"# CELLTYPE{nsp}_COBJS terminator\n\n")

        f.print("# TECSGEN_SRCS: sources automatically generated by tecsgen\n")
        for r in domain_regions:
            nsp = decide_domain_name(r)
            f.print(f"TECSGEN{nsp}_SRCS = \\\n")
            self.gen_celltype_names_domain(
                f, "\t$(GEN_DIR)/", f"_tecsgen.{c} \\\n", domain_type, r, False
            )
            f.print(f"# TECSGEN{nsp}_SRCS terminator\n\n")

        f.print("# PLUGIN_SRCS: sources automatically generated by plugin\n")
        f.print("PLUGIN_CELLTYPE_SRCS = \\\n")
        for r in domain_regions:
            f.print(f"  $(PLUGIN{decide_domain_name(r)}_CELLTYPE_SRCS)\\\n")
        f.print("# PLUGIN_CELLTYPE_SRCS terminator\n\n")
        f.print("PLUGIN_TECSGEN_SRCS = \\\n")
        for r in domain_regions:
            f.print(f"  $(PLUGIN{decide_domain_name(r)}_TECSGEN_SRCS)\\\n")
        f.print("# PLUGIN_TECSGEN_SRCS terminator\n\n")
        for r in domain_regions:
            nsp = decide_domain_name(r)
            f.print(
                f"PLUGIN{nsp}_SRCS = $(PLUGIN{nsp}_CELLTYPE_SRCS) $(PLUGIN{nsp}_TECSGEN_SRCS)\n\n"
            )
            f.print(f"PLUGIN{nsp}_CELLTYPE_SRCS = \\\n")
            self.gen_celltype_names_domain2(
                f, "", f".{c} \\\n", domain_type, r, True, False
            )
            f.print(f"# PLUGIN{nsp}_CELLTYPE_SRCS terminator\n\n")
            f.print(f"PLUGIN{nsp}_TECSGEN_SRCS = \\\n")
            self.gen_celltype_names_domain(
                f, "", f"_tecsgen.{c} \\\n", domain_type, r, True
            )
            f.print(f"# PLUGIN{nsp}_TECSGEN_SRCS terminator\n\n")

        f.print("# CELLTYPE_SRCS: sources of celltype code written by user\n")
        f.print("CELLTYPE_SRCS = \\\n")
        self.gen_celltype_names(f, "\t", f".{c} \\\n", False, False)
        f.print("# CELLTYPE_SRCS terminator\n\n")
        f.close()

    def gen_celltype_names(
        self,
        f: Any,
        prepend: str,
        append: str,
        b_plugin: bool,
        b_inline_only_or_proc: Any = True,
    ) -> None:
        """すべてのセルタイプの名前を出力。

        b_inline_only_or_proc:: bool|Proc: true ならば inline の entry port のみ、かつインアクティブな
        セルタイプを含める。Proc（Python では呼び出し可能なもの）ならば、実行した結果 true ならば含める。
        """
        dbg_print(f"gen_celltype_names {to_s(self._name)}\n")

        for ct in self._celltype_list:
            if not ct.need_generate():
                continue
            if (
                b_inline_only_or_proc is False
                and ct.is_all_entry_inline()
                and not truthy(ct.is_active())
            ):
                continue
            if callable(b_inline_only_or_proc) and (b_inline_only_or_proc(ct) is False):
                continue
            if (b_plugin and truthy(ct.get_plugin())) or (
                not b_plugin and not truthy(ct.get_plugin())
            ):
                f.print(f" {prepend}{to_s(ct.get_global_name())}{append}")
        for ns in self._namespace_list:
            ns.gen_celltype_names(f, prepend, append, b_plugin, b_inline_only_or_proc)

    def get_up_global_name(self) -> str:
        """underscore prepended global name"""
        s: Any = self
        if s.is_root():
            return ""
        return f"_{to_s(s.get_global_name())}"

    def gen_celltype_names_domain(
        self,
        f: Any,
        prepend: str,
        append: str,
        domain_type: Any,
        region: Any,
        b_plugin: bool,
        b_inline_only: bool = True,
    ) -> None:
        """すべてのセルタイプの名前を出力（region を domain_roots に含む場合など）。"""
        ctx = get_context()
        dbg_print(f"gen_celltype_names namespace={to_s(self._name)}\n")

        for ct in self._celltype_list:
            if not ct.need_generate():
                continue
            if (
                b_inline_only is False
                and ct.is_all_entry_inline()
                and not truthy(ct.is_active())
            ):
                continue
            if (b_plugin and truthy(ct.get_plugin())) or (
                not b_plugin and not truthy(ct.get_plugin())
            ):
                regions = list(ct.get_domain_class_roots2().keys())
                if ctx.debug:
                    dbg_print(
                        f"gen_celltype_names_domain: region={to_s(region.get_name())} "
                        f"domain_root={to_s(region.get_domain_root().get_name())} "
                        f"domain_type={to_s(domain_type)}\n"
                    )
                    dbg_print("gen_celltype_names_domain:\n")
                    for r in regions:
                        dbg_print(
                            f"    ct={to_s(ct.get_name())} region={to_s(r.get_name())} "
                            f"domain_root={to_s(r.get_domain_root().get_name())}, "
                        )
                    dbg_print("\n")

                rdr = region  # rdr = domain or class root, sub region
                if any(r is rdr for r in regions):
                    if rdr.is_root():
                        nsp = ""
                    else:
                        nsp = f"_{to_s(region.get_namespace_path().get_global_name())}"
                    f.print(f" {prepend}{to_s(ct.get_global_name())}{nsp}{append}")
                elif rdr.is_link_root():
                    # the case of domain_roots >= 2 && no cell in root region
                    if len(regions) > 1:
                        f.print(
                            f" {prepend}{to_s(ct.get_global_name())}{rdr.get_up_global_name()}{append}"
                        )
        for ns in self._namespace_list:
            ns.gen_celltype_names_domain(
                f, prepend, append, domain_type, region, b_plugin, b_inline_only
            )

    def gen_celltype_names_domain2(
        self,
        f: Any,
        prepend: str,
        append: str,
        domain_type: Any,
        region: Any,
        b_plugin: bool,
        b_inline_only: bool = True,
    ) -> None:
        """すべてのセルタイプの名前を出力（セルタイプコードのための名前出力）。"""
        dbg_print(f"gen_celltype_names {to_s(self._name)}\n")

        for ct in self._celltype_list:
            if not ct.need_generate():
                continue
            if (
                b_inline_only is False
                and ct.is_all_entry_inline()
                and not truthy(ct.is_active())
            ):
                continue
            if (b_plugin and truthy(ct.get_plugin())) or (
                not b_plugin and not truthy(ct.get_plugin())
            ):
                regions = ct.get_domain_class_roots2()
                rdr = region
                if rdr in regions and len(regions) == 1:
                    f.print(f" {prepend}{to_s(ct.get_global_name())}{append}")
                elif rdr.is_link_root() and len(regions) > 1:
                    # the case of domain_roots >= 2 && no cell in root region
                    f.print(
                        f" {prepend}{to_s(ct.get_global_name())}{rdr.get_up_global_name()}{append}"
                    )
        for ns in self._namespace_list:
            ns.gen_celltype_names_domain2(
                f, prepend, append, domain_type, region, b_plugin, b_inline_only
            )

    def travers_all_signature(self, proc: Any) -> None:
        """すべてのシグニチャをたどる（Ruby のブロック引数を関数で渡す）。"""
        for sig in self._signature_list:
            proc(sig)
        for ns in self._namespace_list:
            ns.travers_all_signature_proc(proc)

    def travers_all_signature_proc(self, proc: Any) -> None:
        for sig in self._signature_list:
            proc(sig)
        for ns in self._namespace_list:
            ns.travers_all_signature_proc(proc)

    def travers_all_celltype(self, proc: Any) -> None:
        """すべてのセルタイプをたどる。"""
        for ct in self._celltype_list:
            proc(ct)
        for ns in self._namespace_list:
            ns.travers_all_celltype_proc(proc)

    def travers_all_celltype_proc(self, proc: Any) -> None:
        for ct in self._celltype_list:
            proc(ct)
        for ns in self._namespace_list:
            ns.travers_all_celltype_proc(proc)


_MAKEFILE_TECSGEN_HEAD = """\
# generated automatically by tecsgen.
# This file is not intended to modify.
#
# Makefile variables below are defined.
#  TECS_IMPORT_CDLS          .cdl files improted by import statement
#  SIGNATURE_HEADERS         .h files of signature
#  CELLTYPE_TECSGEN_HEADERS  .h files of celltype
#  CELLTYPE_FACTORY_HEADERS  .h files of celltype's factory
#  TECS_HEADERS              summary of .h files above
#  TECS_INLINE_HEADERS       .h files of celltype inline header
#  PLUGIN_INLINE_HEADERS     .h files of plugin generated inline header
#
#  TECS_COBJS                .o files of TECS
#                            = $(TECSGEN_COBJS)+$(PLUGIN_COBJS)+$(CELLTYPE_COBJS)
#                            = $(TECS_KERNEL_COBJS)+$(TECS_USER_COBJS)+$(TECS_OUTOFDOMAIN_COBJS)
#                            = $(TECSGEN_domain_COBJS)+$(PLUGIN_domain_COBJS)+$(CELLTYPE_domain_COBJS) for each domain
#
#  TECSGEN_COBJS             .o files of celltype_tecsgen.c
#  CELLTYPE_COBJS            .o files of celltype.c (celltype code)
#  PLUGIN_COBJS              .o files of plugin generated .c files
#
#  TECSGEN_SRCS              .c files of celltype_tecsgen.c
#  CELLTYPE_SRCS             .c files of celltype.c (celltype code)
#  PLUGIN_SRCS               .c files of plugin generated
#  PLUGIN_CELLTYPE_SRCS      .c files of plugin generated celltype.c (celltype code)
#  PLUGIN_TECSGEN_SRCS       .c files of plugin generated celltype_tecsgen.c
#
# Variables for domain (These are defined if domain is specified)
#  TECS_DOMAINS             domain names
#  TECS_KERNEL_COBJS        .o files of kernel domain (tecsgen, celltype, plugin)
#  TECS_USER_COBJS          .o files of user domain (tecsgen, celltype, plugin)
#  TECS_OUTOFDOMAIN_COBJS   .o files of OutOfDomain (tecsgen, celltype, plugin)
#  TECSGEN_domain_COBJS     .o files of celltype_tecsgen.c files for each domain
#  PLUGIN_domain_COBJS      .o files of plugin generated .c files for each domain
#  CELLTYPE_domain_COBJS    .o files of celltype.c files for each domain
#  TECSGEN_domain_SRCS      .c files of celltype_domain_tecsgen.c
#  PLUGIN_domain_SRCS       .c files of plugin generated .c files for each domain
#  CELLTYPE_domain_SRCS     .c files of celltype.c files for each domain

"""


class TypedefGenerate:
    """generate.rb の Typedef 再オープン部分。"""

    _declarator: Any

    def gen_gh(self, f: Any) -> None:
        f.printf(
            "typedef %-14s %s%s;\n",
            to_s(self._declarator.get_type().get_type_str()),
            to_s(self._declarator.get_name()),
            to_s(self._declarator.get_type().get_type_str_post()),
        )


class StructTypeGenerate:
    """generate.rb の StructType 再オープン部分。"""

    _b_define: Any
    _tag: Any
    _members_decl: Any

    def gen_gh(self, f: Any) -> None:
        if not truthy(self._b_define):
            return

        f.print(f"struct {to_s(self._tag)} {{\n")
        for i in self._members_decl.get_items():
            f.printf(
                "                %-14s %s%s;\n",
                to_s(i.get_type().get_type_str()),
                to_s(i.get_name()),
                to_s(i.get_type().get_type_str_post()),
            )
        f.print("};\n")


class SignatureGenerate:
    """generate.rb の Signature 再オープン部分。"""

    _name: Any
    _global_name: Any
    _singleton: Any

    def generate(self) -> None:
        self.generate_signature_header()

    def generate_post(self) -> None:
        self.generate_signature_header_post()

    def generate_signature_header(self) -> None:
        ctx = get_context()
        dbg_print(
            f"generate_signature_header signature={to_s(self._name)} "
            f"$generating_region={to_s(ctx.generating_region.get_name())}\n"
        )
        f = AppFile.open(f"{ctx.gen}/{to_s(self._global_name)}_tecsgen.{ctx.h_suffix}")

        print_note(f)
        self.gen_sh_guard(f)
        self.gen_sh_info(f)
        self.gen_sh_include(f)

        ifndef_macro_only(f)
        self.gen_sh_func_tab(f)
        endif_macro_only(f)
        self.gen_sh_func_id(f)

        f.close()

    def generate_signature_header_post(self) -> None:
        ctx = get_context()
        f = AppFile.open(f"{ctx.gen}/{to_s(self._global_name)}_tecsgen.{ctx.h_suffix}")
        self.gen_sh_endif(f)
        f.close()

    def gen_sh_guard(self, f: Any) -> None:
        gn = to_s(self._global_name)
        f.print(f"#ifndef {gn}_TECSGEN_H\n")
        f.print(f"#define {gn}_TECSGEN_H\n\n")

    def gen_sh_info(self, f: Any) -> None:
        s: Any = self
        f.print(
            f"""/*
 * signature   :  {to_s(self._name)}
 * global name :  {to_s(self._global_name)}
 * context     :  {to_s(s.get_context())}
 */

"""
        )

    def gen_sh_include(self, f: Any) -> None:
        from tecsgen.core.messages import TECSMsg

        s: Any = self
        dl = s.get_descriptor_list()
        if len(dl) > 0:
            f.printf(TECSMsg.get("SDI_comment"), "#_SDI_#")
            for dt in dl:
                gn = to_s(dt.get_global_name())
                f.print(
                    f"""/* pre-typedef incomplete-type to avoid error in case of mutual or cyclic reference */
#ifndef Descriptor_of_{gn}_Defined
#define  Descriptor_of_{gn}_Defined
typedef struct {{ struct tag_{gn}_VDES *vdes; }} Descriptor( {gn} );
#endif
"""
                )
            f.print("\n")

    def gen_sh_func_tab(self, f: Any) -> None:
        from tecsgen.core.messages import TECSMsg

        s: Any = self
        gn = to_s(self._global_name)
        # シグニチャディスクリプタの出力
        f.printf(TECSMsg.get("SD_comment"), "#_SD_#")
        f.print(f"struct tag_{gn}_VDES {{\n")
        f.print(f"    struct tag_{gn}_VMT *VMT;\n")
        f.print("};\n\n")

        # シグニチャ関数テーブルの出力
        f.printf(TECSMsg.get("SFT_comment"), "#_SFT_#")
        f.print(f"struct tag_{gn}_VMT {{\n")
        for fun in s.get_function_head_array():
            f.print("    ")
            functype = fun.get_declarator().get_type()
            f.printf("%-14s", functype.get_type_str())

            f.print(f" (*{to_s(fun.get_name())}__T)(")
            if not truthy(self._singleton):
                f.print(f" const struct tag_{gn}_VDES *edp")

            if truthy(functype.get_paramlist()):
                items = functype.get_paramlist().get_items()
            else:
                # ここで nil になるのは、引数なしの時に void がなかった場合
                items = []

            for param in items:
                f.print(", ")
                f.print(param.get_type().get_type_str())
                f.print(" ")
                f.print(param.get_name())
                f.print(param.get_type().get_type_str_post())
            f.print(" );\n")
        if len(s.get_function_head_array()) == 0:
            f.print("    void   (*dummy__)(void);\n")

        f.print("};\n\n")
        f.printf(TECSMsg.get("SDES_comment"), "#_SDES_#")
        f.print(
            f"""#ifndef Descriptor_of_{gn}_Defined
#define  Descriptor_of_{gn}_Defined
typedef struct {{ struct tag_{gn}_VDES *vdes; }} Descriptor( {gn} );
#endif
"""
        )

    def gen_sh_func_id(self, f: Any) -> None:
        """関数の ID の define を出力。"""
        s: Any = self
        f.print("/* function id */\n")
        for fun in s.get_function_head_array():
            f.printf(
                "#define\tFUNCID_%-31s (%d)\n",
                f"{to_s(self._global_name)}_{to_s(fun.get_name())}".upper(),
                s.get_id_from_func_name(fun.get_name()),
            )
        f.print("\n")

    def gen_sh_endif(self, f: Any) -> None:
        f.print(f"#endif /* {to_s(self._global_name)}_TECSGEN_H */\n")


class RegionGenerate:
    """generate.rb の Region 再オープン部分。"""

    _family_line: list[Any]

    def gen_region_str_pre(self, f: Any) -> int:
        nest = 1
        while nest < len(self._family_line):
            f.print("  " * (nest - 1))
            f.print(f"region {to_s(self._family_line[nest].get_name())}{{\n")
            nest += 1
        return nest - 1

    def gen_region_str_post(self, f: Any) -> int:
        nest = len(self._family_line) - 1
        while nest >= 1:
            f.print("  " * (nest - 1))
            f.print("};\n")
            nest -= 1
        return nest - 1


class DomainTypeGenerate:
    _plugin: Any

    def gen_factory(self, node_root: Any) -> None:
        self._plugin.gen_factory(node_root)


class ClassTypeGenerate:
    _plugin: Any

    def gen_factory(self, node_root: Any) -> None:
        self._plugin.gen_factory(node_root)


def reraise_if_not_standard_error(evar: BaseException) -> None:
    """Ruby の `rescue => evar`（StandardError）で捕まえない例外なら、そのまま投げ直す。

    `exit`（SystemExit）・スタックあふれ（SystemStackError）に当たるものと、未移植の部分
    （NotImplementedError。Ruby でも ScriptError で StandardError ではない）。
    """
    from tecsgen.cli import TecsgenExit

    if isinstance(evar, (TecsgenExit, RecursionError, NotImplementedError)):
        raise evar
