"""tool_info.rb の移植。`__tool_info__` の内容を保持し、簡易スキーマで検証する（`TOOL_INFO`）。

`__tool_info__` の内容の文法は JSON と同じ。スキーマは自家製で、検証は `TOOL_INFO.VALIDATOR` が行う。
Ruby 版の obsolete な位置情報（`Cell_location`・`Join_location`）は、このモジュールに含めない。
"""

from __future__ import annotations

import sys
from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.ruby_compat import Symbol, Y, sym, to_s, truthy


def _is_string(obj: Any) -> bool:
    """Ruby の `obj.kind_of? String`（Symbol は含まない）。"""
    return isinstance(obj, str) and not isinstance(obj, Symbol)


class VALIDATOR:  # Ruby: TOOL_INFO::VALIDATOR
    """簡易 JSON バリデータ。配列の長さは調べない（必要なら呼び出し側で調べる）。"""

    def __init__(self, name: Any, schema: dict[Any, Any]) -> None:
        self._name = name
        self._schema = schema
        self._b_ok = True

    def error(self, msg: str) -> None:
        sys.stderr.write("__tool_info__: " + msg)
        self._b_ok = False

    def validate(self) -> bool:
        info = TOOL_INFO.get_tool_info(self._name)
        if info is None:
            self.error(f'"{to_s(self._name)}" not found\n')
            return self._b_ok
        self.validate_object(info, self._name, self._name)
        return self._b_ok

    def validate_object(self, obj: Any, require_type: Any, path: Any) -> None:
        obj_type = self._schema[require_type]
        dbg_print(
            f"validate_object: {to_s(path)}  object={to_s(obj_type.get(Y.type))}  required={to_s(obj.get(Y.type))}\n"
        )

        for name, val_type in obj_type.items():
            val = obj.get(name)
            path2 = to_s(path) + "." + to_s(name)
            if val is None:
                self.error(
                    f"{to_s(path)}: required property not found '{to_s(name)}'\n"
                )
                continue
            if isinstance(val_type, list):
                self.validate_array_member(val, val_type, path2)
            else:
                self.validate_types(val, val_type, path2)

        optional = self._schema.get(sym("__" + to_s(require_type)))
        if optional is not None:
            dbg_print(f"{to_s(require_type)} has optional\n")

            for name, val_type in optional.items():
                val = obj.get(name)
                path2 = to_s(path) + "." + to_s(name)
                if val is None:
                    continue  # no need to occur error
                if isinstance(val_type, list):
                    self.validate_array_member(val, val_type, path2)
                else:
                    self.validate_types(val, val_type, path2)

    def validate_array_member(
        self, array: Any, val_types: list[Any], path: Any
    ) -> None:
        if not isinstance(array, list):
            # Ruby 版は未定義のローカル変数 path2 を参照して NameError になる
            raise NameError(  # noqa: TRY004
                "undefined local variable or method 'path2'"
            )
        index = 0
        for member in array:
            type_ = self.get_object_type(member)
            i = _find_index(val_types, type_)
            if i is None and type_ == Y.integer:
                i = _find_index(val_types, Y.number)
            if i is None:
                self.error(
                    f"{to_s(path)}: array member type mismatch, {to_s(type_)} for {to_s(val_types)}\n"
                )
                continue
            val_type = val_types[i]
            self.validate_types(member, val_type, to_s(path) + "[" + str(index) + "].")
            index += 1

    def validate_types(self, obj: Any, val_type: Any, path: Any) -> None:
        """obj:: Integer, Float, String, Hash / val_type:: Symbol (要求される型)"""
        type_ = self.get_object_type(obj)
        if val_type == Y.integer:
            if type_ == Y.integer:
                return
        elif val_type == Y.number:
            if type_ in (Y.integer, Y.number):
                return
        elif val_type == Y.string:
            if type_ == Y.string:
                return
        elif _is_string(val_type):
            # 固定文字列
            if type_ == Y.string and obj == val_type:
                return
        else:
            if type_ is None:
                raise AttributeError("undefined method 'to_sym' for nil")
            if sym(type_) == val_type:
                self.validate_object(obj, val_type, to_s(path) + to_s(val_type))
                return
        self.error(f"{to_s(path)}: type mismatch, {to_s(type_)} for {to_s(val_type)}\n")

    def get_object_type(self, obj: Any) -> Any:
        if isinstance(obj, bool):
            return None
        if isinstance(obj, int):
            return Y.integer
        if isinstance(obj, float):
            return Y.number
        if _is_string(obj):
            return Y.string
        if isinstance(obj, dict):
            t = obj.get(Y.type)
            if t is None:
                raise AttributeError("undefined method 'to_sym' for nil")
            return sym(t)
        return None


def _find_index(values: list[Any], target: Any) -> int | None:
    for i, v in enumerate(values):
        if v == target:
            return i
    return None


class TOOL_INFO:  # Ruby と同名
    VALIDATOR = VALIDATOR

    # tool_info
    _tool_info: ClassVar[dict[Any, Any]] = {}

    # tool_info schema for tecsgen
    _TECSGEN_schema: ClassVar[dict[Any, Any]] = {
        Y.tecsgen: {  # require
            Y.base_dir: [Y.string],  # dir where the cde created initially
            Y.direct_import: [Y.string],  # .cdl (sometimes .cde) specified in argments
            Y.import_path: [Y.string],  # -I of tecsgen
            Y.define_macro: [Y.string],  # -D of tecsgen
            Y.tecscde_version: Y.string,  # TECSCDE version
            Y.cde_format_version: Y.string,  # CDE format version
            Y.save_date: Y.string,  # last save date & time
        },
        sym("__tecsgen"): {  # optioanl
            Y.cpp: Y.string  # -c or TECS_CPP environment variable
        },
    }

    @classmethod
    def reset(cls) -> None:
        TOOL_INFO._tool_info = {}

    def __init__(self, name: Any, val: Any) -> None:
        TOOL_INFO._tool_info[name] = val

        # __tool_info__( "tecsgen" ): validate & reflect immediately
        if name == Y.tecsgen:
            self.set_tecsgen_tool_info()

    @classmethod
    def get_tool_info(cls, name: Any) -> Any:
        return TOOL_INFO._tool_info.get(name)

    def set_tecsgen_tool_info(self) -> None:
        """__tool_info__( "tecsgen" )"""
        from tecsgen.core.componentobj.import_cdl import Import

        ctx = get_context()
        validator = VALIDATOR(Y.tecsgen, TOOL_INFO._TECSGEN_schema)
        if validator.validate() or truthy(ctx.b_force_apply_tool_info):
            info = TOOL_INFO.get_tool_info(Y.tecsgen)
            for bd in info[Y.base_dir]:
                if bd not in ctx.base_dir:
                    ctx.base_dir[bd] = True

            for path in info[Y.import_path]:
                if path not in ctx.import_path:
                    ctx.import_path.append(path)

            for define in info[Y.define_macro]:
                if define not in ctx.define:
                    ctx.define.append(define)
            if truthy(info.get(Y.cpp)) and not ctx.b_cpp_specified:
                ctx.cpp = info[Y.cpp]
                ctx.b_cpp_specified = True

            if truthy(info.get(Y.direct_import)):
                for imp in info[Y.direct_import]:
                    Import(imp, False, False)
