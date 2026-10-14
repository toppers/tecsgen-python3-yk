"""tcflow の関数情報（flowlib/classes.rb の `TCFlow::Function`）。

C の関数定義ごとに、参照したグローバル変数（読み書きの回数）と呼び出した関数を記録する。
関数の一覧（`@@Function_list`）はクラス変数で、名前 → `Function`、または「呼ばれたが
定義が無い」ことを表す整数 0 を持つ。Hash の挿入順は Ruby と同じく保つ。

Ruby 版は一覧を `Marshal` 形式（`tcflow.rbdmp`）で保存する。Python 版は JSON
（`tcflow.json`）で保存する（Marshal は再現しない。決定は移植計画ノート参照）。

サマリー表示（`print_summarize`）と一覧のツリー表示（クラスメソッド `print_all_functions`）は、
Ruby 版でも呼び出し元がコメントアウトされていて使われないので移植しない。tecsflow が使う
関数ごとのツリー表示（インスタンスメソッド `print_all_functions`）は移植した。
"""

from __future__ import annotations

import json
from typing import Any, ClassVar

from tecsgen.flowlib.ruby_errors import open_error
from tecsgen.ruby_compat import Symbol, sym, write_stdout


def out(text: str) -> None:
    """tcflow が持つ文字列はバイト列を latin-1 で復号した表現なので、同じ符号化で書く。"""
    write_stdout(text, "latin-1")


def print_locale(locale: list[Any]) -> None:
    """Ruby の `Locale_printer#print_locale`。`" (ファイル 行)"` を出す。"""
    out(f" ({locale[0]} {locale[1]})")


