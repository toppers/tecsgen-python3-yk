"""NotifierPlugin.rb の移植（内部仕様9章）。

タイムイベント通知（CRE_CYC・CRE_ALM など）のハンドラ指定を、セルの結合と属性から判別して
カーネルコンフィギュレーションファイル（output_file）に生成するセルタイププラグイン。
siHandlerBody の受け口を通知先にする場合は、カーネルからの呼出しを TECS の呼出しに変換する
アダプタ関数（tTimeEventHandler.c・.h・_aux.h）も生成する。

ドメイン（HRP・HRMP）・クラス（FMP・HRMP）に関する分岐も Ruby 版どおり移植しているが、
それらのカーネル依存プラグインは P5l 以降で移植（カーネルのケースから通る）。
SAC の生成（gen_sac）は、読み込み済みのドメインプラグイン（HRPPlugin・HRMPDomainPlugin）の get_sac_str を呼ぶ。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import gsub, sub_first, sym, to_s, truthy

_ATTR_SUBST_RE = re.compile(r"\{\{([a-zA-Z0-9_]*?)\}\}")


# ---------- アダプタ関数の生成 -------------
#
# siHandlerBodyの受け口関数は，タイムイベント通知の通知先として直接指定する
# ことはできない．シグネチャが一致していないことが理由である．このため，アダ
# プタとして動作する関数を生成し，カーネルからの呼出しをTECSの呼出しに変換で
# きるようにする必要がある．
#
# 受け口毎にアダプタ関数を生成するとメモリ消費量が増えるので，通知先関数に
# intptr_t型の引数を渡せることを使い，セルインデックスか受け口配列の添字の一方
# について関数を"一般化"する（詳細は Ruby 版のコメントを参照）．
# tecsgen.cfg ではアダプタ関数を直接指定せず，アダプタ関数ハンドル（アダプタ関数
# へのポインタと引数を表すマクロ）を使う．


class EntryProperty:
    """結合先に関する属性（受け口側のセル，受け口配列の添字）。

    同一の EntryProperty となる結合は，全く同じ方法でその受け口関数を呼び出せる．
    """

    def __init__(self, cell: Any, subscript: Any) -> None:
        self.cell = cell
        self.subscript = subscript

    @staticmethod
    def from_join(join: Any) -> EntryProperty:
        return EntryProperty(join.get_rhs_cell(), join.get_rhs_subscript())

    # 同値性の定義．Hash のキーとして使用するのに必要．
    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, EntryProperty)
            and self.cell == o.cell
            and self.subscript == o.subscript
        )

    def __hash__(self) -> int:
        return hash(self.cell) ^ hash(self.subscript)


def _group_by(items: list[Any], key: Any) -> dict[Any, list[Any]]:
    """Ruby の Enumerable#group_by（最初に現れた順を保つ）。"""
    groups: dict[Any, list[Any]] = {}
    for it in items:
        groups.setdefault(key(it), []).append(it)
    return groups


