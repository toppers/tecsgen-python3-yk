"""bnf.y.rb の `TECSIO` の移植（内部仕様10章）。CDL ファイルを文字コードに合わせて読む。

Ruby 版は Shift_JIS 以外のファイルを ASCII-8BIT（バイト列のまま）で読む。Python 版は
`TecsgenContext.file_codec` で復号し、`surrogateescape` で復号できないバイトを保存する。
書き出すときも同じコーデックと `surrogateescape` で符号化するので、入力のバイト列は
そのまま出力へ戻る。
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from tecsgen.context import get_context


class TECSIO:
    @staticmethod
    def foreach(file: str | Path) -> Iterator[str]:
        """ファイルを1行ずつ返す（改行文字を含む。CRLF も変換しない）。

        Ruby 版の `TECSIO.foreach(file) { |line| ... }` に当たる。
        Shift_JIS は Ruby 版と同じく Windows-31J（cp932）として読む。
        """
        codec = get_context().file_codec
        # テキストモードの newline="" は単独の CR でも行を分けてしまう。Ruby は LF だけで分けるので、
        # バイト列を LF で分けてから復号する（ASCII 互換の EUC-JP・cp932・UTF-8 では LF が文字の
        # 途中に現れないので、行単位で復号しても結果は変わらない）
        data = Path(file).read_bytes()
        start = 0
        while start < len(data):
            end = data.find(b"\n", start)
            end = len(data) if end < 0 else end + 1
            yield data[start:end].decode(codec, errors="surrogateescape")
            start = end

    @staticmethod
    def str_code_convert(msg: str, s: str) -> str:
        """msg と s の文字コードが相違する場合、s を msg の文字コードに変換する。

        Python の str は文字コードを持たないため、変換は不要で s をそのまま返す。
        エラーメッセージの組み立てで呼ばれる箇所を Ruby 版と対応させるために残している。
        """
        return s
