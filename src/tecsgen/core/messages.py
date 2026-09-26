"""messages.rb の移植。多言語化が必要な文字列（エラーメッセージと生成ファイルのコメント）。

メッセージ表そのものは `tecsgen.messages.messages_*` にあり、`TECS_LANG.setup()` が
言語に応じて `TECSMsg.load()` で読み込む。
"""

from __future__ import annotations

import re
from types import ModuleType
from typing import ClassVar

_NUM_RE = re.compile(r"^[A-Z0-9]+", re.MULTILINE)


class TECSMsg:
    _comment: ClassVar[dict[str, str]] = {}
    _error_message: ClassVar[dict[str, str]] = {}
    _warning_message: ClassVar[dict[str, str]] = {}
    _info_message: ClassVar[dict[str, str]] = {}

    @classmethod
    def load(cls, module: ModuleType) -> None:
        """メッセージモジュールの表を取り込む（Ruby の require による @@ 変数の定義に相当）。"""
        for name in ("comment", "error_message", "warning_message", "info_message"):
            table = getattr(module, name, None)
            if table is not None:
                setattr(cls, f"_{name}", table)

    @classmethod
    def get(cls, msg: str) -> str:
        """生成するヘッダやテンプレートに含めるコメントを得る。

        Ruby 版はここで CDL の文字コードへ変換する（kconv）。Python 版は文字列を Unicode のまま
        返し、ファイルへ書き出すときに CDL の文字コードで符号化する（内部仕様10章）。
        """
        return cls._comment[msg]

    @staticmethod
    def _localize(table: dict[str, str], body: str, allow_no_num: bool) -> str:
        m = _NUM_RE.search(body)
        num = m.group(0) if m else None
        if num is None:
            if not allow_no_num:
                # Ruby 版では nil.to_sym で NoMethodError になる
                raise TypeError(f"message has no number: {body!r}")
            return body
        msg = table.get(num)
        if msg is None:
            return body
        return num + " " + msg

    @classmethod
    def get_error_message(cls, body: str) -> str:
        """ローカライズされたエラーメッセージを得る。body は "S0001 error message body" の形式。"""
        return cls._localize(cls._error_message, body, allow_no_num=True)

    @classmethod
    def get_warning_message(cls, body: str) -> str:
        return cls._localize(cls._warning_message, body, allow_no_num=False)

    @classmethod
    def get_info_message(cls, body: str) -> str:
        return cls._localize(cls._info_message, body, allow_no_num=False)