class EntryPort:
    def __init__(self, port: Any, prefix: str) -> None:
        """port:: Port 結合先のセルのセルタイプの受け口。"""
        self.port = port
        ct_gname = to_s(port.get_celltype().get_global_name())
        # グローバルに一意(なものとして扱えるよう)な識別子
        self.global_name = f"{prefix}_{ct_gname}_{to_s(port.get_name())}"

        # 受け口関数名．siHandlerBodyを想定しているので，関数名はmainで固定である．
        self._entry_fn_name = f"{ct_gname}_{to_s(port.get_name())}_main"

        self._props: list[EntryProperty] = []
        self._prop_map: dict[EntryProperty, int] = {}

    def adapter_handle_for_entry_property(self, ep: EntryProperty) -> list[str]:
        """指定した EntryProperty に対応するアダプタ関数ハンドルを取得する。"""
        index = self._prop_map[ep]
        return [f"{self.global_name}_{index}_fp", f"{self.global_name}_{index}_arg"]

    def generate_inner(
        self,
        context: AdapterGenerator,
        fn_name: str,
        cell: Any,
        subscript: Any,
        callee_ct: Any = None,
    ) -> None:
        """結合先の情報に応じたアダプタ関数をソース・ヘッダーに出力する。

        一般化指定は，cell または subscript の一方のみ行うことができる（:generic）。
        """
        source_file = context.source_file
        header_file = context.header_file

        source_file.print(f"void {fn_name}(intptr_t extinf) {{\n")

        params: list[str] = []
        ct = self.port.get_celltype()

        # シングルトンセルタイプ以外では，CELLIDXの指定が必要．
        if not ct.is_singleton():
            if cell == _GENERIC:
                params.append(f"({to_s(callee_ct.get_global_name())}_IDX)extinf")
            elif ct.has_INIB() or ct.has_CB():
                # セルのCELLIDXを得る
                params.append(to_s(ct.get_name_array(cell)[7]))
            else:
                params.append("0")

        # 受け口配列の添字．
        if truthy(self.port.get_array_size()):
            if subscript == _GENERIC:
                params.append("(int_t)extinf")
            else:
                params.append(to_s(subscript))

        params_str = ", ".join(params)

        source_file.print(f"\t{self._entry_fn_name}({params_str});\n")
        source_file.print("}\n\n")

        header_file.print(f"extern void {fn_name}(intptr_t extinf);\n\n")

    def make_adapter_handle(self, join: Any) -> list[str]:
        """指定した Join に対応するアダプタ関数ハンドルを取得する。"""
        prop = EntryProperty.from_join(join)
        if prop not in self._prop_map:
            self._prop_map[prop] = len(self._props)
            self._props.append(prop)
        return self.adapter_handle_for_entry_property(prop)

    def generate(self, context: AdapterGenerator) -> None:
        """ソース・ヘッダーの記述を生成する。"""
        header_file = context.header_file
        if not self._props:
            return

        ct = self.port.get_celltype()

        header_file.print(f"/*\n * {self.global_name}\n")

        cells = _group_by(self._props, lambda prop: prop.cell)
        subscripts = _group_by(self._props, lambda prop: prop.subscript)
        no_cellidx = False
        if not (ct.has_INIB() or ct.has_CB()):
            # CB, INIB最適化により，CB, INIBが両方不要になったケース．
            # CELLIDXが不要であるので，添字による一般化を選択する．
            generalize_by_cell_idx = False
            no_cellidx = True

            # 全てのセルを同一視する．
            cells = {self._props[0].cell: self._props}

            header_file.print(" * No INIB & CB: generalized by subscript\n")
        elif truthy(self.port.get_array_size()):
            # 受け口側セルや添字のパターン数を分析して，最適な方を選択する．
            generalize_by_cell_idx = len(cells) >= len(subscripts)
            if generalize_by_cell_idx:
                header_file.print(
                    " * more cells than subscripts: generalized by cell\n"
                )
            else:
                header_file.print(
                    " * more subscripts than cells: generalized by subscript\n"
                )
        else:
            # 常にCELLIDXで一般化
            generalize_by_cell_idx = True
            header_file.print(" * non-array entry port: generalized by cell\n")

        header_file.print(" */\n\n")

        if generalize_by_cell_idx:
            # CELLIDXについて一般化
            for subscript, props in subscripts.items():
                if truthy(subscript):
                    fn_name = f"{self.global_name}_adap_{to_s(subscript)}"
                else:
                    # 受け口配列でない場合
                    fn_name = f"{self.global_name}_adap"

                self.generate_inner(context, fn_name, _GENERIC, subscript, ct)

                for prop in props:
                    handle = self.adapter_handle_for_entry_property(prop)

                    # セルのCELLIDXを得る
                    if ct.has_INIB() or ct.has_CB():
                        idx = to_s(ct.get_name_array(prop.cell)[7])
                    else:
                        idx = "0"
                    header_file.print(f"#define {handle[0]} &{fn_name}\n")
                    header_file.print(f"#define {handle[1]} {idx}\n\n")
        else:
            # 添字について一般化
            for cell, props in cells.items():
                if no_cellidx:
                    # CB/INIB なし
                    fn_name = f"{self.global_name}_adap"
                else:
                    fn_name = f"{self.global_name}_adap_{to_s(cell.get_global_name())}"

                self.generate_inner(context, fn_name, cell, _GENERIC)

                for prop in props:
                    handle = self.adapter_handle_for_entry_property(prop)
                    sub = prop.subscript if truthy(prop.subscript) else 0
                    header_file.print(f"#define {handle[0]} &{fn_name}\n")
                    header_file.print(f"#define {handle[1]} {to_s(sub)}\n\n")


# 一般化を表す印（Ruby 版の :generic）
_GENERIC = sym("generic")


