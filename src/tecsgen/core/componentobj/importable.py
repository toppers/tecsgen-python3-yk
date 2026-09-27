"""importable.rb の移植。Import_C と Import が include するモジュール（`Importable`）。"""

from __future__ import annotations

from typing import Any

from tecsgen.context import dbg_print, get_context
from tecsgen.host import get_host
from tecsgen.ruby_compat import rb_print


class Importable:
    """@last_base_dir::String"""

    _last_base_dir: Any

    def find_file(self, file: str) -> str | None:
        """import パスからファイルを探す（見つからなければ nil）。

        Ruby 版は2段目の探索で `Dir.chdir` し、戻さない。cwd は `Host` が持つ。
        """
        ctx = get_context()
        host = get_host()
        for path in ctx.import_path:
            pt = file if path == "." else f"{path}/{file}"
            if host.exists(pt):
                cwd = host.getcwd()
                if not ctx.base_dir.get(cwd):
                    ctx.base_dir[cwd] = True
                if ctx.verbose:
                    rb_print(f"{file} is found in {path}\n")
                self._last_base_dir = None
                dbg_print(f"base_dir=. while searching {file}\n")
                return pt

        for bd in list(ctx.base_dir.keys()):
            for path in ctx.import_path:
                pt = f"{path}/{file}"
                try:
                    host.chdir(ctx.run_dir)
                    host.chdir(bd)
                    if host.exists(pt):
                        if ctx.verbose:
                            rb_print(f"{file} is found in {bd}/{path}\n")
                        self._last_base_dir = bd
                        dbg_print(f"base_dir={bd} while searching {file}\n")
                        ctx.base_dir[bd] = True
                        return pt
                except OSError:
                    pass
        self._last_base_dir = None
        dbg_print(f"base_dir=. while searching {file}\n")
        return None

    def get_base_dir(self) -> Any:
        return self._last_base_dir
