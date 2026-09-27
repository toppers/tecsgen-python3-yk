"""Python 版のモデルを、Ruby 版オラクル（tests/ruby/p3_oracle.rb）と同じ形式でダンプし、比べる。

形式は p3_oracle.rb の冒頭のコメントを参照。Python 版の対応:

- インスタンス変数 `@x` ↔ 属性 `_x`（P1 以来の命名規約）。`_py_` で始まる属性は Python 版だけの
  補助なので含めない。`_` で始まらない属性も含めない
- クラス変数 `@@x` ↔ クラス属性 `_x`（そのクラスの `__dict__` にあるもの）
- クラス名は Ruby の名前にそろえる（`RUBY_NAME` を持つクラスはそれを使う。`CLASS_NAMES` も参照）

比較（`compare`）は構造で行う。オブジェクトの番号は出現順に振られるので、片方にだけ属性が
あると以降の番号がずれる。そこで両方を同時に辿り、対応するオブジェクトの組を覚えながら比べる。
値が nil の属性は、無い属性と同じに扱う（Ruby は代入した時点で変数ができるが、Python 版は
`__init__` でまとめて初期化することがあるため）。
"""

from __future__ import annotations

import math
import sys
from typing import Any

from tecsgen.ruby_compat import Symbol

# Python 版のクラス名 → Ruby 版のクラス名（名前が違うもの）
CLASS_NAMES: dict[str, str] = {
    "CdlParser": "Generator",
    "CdeclParser": "C_parser",
}

# クラス変数を比べないクラス（Python 版だけのクラスや、Ruby 版で比べていないもの）
SKIP_CV_CLASSES = frozenset({"CdlParser", "TECSMsg", "TECS_LANG"})


def ruby_class_name(cls: type) -> str:
    name = cls.__dict__.get("RUBY_NAME")
    if isinstance(name, str):
        return name
    return CLASS_NAMES.get(cls.__name__, cls.__name__)


def _is_parser(obj: Any) -> bool:
    from tecsgen.syntax.racc_runtime import RaccParser

    return isinstance(obj, RaccParser)


def _is_model(obj: Any) -> bool:
    return type(obj).__module__.startswith("tecsgen.")


def _ruby_str(s: str) -> str:
    """Python の文字列を、オラクルと同じ「バイト列を latin-1 で読んだ文字列」にする。

    CDL から読んだ文字列はファイルの文字コード（Shift_JIS なら cp932）で復号しているので、
    同じ文字コードで符号化してバイト列に戻す。
    """
    from tecsgen.context import get_context

    try:
        data = s.encode(get_context().file_codec, "surrogateescape")
    except UnicodeEncodeError:
        data = s.encode("utf-8", "surrogateescape")
    return data.decode("latin-1")


class Dumper:
    def __init__(self) -> None:
        self._seen: dict[int, int] = {}
        self._keep: list[Any] = []  # id() の再利用を防ぐ

    def dump(self, v: Any) -> Any:
        if v is None or isinstance(v, bool):
            return v
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            if math.isnan(v):
                return {"f": "NaN"}
            if math.isinf(v):
                return {"f": "Infinity" if v > 0 else "-Infinity"}
            return {"f": v}
        if isinstance(v, Symbol):
            return {"y": _ruby_str(v)}
        if isinstance(v, str):
            return _ruby_str(v)
        if isinstance(v, (list, tuple)):
            return [self.dump(e) for e in v]
        if isinstance(v, dict):
            return {"h": [[self.dump(k), self.dump(e)] for k, e in v.items()]}
        if isinstance(v, type):
            return {"cls": ruby_class_name(v)}
        return self.dump_object(v)

    def dump_object(self, v: Any) -> Any:
        name = ruby_class_name(type(v))
        if _is_parser(v) or not _is_model(v):
            return {"c": name}
        if id(v) in self._seen:
            return {"ref": self._seen[id(v)]}
        self._seen[id(v)] = len(self._seen)
        self._keep.append(v)
        ivars = instance_variables(v)
        iv: dict[str, Any] = {}
        for key in sorted(ivars):
            iv[key] = self.dump(ivars[key])
        return {"c": name, "iv": iv}


def instance_variables(obj: Any) -> dict[str, Any]:
    """Ruby のインスタンス変数に当たる属性（名前は先頭の _ を除いたもの）。

    __slots__ で属性を持つクラス（Token）は、スロット名をそのまま Ruby の変数名とする。
    """
    if not hasattr(obj, "__dict__"):
        return {n: getattr(obj, n) for n in type(obj).__slots__}
    names = {}
    for key, value in vars(obj).items():
        if key.startswith("_") and not key.startswith(("_py_", "__")):
            names[key[1:]] = value
    return names


def class_vars(cls: type) -> dict[str, Any]:
    result = {}
    for key, value in cls.__dict__.items():
        if not key.startswith("_") or key.startswith(("__", "_py_")):
            continue
        is_method = isinstance(value, (classmethod, staticmethod, property))
        if (is_method or callable(value)) and not isinstance(value, type):
            continue
        result[key[1:]] = value
    return result


def model_classes() -> list[type]:
    """読み込まれている tecsgen のクラス（Ruby 名の順）。"""
    seen: dict[int, type] = {}
    for mod_name, mod in list(sys.modules.items()):
        if not mod_name.startswith("tecsgen.") or mod is None:
            continue
        for obj in vars(mod).values():
            if isinstance(obj, type) and obj.__module__ == mod_name:
                seen[id(obj)] = obj
                for inner in vars(obj).values():
                    if isinstance(inner, type) and inner.__module__ == mod_name:
                        seen[id(inner)] = inner
    return sorted(seen.values(), key=ruby_class_name)


