"""ThroughPlugin.rb の移植（内部仕様9.1節）。

スループラグインの共通の親クラス、かつ（何もせず）スルーするセルを挿入するスループラグイン。
スループラグインは ThroughPlugin の子クラスとして定義する。

mikan through plugin: namespace が考慮されていない
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.core.plugin import Plugin
from tecsgen.ruby_compat import Y, gsub, sym, to_s, utf8_literal


class ThroughPlugin(Plugin):
    """@cell_name:: Symbol             生成するセル名（複数セルを生成する場合、受け口側のセル）
    @plugin_arg_str:: str              through で指定された引数
    @next_cell:: Cell                  呼び口を結合するセル
    @next_cell_port_name:: Symbol      呼び口を結合する受口の名前
    @next_cell_port_subscript:: int|None  呼び口を結合する受口の配列添数．受け口配列でない場合 None
    @signature:: Signature             シグニチャ
    @celltype:: Celltype               呼び先のセルのセルタイプ．through が連接する場合、最終的な呼び先のセルのセルタイプ
    @entry_port_name:: Symbol          生成するセルの受け口名  "eThroughEntry"
    @call_port_name:: Symbol           生成するセルの呼び口名  "cCall"
    @ct_name:: Symbol                  生成するセルのセルタイプ名   "t{class}_{signature.get_global_name}"
    @plugin_arg_list:: dict            プラグイン引数をパースした結果のハッシュ変数
    @caller_cell:: Cell                呼び元のセル．through プラグインが連接する場合では、最も呼び元のセル．($source$)
    @callee_cell:: Cell                呼び先のセル($destination$)

    以下は initialize ではなく、set_through_info で後から設定される:
    @start_region:: Region  始まりのリージョン（$start_region$）
    @end_region:: Region    終わりのリージョン（$end_region$）
    @region:: Region        start_region と end_region のいずれかで、cell を置くのが好ましいリージョン（$preferred_region$）
    @through_type:: Symbol  :THROUGH, :TO_THROUGH, :FROM_THROUGH, :IN_THROUGH, :OUT_THROUGH のいずれか
    """

    # この Plugin が生成したセルタイプのリスト
    _generated_celltype: ClassVar[dict[Any, list[Any]]] = {}

    @classmethod
    def reset(cls) -> None:
        """`@@generated_celltype` を初期化する（1プロセスで何度も実行するテスト用）。

        Ruby のクラス変数なので ThroughPlugin の子クラス全体で1つを共有する。子クラスは
        この辞書を書き換えるだけで代入し直さないので、ここで中身を空にすればよい。
        """
        ThroughPlugin._generated_celltype.clear()

    def __init__(
        self,
        cell_name: Any,
        plugin_arg: Any,
        next_cell: Any,
        next_cell_port_name: Any,
        next_cell_port_subscript: Any,
        signature: Any,
        celltype: Any,
        caller_cell: Any,
    ) -> None:
        """through が指定された時点で生成が行われる。初期化では、指定された引数を記録するに留める。

        cell_name:: Symbol             生成すべきセル名（受口側）
        plugin_arg:: str                through で指定された引数
        next_cell:: Cell                呼び口を接続するセル
        next_cell_port_name:: Symbol    呼び口を接続する受口の名前
        next_cell_port_subscript:: int|None  呼び口を接続する受口配列添数
        signature:: Signature           シグニチャ
        celltype:: Celltype             セルタイプ (呼び先のセルのセルタイプ)
        caller_cell:: Cell              呼び元のセル．@caller_cell の項を参照
        """
        from tecsgen.core.componentobj.join import Join
        from tecsgen.ruby_compat import class_name, rb_print

        super().__init__()
        self._cell_name = cell_name  # 生成すべきセル名（受け口側のセル名）
        self._next_cell = next_cell  # 呼び先のセル
        self._next_cell_port_name = next_cell_port_name
        self._next_cell_port_subscript = next_cell_port_subscript
        self._signature = signature
        self._entry_port_name = sym("eThroughEntry")
        self._call_port_name = sym("cCall")
        self._ct_name = sym(
            f"t{class_name(type(self))}_{to_s(signature.get_global_name())}"
        )
        self._celltype = celltype
        self._plugin_arg_str = plugin_arg
        self._plugin_arg_list = {}  # プラグイン引数をパースした結果のハッシュ変数
        self._caller_cell = caller_cell
        Join.set_through_info(
            self
        )  # 引数で渡らない(後から追加された)ものは set_through_info で設定される
        rb_print(
            f"{class_name(type(self))}.new( '{to_s(cell_name)}', '{to_s(plugin_arg)}', "
            f"'{to_s(next_cell.get_name())}', '{to_s(next_cell_port_name)}', "
            f"{to_s(celltype.get_name())} )\n"
        )

    def set_through_info(
        self,
        start_region: Any,
        end_region: Any,
        through_type: Any,
        join: Any,
        callee_cell: Any,
        count: Any,
    ) -> None:
        """情報を設定する。共有チャンネルの場合 caller_cell, next_cell のいずれの region でもないケースがある。

        後から追加したので initialize の引数ではなく、別メソッドで設定する。
        このメソッドは、オーバーライドしないでください。かわりに set_through_info_hook をオーバーライドしてください。
        """
        self._start_region = start_region
        self._end_region = end_region
        self._through_type = through_type
        self._join = join
        self._callee_cell = callee_cell
        self._count = count

        # preferred_region の設定
        if through_type in (Y.IN_THROUGH, Y.THROUGH, Y.FROM_THROUGH):
            self._region = end_region
        elif through_type in (Y.OUT_THROUGH, Y.TO_THROUGH):
            self._region = start_region
        else:
            raise RuntimeError(f"Unknown through_type {through_type}")
        self.set_through_info_hook()

    def set_through_info_hook(self) -> None:
        """情報が設定されたあと呼び出されるメソッド。オーバーライドしてもよい。"""

    def get_cell_name(self) -> Any:
        return self._cell_name

    def get_cell_namespace_path(self) -> Any:
        """生成するセルの namespace path を生成する。"""
        nsp = self._region.get_namespace_path()
        return nsp.append(self._cell_name)

    def get_through_entry_port_name(self) -> Any:
        return self._entry_port_name

    def get_through_entry_port_subscript(self) -> Any:
        return self._entry_port_subscript

    def gen_plugin_decl_code(self, file: Any) -> None:
        """宣言コードの生成。typedef, signature, celltype など（cell 以外）のコードを生成する。

        重複して生成してはならない（すでに生成されている場合は出力しないこと）。
        """
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if ThroughPlugin._generated_celltype.get(self._ct_name) is None:
            ThroughPlugin._generated_celltype[self._ct_name] = [self]
        else:
            ThroughPlugin._generated_celltype[self._ct_name].append(self)
            return

        gen_dir = get_context().gen
        file2 = CFile.open(f"{gen_dir}/{to_s(self._ct_name)}.cdl", "w")

        send_receive: list[tuple[Any, Any, Any]] = []
        if self._signature is not None:

            def collect(fd: Any, param: Any) -> None:
                d = param.get_direction()
                if d in (Y.SEND, Y.RECEIVE):
                    send_receive.append((d, fd, param))

            self._signature.each_param(collect)

        file2.print(
            f"/* generated by ThroughPlugin */\n\ncelltype {to_s(self._ct_name)} {{\n"
        )

        if len(send_receive) > 0:
            file2.print("  [allocator(\n")
            delim = ""
            for _d, fd, param in send_receive:
                file2.print(
                    f"{delim}\t{to_s(fd.get_name())}.{to_s(param.get_name())}<="
                    f"{to_s(self._call_port_name)}.{to_s(fd.get_name())}.{to_s(param.get_name())}"
                )
                delim = ",\n"
            file2.print("), inline]\n")
        else:
            file2.print("  [inline]\n")

        file2.print(
            f"    entry {to_s(self._signature.get_namespace_path())} {to_s(self._entry_port_name)};\n"
            f"  call  {to_s(self._signature.get_namespace_path())} {to_s(self._call_port_name)};\n"
            "};\n"
        )
        file2.close()

        file.print(f'import( "{gen_dir}/{to_s(self._ct_name)}.cdl" );\n')

    def gen_cdl_file(self, file: Any) -> None:
        """CDL ファイルの生成。"""
        self.gen_plugin_decl_code(file)
        self.gen_through_cell_code(file)

    def gen_through_cell_code(self, file: Any) -> None:
        """セルコードの生成。through 指定により生じるセルコード(CDL)を生成する。"""
        nest = self._region.gen_region_str_pre(file)
        nest_str = "  " * nest

        file.print(
            f"{nest_str}cell {to_s(self._ct_name)} {to_s(self._cell_name)} {{\n"
            f"{nest_str}  {to_s(self._call_port_name)} = "
            f"{self._next_cell.get_namespace_path().get_path_str()}."
            f"{to_s(self._next_cell_port_name)};\n"
            f"{nest_str}}};\n"
        )
        self._region.gen_region_str_post(file)

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """プラグインの後ろのコード (CDL) を生成する。

        複数のプラグインの post_code が一つのファイルに含まれるため、見出しをつけること。
        """

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
        params: list[Any],
    ) -> None:
        """受け口関数の本体(C言語)を生成する。

        通常であれば、ジェネレータは受け口関数のテンプレートを生成する。プラグインの場合、
        変更する必要のないセルタイプコードを生成する。
        """
        ret_type = func_type.get_type()
        b_ret_void = ret_type.is_void()

        if not b_ret_void:
            file.print(f"  {ret_type.get_type_str()}  retval;\n")

        if not b_singleton:
            file.print(
                f"  {to_s(ct_name)}_CB    *p_cellcb;\n"
                "  if( VALID_IDX( idx ) ){\n"
                f"    p_cellcb = {to_s(global_ct_name)}_GET_CELLCB(idx);\n"
                "  }else{\n"
                + utf8_literal("     /* エラー処理コードをここに記述 */\n")
                + "  }\n\n"
            )

        delim = ""
        if not b_ret_void:
            file.print("  retval = ")

        file.print(f"{to_s(self._call_port_name)}_{to_s(func_name)}(")

        for param in params:
            file.printf(f"{delim} {to_s(param.get_name())}")
            delim = ","

        file.print(" );\n")

        if not b_ret_void:
            file.print("  return retval;\n")

    def check_plugin_arg(self, ident: str, rhs: str) -> None:
        """Through プラグインの引数の名前を置換する。"""
        rhs = self.subst_name(rhs)
        super().check_plugin_arg(ident, rhs)

    def subst_name(self, s: str) -> str:
        r"""プラグインオプション引数内の文字列を置換する。

        ``$source$``       呼び元のセル名
        ``$destination$``  呼び先のセル名
        ``$SOURCE$``       呼び元のセル名 (リージョン名を '_' で連結した global_name)
        ``$DESTINATION$``  呼び先のセル名 (リージョン名を '_' で連結した global_name)
        ``$next$``         次のセル名（複数の through がつながっている場合、すぐ後ろに来るもの）
        ``$NEXT$``         次のセル名 (global_name)
        ``$start_region$`` $source$ のセルの存在する region (global_name)
        ``$end_region$``   $destination$ のセルの存在する region (global_name)
        ``$preferred_region$``  適切な region (global_name)、start_region または end_region
        ``$count$``        region 間の through の適用数
        ``$$``             $ に置換
        """

        def repl(pattern: str, value: str, text: str) -> str:
            return gsub(re.compile(pattern), rf"\1{value}", text)

        s = repl(r"(^|[^\$])\$source\$", to_s(self._caller_cell.get_name()), s)
        s = repl(r"(^|[^\$])\$destination\$", to_s(self._callee_cell.get_name()), s)
        s = repl(r"(^|[^\$])\$SOURCE\$", to_s(self._caller_cell.get_global_name()), s)
        s = repl(
            r"(^|[^\$])\$DESTINATION\$", to_s(self._callee_cell.get_global_name()), s
        )
        s = repl(r"(^|[^\$])\$next\$", to_s(self._next_cell.get_name()), s)
        s = repl(r"(^|[^\$])\$NEXT\$", to_s(self._next_cell.get_global_name()), s)
        s = repl(
            r"(^|[^\$])\$start_region\$", to_s(self._start_region.get_global_name()), s
        )
        s = repl(
            r"(^|[^\$])\$end_region\$", to_s(self._end_region.get_global_name()), s
        )
        s = repl(
            r"(^|[^\$])\$preferred_region\$", to_s(self._region.get_global_name()), s
        )
        s = repl(r"(^|[^\$])\$count\$", to_s(self._count), s)

        return gsub(re.compile(r"\$\$"), "$", s)

    def show_tree(self, indent: int) -> None:
        from tecsgen.ruby_compat import rb_print, rb_puts

        rb_print("  " * indent)
        rb_puts(
            f"Plugin: celltype: {to_s(self._ct_name)} cell: {to_s(self._cell_name)}"
        )
        rb_print("  " * (indent + 1))
        rb_puts(
            f"next: signature: {to_s(self._signature.get_namespace_path())} call = "
            f"{to_s(self._next_cell.get_name())}.{to_s(self._next_cell_port_name)}"
        )
