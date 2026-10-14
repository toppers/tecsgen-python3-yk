"""Ruby の例外メッセージの再現（tcflow が `fatal error: ...` として出力する文言）。"""

from __future__ import annotations

import errno


def ruby_open_message(exc: OSError, path: str) -> str:
    """Ruby の `Errno::*` の message（`File.open`・`File.write` の失敗）。

    path は Ruby 版が表示する、呼び出し側が渡したままのパス（絶対パスにしない）。
    """
    reason = {
        errno.ENOENT: "No such file or directory",
        errno.EACCES: "Permission denied",
    }.get(exc.errno or 0, exc.strerror or "Input/output error")
    return f"{reason} @ rb_sysopen - {path}"


def open_error(exc: OSError, path: str) -> OSError:
    """`exc` を、Ruby と同じメッセージを持つ OSError にして返す（`raise open_error(e, p) from e`）。"""
    return OSError(ruby_open_message(exc, path))