class AdapterGenerator:
    def __init__(self, celltype_name: str, prefix: Any) -> None:
        """celltype_name:: ハンドラ関数のセルタイプ / prefix:: 名前衝突を防ぐためのプレフィックス"""
        self._celltype_name = celltype_name
        self._prefix = prefix
        self.source_file: Any = None
        self.header_file: Any = None

        # Hash<Port, EntryPort>
        self._entry_ports: dict[Any, EntryPort] = {}

    def make_adapter_handle(self, join: Any) -> list[str]:
        """指定した結合の呼出しを行うためのアダプタ関数ハンドルを生成する。"""
        port = join.get_rhs_port()
        entry_port = self._entry_ports.get(port)
        if entry_port is None:
            entry_port = EntryPort(port, f"{self._celltype_name}_{to_s(self._prefix)}")
            self._entry_ports[port] = entry_port
        return entry_port.make_adapter_handle(join)

    def finish(self) -> None:
        """各受け口に対し，アダプタ関数を生成する。"""
        from tecsgen.context import get_context
        from tecsgen.core.generate import AppFile

        ctx = get_context()
        name = self._celltype_name
        prefix = to_s(self._prefix)
        cls_name = "NotifierPlugin::AdapterGenerator"

        self.source_file = AppFile.open(f"{ctx.gen}/{name}.c")
        self.source_file.print(f"\n/* Generated by {cls_name} */\n\n")
        self.source_file.print(f'#include "{name}_aux.h"\n\n')
        self.source_file.print(f'#include "{name}_tecsgen.h"\n\n')

        self.header_file = AppFile.open(f"{ctx.gen}/{name}.h")
        self.header_file.print(f"\n/* Generated by {cls_name} */\n\n")

        # NotifierPluginを使用するセルタイプが複数ある場合，それぞれに対し finish が
        # 呼び出されるので，ファイル名 + セルタイプ名というヘッダーガードを用いる．
        header_guard = f"{name}_H_{prefix}"

        self.header_file.print(f"#ifndef {header_guard}\n")
        self.header_file.print(f"#define {header_guard}\n\n")

        # カーネルコンフィギュレータを実行する際，ハンドラ受け口のセルタイプ
        # のセルCBの定義が必要な場合がある．
        self.header_file.print(f'#include "{name}_aux.h"\n\n')

        # 結合先のセルタイプの定義はもう一つのヘッダーファイル(tCelltypeName_aux.h)から読み込む
        aux_header_file = AppFile.open(f"{ctx.gen}/{name}_aux.h")
        aux_header_file.print(f"\n/* Generated by {cls_name} */\n\n")

        aux_header_guard = f"{name}_AUX_H_{prefix}"

        aux_header_file.print(f"#ifndef {aux_header_guard}\n")
        aux_header_file.print(f"#define {aux_header_guard}\n\n")

        cb_type_only_guard = f"{name}_AUX_H_{prefix}_CB_TYPE_ONLY"

        # 結合先のセルタイプの定義を読み込む
        aux_header_file.print("#ifndef TOPPERS_CB_TYPE_ONLY\n")
        aux_header_file.print("#define TOPPERS_CB_TYPE_ONLY\n")
        aux_header_file.print(f"#define {cb_type_only_guard}\n")
        aux_header_file.print("#endif\n")
        celltypes: list[Any] = []
        for ep in self._entry_ports.values():
            ct = ep.port.get_celltype()
            if not any(c is ct for c in celltypes):
                celltypes.append(ct)
        for ct in celltypes:
            hname = f"{to_s(ct.get_global_name())}_tecsgen.{ctx.h_suffix}"
            aux_header_file.print(f'#include "{hname}"\n')
        aux_header_file.print(f"#ifdef {cb_type_only_guard}\n")
        aux_header_file.print(f"#undef {cb_type_only_guard}\n")
        aux_header_file.print("#undef TOPPERS_CB_TYPE_ONLY\n")
        aux_header_file.print("#endif\n\n")

        aux_header_file.print("#endif\n")
        aux_header_file.close()

        for entry_port in self._entry_ports.values():
            entry_port.generate(self)

        self.header_file.print("#endif\n")

        self.source_file.close()
        self.header_file.close()


# ------ 通知のハンドラの種類の定義 -------


class Handler:
    def __init__(self, call_port_name: str) -> None:
        self.call_port_name = call_port_name


# 通常のハンドラ
EVENT_HANDLER = Handler("ciNotificationHandler")

# エラーハンドラ (通常のハンドラが失敗した場合に呼び出される)
ERROR_HANDLER = Handler("ciErrorNotificationHandler")

HANDLERS = [EVENT_HANDLER, ERROR_HANDLER]


class HandlerAttribute:
    def __init__(self, name: str, error_name: str | None = None) -> None:
        self._name = name
        self._error_name = error_name or (name + "ForError")

    def name_for_handler(self, handler: Handler) -> str:
        if handler is EVENT_HANDLER:
            return self._name
        if handler is ERROR_HANDLER:
            return self._error_name
        raise RuntimeError(f"unknown handler {handler}")


# ------ 通知の属性の定義 -------
#
# ハンドラタイプに合致しない属性が指定された場合に
# エラーを出力できるよう、全ての属性をここで列挙する。

SETVAR_ADDR_ATTR = HandlerAttribute("setVariableAddress")
SETVAR_VALUE_ATTR = HandlerAttribute("setVariableValue")
INCVAR_ADDR_ATTR = HandlerAttribute("incrementedVariableAddress")
SNDDTQ_VALUE_ATTR = HandlerAttribute("dataqueueSentValue")
SETFLG_FLAG_ATTR = HandlerAttribute("flagPattern")

