"""ファイルシステム・カレントディレクトリ・外部コマンドとのやりとりを1か所に集める。

Ruby 版は `File.exist?`・`Dir.chdir`・`IO.popen` などを各所で直接呼ぶ。Python 版では
それらを `Host` のメソッドにまとめ、`get_host()` で参照する。差分テストでは、Ruby 版の
記録（tests/golden/p3/）を再生する `Host` に差し替えて、移植元のテストツリーや cpp が
無い環境でも同じ入力を与える。

パスは Ruby と同じく文字列のまま扱い、`/` 区切りで連結する（`posixpath`）。
カレントディレクトリは `Host` が持つ（Ruby の `Dir.chdir` はプロセス全体に効くが、
tecsgen が cwd を使うのは import の探索だけなので、Python 版ではプロセスの cwd を変えない）。
"""

from __future__ import annotations

import os
import posixpath
import subprocess


class Host:
    """実際の OS に対して操作する。"""

    def __init__(self, cwd: str | None = None) -> None:
        self._cwd = cwd if cwd is not None else os.getcwd().replace(os.sep, "/")

    # --- カレントディレクトリ ---------------------------------------------------

    def getcwd(self) -> str:
        """Ruby の `Dir.pwd`。"""
        return self._cwd

    def chdir(self, path: str) -> None:
        """Ruby の `Dir.chdir`。無いディレクトリなら例外（`Errno::ENOENT`）。"""
        target = self.expand_path(path)
        if not self._is_directory(target):
            raise FileNotFoundError(2, "No such file or directory", path)
        self._cwd = target

    def expand_path(self, path: str) -> str:
        """Ruby の `File.expand_path`（`~` の展開は扱わない）。"""
        joined = posixpath.join(self._cwd, path)
        return posixpath.normpath(joined).replace("//", "/")

    def _abs(self, path: str) -> str:
        return path if posixpath.isabs(path) else posixpath.join(self._cwd, path)

    # --- 問い合わせ ---------------------------------------------------------

    def exists(self, path: str) -> bool:
        """Ruby の `File.exist?`。"""
        return os.path.exists(self._abs(path))

    def is_directory(self, path: str) -> bool:
        """Ruby の `File.directory?`。"""
        return self._is_directory(self._abs(path))

    def _is_directory(self, abs_path: str) -> bool:
        return os.path.isdir(abs_path)

    def listdir(self, path: str) -> list[str]:
        """Ruby の `Dir.foreach(path)` が返す名前（`.`・`..` を含む）。無ければ例外。"""
        names = os.listdir(self._abs(path))
        return [".", "..", *names]

    # --- 読み書き -----------------------------------------------------------

    def read_bytes(self, path: str) -> bytes:
        with open(self._abs(path), "rb") as f:
            return f.read()

    def write_bytes(self, path: str, data: bytes) -> None:
        with open(self._abs(path), "wb") as f:
            f.write(data)

    def mkdir(self, path: str) -> None:
        """Ruby の `Dir.mkdir`。"""
        os.mkdir(self._abs(path))

    # --- 外部コマンド ---------------------------------------------------------

    def popen_read(self, cmd: str) -> bytes:
        """Ruby の `IO.popen(cmd, "r:ASCII-8BIT")` で読める出力全体。

        Ruby と同じく、コマンドはシェル（/bin/sh）経由で実行する。起動できないときは例外。
        """
        proc = subprocess.run(
            cmd, shell=True, cwd=self._cwd, stdout=subprocess.PIPE, check=False
        )
        return proc.stdout


_host: Host | None = None


def get_host() -> Host:
    global _host
    if _host is None:
        _host = Host()
    return _host


def set_host(host: Host | None) -> None:
    """差し替える（None で既定に戻す）。テスト用。"""
    global _host
    _host = host