def dump_model(root: Any) -> dict[str, Any]:
    d = Dumper()
    top = d.dump(root)
    cv: dict[str, Any] = {}
    for cls in model_classes():
        if cls.__name__ in SKIP_CV_CLASSES:
            continue
        cvars = class_vars(cls)
        if not cvars:
            continue
        cv[ruby_class_name(cls)] = {k: d.dump(cvars[k]) for k in sorted(cvars)}
    return {"root": top, "cv": cv}


# --- 比較 -------------------------------------------------------------------


def _index_objects(doc: Any) -> dict[int, dict[str, Any]]:
    """ダンプの中のオブジェクトに、出現順（前順）の番号を振る。"""
    table: dict[int, dict[str, Any]] = {}

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            if "c" in x and "iv" in x:
                table[len(table)] = x
                for v in x["iv"].values():
                    walk(v)
                return
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(doc["root"])
    walk(doc["cv"])
    return table


class Comparer:
    def __init__(self, ruby: dict[str, Any], py: dict[str, Any], limit: int = 20):
        self._r_objs = _index_objects(ruby)
        self._p_objs = _index_objects(py)
        self._r_ids = {id(o): n for n, o in self._r_objs.items()}
        self._p_ids = {id(o): n for n, o in self._p_objs.items()}
        self._pair: dict[int, int] = {}
        self.diffs: list[str] = []
        self._limit = limit
        self._ruby = ruby
        self._py = py

    def run(self) -> list[str]:
        self._cmp(self._ruby["root"], self._py["root"], "root")
        r_cv, p_cv = self._ruby["cv"], self._py["cv"]
        for cls in sorted(set(r_cv) | set(p_cv)):
            if cls not in p_cv:
                self._diff(f"cv.{cls}", "class variables missing in Python")
                continue
            if cls not in r_cv:
                self._diff(f"cv.{cls}", "class variables only in Python")
                continue
            self._cmp_ivars(r_cv[cls], p_cv[cls], f"cv.{cls}")
        return self.diffs

    def _diff(self, path: str, msg: str) -> None:
        if len(self.diffs) < self._limit:
            self.diffs.append(f"{path}: {msg}")

    def _obj(
        self, x: Any, table_ids: dict[int, int], objs: dict[int, Any]
    ) -> tuple[int, Any] | None:
        if isinstance(x, dict) and "ref" in x:
            return x["ref"], objs[x["ref"]]
        if isinstance(x, dict) and "iv" in x:
            return table_ids[id(x)], x
        return None

    def _cmp_ivars(self, r: dict[str, Any], p: dict[str, Any], path: str) -> None:
        keys = sorted(set(r) | set(p))
        for k in keys:
            rv, pv = r.get(k), p.get(k)
            if k not in p and rv is not None:
                self._diff(f"{path}.{k}", "missing in Python")
            elif k not in r and pv is not None:
                self._diff(f"{path}.{k}", f"only in Python: {_short(pv)}")
            else:
                self._cmp(rv, pv, f"{path}.{k}")

    def _cmp(self, r: Any, p: Any, path: str) -> None:
        if len(self.diffs) >= self._limit:
            return
        ro = self._obj(r, self._r_ids, self._r_objs)
        po = self._obj(p, self._p_ids, self._p_objs)
        if ro is not None or po is not None:
            if ro is None or po is None:
                self._diff(path, f"ruby={_short(r)} python={_short(p)}")
                return
            (rn, rd), (pn, pd) = ro, po
            if rn in self._pair:
                if self._pair[rn] != pn:
                    self._diff(
                        path,
                        f"object identity differs (ruby #{rn} {rd['c']}, python #{pn} {pd['c']})",
                    )
                return
            self._pair[rn] = pn
            if rd["c"] != pd["c"]:
                self._diff(path, f"class ruby={rd['c']} python={pd['c']}")
                return
            self._cmp_ivars(rd["iv"], pd["iv"], f"{path}<{rd['c']}>")
            return
        if isinstance(r, list) and isinstance(p, list):
            if len(r) != len(p):
                self._diff(
                    path,
                    f"length ruby={len(r)} python={len(p)}: ruby={_short(r)} python={_short(p)}",
                )
            for i, (a, b) in enumerate(zip(r, p, strict=False)):
                self._cmp(a, b, f"{path}[{i}]")
            return
        if isinstance(r, dict) and isinstance(p, dict) and "h" in r and "h" in p:
            if len(r["h"]) != len(p["h"]):
                rk = [_short(k) for k, _ in r["h"]]
                pk = [_short(k) for k, _ in p["h"]]
                self._diff(
                    path,
                    f"hash size ruby={len(rk)} python={len(pk)}: ruby keys={rk[:8]} python keys={pk[:8]}",
                )
            for i, ((rk, rv), (pk, pv)) in enumerate(zip(r["h"], p["h"], strict=False)):
                self._cmp(rk, pk, f"{path}{{key {i}}}")
                self._cmp(rv, pv, f"{path}[{_short(rk)}]")
            return
        if type(r) is not type(p) or r != p:
            self._diff(path, f"ruby={_short(r)} python={_short(p)}")


def _short(x: Any, n: int = 120) -> str:
    s = repr(x)
    return s if len(s) <= n else s[: n - 3] + "..."


def compare(ruby: dict[str, Any], py: dict[str, Any], limit: int = 20) -> list[str]:
    return Comparer(ruby, py, limit).run()