ATTRS = [
    SETVAR_ADDR_ATTR,
    SETVAR_VALUE_ATTR,
    INCVAR_ADDR_ATTR,
    SNDDTQ_VALUE_ATTR,
    SETFLG_FLAG_ATTR,
]


def _rhs_celltype_name_is(join: Any, name: str) -> bool:
    return truthy(join) and join.get_rhs_cell().get_celltype().get_name() == sym(name)


def _object_id_param(join: Any) -> str:
    """結合先のカーネルオブジェクトのセル（tTask など）の id 属性を $id$ 等を置換して得る。"""
    obj_cell = join.get_cell()
    id_attr_join = obj_cell.get_join_list().get_item(sym("id"))
    id_attr = join.get_rhs_cell().get_celltype().find(sym("id"))
    if truthy(id_attr_join):
        # セル生成時に初期化する場合
        id_ = to_s(id_attr_join.get_rhs())
    else:
        # セルタイプの初期化値を使う場合
        id_ = to_s(id_attr.get_initializer())

    # $id$等の置換
    name_array = obj_cell.get_celltype().get_name_array(obj_cell)
    return obj_cell.get_celltype().subst_name(id_, name_array)


def _subst_attr(cell: Any, attr_join: Any) -> str:
    """セルの属性の結合の右辺を $id$ 等を置換して得る。"""
    s = to_s(attr_join.get_rhs())
    name_array = cell.get_celltype().get_name_array(cell)
    return cell.get_celltype().subst_name(s, name_array)


# ------ ハンドラタイプの定義 -------


class BaseHandlerType:
    def __init__(self) -> None:
        # HandlerAttribute[]
        self.required_attributes: list[HandlerAttribute] = []

    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        """指定したセルの結合先が、このハンドラタイプに該当するかを検証。"""
        return self.generate_attr_map(handler, cell) is not None

    def generate_attr_map(
        self, handler: Handler, cell: Any
    ) -> dict[HandlerAttribute, Any] | None:
        """セルの属性と既知の HandlerAttribute のマッピング（属性の不足・過剰なら None）。"""
        amap: dict[HandlerAttribute, Any] = {}

        join_list = cell.get_join_list()

        for known_attr in ATTRS:
            attr_name = known_attr.name_for_handler(handler)
            join = join_list.get_item(sym(attr_name))

            # このセルタイプにおいて必須の属性か?
            is_required = known_attr in self.required_attributes

            # 属性の指定が不足している? or 過剰?
            # 注: セルタイプで初期値が指定されていても、ハンドラタイプの決定に影響しない。
            if (join is None) != (not is_required):
                return None

            # 必要のない属性であり、指定もされていないので飛ばす
            if join is None:
                continue

            amap[known_attr] = join

        return amap

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        """タイムイベントの通知の種類を表すコンフィギュレータの記述を生成する。"""
        raise RuntimeError("called abstract method gen_cfg_handler_type")

    def gen_cfg_handler_parameters(
        self,
        handler: Handler,
        join: Any,
        attr_map: Any,
        cell: Any,
        adpt_gen: AdapterGenerator,
    ) -> list[str] | None:
        """タイムイベントの通知の引数を表すコンフィギュレータの記述を生成する。"""
        return None

    def might_fail(self) -> bool:
        """通知の際にエラーが発生し、エラー通知を呼ぶ必要が生じうるか。"""
        return False


def _unknown_handler(handler: Handler) -> RuntimeError:
    return RuntimeError(f"unknown handler {handler}")


