# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Port of tecsgen (the TECS component description compiler, Ruby v1.9.1) to Python 3. The acceptance criterion is **byte-for-byte identical output to the Ruby version** for the same input: generated files under `gen/`, stdout, and exit status. The CLI must stay fully compatible with Ruby's. Code comments, docstrings, and docs are written in Japanese; keep that convention.

Porting proceeds in phases P1–P5 (messages → parser → model/semantic analysis → optimize/codegen → plugins). Test files and commit subjects are tagged with the phase (`test_p3_model.py`, `feat: ... (P5i)`). P5 (plugins) is in progress, one plugin family per commit. Status as of 2026-10-01: the standard plugins that have golden data are ported (P5j), and so are the kernel-dependent plugins (HRP, FMP, HRMP, HRP2, ATK1Event; P5l–P5p). `uv run python tools/port/p4_progress.py` shows 119/119 (no plugin) and 34/46 (plugin) cases matching, including all 11 kernel cases (`tests/golden/kernel/`); the rest wait for `-L` user plugins and a few output differences. Plugins without golden data (HRP2 kernel objects other than Task/Handler/Object, HRP2/HRP RPC and SVC, `lib/GenHRP2Marshaler`, ...) are not ported; `ATK1EventPlugin`'s output is empty for its only input. See `tools/golden/README.md` and the progress log in the Vault (`tecsgen-python3移植計画 — P5 進捗ログ`).

## 移植の基本方針

1. **正解は Ruby 版の実行結果**。移植の受入基準は、同じ入力に対して `gen/` 以下の生成物がバイト単位で一致し、エラー／警告コード・件数・終了コードも一致すること（[[tecsgen-python3外部仕様]] 4章・7章の一致要件）。
2. **差分テストを先に作る**。Ruby 4.0.6 はローカルで動く（2026-09-26 確認）。`test/` のケース（一覧は157ケース、採取できたのは155ケース。採取しなかった2件は `import_C/z` と `mruby`）を Ruby 版で実行し、ゴールデン出力として固定してから移植を始める。TOPPERS カーネルの CDL を使うカーネル依存プラグインのケースは、別に `tests/golden/kernel/` に11ケースを採取している。
3. **フェーズごとに内部状態を比べる**。生成物の一致だけを見ると、どのフェーズでずれたかが分からない。Ruby 側に小さな JSON ダンプ用フックを足し、パース後・意味解析後・最適化後のモデルを Python 側と比べる。
4. **仕様書は実装の少し前に書く**。[[tecsgen-python3内部仕様]] は章ごとに、該当フェーズに着手する直前に書く。12章を全部書いてから実装に入る進め方はとらない。
5. **WSL での検証は必ず `tools/port/wsl_check.ps1` で行う**（2026-09-28 ユーザー採用）。`wsl.exe -e bash -lc "..."` をその場で手書きしない。このスクリプトは、WSL 用の仮想環境の分離（`~/.venvs/tecsgen-python3`）、`VIRTUAL_ENV` の解除、パス変換、`uv sync`・ruff・ty・pytest の一括実行と結果のまとめ表示を済ませている。各フェーズの計画には「完了時に `pwsh tools/port/wsl_check.ps1` を通す」を検証手順として入れる。スクリプトに無い操作（例: WSL で `tools/port/p4_progress.py` を回す、特定ケースだけ実行する）が必要になったら、手書きで済ませずにスクリプトへオプションとして足してから使い、README の表も更新する。
   - 経緯: P5e〜P5i のセッションで、このスクリプトの存在を見落として WSL コマンドを毎回手書きし、Windows 側と共有の `.venv` を作り直させて1回失敗、さらに場当たりの別の仮想環境（`~/.cache/tecsgen-python3-venv`）まで作った。

## Commands

