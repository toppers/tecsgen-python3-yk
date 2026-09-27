"""signature.rb の移植。シグニチャ（`Signature`）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import get_context, print_exception
from tecsgen.core.generate import SignatureGenerate
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.plugin_module import PluginModule, PluginNotPorted
from tecsgen.core.syntaxobj.node import NSBDNode
from tecsgen.core.tecsinfo import SignatureTECSInfo
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    class_name,
    dualmethod,
    rb_downcase,
    rb_print,
    rb_puts,
    sym,
    to_s,
    truthy,
)


class Signature(SignatureTECSInfo, SignatureGenerate, PluginModule, NSBDNode):  # < Nestable
    """@name:: Symbol / @global_name:: Symbol
    @function_head_list:: NamedList : FuncHead のインスタンスが要素
    @func_name_to_id::  {String}  :  関数名を添字とする配列で id を記憶する（1から始まる）
    @context:: string : コンテキスト名 / @b_callback:: bool / @b_deviate:: bool
    @b_checked_as_allocator_signature:: bool / @b_empty:: Bool
    @descriptor_list:: nil | { Signature => ParamDecl }  最後の ParamDecl しか記憶しないことに注意
    @generate:: [ Symbol, String, Plugin ]  = [ PluginName, option, Plugin ]
    """

    _nest_stack_index: ClassVar[int] = -1
    _nest_stack: ClassVar[list[Any]] = []
    _current_object: ClassVar[Any] = None
    _set_descriptor_list: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        Signature._nest_stack_index = -1
        Signature._nest_stack = []
        Signature._current_object = None
        Signature._set_descriptor_list = {}

    @classmethod
    def push(cls) -> None:
        Signature._nest_stack_index += 1
        _set_at(
            Signature._nest_stack,
            Signature._nest_stack_index,
            Signature._current_object,
        )
        Signature._current_object = None

    @classmethod
    def pop(cls) -> None:
        Signature._current_object = _get_at(
            Signature._nest_stack, Signature._nest_stack_index
        )
        Signature._nest_stack_index -= 1
        if Signature._nest_stack_index < -1:
            raise RubyRuntimeError("TooManyRestore")

    @classmethod
    def get_current(cls) -> Any:
        """STAGE: P（parse 中のみ呼び出される）。"""
        return Signature._current_object

    def __init__(self, name: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.generator import Generator

        super().__init__()
        self._name = name
        Namespace.new_signature(self)
        self.set_namespace_path()  # @NamespacePath の設定
        if to_s(Namespace.get_global_name()) == "":
            self._global_name = self._name
        else:
            self._global_name = sym(
                f"{to_s(Namespace.get_global_name())}_{to_s(self._name)}"
            )

        self._func_name_to_id: dict[Any, Any] = {}
        self._context: Any = None
        self._b_callback = False
        self._b_deviate = False
        self._b_empty = False
        self._b_checked_as_allocator_signature = False
        self._descriptor_list: Any = None
        self._generate: Any = None
        Signature._current_object = self
        self.set_specifier_list(Generator.get_statement_specifier())

    def end_of_parse(self, function_head_list: Any) -> Signature:
        """STAGE: B"""
        self._function_head_list = function_head_list

        # id を割付ける
        fid = 1
        for f in function_head_list.get_items():
            self._func_name_to_id[f.get_name()] = fid
            f.set_owner(self)
            fid += 1
        if fid == 1:
            self._b_empty = True

        if truthy(self._generate):
            self.signature_plugin()

        Signature._current_object = None
        return self

    def set_specifier_list(self, spec_list: Any) -> None:
        """signature の指定子を設定（STAGE: B）。spec_list:: [ [ :CONTEXT,  String ], ... ]"""
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        if spec_list is None:  # 空ならば何もしない
            return

        for s in spec_list:
            s0 = s[0]  # statement_specifier
            if s0 == Y.CALLBACK:
                self._b_callback = True
            elif s0 == Y.CONTEXT:  # [context("non-task")] etc
                if truthy(self._context):
                    self.cdl_error("S1001 context specifier duplicate")
                self._context = CDLString.remove_dquote(s[1])
                if self._context not in ("non-task", "task", "any"):
                    self.cdl_warning(
                        "W1001 '$1': unknown context type. usually specifiy task, non-task or any",
                        self._context,
                    )
            elif s0 == Y.DEVIATE:
                self._b_deviate = True
            elif s0 == Y.GENERATE:
                if truthy(self._generate):
                    self.cdl_error("S9999 generate specifier duplicate")
                self._generate = [s[1], s[2]]  # [ PluginName, "option" ]
            else:
                self.cdl_error("S1002 '$1': unknown specifier for signature", s0)

    def get_name(self) -> Any:
        return self._name

    def get_global_name(self) -> Any:
        return self._global_name

    def get_function_head_array(self) -> Any:
        if truthy(self._function_head_list):
            return self._function_head_list.get_items()
        return None

    def get_function_head(self, func_name: Any) -> Any:
        return self._function_head_list.get_item(sym(func_name))

    def get_id_from_func_name(self, func_name: Any) -> Any:
        """関数名から signature 内の id を得る。"""
        return self._func_name_to_id.get(func_name)

    def get_context(self) -> Any:
        """context 文字列を返す（未指定時のデフォルトとして task を返す）。"""
        if truthy(self._context):
            return self._context
        return "task"

    def each_param(self, pr: Any) -> None:
        """signaure のすべての関数のすべてのパラメータをたどる。pr(func_decl, param_decl)"""
        fha = self.get_function_head_array()
        if fha is None:  # nil なら文法エラーで有効値が設定されなかった
            return
        for fh in fha:
            fd = fh.get_declarator()
            if fd.is_function():  # fd が関数でなければ、すでにエラー
                for par in fd.get_type().get_paramlist().get_items():
                    pr(fd, par)

    def is_allocator(self) -> bool:  # Ruby: is_allocator?
        """正当なアロケータ シグニチャかテストする。"""
        from tecsgen.core.cdl_types import IntType, PtrType
        from tecsgen.core.syntaxobj.paramdecl import ParamDecl

        # 一回だけチェックする
        if self._b_checked_as_allocator_signature is True:
            return True
        self._b_checked_as_allocator_signature = True

        fha = self.get_function_head_array()
        if fha is None:
            return False

        def p(params: list[Any], i: int) -> Any:
            return params[i] if i < len(params) else None

        found_alloc = False
        found_dealloc = False
        for fh in fha:
            fd = fh.get_declarator()
            if fd.is_function():
                func_name = sym(fd.get_name())
                if func_name == Y.alloc:
                    found_alloc = True
                    params = fd.get_type().get_paramlist().get_items()
                    if truthy(params):
                        p0, p1 = p(params, 0), p(params, 1)
                        if (
                            type(p0) is not ParamDecl
                            or not isinstance(
                                p0.get_type().get_original_type(), IntType
                            )
                            or p0.get_direction() != Y.IN
                        ):
                            # 第一引数が int 型でない
                            if (
                                type(p0) is not ParamDecl
                                or not isinstance(p0.get_type(), PtrType)
                                or not isinstance(p0.get_type().get_type(), PtrType)
                                or isinstance(
                                    p0.get_type().get_type().get_type(), PtrType
                                )
                                or p0.get_direction() != Y.OUT
                            ):
                                # 第一引数がポインタ型でもない
                                self.cdl_error3(
                                    self._locale,
                                    "S1003 $1: 'alloc' 1st parameter neither [in] integer type nor [out] double pointer type",
                                    self._name,
                                )
                        elif (
                            type(p1) is not ParamDecl
                            or not isinstance(p1.get_type(), PtrType)
                            or not isinstance(p1.get_type().get_type(), PtrType)
                            or isinstance(p1.get_type().get_type().get_type(), PtrType)
                            or p0.get_direction() != Y.IN
                        ):
                            # (第一引数が整数で) 第二引数がポインタでない
                            self.cdl_error3(
                                self._locale,
                                "S1004 $1: 'alloc' 2nd parameter not [in] double pointer",
                                self._name,
                            )
                    else:
                        self.cdl_error3(
                            self._locale,
                            "S1005 $1: 'alloc' has no parameter, unsuitable for allocator signature",
                            self._name,
                        )
                elif func_name == Y.dealloc:
                    found_dealloc = True
                    params = fd.get_type().get_paramlist().get_items()
                    if truthy(params):
                        p0 = p(params, 0)
                        if (
                            type(p0) is not ParamDecl
                            or not isinstance(p0.get_type(), PtrType)
                            or isinstance(p0.get_type().get_type(), PtrType)
                            or p0.get_direction() != Y.IN
                        ):
                            self.cdl_error3(
                                self._locale,
                                "S1006 $1: 'dealloc' 1st parameter not [in] pointer type",
                                self._name,
                            )
                    else:
                        self.cdl_error3(
                            self._locale,
                            "S1008 $1: 'dealloc' has no parameter, unsuitable for allocator signature",
                            self._name,
                        )
                if found_alloc and found_dealloc:
                    return True
        if not found_alloc:
            self.cdl_error3(
                self._locale,
                "S1009 $1: 'alloc' function not found, unsuitable for allocator signature",
                self._name,
            )
        if not found_dealloc:
            self.cdl_error3(
                self._locale,
                "S1010 $1: 'dealloc' function not found, unsuitable for allocator signature",
                self._name,
            )
        return False

    def signature_plugin(self) -> None:
        """シグニチャプラグイン (generate 指定子)。"""
        plugin_name = self._generate[0]
        option = self._generate[1]
        self.apply_plugin(plugin_name, option)

    def apply_plugin(self, plugin_name: Any, option: Any) -> None:
        if self.is_empty():
            self.cdl_warning(
                "S9999 $1 is empty. cannot apply signature plugin. ignored", self._name
            )
            return

        pl_class = self.load_plugin(plugin_name, "SignaturePlugin")
        if pl_class is None:
            return
        if get_context().verbose:
            rb_print(
                f"new through: plugin_object = {class_name(type(pl_class))}.new( "
                f"{to_s(self._name)}, {to_s(option)} )\n"
            )

        plugin_object = None
        try:
            plugin_object = pl_class(self, option)
            plugin_object.set_locale(self._locale)
        except PluginNotPorted:
            raise
        except Exception as evar:  # noqa: BLE001  Ruby の rescue Exception
            self.cdl_error("S1150 $1: fail to new", plugin_name)
            print_exception(evar)
        self.generate_and_parse(plugin_object)

    def get_descriptor_list(self) -> Any:
        """引数で参照されている Descriptor 型のリスト（{ Signature => ParamDecl }）。

        post_code.cdl (ジェネレータ生成) で生成、または import されたシグニチャには
        Signature.set_descriptor_list で設定されないので、読み出し時に、オンデマンドで設定する。
        """
        if self._descriptor_list is None:
            self.set_descriptor_list()
        return self._descriptor_list

    @dualmethod
    def set_descriptor_list(cls) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        def visit(sig: Any) -> None:
            if Signature._set_descriptor_list.get(sig) is None:
                Signature._set_descriptor_list[sig] = True
                sig.set_descriptor_list()

        Namespace.get_root().travers_all_signature(visit)

    @set_descriptor_list.instance
    def set_descriptor_list(self) -> dict[Any, Any]:
        """引数で参照されている Descriptor 型のリストを作成する。"""
        from tecsgen.core.cdl_types import DescriptorType, PtrType

        desc_list: dict[Any, Any] = {}
        fha = self.get_function_head_array()
        if fha is None:  # nil の場合、自己参照によるケースと仮定
            self._descriptor_list = desc_list
            return desc_list
        for fh in fha:
            fd = fh.get_declarator()
            if fd.is_function():
                params = fd.get_type().get_paramlist().get_items()
                if truthy(params):
                    for param in params:
                        t = param.get_type().get_original_type()
                        while isinstance(t, PtrType):
                            t = t.get_referto()
                        if isinstance(t, DescriptorType):
                            desc_list[t.get_signature()] = param
                            d = param.get_direction()
                            if d != Y.IN and d != Y.OUT and d != Y.INOUT:
                                self.cdl_error(
                                    "S9999 Descriptor argument '$1' cannot be specified for $2 parameter",
                                    param.get_name(),
                                    rb_downcase(d),
                                )
        self._descriptor_list = desc_list
        return desc_list

    def has_descriptor(self) -> bool:  # Ruby: has_descriptor?
        """引数に Descriptor があるか？"""
        dl = self.get_descriptor_list()
        if dl is None:
            # end_of_parse が呼び出される前に has_descriptor? が呼び出された
            return True
        return len(dl) > 0

    def is_callback(self) -> Any:  # Ruby: is_callback?
        return self._b_callback

    def is_deviate(self) -> Any:  # Ruby: is_deviate?
        return self._b_deviate

    def is_empty(self) -> Any:  # Ruby: is_empty?
        return self._b_empty

    def need_PPAllocator(self, b_opaque: bool = False) -> bool:
        """Push Pop Allocator が必要か？"""
        fha = self.get_function_head_array()
        for fh in fha:
            fd = fh.get_declarator()
            if fd.get_type().need_PPAllocator(b_opaque):
                self._b_need_PPAllocator = True
                return True
        return False

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"Signature: name: {to_s(self._name)} context: {to_s(self._context)} "
            f"deviate : {to_s(self._b_deviate)} PPAllocator: {to_s(self.__dict__.get('_b_PPAllocator'))} "
            f"#<Signature>"
        )
        rb_print("  " * (indent + 1))
        rb_puts(f"namespace_path: {to_s(self._NamespacePath)}")
        rb_print("  " * (indent + 1))
        rb_puts("function head list:")
        self._function_head_list.show_tree(indent + 2)
