"""core/tecsgen.rb と tecsgen.rb（トップ）の `TECSGEN` クラスの移植（内部仕様3章）。

Ruby 版の `TECSGEN` は2つのファイルにまたがる。

- tecsgen.rb（トップ）: `initialize`・`run1`・`run2`・`init`（オプション解析などは
  `tecsgen.cli` へ移した）
- core/tecsgen.rb: import パスの操作、`Makefile`、構文解析・意味解析・生成の各段階

P3 で構文解析と意味解析（`run1`）、P4 で最適化・コード生成（`run2`・`finalize`）と
`dump_tecsgen_rbdmp`（ファイルは書かない）を移植した。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.ruby_compat import Y, gsub, rb_print, sub_first, sym, to_s, truthy


class TECSGEN:
    # ポストコード生成開始後 true
    _b_post_coded: ClassVar[bool] = False
    _current_tecsgen: ClassVar[TECSGEN | None] = None

    @classmethod
    def reset(cls) -> None:
        """クラス変数を初期状態に戻す（Ruby 版には無い。1プロセスで複数回実行するテスト用）。"""
        cls._b_post_coded = False
        cls._current_tecsgen = None
        Makefile.reset()
        CMake.reset()

    # --- tecsgen.rb（トップ） --------------------------------------------------

    def __init__(self) -> None:
        self._cell_list: Any = None
        self._cell_list2: Any = None
        self._celltype_list: Any = None
        self._root_namespace: Any = None
        # obsolete（TOOL_INFO に置き換わった）
        self._cell_location_list: list[Any] = []
        self._join_location_list: list[Any] = []

    def run1(self) -> None:
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype

        TECSGEN._current_tecsgen = self

        self.syntax_analisys(get_context().argv)
        self.semantics_analisys_1()
        self.semantics_analisys_2()

        self._celltype_list = Celltype.get_celltype_list()
        self._cell_list = Cell.get_cell_list()
        self._cell_list2 = Cell.get_cell_list2()

        TECSGEN._current_tecsgen = None

    def run2(self) -> None:
        """最適化とコード生成。"""
        TECSGEN._current_tecsgen = self

        self.optimize_and_generate()
        self.finalize()

        TECSGEN._current_tecsgen = None

    def get_celltype_list(self) -> Any:
        return self._celltype_list

    def get_cell_list(self) -> Any:
        return self._cell_list

    def get_root_namespace(self) -> Any:
        return self._root_namespace

    # --- core/tecsgen.rb ---------------------------------------------------

    @staticmethod
    def add_import_path(path: str) -> None:
        """import パス (-I) を末尾に追加する。既に登録済みであれば、追加しない。"""
        ctx = get_context()
        if path not in ctx.import_path:
            dbg_print(f"add_import_path: '{path}'\n")
            ctx.import_path.append(path)

    @staticmethod
    def adjust_exerb_path() -> None:
        """EXERB 版のパスの調整。Python 版は exerb で動かないので何もしない。"""
        return

    @staticmethod
    def subst_tecspath(path: str, b_global: bool = False) -> str:
        """path のうち $tecspath に一致する部分を "$(TECSPATH)" に置換する。

        Ruby 版は $tecspath をそのまま正規表現にしている（`\\` だけを二重にする）ので、
        `.` などのメタ文字は正規表現として解釈される。それも再現する。
        """
        tp = get_context().tecspath.replace("\\", "\\\\")
        pattern = re.compile(tp)
        substr = "$(TECSPATH)"
        if b_global:
            s = gsub(pattern, substr, path)
        else:
            s = sub_first(pattern, substr, path)
        dbg_print(f"subst_tecspath {path}, {s}\n")
        return s

    @staticmethod
    def is_absolute_path(path: str) -> bool:  # Ruby: is_absolute_path?
        """'/' または '$' で始まる場合、絶対パスと判定する。

        '/' で始まるかは Host に問い合わせる（記録を再生する差分テストでは、絶対パスの先頭が
        `@WORK@` などに置き換わっているため）。
        """
        from tecsgen.host import get_host

        pa = path[0:1]
        pa2 = path[0:2]
        res = (
            get_host().isabs(path)
            or pa == "$"
            or re.search(r"[A-Za-z]:", pa2) is not None
        )
        dbg_print(
            f"is_absolute( {path} ) = {'true' if res else 'false'}  {path[0:1]}\n"
        )
        return res

    @staticmethod
    def set_default_config() -> None:
        """tecsgen のデフォルトを設定する。"""
        Makefile.set_default_config()
        CMake.set_default_config()

    @staticmethod
    def get_argv() -> list[str]:
        return get_context().argv

    @classmethod
    def is_post_coded(cls) -> bool:  # Ruby: post_coded?
        return cls._b_post_coded

    # ------ TECSGEN CDL analyze and generate ------

    def syntax_analisys(self, argv: list[str]) -> None:
        from tecsgen.core.componentobj.import_cdl import Import
        from tecsgen.core.componentobj.region import Region
        from tecsgen.core.generator import Generator

        # ルート namespace (region) を生成
        self._root_namespace = Region("::")

        ####  構文解析 (post コードを除く) ####
        # すべての cdl を import する
        for f in argv:
            dbg_print(f"## Import: {f}\n")
            Import(f, False, False)

        # すべての構文解釈が完了したことの報告
        #   実際には、後からプラグインの生成する CDL のパースが行われる
        #   エラー行数の決定方法の変更のために行う
        Generator.end_all_parse()
        dbg_print("## End all parse (except Post Code)\n")

    def semantics_analisys_1(self) -> None:
        """意味解析1。セルだけを検査する（他のものは構文解析中に検査されている）。"""
        from tecsgen.core.cdl_types import DescriptorType
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.signature import Signature
        from tecsgen.core.plugin_module import PluginModule

        ####  意味解析１ (post コードを除く) ####
        dbg_print("## Creating reverse join \n")
        Cell.create_reverse_join()

        DescriptorType.check_signature()
        Signature.set_descriptor_list()
        Celltype.check_dynamic_join()

        # set_definition_join は2回呼び出される（1回目）
        dbg_print("## Checking all join\n")
        self._root_namespace.set_definition_join()

        ####  post コードの生成と構文解析 ####
        TECSGEN._b_post_coded = True  # ポストコード生成開始後 true
        # 引数がなければ、プラグインのポストコードを出力しない
        if len(get_context().argv) > 0:
            dbg_print("## Generating Post Code\n")
            # プラグインのポストコードの出力と import
            PluginModule.gen_plugin_post_code()

        ####  意味解析１ (post コード) ####
        dbg_print("## Creating reverse join (for post code) \n")
        Cell.create_reverse_join()

        # set_definition_join は2回呼び出される（2回目）  post_code で生成された
        dbg_print("## Checking all join (for cells generated by Post Code\n")
        self._root_namespace.set_definition_join()
        self._root_namespace.set_max_entry_port_inner_cell()

        dbg_print("## Set require join\n")
        self._root_namespace.set_require_join()

    def semantics_analisys_2(self) -> None:
        from tecsgen.core.componentobj.cell import Cell

        ####  意味解析２ ####
        Cell.make_cell_list2()
        dbg_print("## Set fixed join\n")
        Cell.create_reverse_require_join()
        dbg_print("## Setting port reference count\n")
        self._root_namespace.set_port_reference_count()

        dbg_print("## Checking all join\n")
        self._root_namespace.check_join()

        dbg_print("## Checking referenced but undefined cell\n")
        self._root_namespace.check_ref_but_undef()

    def optimize_and_generate(self) -> None:
        from tecsgen.cli import TecsgenExit
        from tecsgen.core.componentobj.region import Region
        from tecsgen.core.generator import Generator, print_report
        from tecsgen.host import get_host

        ctx = get_context()
        host = get_host()
        #### Region link root ごとにオプティマイズおよび生成 ####
        for region in list(Region.get_link_roots()):
            n_cells = region.get_n_cells()
            path_str = region.get_namespace_path().get_path_str()

            dbg_print(f"{to_s(region.get_name())} has {n_cells} cells\n")
            if ctx.verbose:
                rb_print("=====================================\n")
                rb_print(f"=== Region.path_str: {to_s(path_str)}\n")
                rb_print("=====================================\n")
            else:
                dbg_print(f"Region.path_str: {to_s(path_str)}\n")

            if len(ctx.region_list) > 0:
                if truthy(ctx.region_list.get(path_str)):
                    ctx.region_list[path_str] = False
                else:
                    continue

            # セルが一つもなければ生成しない
            if region.get_n_cells() == 0:
                if len(ctx.region_list) > 0:
                    Generator.warning(
                        "W9999 $1: specified to generate but has no cell",
                        region.get_name(),
                    )
                if region is not self._root_namespace:
                    continue

            ctx.generating_region = region
            if len(Region.get_link_roots()) > 1:
                if region.get_name() == "::":
                    ctx.gen = ctx.gen_base
                else:
                    ctx.gen = ctx.gen_base + "/" + to_s(region.get_global_name())
                    try:
                        if not host.is_directory(ctx.gen):
                            host.mkdir(ctx.gen)
                    except Exception:  # noqa: BLE001  Ruby の rescue
                        rb_print(f"Cannot mkdir {ctx.gen}\n")
                        raise TecsgenExit(1) from None
            else:
                ctx.gen = ctx.gen_base

            dbg_print("## Unset optimize variables\n")
            self._root_namespace.reset_optimize()  # 最適化をリセットする

            if Generator.get_n_error() == 0:
                # エラーが発生していたら、設定しない
                dbg_print("## Set cell id\n")
                # セルの ID とドメイン情報を設定（linkunit 毎に0からつける）
                self._root_namespace.set_cell_id_and_domain()

                # エラーが発生していたら、最適化は実施しない
                if not ctx.unopt:
                    dbg_print(
                        f"## Optimizing: Link Region={to_s(self._root_namespace.get_name())}\n"
                    )
                    self._root_namespace.optimize()

            if ctx.show_tree:
                # エラーが発生していても表示（エラー発生時は最適化されていないので注意）
                rb_print(
                    f"##### show_tree LinkRegion={to_s(region.get_name())} #####\n"
                )
                self._root_namespace.show_tree(0)
                rb_print(
                    f"##### END       LinkRegion={to_s(region.get_name())} #####\n\n"
                )

            # 構文解釈、意味解析でエラー発生していたら、コード生成をしない
            if Generator.get_n_error() != 0:
                print_report()
                raise TecsgenExit(1)

            #### コード生成 ####
            try:
                dbg_print(
                    f"## Generating: Link Region={to_s(self._root_namespace.get_name())}\n"
                )
                self._root_namespace.generate()
                dbg_print(
                    f"## Generating Post: Link Region={to_s(self._root_namespace.get_name())}\n"
                )
                self._root_namespace.generate_post()
            except (TecsgenExit, RecursionError, NotImplementedError):
                raise
            except Exception:  # noqa: BLE001  Ruby の rescue（StandardError）
                # 通常ここへは来ない (generate, generate_post で処置される)
                Generator.error("G9999 fail to generate")

    def finalize(self) -> None:
        from tecsgen.cli import TecsgenExit, _stderr
        from tecsgen.context import print_exception
        from tecsgen.core.generate import AppFile
        from tecsgen.core.generator import Generator, print_report
        from tecsgen.host import get_host

        ctx = get_context()
        dbg_print("## Generating XML\n")

        for region_path_str, val in ctx.region_list.items():
            if val is True:
                Generator.warning(
                    "W9999 $1: not link root, -G ignored", region_path_str
                )

        # update する
        # APPFile で生成されたファイルは、もし変化があれば、ここで更新する
        # コード生成段階でエラーが発生すれば、更新しない
        # CFile で生成されたものは、更新されている
        if Generator.get_n_error() == 0:
            try:
                AppFile.update()
            except Exception as evar:  # noqa: BLE001  Ruby の rescue => evar
                Generator.error(
                    "G9999 Fail to update. (error occurred while renaming generated files)"
                )
                print_exception(evar)

        print_report()
        if Generator.get_n_error() != 0:
            _stderr(
                f"error occurred while generating. some file can be corrupt in {ctx.gen_base}\n"
            )
            raise TecsgenExit(1)

        get_host().open_write(f"{ctx.gen_base}/tecsgen.timestamp").close()

    def dump_tecsgen_rbdmp(self) -> None:
        """tecsgen.rbdmp（Ruby の Marshal 形式のモデル）の出力。

        ファイルそのものは再現しない（P0 基本方針決定）。ただし Ruby 版はダンプの前に link root
        ごとに最適化をやり直し、-v ではその経過を標準出力に出すので、そこまでは移植する。
        unjoin_plugin（プラグインの参照を外す。unjoin_plugin.rb）は P5 で移植する。
        """
        from tecsgen.core.componentobj.region import Region

        ctx = get_context()
        dbg_print("dump_tecsgen_rbdmp 0:\n")
        #### unjoin_plugin 後に行う必要があるため、コード生成後にダンプを行う
        #### Region link root ごとにオプティマイズしてダンプ ####
        for region in list(Region.get_link_roots()):
            path_str = region.get_namespace_path().get_path_str()
            dbg_print(f"dump_tecsgen_rbdmp 1: Region.path_str: {to_s(path_str)}\n")

            if len(ctx.region_list) > 0:
                if ctx.region_list.get(path_str) is False:
                    ctx.region_list[path_str] = True
                else:
                    continue

            dbg_print(f"dump_tecsgen_rbdmp 2: Region.path_str: {to_s(path_str)}\n")
            # セルが一つもなければ生成しない
            if region.get_n_cells() == 0 and region is not self._root_namespace:
                continue

            dbg_print(f"dump_tecsgen_rbdmp 3: Region.path_str: {to_s(path_str)}\n")
            ctx.generating_region = region
            if len(Region.get_link_roots()) > 1:
                if region.get_name() == "::":
                    ctx.gen = ctx.gen_base
                else:
                    ctx.gen = ctx.gen_base + "/" + to_s(region.get_global_name())
            else:
                ctx.gen = ctx.gen_base

            dbg_print(f"dump_tecsgen_rbdmp 4: Region.path_str: {to_s(path_str)}\n")
            dbg_print("## Unset optimize variables\n")
            self._root_namespace.reset_optimize()  # 最適化をリセットする

            dbg_print("## Set cell id\n")
            # セルの ID とドメイン情報を設定（linkunit 毎に0からつける）
            self._root_namespace.set_cell_id_and_domain()

            if not ctx.unopt:
                dbg_print(
                    f"## Optimizing: Link Region={to_s(self._root_namespace.get_name())}\n"
                )
                self._root_namespace.optimize()
            dbg_print(f"dump_tecsgen_rbdmp final: Region.path_str: {to_s(path_str)}\n")
            # ここで Ruby 版は "#{$gen}/tecsgen.rbdmp" に Marshal.dump(Namespace.get_root) を書く


class Makefile:
    """Makefile.templ の出力内容を追加、変更するための操作（TECSGEN::Makefile）。"""

    RUBY_NAME = "TECSGEN::Makefile"

    # 固定されている変数(add_var で変更できない)
    _fixed_vars: ClassVar[dict[str, Any]] = {}
    _config_mode: ClassVar[bool] = False
    _vars: ClassVar[dict[str, Any]] = {}
    _vars_default: ClassVar[dict[str, Any]] = {}
    _var_comments: ClassVar[dict[str, Any]] = {}
    _objs: ClassVar[list[Any]] = []
    _ldflags: ClassVar[str] = ""
    _search_path: ClassVar[list[Any]] = []
    _pre_tecsgen_target: ClassVar[list[Any]] = []
    _post_tecsgen_target: ClassVar[list[Any]] = []
    _lines: ClassVar[list[str]] = []

    @classmethod
    def reset(cls) -> None:
        cls._fixed_vars = {
            Y.INCLUDES: None,
            Y.DEFINES: None,
            Y.TARGET_BASE: None,
            Y.BASE_DIR: None,
        }
        cls._config_mode = False
        cls._vars = {}
        cls._vars_default = {}
        cls._var_comments = {}
        cls._objs = []
        cls._ldflags = ""
        cls._search_path = []
        cls._pre_tecsgen_target = []
        cls._post_tecsgen_target = []
        cls._lines = []

    @classmethod
    def add_obj(cls, obj: Any) -> None:
        """OTHER_OBJS に追加する。"""
        cls._objs.append(obj)

    @classmethod
    def add_var(cls, var: str, val: Any, comment: Any = None) -> None:
        """追加する変数。プラグインからは、デフォルト値を変更できる。"""
        if cls._fixed_vars.get(var) is not None:
            raise RuntimeError(f"fixed var '{var}' cannot be changed")
        if cls._config_mode:
            # Ruby 版は未定義の @@var_comments_default を参照して例外になる（そのまま再現する）
            cls._vars_default[sym(var)] = val
            raise NameError(
                "uninitialized class variable @@var_comments_default in TECSGEN::Makefile"
            )
        cls._vars[sym(var)] = val
        cls._var_comments[sym(var)] = comment

    @classmethod
    def add_ldflag(cls, ldflag: str) -> None:
        cls._ldflags += " " + ldflag

    @classmethod
    def add_search_path(cls, path: Any) -> None:
        cls._search_path.append(path)

    @classmethod
    def add_pre_tecsgen_target(cls, target: Any) -> None:
        # Ruby 版は未定義のローカル変数 pre_tecsgen_target を参照して例外になる（そのまま再現する）
        raise NameError(
            "undefined local variable or method `pre_tecsgen_target' for TECSGEN::Makefile:Module"
        )

    @classmethod
    def add_post_tecsgen_target(cls, target: Any) -> None:
        raise NameError(
            "undefined local variable or method `pre_tecsgen_target' for TECSGEN::Makefile:Module"
        )

    @classmethod
    def add_line(cls, line: Any) -> None:
        from tecsgen.ruby_compat import to_s

        cls._lines.append(to_s(line) + "\n")

    @classmethod
    def get_objs(cls) -> list[Any]:
        return _uniq(cls._objs)

    @classmethod
    def get_vars(cls) -> list[str]:
        return sorted(set(list(cls._vars) + list(cls._vars_default)))

    @classmethod
    def get_var_val(cls, var: str) -> Any:
        v = cls._vars.get(var)
        return v if v is not None and v is not False else cls._vars_default.get(var)

    @classmethod
    def get_var_comment(cls, var: str) -> Any:
        return cls._var_comments.get(var)

    @classmethod
    def get_ldflags(cls) -> str:
        return cls._ldflags

    @classmethod
    def get_search_path(cls) -> list[Any]:
        return _uniq(cls._search_path)

    @classmethod
    def get_pre_tecsgen_target(cls) -> list[Any]:
        return _uniq(cls._pre_tecsgen_target)

    @classmethod
    def get_post_tecsgen_target(cls) -> list[Any]:
        return _uniq(cls._post_tecsgen_target)

    @classmethod
    def get_lines(cls) -> list[str]:
        return _uniq(cls._lines)

    @classmethod
    def set_default_config(cls) -> None:
        """TECSGEN のデフォルト設定を行う（Makefile）。"""
        cls.add_var("TARGET", "$(TARGET_BASE).exe", "default target name")
        cls.add_var("TECSGEN", "tecsgen", "default TECS generator")
        cls.add_var("TIMESTAMP", "$(GEN_DIR)/tecsgen.timestamp", "Time Stamp")
        cls.add_var("CC", "gcc", "default C Compiler")
        cls.add_var(
            "CFLAGS",
            '$(INCLUDES) $(DEFINES) -D  "Inline=static inline"',
            "default C Compiler options",
        )
        cls.add_var("LD", "gcc", "default Liknker")
        cls.add_var("LDFLAGS", cls._ldflags, "default Liknker Options")
        cls.add_var("SRC_DIR", "$(BASE_DIR)/src", "default source directory")
        cls.add_var(
            "_TECS_OBJ_DIR", "$(GEN_DIR)/", "default relocatable object (.o) directory"
        )


class CMake:
    """CMakeLists.tecsgen.cmake の出力内容を追加、変更するための操作（TECSGEN::CMake）。

    Ruby 版 tecslib/core/tecsgen.rb の module CMake に対応する（tecsgen-rb で追加された）。
    プラグインから add_* で追加した内容は、gen_cmake_tecsgen（core/generate.py）が出力する。
    """

    RUBY_NAME = "TECSGEN::CMake"

    _sources: ClassVar[list[str]] = []
    _includes: ClassVar[list[str]] = []
    _defines: ClassVar[list[str]] = []
    _link_options: ClassVar[list[str]] = []
    _custom_commands: ClassVar[list[str]] = []
    _lines: ClassVar[list[str]] = []

    @classmethod
    def reset(cls) -> None:
        cls._sources = []
        cls._includes = []
        cls._defines = []
        cls._link_options = []
        cls._custom_commands = []
        cls._lines = []

    @classmethod
    def set_default_config(cls) -> None:
        """Ruby の self.set_default_config（すべて空に戻す）。"""
        cls.reset()

    @classmethod
    def add_source(cls, src: Any) -> None:
        cls._sources.append(to_s(src))

    @classmethod
    def add_include(cls, path: Any) -> None:
        cls._includes.append(to_s(path))

    @classmethod
    def add_define(cls, define: Any) -> None:
        cls._defines.append(to_s(define))

    @classmethod
    def add_link_option(cls, opt: Any) -> None:
        cls._link_options.append(to_s(opt))

    @classmethod
    def add_custom_command(cls, cmd: Any) -> None:
        cls._custom_commands.append(to_s(cmd))

    @classmethod
    def add_line(cls, line: Any) -> None:
        cls._lines.append(to_s(line))

    @classmethod
    def get_sources(cls) -> list[str]:
        return _uniq(cls._sources)

    @classmethod
    def get_includes(cls) -> list[str]:
        return _uniq(cls._includes)

    @classmethod
    def get_defines(cls) -> list[str]:
        return _uniq(cls._defines)

    @classmethod
    def get_link_options(cls) -> list[str]:
        return _uniq(cls._link_options)

    @classmethod
    def get_custom_commands(cls) -> list[str]:
        return _uniq(cls._custom_commands)

    @classmethod
    def get_lines(cls) -> list[str]:
        return _uniq(cls._lines)


def _uniq(items: list[Any]) -> list[Any]:
    """Ruby の Array#uniq（最初に出たものを残す）。"""
    out: list[Any] = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


Makefile.reset()
CMake.reset()