```sh
uv sync
uv run pytest                                   # all tests
uv run pytest "tests/test_p4_gen.py::test_generated_files_match_ruby[ErrorCase/attribute-err]"  # one golden case
uv run ruff check . && uv run ruff format --check .
uv run ty check                                 # type checker (not mypy)

# Per-case match status for non-plugin AND plugin cases (Ruby not needed; replays P3 records)
uv run python tools/port/p4_progress.py [case-id-prefix...] [-v]
```

`tests/test_p4_gen.py` skips cases that use plugins, so **plugin work is verified with `p4_progress.py`** (e.g. `p4_progress.py multiplugin/ -v` shows differing files and stdout diffs).

Golden data was captured on Linux, so the authoritative full check runs in WSL with a separate venv (`~/.venvs/tecsgen-python3`; never let WSL rebuild the Windows `.venv`):

```powershell
pwsh tools/port/wsl_check.ps1                          # uv sync, ruff, ruff format --check, ty, pytest
pwsh tools/port/wsl_check.ps1 -PytestArgs tests/test_p2_parser.py, -x
pwsh tools/port/wsl_check.ps1 -Oracle <Ruby source working copy>  # re-record Ruby oracle first (needs Ruby)
pwsh tools/port/wsl_check.ps1 -KernelGolden <Ruby source working copy>    # instead of tests: collect tests/golden/kernel/ (kernel plugins; ~10 min)
pwsh tools/port/wsl_check.ps1 -KernelGolden <Ruby source working copy> -KernelP3   # instead: re-record tests/golden/kernel/p3/ (Ruby I/O replayed by p4_progress.py; checks the output equals the committed golden data; ~30 min)
pwsh tools/port/wsl_check.ps1 -PluginCoverage <Ruby source working copy>  # instead of tests: measure which plugins the golden cases run (20-40 min)
```

To collect only some kernel cases, pass the arguments as an array through `-PytestArgs`, calling the script from a PowerShell session (`& ./tools/port/wsl_check.ps1 -KernelGolden <wc> -PytestArgs '--case','atk1/*'`). Writing `--case` directly after `-KernelGolden` never reaches `collect_kernel.py`, so every case is recollected; a child `pwsh` with `--case,'x'` passes it as one string and fails.

Pass/skip counts differ slightly between Windows and WSL; commit messages report both.

## Architecture

**Porting fidelity is the design principle.** Python modules mirror Ruby files (`core/tecsgen.py` ← `core/tecsgen.rb`, `plugin/RPCPlugin.py` ← `RPCPlugin.rb`), keeping Ruby names (plugin modules are CamelCase, hence the `N999` ruff ignore). Module docstrings cite the Ruby source and the internal spec chapter (「内部仕様N章」). When porting, reproduce Ruby semantics exactly rather than idiomatic Python.

