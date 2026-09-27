"""core/tecsgen.rb と tecsgen.rb（トップ）の `TECSGEN` クラスの移植（内部仕様3章）。

Ruby 版の `TECSGEN` は2つのファイルにまたがる。

- tecsgen.rb（トップ）: `initialize`・`run1`・`run2`・`init`（オプション解析などは
  `tecsgen.cli` へ移した）
- core/tecsgen.rb: import パスの操作、`Makefile`、構文解析・意味解析・生成の各段階

P3 では構文解析と意味解析（`run1`）までを移植した。`run2`（最適化・コード生成）は P4。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.ruby_compat import Y, gsub, sub_first, sym


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
        """最適化とコード生成（P4 で移植）。"""
        raise NotImplementedError("TECSGEN#run2 is ported in P4")

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
        """'/' または '$' で始まる場合、絶対パスと判定する。"""
        pa = path[0:1]
        pa2 = path[0:2]
        res = pa == "/" or pa == "$" or re.search(r"[A-Za-z]:", pa2) is not None
        dbg_print(
            f"is_absolute( {path} ) = {'true' if res else 'false'}  {path[0:1]}\n"
        )
        return res

    @staticmethod
    def set_default_config() -> None:
        """tecsgen のデフォルトを設定する。"""
        Makefile.set_default_config()

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


def _uniq(items: list[Any]) -> list[Any]:
    """Ruby の Array#uniq（最初に出たものを残す）。"""
    out: list[Any] = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


Makefile.reset()
