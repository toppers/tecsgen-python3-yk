# tecsgen-python3-yk

TECSジェネレータ tecsgen（Ruby 実装、v1.9.1）を Python 3 へ、AIコーディングエージェントを用いて移植する実験プロジェクトです。
- 2026-10-11現在、開発中です。
- 開発ドキュメントを、記録として以下で公開しています。
 - https://github.com/toppers/obsidian-mind-yk
- AIコーディングエージェントとして、Claude Code, Codexを用いています。
- CLI は Ruby 版と完全互換にします。
- CDL と import_C の C ヘッダは、Ruby 版と同じ方法で構文解析します。字句解析器は Ruby 版から移植し、パーサは Ruby 版の racc が生成した LALR 表（`bnf.tab.rb`・`C_parser.tab.rb`）を取り出して、racc の駆動部を移植したもので動かします。構文エラーの位置・件数やエラー回復も Ruby 版と一致します。
- 同じ入力に対して、Ruby 版と同一の生成物を出力することを受入基準にします（正解データは `tests/golden/`、採取手順は `tools/golden/README.md`）。プラグインを使わないテストケースは、生成物がすべてバイト単位で一致します（`tests/test_p4_gen.py`）。プラグイン機構は移植中です。
 

# 移植方法(AIコーディングエージェント使用)
 - obsidian, obsidian-mind, orca, llm-wiki について以下を参照してください。
  - https://github.com/toppers/tecsgen-python3-yk
 - Ruby版tecsgeのソースコード -> Ruby版クラス別内部仕様書 -> Ruby版クラス別外部仕様書を自動生成させる(人間はAIに指示するのみ)
 - RubyとPython3の言語仕様、ライブラリなどの相違に対する対応策をAIに提案させる。どれを採用するかは、人間が判断し、基本方針に明記させる(人間はAIに指示するのみ)
 - どの状態になったら完了とするかを決定し、基本方針に明記させる。
  - Ruby版tecsgenのテストと同一の結果が得られることなど
 - AIにRuby版tecsgeのソースコード、Ruby版クラス別内部仕様書、Ruby版クラス別外部仕様書を参照させ、基本方針に基づいた移植計画を立案させる(人間はAIに指示するのみ)
  - 移植計画立案時に不明点をAIに質問させ、それへの回答を決定事項として、明記させる
 - 移植計画について、必要と判断した修正をAIに行わせたうえで、最終的に移植計画(複数のフェーズからなる)を承認する。承認したことをドキュメントに明記させる(人間はAIに指示するのみ)
  - Python版での実装の複雑さ、Ruby版ソースコードは存在するが、どこからも呼び出されない部分や、テストケースが見つからないものなどについて、移植に含めるか検討し、決定し、、ドキュメントに明記させる
  - テストケースが見つからない場合、移植対象から外すか、テストケースをAIに作成させる（どのレベルまでのものを作成するかを決定し、ドキュメントに明記させる）
 - 承認した移植計画のフェーズごとに、Python版外部仕様の章・節をAIに作成させる（移植計画に基づき、何をやるかAIが提案してくるので、それを承認すると、そのままAIが取り掛かる）。
  - Python版外部仕様作成時の不明点をAIに質問させ、それへの回答を決定事項として、明記させる。
  - 変更が発生した場合、必要に応じ、作成済みのドキュメントも修正させる。
 - 承認した移植計画のフェーズごとに、Python版内部仕様の章・節をAIに作成させる（移植計画に基づき、何をやるかAIが提案してくるので、それを承認すると、そのままAIが取り掛かる）。
  - Python版内部仕様作成時の不明点をAIに質問させ、それへの回答を決定事項として、明記させる
  - 変更が発生した場合、必要に応じ、作成済みのドキュメントも修正させる。
 - AIに、Ruby版tecsgenのテストを実行させ、Ruby版におけるテスト結果を採取させる。
 - 承認した移植計画のフェーズごとに、Python版ソースコードを実装ソースコードを生成させ、テスト結果を報告させた（移植計画に基づき、何をやるかAIが提案してくるので、それを承認すると、そのままAIが取り掛かる）。
  - Python版ソースコード作成時の不明点をAIに質問させ、それへの回答を決定事項として、明記させる
  - 変更が発生した場合、必要に応じ、作成済みのドキュメント、ソースコードも修正させる。
   - 例：CDLの構文解析をtree-sitter(JS/TSで文法記述->パーサをWASMまたはC言語による共有ライブラリで実装)で行うことを計画したが、用意したテストの結果で多数の不一致が見つかる。
   - AIに原因を調査させたところ、特にエラー処理において、Ruby版(RACCが生成したパーサ)の挙動と一致させることが難しいことが判明。
   - AIが提案したRACCの生成したLALR表をそのまま用い、Rubyで記述されたアクションを1対1でPythonに書き換えるという方針を採用。ドキュメントに明記させ、実装させる。
 - AIがすべてのフェーズの完了を報告したら、人間が必要と思う確認をし、完了を承認する。
 