class Function:
    """関数1つ分の情報。"""

    function_list: ClassVar[dict[Symbol, Function | int]] = {}
    pending_param_list: ClassVar[list[Symbol] | None] = None

    def __init__(self, locale: list[Any]) -> None:
        self.param_var: dict[Symbol, Symbol] = {}
        self.local_var: dict[Symbol, Symbol] = {}
        # 変数名 -> [読み取り回数, 書き込み回数]
        self.global_var: dict[Symbol, list[int]] = {}
        self.call_func: dict[Symbol, Function | int] = {}
        self.b_ref = False
        self.b_printed = False
        self.ref_func_owner: Function | None = None
        self.locale = locale
        self.name: Symbol | None = None

        # param_list は関数が new される前に解釈されている
        if Function.pending_param_list is not None:
            for param in Function.pending_param_list:
                self.new_param(param)

    @classmethod
    def reset(cls) -> None:
        """クラス変数を初期状態に戻す（Ruby 版には無い。1プロセスで複数回実行するテスト用）。"""
        cls.function_list = {}
        cls.pending_param_list = None

    def set_name(self, name: Any) -> None:
        """関数をパースする最後で名前が確定する。"""
        self.name = sym(name)
        if Function.function_list.get(self.name) == 0:
            self.b_ref = True
        Function.function_list[self.name] = self
        Function.pending_param_list = None

    @classmethod
    def param_list(cls, param_list: list[Symbol] | None) -> None:
        cls.pending_param_list = param_list

    def new_param(self, param: Symbol) -> None:
        self.param_var[param] = param

    def new_local(self, local: Symbol) -> None:
        self.local_var[local] = local

    def ref_var(self, var: Any, b_write: bool = False) -> None:
        var = sym(var)
        if var in self.local_var or var in self.param_var:
            return
        count_array = self.global_var.get(var)
        if count_array is None:
            count_array = [0, 0]
            self.global_var[var] = count_array
        if b_write:
            count_array[1] += 1
        else:
            count_array[0] += 1

    def ref_func(self, func_name: Any) -> None:
        func_name = sym(func_name)
        function = Function.function_list.get(func_name)
        if isinstance(function, Function):
            function.referenced()
            self.call_func[func_name] = function
        else:
            Function.function_list[func_name] = 0
            self.call_func[func_name] = 0

    def referenced(self, ref_func: Function | None = None) -> None:
        self.b_ref = True
        self.ref_func_owner = ref_func

    def is_local_var(self, var: Any) -> bool:
        """ローカル変数または引数か（グローバルなら False）。"""
        return var in self.local_var or var in self.param_var

    def is_top(self) -> bool:
        return not self.b_ref

    def is_printed(self) -> bool:
        return self.b_printed

    def set_printed(self) -> None:
        self.b_printed = True

    def get_call_funcs(self) -> dict[Symbol, Function | int]:
        return self.call_func

    def get_locale(self) -> list[Any]:
        return self.locale

    def get_name(self) -> Symbol | None:
        return self.name

    # --- 呼び出し関数の更新・ツリー表示 -------------------------------------------

    @classmethod
    def update(cls) -> None:
        """全関数の `call_func` を更新する（構文解釈中に設定された右辺は不完全なため）。"""
        for func in list(cls.function_list.values()):
            if isinstance(func, Function):
                func.update_call_funcs()

    def update_call_funcs(self) -> None:
        for name, func in list(self.call_func.items()):
            if isinstance(func, Function):
                continue
            func = Function.function_list.get(name)
            if isinstance(func, Function):
                self.call_func[name] = func
                func.referenced(self)

    def print_all_functions(self, level: int) -> None:
        """この関数から呼ばれる関数のツリー表示。

        level == 0: 参照されていない（トップレベルの）関数だけ表示する。
        """
        if level == 0 and self.b_ref:
            return
        if level == -1:
            if self.b_printed:
                return
            level = 0

        indent = "    " * level
        if self.b_printed:
            # 印刷済みは再帰的に印刷しない
            out(f"{indent}{self.name} : printed\n")
            return
        self.b_printed = True

        if self.call_func:
            out(f"{indent}  Calling Function: \n")
            for name in sorted(self.call_func, key=str):
                func = self.call_func[name]
                if isinstance(func, Function):
                    out(f"{indent}    {name}")
                    print_locale(self.locale)
                    out("\n")
                    func.print_all_functions(level + 1)
                else:
                    out(f"{indent}    {name}() : not defined\n")

    # --- 保存・読み込み（JSON） ------------------------------------------------

    def to_json_data(self) -> dict[str, Any]:
        return {
            "param_var": [str(p) for p in self.param_var],
            "local_var": [str(p) for p in self.local_var],
            "global_var": {
                str(name): list(counts) for name, counts in self.global_var.items()
            },
            "call_func": {
                str(name): (str(name) if isinstance(f, Function) else 0)
                for name, f in self.call_func.items()
            },
            "b_ref": self.b_ref,
            "locale": list(self.locale),
        }

    @classmethod
    def dump_funclist(cls, dump_file_name: str) -> None:
        """Ruby の `p "Dump Funclist"`（引用符つきで標準出力へ）と、一覧のファイルへの保存。"""
        from tecsgen.host import get_host

        write_stdout('"Dump Funclist"\n')
        data = {
            str(name): (f.to_json_data() if isinstance(f, Function) else 0)
            for name, f in cls.function_list.items()
        }
        text = json.dumps(data, ensure_ascii=True, indent=1) + "\n"
        try:
            get_host().write_bytes(dump_file_name, text.encode("ascii"))
        except OSError as e:
            raise open_error(e, dump_file_name) from e

    @classmethod
    def load_funclist(cls, dump_file_name: str) -> dict[Symbol, Function | int]:
        """保存した一覧を読み込み、`function_list` に置く。"""
        from tecsgen.host import get_host

        try:
            raw = get_host().read_bytes(dump_file_name)
        except OSError as e:
            raise open_error(e, dump_file_name) from e
        data = json.loads(raw.decode("ascii"))
        functions: dict[Symbol, Function | int] = {}
        for name, entry in data.items():
            if entry == 0:
                functions[sym(name)] = 0
                continue
            f = Function(list(entry["locale"]))
            f.name = sym(name)
            f.param_var = {sym(p): sym(p) for p in entry["param_var"]}
            f.local_var = {sym(p): sym(p) for p in entry["local_var"]}
            f.global_var = {sym(k): list(v) for k, v in entry["global_var"].items()}
            f.b_ref = entry["b_ref"]
            functions[sym(name)] = f
        # call_func は、読み込んだ関数どうしの参照に戻す
        for name, entry in data.items():
            if entry == 0:
                continue
            owner = functions[sym(name)]
            assert isinstance(owner, Function)
            owner.call_func = {
                sym(k): (functions[sym(v)] if v != 0 else 0)
                for k, v in entry["call_func"].items()
            }
        cls.function_list = functions
        return functions
