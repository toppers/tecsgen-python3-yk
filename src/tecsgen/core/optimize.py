"""optimize.rb の移植（内部仕様7章）。意味解析からコード生成の間で行う処理。

最適化の他に、セル毎の ID 付け、ドメインわけを行う。コード生成対象となるセルを対象に処理を行う。
Ruby 版は `Namespace`・`Celltype` を再オープンしてメソッドを足している。Python 版は mixin にする。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    inspect,
    rb_print,
    rb_puts,
    to_s,
    truthy,
)


class NamespaceOptimize:
    """optimize.rb の Namespace 再オープン部分。"""

    _celltype_list: list[Any]
    _namespace_list: list[Any]

    def set_cell_id_and_domain(self) -> None:
        """各セルに ID （整数値）を割付ける。"""
        # celltype の各セルに ID を割付ける
        for t in self._celltype_list:
            t.set_cell_id_and_domain()
        # サブネームスペースの各セルに ID を割付ける
        for n in self._namespace_list:
            n.set_cell_id_and_domain()

    def optimize(self) -> None:
        for t in self._celltype_list:
            t.optimize()
        for n in self._namespace_list:
            n.optimize()

    def reset_optimize(self) -> None:
        for t in self._celltype_list:
            t.reset_optimize()
        for n in self._namespace_list:
            n.reset_optimize()


class CelltypeOptimize:
    """optimize.rb の Celltype 再オープン部分。

    クラス変数 `@@ID_BASE`・`@@domain_class_roots` は Celltype 本体（celltype.py）に置いている。
    インスタンス変数 `@domain_class_roots` はクラス変数と名前が同じなので `__dict__` で読み書きする。
    """

    _cell_list: list[Any]
    _port: list[Any]
    _name: Any
    _ID_BASE: ClassVar[int]

    def set_cell_id_and_domain(self) -> None:
        self.set_cell_id()
        self.set_domain()
        self.set_domain_class()

    def set_cell_id(self) -> None:
        """各セルに ID （整数値）を割付ける。"""
        from tecsgen.core.componentobj.celltype import Celltype

        ctx = get_context()
        s: Any = self
        if ctx.verbose:
            rb_print(
                f"=== id for the cells of celltype {to_s(s.get_namespace_path())} ===\n"
            )

        if ctx.unique_id:
            s._id_base = Celltype._ID_BASE  # id をシステム全体で連番にする
        else:
            s._id_base = 1  # base を常に 1 から始める

        id_specified_cells: list[Any] = []
        no_id_specified_cells: list[Any] = []

        # プロトタイプを除いた数を求める
        for c in self._cell_list:
            if c.is_generate():
                cid = c.get_specified_id()
                if truthy(cid):
                    id_specified_cells.append(c)
                else:
                    no_id_specified_cells.append(c)
                Celltype._ID_BASE += 1
                s._n_cell_gen += 1

        s._ordered_cell_list = []  # id = 1 が添数 0 に格納される
        ordered: list[Any] = s._ordered_cell_list
        n_cell_gen = s._n_cell_gen
        # ID 指定されているセルに id 番号を与える
        for c in id_specified_cells:
            cid = c.get_specified_id()
            dbg_print(
                f"id_specified_cells celltype={to_s(self._name)} cell={to_s(c.get_name())} "
                f"id={to_s(cid)} n_cell={n_cell_gen}\n"
            )
            if cid > 0:
                if cid >= n_cell_gen:
                    s.cdl_error(
                        "S3001 $1: id too large $2 (max=$3)",
                        c.get_name(),
                        cid,
                        n_cell_gen,
                    )
                    continue
            else:
                if -cid >= n_cell_gen:
                    s.cdl_error(
                        "S3002 $1: id too large $2 (max=$3)",
                        c.get_name(),
                        cid,
                        n_cell_gen,
                    )
                    continue
                cid = n_cell_gen + cid + 1

            prev = _get_at(ordered, cid - 1)
            if truthy(prev):
                s.cdl_error(
                    "S3003 $1: id number '$2' conflict with $3",
                    c.get_name(),
                    cid,
                    prev.get_name(),
                )
            _set_at(ordered, cid - 1, c)
            # 通し番号とする場合のため @id_base を加える
            c.set_id(s._id_base - 1 + cid)
            if ctx.verbose:
                rb_print(
                    f"{to_s(c.get_name())}: id={to_s(c.get_id())}  "
                    f"specified id={to_s(c.get_specified_id())}\n"
                )

        # ID 指定されていないセルに id 番号を与える
        i = 0
        for c in no_id_specified_cells:
            while _get_at(ordered, i) is not None:
                i += 1
            _set_at(ordered, i, c)
            c.set_id(s._id_base + i)
            if ctx.verbose:
                rb_print(f"{to_s(c.get_name())}: id={to_s(c.get_id())}\n")
        if n_cell_gen > 0 and i >= n_cell_gen:
            raise RubyRuntimeError(f"id over id={i} N={n_cell_gen}")

    def set_domain(self) -> None:
        ctx = get_context()
        s: Any = self
        domain_cells: dict[Any, list[Any]] = {}
        domain_roots: dict[Any, list[Any]] = s._domain_roots
        for c in self._cell_list:
            if c.is_generate():
                dr = c.get_region().get_domain_root()
                dn = (
                    dr.get_domain_type().get_name()
                    if truthy(dr.get_domain_type())
                    else None
                )
                if truthy(domain_roots.get(dn)):
                    domain_roots[dn].append(dr)
                else:
                    domain_roots[dn] = [dr]
                if truthy(domain_cells.get(dr)):
                    domain_cells[dr].append(c)
                else:
                    domain_cells[dr] = [c]

        for dn in list(domain_roots):
            drs = _uniq(domain_roots[dn])
            domain_roots[dn] = drs
            if ctx.verbose and truthy(dn):
                delim = ""
                for r in drs:
                    rb_print(delim, r.get_name())
                    delim = ", "
                rb_print("}\n")
                for r in drs:
                    rb_print(
                        f"[domain] celltype={to_s(self._name)} domainRootRegion={to_s(r.get_name())} "
                        f"domainType={to_s(dn)}("
                    )
                    delim = ""
                    for c in domain_cells[r]:
                        rb_print(delim, c.get_name())
                        delim = ", "
                    rb_print("}\n")
        if len(domain_roots) > 1:
            rb_puts(inspect(domain_roots))
            raise RubyRuntimeError("ambigous DomainType")

        for regions in domain_roots.values():
            # domain_type は一つのノードに一つしかないので、一つの要素を無条件で取り出す
            if len(regions) > 1:
                if ctx.verbose:
                    s.cdl_info(
                        "I9999 celltype '$1' has cells in multi-domain.\n", self._name
                    )
                s._b_need_ptab = True

    def set_domain_class(self) -> None:
        """@domain_class_roots を設定。"""
        from tecsgen.core.componentobj.celltype import Celltype

        ctx = get_context()
        s: Any = self
        domain_class_roots: dict[Any, dict[Any, list[Any]]] = {}
        s.__dict__["_domain_class_roots"] = domain_class_roots
        roots2: dict[Any, list[Any]] = s.__dict__["_domain_class_roots2"]
        total = Celltype._domain_class_roots
        for c in self._cell_list:
            if c.is_generate():
                dr = c.get_region().get_domain_root()
                cr = c.get_region().get_class_root()

                # set @domain_class_roots
                if domain_class_roots.get(dr) is None:
                    domain_class_roots[dr] = {}
                if truthy(domain_class_roots[dr].get(cr)):
                    domain_class_roots[dr][cr].append(c)
                else:
                    domain_class_roots[dr][cr] = [c]

                # set @domain_class_roots2
                sub_region = dr if dr.is_sub_region_of(cr) else cr
                if truthy(roots2.get(sub_region)):
                    roots2[sub_region].append(c)
                else:
                    roots2[sub_region] = [c]

                # set @@domain_class_roots
                if truthy(total.get(sub_region)):
                    total[sub_region].append(self)
                else:
                    total[sub_region] = [self]

        # domain_type は一つのノードに一つしかないので、一つの要素を無条件で取り出す
        if len(roots2) > 1:
            s._b_need_ptab = True
            nr = next(iter(roots2)).get_link_root()
            if (
                truthy(nr.get_domain_type())
                and nr.get_domain_type().get_kind() != Y.OutOfDomain
            ):
                # link root が OutOfDomain でない場合エラーとする
                s.cdl_error(
                    "S9999 region '$1' is node/link root and not out of domain ($2). "
                    "This is limitation in current version",
                    nr.get_name(),
                    to_s(nr.get_domain_type().get_kind()),
                )
            # node root
            if total.get(nr) is None:
                total[nr] = []

        if ctx.verbose:
            s.cdl_info("I9999 celltype '$1' has cells in multi-domain.\n", self._name)
            for sub_region, cell_list in roots2.items():
                delim = ""
                rb_print(
                    f"celltype={to_s(self._name)} subRegion={to_s(sub_region.get_name())} cells={{"
                )
                for c in cell_list:
                    rb_print(f"{delim} {to_s(c.get_name())}")
                    delim = ","
                rb_print(" }\n")

    def optimize(self) -> None:
        ctx = get_context()
        s: Any = self
        # port の参照するセルタイプの数、セルの数を求める
        if ctx.verbose:
            rb_print(f"=== optimizing celltype {to_s(s.get_namespace_path())} ===\n")
        self.optimize_call()
        if ctx.unopt_entry is False:
            self.optimize_entry()

    def optimize_call(self) -> None:
        """呼び口最適化。"""
        ctx = get_context()
        s: Any = self
        for port in self._port:
            if port.get_port_type() != Y.CALL:
                continue
            if port.is_omit():
                # 呼び口最適化実施
                s._b_cp_optimized = True
                s._n_call_port_omitted_in_CB += 1  # CB で省略する呼び口
                port.set_skelton_useless()  # スケルトン関数不要最適化
                port.set_VMT_useless()  # VMT 不要最適化 (直接受け口関数を呼出す)
                if ctx.verbose:
                    rb_print(f"optimized by omit: port: {to_s(port.get_name())} : o\n")
                continue
            elif port.is_dynamic():
                if ctx.verbose:
                    rb_print(f"unoptimized by dynamic: port: {to_s(port.get_name())}\n")
                continue
            elif port.is_ref_desc():
                if ctx.verbose:
                    rb_print(
                        f"unoptimized by ref_desc: port: {to_s(port.get_name())}\n"
                    )
                continue

            if ctx.verbose:
                rb_print(f"optimizing port : {to_s(port.get_name())}\n")

            port_cells: list[Any] = []  # 呼び先セル
            port_ports: list[Any] = []  # 呼び先のポート

            # セルの参照するセルを集める（ポートも一緒に集める）
            for cell in self._cell_list:
                if not cell.is_generate():
                    continue
                jl = cell.get_join_list()
                j = jl.get_item(port.get_name())
                if truthy(j):
                    am = j.get_array_member2()
                    if truthy(am):
                        # 呼び口配列の場合、全部の結合先を集める
                        for j2 in am:
                            if truthy(j2):
                                port_cells.append(j2.get_rhs_cell())
                                port_ports.append(j2.get_rhs_port())  # 右辺のポート
                            else:
                                # optional で、ある添数のみ初期化されていない
                                port_cells.append(None)
                                port_ports.append(None)
                    else:
                        # 全ての結合先を集める
                        port_cells.append(j.get_rhs_cell())
                        port_ports.append(j.get_rhs_port())  # 右辺のポート
                else:
                    # optional で初期化されていない（nil を要素に加えておく）
                    port_cells.append(None)
                    port_ports.append(None)

            # 重複要素を取り除く
            port_cells = _uniq(port_cells)
            port_ports = _uniq(port_ports)

            # 呼び口の呼び先が一つのポートだけか？
            if len(port_ports) == 1:
                # 呼び口配列が可変長の場合、最適化しない
                if port.get_array_size() == "[]":
                    continue

                # 呼び口最適化実施
                s._b_cp_optimized = True

                # 呼び先が一つのセルだけか？
                if len(port_cells) == 1:
                    # 呼び口は optional で初期化されていない、または受け口は配列ではないか？
                    if port_ports[0] is None or port_ports[0].get_array_size() is None:
                        s._n_call_port_omitted_in_CB += 1  # CB で省略する呼び口
                        port.set_cell_unique()  # セル一つだけ最適化
                        port.set_skelton_useless()  # スケルトン関数不要最適化
                        port.set_VMT_useless()  # VMT 不要最適化 (直接受け口関数を呼出す)
                        if ctx.verbose:
                            rb_print(
                                "cell_unique, VMT_useless & skelton_useless optimize\n"
                            )
                    else:
                        port.set_VMT_useless()  # VMT 不要最適化 (スケルトン関数を呼出す)
                        if ctx.verbose:
                            rb_print("VMT_useless optimize\n")
                else:  # 呼び先が複数のセル（単一のポート）
                    # 呼び口は optional で初期化されていない、または受け口は配列ではないか？
                    if port_ports[0] is None or port_ports[0].get_array_size() is None:
                        if not truthy(s._singleton):
                            port.set_skelton_useless()  # スケルトン関数不要最適化
                            port.set_VMT_useless()  # VMT 不要最適化
                            if ctx.verbose:
                                rb_print("VMT_useless & skelton useless optimize\n")
                        else:
                            port.set_VMT_useless()  # VMT 不要最適化
                            if ctx.verbose:
                                rb_print("VMT_useless optimize\n")

                port.set_only_callee(port_ports[0], port_cells[0])
                # set_cell_unique でない場合 cell は意味がない

            dbg_print(
                f"{to_s(port.get_name())} : # of cells : {len(port_cells)}  "
                f"# of ports : {len(port_ports)}\n"
            )

    def optimize_entry(self) -> None:
        """受け口最適化。optimize_entry は、呼び口最適化の結果を使用している。"""
        for port in self._port:
            if port.get_port_type() != Y.CALL:
                continue

            # 呼び口側の最適化状態
            b_VMT_useless = port.is_VMT_useless()
            b_skelton_useless = port.is_skelton_useless()

            # セルの参照するセルを集める（ポートも一緒に集める）
            for cell in self._cell_list:
                if not cell.is_generate():
                    continue
                jl = cell.get_join_list()
                j = jl.get_item(port.get_name())
                if truthy(j):  # optional で結合されていない場合 nil
                    am = j.get_array_member2()
                    if truthy(am):
                        # 呼び口配列
                        for j2 in am:
                            if truthy(j2):
                                port2 = j2.get_rhs_port()  # 右辺のポート
                                # 受け口側の最適化可能性を設定
                                port2.set_entry_VMT_skelton_useless(
                                    b_VMT_useless, b_skelton_useless
                                )
                    else:
                        port2 = j.get_rhs_port()  # 右辺のポート
                        port2.set_entry_VMT_skelton_useless(
                            b_VMT_useless, b_skelton_useless
                        )

    def reset_optimize(self) -> None:
        """リセットする。"""
        from tecsgen.core.componentobj.celltype import Celltype

        s: Any = self
        Celltype._ID_BASE = Celltype.ID_BASE  # 本当は一回だけでよい
        s._id_base = 1  # set_cell_id でリセットされるので不要

        s._b_cp_optimized = False  # 呼び口最適化
        s._n_call_port_omitted_in_CB = 0  # 呼び口最適化により不生成となったポートの数
        s._n_cell_gen = 0  # 生成セル個数
        for p in self._port:
            p.reset_optimize()
        s._included_header = {}
        s._domain_roots = {}
        s.__dict__["_domain_class_roots"] = {}
        s.__dict__["_domain_class_roots2"] = {}

    def header_included(self, hname: Any) -> bool:  # Ruby: header_included?
        """ヘッダは include されているか。

        #_ISH_#, #_ICT_# でヘッダが取り込まれているかチェックする。
        false が返った場合、hname は登録されて、次回の呼び出しでは true が返る。
        """
        s: Any = self
        if s._included_header.get(hname) is None:
            s._included_header[hname] = True
            return False
        return True


def _uniq(items: list[Any]) -> list[Any]:
    """Ruby の Array#uniq（`eql?`/`hash` で比べる。モデルのオブジェクトは同一性）。"""
    out: list[Any] = []
    seen_ids: set[int] = set()
    for x in items:
        k = id(x)
        if k in seen_ids:
            continue
        seen_ids.add(k)
        out.append(x)
    return out