## インストール（利用者向け）

```sh
uv tool install .          # または: uv build して dist/*.whl を pip / uv でインストール
tecsgen --version
```

`tecsmerge`（テンプレートと保守中のコードのマージ）も同じパッケージのコマンドとして入ります（`tecsmerge [options] files_templ.c src_dir`）。

標準 CDL ライブラリ（Ruby 版の `tecs/`）はパッケージに同梱され、`TECSPATH` 未設定のときはそれを使います。

`tecsgen-path` は、その `tecs/` を直下に持つディレクトリ（Ruby 版の「tecsgen のディレクトリ」に当たる）を、`/` 区切りの1行で標準出力へ書きます。CMake などの呼び出し側が、標準 CDL ライブラリ・C ヘッダの場所（`<出力>/tecs`）を知るために使います（`tecsgen` コマンド自体には、Ruby 版に無いオプションを足さない方針のため、別のコマンドにしてあります）。

```sh
tecsgen-path       # 例: /home/user/.local/share/uv/tools/tecsgen-python3/lib/python3.13/site-packages/tecsgen
```

## セットアップ

```sh
uv sync
uv run pytest
```

### WSL で使う場合

正解データとの比較は WSL（Linux）で行います。Windows 側の `.venv` と混ざらないよう、仮想環境を別の場所に作ります（`/tmp` は WSL の再起動で消えるので使いません）。

Windows から一式（lint・型検査・pytest）を WSL で実行するには:

WSL 内（リポジトリのルート）で実行します。作業コピーのパスは WSL のパス（`/mnt/e/...`）で渡します。

```sh
sh tools/port/wsl_check.sh                      # テスト一式
sh tools/port/wsl_check.sh --oracle <移植元の作業コピー>   # 先に Ruby 版の記録を採り直す
sh tools/port/wsl_check.sh tests/test_p2_parser.py -x
sh tools/port/wsl_check.sh --kernel-golden <移植元の作業コピー>    # テストの代わりに、カーネル依存プラグイン用の正解データ（tests/golden/kernel/）を採取する
sh tools/port/wsl_check.sh --kernel-golden <移植元の作業コピー> --p3-oracle    # 正解データは採り直さず、P3 オラクルを差し込んで実行し、差分テスト用の記録（tests/golden/kernel/p3/）を採る
sh tools/port/wsl_check.sh --plugin-coverage <移植元の作業コピー>  # テストの代わりに、正解データがどのプラグインを実行したかを計測する
sh tools/port/wsl_check.sh --package-inventory  # WSL の展開済みパッケージにある CDL の件数を表示
sh tools/port/wsl_check.sh --tecsmerge-golden <移植元の作業コピー>  # テストの代わりに、tecsmerge の正解データ（tests/golden/tecsmerge/）を Ruby 版から採取する
sh tools/port/wsl_check.sh --package-golden <移植元の作業コピー> --out /home/ykomi/p5packageplugins/new-capture  # Plugin 正解データを採集
```

Windows の PowerShell からは `wsl.exe -e bash -lc 'cd /mnt/e/Ccur/python3/tecsgen-python3 && sh tools/port/wsl_check.sh ...'` で呼びます（Git Bash から `/` で始まるパスを `wsl.exe` に渡すと MSYS のパス変換で壊れます）。

`--kernel-golden` の採取を一部のケースに絞るには、`collect_kernel.py` の引数をそのまま後ろに付けます（例: `sh tools/port/wsl_check.sh --kernel-golden <作業コピー> --case 'atk1/*'`）。詳しくは `tools/golden/README.md` です。

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
| `wsl_check.sh` | WSL で uv sync・ruff・ty・pytest を実行する（仮想環境は `~/.venvs/tecsgen-python3`）。`--oracle` で記録の採り直し、`--kernel-golden` でカーネル用、`--package-golden` で展開済みパッケージの Plugin 正解データを採集する。`--package-inventory` は CDL のあるパッケージを調べ、`--plugin-coverage` はプラグイン網羅状況を計測する |
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
