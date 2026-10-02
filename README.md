# tecsgen-python3

TECS のコンポーネント記述コンパイラ tecsgen（Ruby 実装、v1.9.1）を Python 3 へ移植するプロジェクトです。

- CLI は Ruby 版と完全互換にします。
- CDL と import_C の C ヘッダは、Ruby 版と同じ方法で構文解析します。字句解析器は Ruby 版から移植し、パーサは Ruby 版の racc が生成した LALR 表（`bnf.tab.rb`・`C_parser.tab.rb`）を取り出して、racc の駆動部を移植したもので動かします。構文エラーの位置・件数やエラー回復も Ruby 版と一致します。
- 同じ入力に対して、Ruby 版と同一の生成物を出力することを受入基準にします（正解データは `tests/golden/`、採取手順は `tools/golden/README.md`）。プラグインを使わないテストケースは、生成物がすべてバイト単位で一致します（`tests/test_p4_gen.py`）。プラグイン機構は移植中です。

## インストール（利用者向け）

```sh
uv tool install .          # または: uv build して dist/*.whl を pip / uv でインストール
tecsgen --version
```

標準 CDL ライブラリ（Ruby 版の `tecs/`）はパッケージに同梱され、`TECSPATH` 未設定のときはそれを使います。

## セットアップ

```sh
uv sync
uv run pytest
```

### WSL で使う場合

正解データとの比較は WSL（Linux）で行います。Windows 側の `.venv` と混ざらないよう、仮想環境を別の場所に作ります（`/tmp` は WSL の再起動で消えるので使いません）。

Windows から一式（lint・型検査・pytest）を WSL で実行するには:

```powershell
pwsh tools/port/wsl_check.ps1                      # テスト一式
pwsh tools/port/wsl_check.ps1 -Oracle <移植元の作業コピー>   # 先に Ruby 版の記録を採り直す
pwsh tools/port/wsl_check.ps1 -PytestArgs tests/test_p2_parser.py, -x
pwsh tools/port/wsl_check.ps1 -KernelGolden <移植元の作業コピー>    # テストの代わりに、カーネル依存プラグイン用の正解データ（tests/golden/kernel/）を採取する
pwsh tools/port/wsl_check.ps1 -KernelGolden <移植元の作業コピー> -KernelP3    # 正解データは採り直さず、P3 オラクルを差し込んで実行し、差分テスト用の記録（tests/golden/kernel/p3/）を採る
pwsh tools/port/wsl_check.ps1 -PluginCoverage <移植元の作業コピー>  # テストの代わりに、正解データがどのプラグインを実行したかを計測する
pwsh tools/port/wsl_check.ps1 -PackageInventory  # WSL の展開済みパッケージにある CDL の件数を表示
& ./tools/port/wsl_check.ps1 -PackageGolden <移植元の作業コピー> -PytestArgs @('--out','/home/ykomi/p5packageplugins/new-capture')  # Plugin 正解データを採集
```

`-KernelGolden` の採取を一部のケースに絞るには、`-PytestArgs` で `collect_kernel.py` の引数を配列で渡します（PowerShell のセッションから直接呼ぶ。例: `& ./tools/port/wsl_check.ps1 -KernelGolden <作業コピー> -PytestArgs '--case','atk1/*'`）。詳しくは `tools/golden/README.md` です。

WSL の中で直接実行する場合は `sh tools/port/wsl_check.sh` です。手で実行するときは、次のように仮想環境の場所を指定します。

```sh
export UV_PROJECT_ENVIRONMENT=$HOME/.venvs/tecsgen-python3
uv sync
uv run pytest
```

## 移植用のツール（`tools/port/`）

移植元の Ruby ソースから Python のコードやテスト用データを作るツールと、検証用のスクリプトです。`wsl_check` 以外は Ruby が必要です。

| ツール | 内容 |
|---|---|
| `gen_messages.py` | メッセージ表 `src/tecsgen/messages/` を生成する |
| `gen_racc_tables.py` | LALR 表 `src/tecsgen/syntax/cdl_tables.py`・`cdecl_tables.py` を生成する |
| `gen_action_stubs.py` | 文法アクションの骨格 `cdl_actions.py`・`cdecl_actions.py` を生成する（一度だけ。本体は手で移植する） |
| `wsl_check.ps1`・`wsl_check.sh` | WSL で uv sync・ruff・ty・pytest を実行する（仮想環境は `~/.venvs/tecsgen-python3`）。`-Oracle` で記録の採り直し、`-KernelGolden` でカーネル用、`-PackageGolden` で展開済みパッケージの Plugin 正解データを採集する。`-PackageInventory` は CDL のあるパッケージを調べ、`-PluginCoverage` はプラグイン網羅状況を計測する |
| `collect_packages.py`・`cases_packages.toml` | Vault Context にある展開済みパッケージから Ruby 版 Plugin の生成物・実行ログ・Plugin trace を `tests/golden/packages/` に採集する。詳細は `tools/golden/README.md` |
| `run_p2_oracle.sh` | 構文解析の差分テスト用に、Ruby 版の経過を記録し直す（WSL で実行。`tests/golden/p2/`） |
| `run_p3_oracle.sh` | モデルの差分テスト用に、Ruby 版のモデル（パース直後・意味解析1回目の後・2回目の後）と、ファイル存在判定・cpp 出力を記録し直す（WSL で実行。`tests/golden/p3/`）。pytest はこの記録を再生するので、Windows でも Ruby なしで動く |
| `p4_progress.py` | プラグインを使うケースも含めて、ケースを通しで実行し、生成物（`gen/`）・標準出力・終了コードの一致をケースごとに一覧する（Ruby 不要。P3 の記録を再生する）。`-v` で一致しなかったファイルと標準出力の差を表示する |

## 正解データの採取（`tools/golden/`）

Ruby 版 tecsgen の実行結果を正解データとして保存するツールです。WSL（Linux）で実行します。詳しい手順は `tools/golden/README.md` です。

| ツール | 内容 |
|---|---|
| `generate_golden.py`・`cases.toml` | tecsgen の `test/` の155ケース（一覧は157ケース、うち2件は採取不可）を実行し、`tests/golden/cases/` に保存する |
| `collect_kernel.py`・`cases_kernel.toml` | TOPPERS カーネル（hrp3+tecs・fmp3+tecs・hrmp3+tecs・ev3rt+tecs・atk1+tecs）のアプリケーション CDL を実行し、HRP・FMP・HRMP・HRP2・ATK1 のプラグインの正解データ11ケースを `tests/golden/kernel/` に保存する |
| `plugin_trace.rb`・`run_plugin_coverage.sh`・`plugin_coverage.py` | 上の採取を計測フック付きで実行し、どのプラグインが一度も実行されなかったか（正解データが無いか）を集計する（採取結果は捨てる） |