- `ruby_compat.py` — Ruby builtins needed for byte-identical output: `truthy` (only nil/false are falsy), `to_s`, `sub_first`/`gsub` (Ruby replacement-string rules), `Symbol`/`sym` (distinct from `str` as hash keys), `rb_print`/`rb_puts` (write bytes, always LF), numeric conversion. Use these instead of plain Python truthiness/str/re.
- `context.py` — Ruby global variables (`$force_overwrite`, `$KCONV_CDL`, …) collected into `TecsgenContext`, accessed via `get_context()`. Attribute name = Ruby variable name in snake_case. Add new globals here when a phase needs them.
- `host.py` — all filesystem / cwd / subprocess access (`File.exist?`, `Dir.chdir`, `IO.popen` for cpp) goes through `get_host()`. Paths are POSIX strings; the process cwd is never changed. Tests swap in `RecordedHost` (`tests/p3_oracle_data.py`), which replays Ruby's recorded I/O, so tests run on Windows without Ruby, the source tree, or gcc. **Never touch the filesystem directly** — it will pass locally but break replay.
- `state.py` — `reset_model_state()` resets Ruby class variables (`@@...`) so many tecsgen runs can share one process (tests). Any new class with class-level state needs a `reset()` registered here; plugins are reset only if already imported (they must not be force-imported, or model comparisons see extra loaded classes). Ruby's load-time side effects of `require`-ing a plugin go in a per-run `on_load()`.
- `cli.py` → `core/tecsgen.py` (`TECSGEN.run1`: parse + semantic analysis; `run2`/`finalize`: optimize + codegen). `ruby_optparse.py` reproduces Ruby OptionParser behavior/messages.
- `syntax/` — lexers ported from Ruby; parsers are driven by LALR tables **extracted from Ruby's racc output** (`cdl_tables.py`, `cdecl_tables.py`, generated) through a port of the racc runtime (`racc_runtime.py`), so syntax-error positions, counts, and recovery match Ruby. Grammar actions are hand-ported in `cdl_actions.py` / `cdecl_actions.py`.
- `core/` — type system, expressions, `syntaxobj/` (declaration nodes), `componentobj/` (Celltype, Cell, Signature, Namespace, Join, Import/Import_C, …), and code generation (`generate_celltype*.py`, templates embedded as in Ruby).
- `core/plugin_module.py` — plugin loading: Ruby's `require` + `const_get` becomes `importlib.import_module("tecsgen.plugin.<Name>")` and the same-named class. Unported plugins raise `PluginNotPorted`.
- `plugin/` — ported plugins; `plugin/lib/` holds their helper modules.

Generated files — regenerate with the tools, don't hand-edit: `messages/*` (`tools/port/gen_messages.py`), `syntax/*_tables.py` (`tools/port/gen_racc_tables.py`). These tools need Ruby and the Ruby source.

## Test data

- `tests/golden/cases/<id>/` — Ruby outputs per case (`files/`, stdout, status). Captured in WSL per `tools/golden/README.md`; case list in `tools/golden/cases.toml`. `.gitattributes` marks `tests/golden/**` as `-text`: never let line endings be converted.
- `tests/golden/kernel/cases/<id>/` — Ruby outputs for the kernel-dependent plugins (HRP: hrp3+tecs, FMP: fmp3+tecs, HRMP: hrmp3+tecs, HRP2: ev3rt+tecs, ATK1: atk1+tecs; 11 cases). Collected by `tools/golden/collect_kernel.py` with `cases_kernel.toml`, using the port-source tecsgen (r3304) in place of each repository's bundled one and `arm-none-eabi-gcc` as the C preprocessor (ATK1 uses host `gcc -E -D NC30`; see the comments in `cases_kernel.toml`). `meta.json` records the tecsgen call in `tecsgen_args`; `environment.json` records the toolchain and revisions. Known limits: hrp2+tecs' own sample1 stops at a G1016 syntax error (old region syntax), and `ATK1EventPlugin` produces empty output because the only input has no event cells. `tests/golden/kernel/p3/<id>.jsonl.gz` holds the Ruby I/O recording for each case (case id `kernel/<id>`); `tools/port/p4_progress.py` replays it (`tests/p3_oracle_data.case_ids(include_kernel=True)`), while pytest does not include the kernel cases yet. The golden stdout was captured through `make`, so `tests/p4_gen_check.golden_stdout` drops make's echo of the tecsgen call and the trailing `touch`, and `tecs.timestamp` (made by `touch`) is excluded.
- `tests/golden/p2/`, `p3/` — Ruby oracle recordings (parser traces; model dumps at three checkpoints plus recorded host I/O) replayed by tests. Re-record with `run_p2_oracle.sh` / `run_p3_oracle.sh` (WSL + Ruby).
- `*.rbdmp` and `tmp_*.h` are written by Ruby but not stored in golden data, so they are excluded from comparison.
- `tests/conftest.py` resets context/state/host per test with `LANG=C`. Tests that run the Ruby oracle live are skipped unless `ruby` and `TECSGEN_RUBY_SRC` (Ruby `tecsgen/` dir with `tecslib/`) are available.