class BaseTaskHandlerType(BaseHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and _rhs_celltype_name_is(
            join, "tTask"
        )

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        return [_object_id_param(join)]

    def might_fail(self) -> bool:
        return True


class ActivateTaskHandlerType(BaseTaskHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(
            handler, cell, join
        ) and join.get_port_name() == sym("eiActivateNotificationHandler")

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_ACTTSK"
        if handler is ERROR_HANDLER:
            return "TENFY_ACTTSK"
        raise _unknown_handler(handler)


class WakeUpTaskHandlerType(BaseTaskHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(
            handler, cell, join
        ) and join.get_port_name() == sym("eiWakeUpNotificationHandler")

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_WUPTSK"
        if handler is ERROR_HANDLER:
            return "TENFY_WUPTSK"
        raise _unknown_handler(handler)


class SetVariableHandlerType(BaseHandlerType):
    def __init__(self) -> None:
        super().__init__()
        self.required_attributes = [SETVAR_ADDR_ATTR, SETVAR_VALUE_ATTR]

    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return (
            super().validate_join(handler, cell, join)
            and join is None
            and handler is EVENT_HANDLER
        )

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        var_addr = _subst_attr(cell, attr_map[SETVAR_ADDR_ATTR])
        var_value = _subst_attr(cell, attr_map[SETVAR_VALUE_ATTR])
        return [var_addr, var_value]

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_SETVAR"
        raise _unknown_handler(handler)


class SetVariableToErrorCodeHandlerType(BaseHandlerType):
    def __init__(self) -> None:
        super().__init__()
        self.required_attributes = [SETVAR_ADDR_ATTR]

    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return (
            super().validate_join(handler, cell, join)
            and join is None
            and handler is ERROR_HANDLER
        )

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        return [_subst_attr(cell, attr_map[SETVAR_ADDR_ATTR])]

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is ERROR_HANDLER:
            return "TENFY_SETVAR"
        raise _unknown_handler(handler)


class IncrementVariableHandlerType(BaseHandlerType):
    def __init__(self) -> None:
        super().__init__()
        self.required_attributes = [INCVAR_ADDR_ATTR]

    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and join is None

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        return [_subst_attr(cell, attr_map[INCVAR_ADDR_ATTR])]

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_INCVAR"
        if handler is ERROR_HANDLER:
            return "TENFY_INCVAR"
        raise _unknown_handler(handler)


class SignalSemaphoreHandlerType(BaseHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and _rhs_celltype_name_is(
            join, "tSemaphore"
        )

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        return [_object_id_param(join)]

    def might_fail(self) -> bool:
        return True

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_SIGSEM"
        if handler is ERROR_HANDLER:
            return "TENFY_SIGSEM"
        raise _unknown_handler(handler)


class SetEventflagHandlerType(BaseHandlerType):
    def __init__(self) -> None:
        super().__init__()
        self.required_attributes = [SETFLG_FLAG_ATTR]

    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and _rhs_celltype_name_is(
            join, "tEventflag"
        )

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        id_ = _object_id_param(join)
        flg_pattern = _subst_attr(cell, attr_map[SETFLG_FLAG_ATTR])
        return [id_, flg_pattern]

    def might_fail(self) -> bool:
        return True

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_SETFLG"
        if handler is ERROR_HANDLER:
            return "TENFY_SETFLG"
        raise _unknown_handler(handler)


class DataqueueHandlerType(BaseHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and _rhs_celltype_name_is(
            join, "tDataqueue"
        )

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        return [_object_id_param(join)]

    def might_fail(self) -> bool:
        return True


class SendToDataqueueHandlerType(DataqueueHandlerType):
    def __init__(self) -> None:
        super().__init__()
        self.required_attributes = [SNDDTQ_VALUE_ATTR]

    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and handler is EVENT_HANDLER

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        params = super().gen_cfg_handler_parameters(
            handler, join, attr_map, cell, adpt_gen
        )
        assert params is not None
        params.append(_subst_attr(cell, attr_map[SNDDTQ_VALUE_ATTR]))
        return params

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_SNDDTQ"
        raise _unknown_handler(handler)


class SendErrorCodeToDataqueueHandlerType(DataqueueHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return super().validate_join(handler, cell, join) and handler is ERROR_HANDLER

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is ERROR_HANDLER:
            return "TENFY_SNDDTQ"
        raise _unknown_handler(handler)


class UserHandlerType(BaseHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return (
            super().validate_join(handler, cell, join)
            and handler is not ERROR_HANDLER  # invalid for error handler
            and _rhs_celltype_name_is(join, "tTimeEventHandler")
        )

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is EVENT_HANDLER:
            return "TNFY_HANDLER"
        raise _unknown_handler(handler)

    def gen_cfg_handler_parameters(
        self, handler: Handler, join: Any, attr_map: Any, cell: Any, adpt_gen: Any
    ) -> list[str] | None:
        # tTimeEventHandlerの結合先を取得
        handler_cell = join.get_rhs_cell()
        call_join = handler_cell.get_join_list().get_item(sym("ciHandlerBody"))

        # 結合されていない場合はtecsgenがエラーを出すはずなのでここでは無視する．
        if not truthy(call_join):
            return []

        # アダプタ関数ハンドルを取得
        adapter_handle = adpt_gen.make_adapter_handle(call_join)
        return [adapter_handle[1], adapter_handle[0]]


class NullHandlerType(BaseHandlerType):
    def validate_join(self, handler: Handler, cell: Any, join: Any) -> bool:
        return (
            super().validate_join(handler, cell, join)
            and join is None
            and handler is not EVENT_HANDLER  # handler is mandatory for normal handler!
        )

    def gen_cfg_handler_type(self, handler: Handler) -> str | None:
        if handler is ERROR_HANDLER:
            return None
        raise _unknown_handler(handler)


HANDLER_TYPES: list[BaseHandlerType] = [
    ActivateTaskHandlerType(),
    WakeUpTaskHandlerType(),
    SetVariableHandlerType(),
    SetVariableToErrorCodeHandlerType(),
    IncrementVariableHandlerType(),
    SignalSemaphoreHandlerType(),
    SetEventflagHandlerType(),
    SendToDataqueueHandlerType(),
    SendErrorCodeToDataqueueHandlerType(),
    UserHandlerType(),
    NullHandlerType(),
]

# ドメインの所属チェックで「パターン1」（同じドメインに置く必要がある）に当たるハンドラタイプ
_SAME_DOMAIN_TYPES = (
    ActivateTaskHandlerType,
    WakeUpTaskHandlerType,
    SetVariableHandlerType,
    SetVariableToErrorCodeHandlerType,
    IncrementVariableHandlerType,
    SignalSemaphoreHandlerType,
    SetEventflagHandlerType,
    SendToDataqueueHandlerType,
    SendErrorCodeToDataqueueHandlerType,
)


class NotifierPlugin(CelltypePlugin):
    """@celltype:: Celltype / @option:: String :オプション文字列"""

    NOTIFIER_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {
        "factory": lambda obj, rhs: obj.set_factory(rhs),
        "output_file": lambda obj, rhs: obj.set_factory_output_file(rhs),
    }

    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        self._plugin_arg_check_proc_tab = NotifierPlugin.NOTIFIER_PLUGIN_ARG_PROC
        # 前後の "" を取り除く
        self._plugin_arg_str = gsub(r'\A"(.*)', r"\1", to_s(option))
        self._plugin_arg_str = sub_first(r'(.*)"\Z', r"\1", self._plugin_arg_str)
        self._factory: Any = None
        self._output_file: Any = None
        self._adpt_gen: Any = None
        self.parse_plugin_arg()
        if self._factory is None:
            self.cdl_error(
                "NTF1003 celltype $1: option factory is not specified",
                celltype.get_name(),
            )
        if self._output_file is None:
            self.cdl_error(
                "NTF1003 celltype $1: option output_file is not specified",
                celltype.get_name(),
            )

    def set_factory(self, template_string: Any) -> None:
        # Ruby 版はここで未定義のローカル変数 celltype を参照する（2回目の指定で NameError）
        if self._factory is not None:
            self.cdl_error(
                "NTF1003 celltype $1: option factory was specified more than once",
                self._celltype.get_name(),
            )
        self._factory = template_string

    def set_factory_output_file(self, output_file: Any) -> None:
        if self._output_file is not None:
            self.cdl_error(
                "NTF1003 celltype $1: option output_file was specified more than once",
                self._celltype.get_name(),
            )
        self._output_file = output_file

    def gen_factory(self, file: Any) -> None:
        from tecsgen.context import get_context
        from tecsgen.core.generate import AppFile

        kernel_cfg = AppFile.open(f"{get_context().gen}/{to_s(self._output_file)}")
        kernel_cfg.print("\n/* Generated by NotifierPlugin */\n")
        kernel_cfg.print('#include "tTimeEventHandler.h"\n')

        # アダプタ関数を生成する準備
        self._adpt_gen = AdapterGenerator(
            "tTimeEventHandler", self._celltype.get_global_name()
        )

        # 属性置換が行えることを検証する（factoryで指定された属性名が存在するか）。
        # {{attribute_name}} -> attribute_value
        for m in _ATTR_SUBST_RE.finditer(to_s(self._factory)):
            name = sym(m.group(1))

            # {{_handler_params_}} はハンドラに関する指定。プラグイン内で値が生成される
            if name == sym("_handler_params_"):
                continue

            subst_attr = self._celltype.find(name)
            if not truthy(subst_attr):
                self.cdl_error(
                    "NTF1007 celltype $1: additional_param: attribute $2 does not exist.",
                    self._celltype.get_name(),
                    name,
                )

        for cell in self._celltype.get_cell_list():
            self._gen_factory_for_cell(kernel_cfg, cell)

        # アダプタ関数の生成を完了させる
        self._adpt_gen.finish()

        kernel_cfg.close()

    def _gen_factory_for_cell(self, kernel_cfg: Any, cell: Any) -> None:
        handler_flags: list[str] = []
        handler_args: list[str] = []

        event_handler_might_fail = True
        handler_flag: Any = None

        # ignoreErrorsを取得
        ignore_errors_attr_join = cell.get_join_list().get_item(sym("ignoreErrors"))
        ignore_errors_attr = cell.get_celltype().find(sym("ignoreErrors"))
        if truthy(ignore_errors_attr_join):
            # セル生成時に初期化する場合
            ignore_errors_str = to_s(ignore_errors_attr_join.get_rhs())
        else:
            # セルタイプの初期化値を使う場合
            ignore_errors_str = to_s(ignore_errors_attr.get_initializer())
        if ignore_errors_str == "true":
            ignore_errors = True
        elif ignore_errors_str == "false":
            ignore_errors = False
        else:
            self.cdl_warning2(
                cell.get_locale(),
                "NTF1005 cell $1: unrecognized value '$2' specified for ignoreErrors",
                cell.get_name(),
                ignore_errors_str,
            )
            ignore_errors = False

        # ドメイン指定用文字列
        pre_text = ""
        post_text = "\n"
        indent = ""

        for handler in (EVENT_HANDLER, ERROR_HANDLER):
            # ドメイン指定用文字列
            pre_text = ""
            post_text = "\n"
            indent = ""

            # 呼び口の結合を取得
            call_join = cell.get_join_list().get_item(sym(handler.call_port_name))

            # ハンドラタイプを判別する
            matches = [
                ht for ht in HANDLER_TYPES if ht.validate_join(handler, cell, call_join)
            ]

            if len(matches) == 0:
                self.cdl_error2(
                    cell.get_locale(),
                    "NTF1001 cell $1: no matching handler type found for $2",
                    cell.get_name(),
                    handler.call_port_name,
                )
                continue

            # 最初に見つかった有効なハンドラタイプを使用
            ht = matches[0]

            # ドメインプラグインが指定されている場合、所属ドメインのチェック
            domain_root = cell.get_region().get_domain_root()
            domain_type = domain_root.get_domain_type()
            if truthy(domain_type):
                if domain_type.get_name() in (sym("HRP"), sym("HRMP")):
                    option = domain_type.get_option()
                    for match in matches:
                        self._check_domain(match, option, cell, call_join, domain_root)

                    if option == "kernel":
                        pre_text = "KERNEL_DOMAIN{\n"
                        post_text = "}\n"
                        indent = "  "
                    elif option != "OutOfDomain":
                        pre_text = f"DOMAIN({to_s(domain_root.get_name())}){{\n"
                        post_text = "}\n"
                        indent = "  "
                else:
                    self.cdl_error(
                        "NTF9999: NotifierPlugin: unknown domain type $1",
                        domain_root.get_domain_type().get_name(),
                    )

            class_root = cell.get_region().get_class_root()
            if truthy(class_root):
                class_type = class_root.get_class_type()
                if truthy(class_type):
                    if class_type.get_name() in (sym("FMP"), sym("HRMP")):
                        attr = class_type.get_plugin().get_PU_attr()
                        if attr[sym("class_name")] == "global":
                            self.cdl_error2(
                                cell.get_locale(),
                                "FMP9999 $1: not be placed in class region",
                                cell.get_name(),
                            )
                        else:
                            pre_text += (
                                f"{indent}CLASS({to_s(attr[sym('class_name')])}){{\n"
                            )
                            post_text = f"{indent}}}\n" + post_text
                            indent += "  "
                    else:
                        self.cdl_error(
                            "NTF9999: NotifierPlugin: unknown class type $1",
                            class_type.get_name(),
                        )
            else:
                raise RuntimeError("class root is nil")

            # 通知ハンドラで「エラーが発生するはずがない」のに「エラーハンドラが指定されている」
            # もしくはその逆のパターンを検出する。
            if (
                handler is ERROR_HANDLER
                and not isinstance(ht, NullHandlerType)
                and not event_handler_might_fail
            ):
                self.cdl_error2(
                    cell.get_locale(),
                    "NTF1004 cell $1: handler type $2 which never raises an error was inferred "
                    "for the normal notification handler, but an error notification handler was specified.",
                    cell.get_name(),
                    handler_flag,
                )
            if (
                handler is ERROR_HANDLER
                and isinstance(ht, NullHandlerType)
                and event_handler_might_fail
                and not ignore_errors
            ):
                self.cdl_warning2(
                    cell.get_locale(),
                    "NTF1006 cell $1: handler type $2 which might raise an error was inferred "
                    "for the normal notificaton handler, but an error notification handler was not specified.",
                    cell.get_name(),
                    handler_flag,
                )

            # assertion
            if not ht.validate_join(handler, cell, call_join):
                raise RuntimeError("!validate_join")

            # 通知方法の静的API記述を生成する
            handler_flag = ht.gen_cfg_handler_type(handler)
            if handler_flag is not None:
                handler_flags.append(handler_flag)

            attr_map = ht.generate_attr_map(handler, cell)

            handler_arg = ht.gen_cfg_handler_parameters(
                handler, call_join, attr_map, cell, self._adpt_gen
            )
            if handler_arg is not None:
                handler_args += handler_arg

            if handler is EVENT_HANDLER:
                event_handler_might_fail = ht.might_fail()

        # $id$等の置換
        name_array = cell.get_celltype().get_name_array(cell)
        handler_args = [
            cell.get_celltype().subst_name(e, name_array) if e == "$cbp$" else e
            for e in handler_args
        ]

        # tecsgen.cfgの記述を生成する。factoryに対し、パラメータ置換を行う。
        # {{attribute_name}} -> attribute_value
        def repl(m: re.Match[str]) -> str:
            name = sym(m.group(1))
            subst_attr = cell.get_celltype().find(name)

            # {{_handler_params_}} はハンドラの指定に置換する。
            if name == sym("_handler_params_"):
                args_joined = " | ".join(handler_flags)
                if len(handler_args) > 0:
                    args_joined += ", "
                    args_joined += ", ".join(handler_args)
                return args_joined

            if not truthy(subst_attr):
                # 属性が見つからないというエラーはすでに報告されているのでダミー値を返す。
                return ""

            subst_attr_join = cell.get_join_list().get_item(name)
            if truthy(subst_attr_join):
                # セル生成時に初期化する場合
                subst = to_s(subst_attr_join.get_rhs())
            else:
                # セルタイプの初期化値を使う場合
                subst = to_s(subst_attr.get_initializer())

            # $id$等の置換
            return cell.get_celltype().subst_name(subst, name_array)

        text = _ATTR_SUBST_RE.sub(repl, to_s(self._factory))

        # 出力 (CRE_xxx)
        kernel_cfg.print(pre_text)
        kernel_cfg.print(f"{indent}{text}\n")
        self.gen_sac(kernel_cfg, cell, indent)
        kernel_cfg.print(post_text)

    def _check_domain(
        self, match: Any, option: Any, cell: Any, call_join: Any, domain_root: Any
    ) -> None:
        """ドメインプラグイン（HRP・HRMP）指定時の、ハンドラタイプごとの所属ドメインのチェック。"""

        def other_root() -> Any:
            return call_join.get_cell().get_region().get_domain_root()

        if isinstance(match, _SAME_DOMAIN_TYPES):
            if option == "OutOfDomain":
                self.cdl_error2(
                    cell.get_locale(),
                    "NTF9999: NotifierPlugin: $1 cannot be placed out of domain",
                    cell.get_name(),
                )
            elif other_root() is None or other_root() != domain_root:
                self.cdl_error2(
                    cell.get_locale(),
                    "NTF9999: NotifierPlugin: $1 and $2 must be placed in same domain",
                    cell.get_name(),
                    call_join.get_cell().get_name(),
                )
        elif isinstance(match, UserHandlerType):
            if option != "kernel":
                self.cdl_error2(
                    cell.get_locale(),
                    "NTF9999: NotifierPlugin: $1 can be placed in kernel domain only, "
                    "because notify target is handler",
                    cell.get_name(),
                )
            elif other_root() is None or other_root() != domain_root:
                self.cdl_error2(
                    cell.get_locale(),
                    "NTF9999: NotifierPlugin: $1 and $2 must be placed in same domain",
                    cell.get_name(),
                    call_join.get_cell().get_name(),
                )
        # Ruby 版の `when NullHandlerType.new` は別インスタンスとの比較で常に偽（何もしない）

    def gen_sac(self, file: Any, cell: Any, indent: str) -> None:
        """ドメインが指定されている場合に SAC_CYC・SAC_ALM を生成する。"""
        from tecsgen.core.plugin_module import _lookup_loaded_plugin_class

        domain_root = cell.get_region().get_domain_root()
        if truthy(domain_root.get_domain_type()):
            id_ = to_s(cell.get_attr_initializer(sym("id")))
            name_array = cell.get_celltype().get_name_array(cell)
            ct_name = cell.get_celltype().get_name()
            if ct_name == sym("tCyclicNotifier"):
                obj_type = "CYC"
            elif ct_name == sym("tAlarmNotifier"):
                obj_type = "ALM"
            else:
                raise RuntimeError(
                    f"NotifierPlugin: unknown celltype {to_s(cell.get_celltype().get_name())}"
                )
            id_ = cell.get_celltype().subst_name(id_, name_array)
            domain_type_name = to_s(domain_root.get_domain_type().get_name())
            # Object.const_defined? : 読み込み済みのプラグインクラスか
            if (
                _lookup_loaded_plugin_class(domain_type_name + "DomainPlugin")
                is not None
            ):
                # HRMPDomainPlugin
                plugin_name = domain_type_name + "DomainPlugin"
            elif _lookup_loaded_plugin_class(domain_type_name + "Plugin") is not None:
                # HRPPlugin
                plugin_name = domain_type_name + "Plugin"
            else:
                raise RuntimeError(
                    f"NotifierPlugin: Unkown Domain Plugin {domain_type_name}"
                )
            pl_class = _lookup_loaded_plugin_class(plugin_name)
            file.print(
                indent,
                f"SAC_{obj_type}( {id_}, {pl_class.get_sac_str(cell)} );\n",
            )
