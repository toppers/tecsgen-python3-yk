# CLAUDE.md

このファイルは、このリポジトリ内のコードを扱う際、Claude Code (claude.ai/code) に指針を提供するものです。

## Project

このプロジェクトは、AIコーディングエージェントを用い、Rubyスクリプトを、Pythonスクリプトに移植する実験プロジェクトである。
移植に伴う、技術的課題を明確にすることを目的とする。

tecsgen（TECSコンポーネント記述コンパイラ、Ruby v1.9.1版）をPython 3へ移植します。合格基準は、同一の入力に対して**Ruby版とバイト単位で完全に一致する出力**（`gen/`配下に生成されるファイル、標準出力、終了ステータス）が得られることです。CLIはRuby版と完全な互換性を維持する必要があります。コードのコメント、docstring、ドキュメントは日本語で記述されているため、その慣例を踏襲してください。

移植作業はP1からP5の段階（メッセージ → パーサー → モデル/意味解析 → 最適化/コード生成 → プラグイン）に沿って進められています。テストファイルやコミットの件名には、該当する段階を示すタグが付与されています（例: `test_p3_model.py`、`feat: ... (P5i)`）。現在P5（プラグイン）の段階にあり、1コミットにつき1つのプラグインファミリーを対象としています。2026年10月1日時点での状況は以下の通りです。ゴールデンデータ（期待値データ）が存在する標準プラグイン（P5j）およびカーネル依存プラグイン（HRP、FMP、HRMP、HRP2、ATK1Event；P5l–P5p）の移植は完了しています。`uv run python tools/port/p4_progress.py` を実行すると、カーネル関連の全11ケース（`tests/golden/kernel/`）を含め、プラグインなしのケースでは119/119、プラグインありのケースでは34/46が一致していることが確認できます。残りのケースについては、`-L`オプションで指定するユーザープラグインへの対応待ち、あるいは出力の軽微な差異が理由となっています。ゴールデンデータを持たないプラグイン（Task/Handler/Object以外のHRP2カーネルオブジェクト、HRP2/HRPのRPCおよびSVC、`lib/GenHRP2Marshaler`など）は移植されていません。また、`ATK1EventPlugin`については、唯一の入力に対する出力が空の状態となっています。詳細は `tools/golden/README.md` および Vault 内の進捗ログ（`tecsgen-python3移植計画 — P5 進捗ログ`）を参照してください。

## 移植の基本方針

1. **正解は Ruby 版の実行結果**。移植の受入基準は、同じ入力に対して `gen/` 以下の生成物がバイト単位で一致し、エラー／警告コード・件数・終了コードも一致すること（[[tecsgen-python3外部仕様]] 4章・7章の一致要件）。
2. **差分テストを先に作る**。Ruby 4.0.6 はローカルで動く（2026-09-26 確認）。`test/` のケース（一覧は157ケース、採取できたのは155ケース。採取しなかった2件は `import_C/z` と `mruby`）を Ruby 版で実行し、ゴールデン出力として固定してから移植を始める。TOPPERS カーネルの CDL を使うカーネル依存プラグインのケースは、別に `tests/golden/kernel/` に11ケースを採取している。
3. **フェーズごとに内部状態を比べる**。生成物の一致だけを見ると、どのフェーズでずれたかが分からない。Ruby 側に小さな JSON ダンプ用フックを足し、パース後・意味解析後・最適化後のモデルを Python 側と比べる。
4. **仕様書は実装の少し前に書く**。[[tecsgen-python3内部仕様]] は章ごとに、該当フェーズに着手する直前に書く。12章を全部書いてから実装に入る進め方はとらない。
5. **WSL での検証は必ず `tools/port/wsl_check.sh` で行う**（2026-09-28 ユーザー採用。2026-10-04 に PowerShell ラッパー `wsl_check.ps1` を廃止して bash に一本化。ただし `tools/port/wsl_check.ps1` と、それを参照する `tools/golden/run_plugin_coverage.sh` のコメントはまだ残っているので、使わない）。Windows からは `wsl.exe -e bash -lc 'cd /mnt/e/Ccur/python3/tecsgen-python3 && sh tools/port/wsl_check.sh ...'` の形で呼び（PowerShell ツールから。Git Bash は `/` で始まるパスが MSYS のパス変換で壊れる）、それ以外のコマンドをその場で手書きしない。このスクリプトは、WSL 用の仮想環境の分離（`~/.venvs/tecsgen-python3`）、`VIRTUAL_ENV` の解除、`uv sync`・ruff・ty・pytest の一括実行と結果のまとめ表示を済ませている。作業コピーのパスは WSL のパス（`/mnt/e/...`）で渡す。各フェーズの計画には「完了時に `sh tools/port/wsl_check.sh` を通す」を検証手順として入れる。スクリプトに無い操作（例: WSL で `tools/port/p4_progress.py` を回す、特定ケースだけ実行する）が必要になったら、手書きで済ませずにスクリプトへオプションとして足してから使い、README の表も更新する。
   - 経緯: P5e〜P5i のセッションで、このスクリプトの存在を見落として WSL コマンドを毎回手書きし、Windows 側と共有の `.venv` を作り直させて1回失敗、さらに場当たりの別の仮想環境（`~/.cache/tecsgen-python3-venv`）まで作った。

## 作業の決まり（常に守る。指示が無くても方針決定・計画立案・作業の実行に取り込む）

- ファイルの書き換えは Write / Edit ツールで行う。Bash の heredoc で Python ソースや置換文字列を渡さない（文字列中の改行エスケープが本物の改行になり、構文エラーになる）。書き換えたら、モジュールを直接 import するか ruff で構文を確かめる（`load_plugin` は例外を握りつぶして `P2003 load failed` としか出さない）。
- カーネルの P3 記録の再採取（`--kernel-golden … --p3-oracle`）は全件で約30分かかる。ケースを足す・直すときは `--case '<id>'` で絞り、バックグラウンドで実行する。

## Commands

```sh
uv sync
uv run pytest                                   # all tests
uv run pytest "tests/test_p4_gen.py::test_generated_files_match_ruby[ErrorCase/attribute-err]"  # one golden case
uv run ruff check . && uv run ruff format --check .
uv run ty check                                 # type checker (not mypy)

# プラグインおよびプラグインの各ケースにおけるマッチ状況（Ruby不要、P3レコードをリプレイ）
uv run python tools/port/p4_progress.py [case-id-prefix...] [-v]
```

`tests/test_p4_gen.py` ではプラグインを使用するケースがスキップされるため、**プラグイン関連の動作確認は `p4_progress.py` で行います**（例: `p4_progress.py multiplugin/ -v` を実行すると、差異のあるファイルや標準出力の差分が表示されます）。

ゴールデンデータはLinux上で取得されたため、信頼できる完全なチェックは、別のvenv（`~/.venvs/tecsgen-python3`）を使用してWSL上で実行します（WSLにWindows側の`.venv`を再構築させてはいけません）。

```sh
# run inside WSL at the repo root; from Windows wrap as: wsl.exe -e bash -lc 'cd /mnt/e/Ccur/python3/tecsgen-python3 && <command>'
# working-copy paths are WSL paths (/mnt/e/...)
sh tools/port/wsl_check.sh                          # uv sync, ruff, ruff format --check, ty, pytest
sh tools/port/wsl_check.sh tests/test_p2_parser.py -x
sh tools/port/wsl_check.sh --oracle <Ruby source working copy>  # re-record Ruby oracle first (needs Ruby)
sh tools/port/wsl_check.sh --kernel-golden <Ruby source working copy>    # instead of tests: collect tests/golden/kernel/ (kernel plugins; ~10 min)
sh tools/port/wsl_check.sh --kernel-golden <Ruby source working copy> --p3-oracle   # instead: re-record tests/golden/kernel/p3/ (Ruby I/O replayed by p4_progress.py; checks the output equals the committed golden data; ~30 min)
sh tools/port/wsl_check.sh --plugin-coverage <Ruby source working copy>  # instead of tests: measure which plugins the golden cases run (20-40 min)
```

特定のカーネルケースのみを収集するには、`--kernel-golden <wc>` の後に `collect_kernel.py` の引数を追加します（例：`sh tools/port/wsl_check.sh --kernel-golden <wc> --case 'atk1/*'`）。

Pass/skipのカウントはWindowsとWSLで若干異なりますが、コミットメッセージにはその両方が記録されます。

## Architecture

**移植における忠実さ**が設計原則です。PythonモジュールはRubyファイルと対応関係にあり（例：`core/tecsgen.py` ← `core/tecsgen.rb`、`plugin/RPCPlugin.py` ← `RPCPlugin.rb`）、Ruby側の命名を維持しています（プラグインモジュールはCamelCaseであるため、ruffで`N999`の警告を無視しています）。モジュールのドキュメンテーション文字列（docstring）には、対応するRubyのソースコードおよび内部仕様書の該当章（「内部仕様N章」）が記載されています。移植の際は、Pythonらしい慣用的な書き方（イディオム）を採用するのではなく、Rubyのセマンティクス（動作仕様）を正確に再現するようにしてください。

- `ruby_compat.py` — バイト単位で完全に一致する出力を得るために必要なRubyの組み込み機能相当のものです。具体的には、`truthy`（`nil`と`false`のみが偽とみなされる）、`to_s`、`sub_first`/`gsub`（Rubyの置換文字列ルール）、`Symbol`/`sym`（ハッシュのキーとして`str`とは区別される）、`rb_print`/`rb_puts`（バイト書き込み、改行は常にLF）、数値変換などが含まれます。これらは、Python標準の真偽値判定、`str`、`re`の代わりに使用してください。
- `context.py` — Rubyのグローバル変数（`$force_overwrite`、`$KCONV_CDL`など）を`TecsgenContext`に集約し、`get_context()`経由でアクセスできるようにしたもの。属性名は、対応するRubyの変数名をスネークケースにしたものとする。あるフェーズで新たなグローバル変数が必要になった場合は、ここに追加すること。
- `host.py` — ファイルシステム、カレントワーキングディレクトリ（cwd）、サブプロセスへのアクセス（`File.exist?`、`Dir.chdir`、C++用の `IO.popen` など）はすべて `get_host()` を経由して行われます。パスはPOSIX形式の文字列として扱われ、プロセスのカレントワーキングディレクトリが変更されることはありません。テスト実行時には `RecordedHost` (`tests/p3_oracle_data.py`) が使用され、Rubyによる記録済みのI/Oが再生されます。そのため、Ruby、ソースツリー、gccがインストールされていないWindows環境でもテストを実行可能です。**ファイルシステムには決して直接アクセスしないでください**。直接アクセスするとローカル環境では動作しても、記録の再生（リプレイ）が失敗する原因となります。
- `host.py` — ファイルシステム、カレントワーキングディレクトリ（cwd）、サブプロセスへのアクセス（`File.exist?`、`Dir.chdir`、C++用の `IO.popen` など）はすべて `get_host()` を経由して行われます。パスはPOSIX形式の文字列として扱われ、プロセスのカレントワーキングディレクトリが変更されることはありません。テスト実行時には `RecordedHost` (`tests/p3_oracle_data.py`) が使用され、Rubyによる記録済みのI/Oが再生されます。そのため、Ruby、ソースツリー、gccがインストールされていないWindows環境でもテストを実行可能です。**ファイルシステムには決して直接アクセスしないでください**。直接アクセスするとローカル環境では動作しても、記録の再生（リプレイ）が失敗する原因となります。
- `state.py` — `reset_model_state()` は Ruby のクラス変数（`@@...`）をリセットします。これにより、1つのプロセス内で tecsgen を複数回実行（テストなど）することが可能になります。クラスレベルの状態を持つ新しいクラスは、ここで `reset()` を登録する必要があります。プラグインは、すでにインポートされている場合にのみリセットされます（強制的にインポートしてはなりません。そうしないと、モデル比較時に余分なクラスが読み込まれているとみなされてしまうためです）。プラグインを `require` する際に生じる Ruby のロード時の副作用は、実行ごとの `on_load()` 内で処理されます。
- `cli.py` は `core/tecsgen.py` に対応します（`TECSGEN.run1` が構文解析と意味解析を、`run2`/`finalize` が最適化とコード生成を担います）。`ruby_optparse.py` は Ruby の OptionParser の挙動やメッセージを再現しています。その他のコンソールスクリプト（`pyproject.toml` 定義）には、`tecsmerge`（`tecsmerge.py`：`tecsmerge.rb` の移植版であり、出力結果の照合テストも実施済み）や `tecsgen-path`（`libpath.py`：CMake から呼び出す際に、同梱されている `tecs/` CDL ライブラリを含むディレクトリを出力するコマンド。`tecsgen` 本体に Ruby 版には存在しないオプションを追加しないようにするため、別コマンドとして実装されています）があります。`tecsgen-rb` から移植された CMake サポート機能は、`gen/CMakeLists.tecsgen.cmake` を生成し、プラグインに対して `CMake` API を提供します。
- `syntax/` — Rubyから移植された字句解析器（lexer）が含まれます。構文解析器（parser）は、Rubyの`racc`の出力から抽出されたLALRテーブル（自動生成される`cdl_tables.py`および`cdecl_tables.py`）と、`racc`ランタイムの移植版（`racc_runtime.py`）を用いて動作します。そのため、構文エラーの位置、個数、およびリカバリの挙動はRubyと一致します。文法アクションは、`cdl_actions.py`および`cdecl_actions.py`にて手作業で移植されています。
- `core/` — 型システム、式、`syntaxobj/`（宣言ノード）、`componentobj/`（Celltype、Cell、Signature、Namespace、Join、Import/Import_Cなど）、およびコード生成（`generate_celltype*.py`、Rubyのように埋め込まれたテンプレート）。
- `core/plugin_module.py` — プラグインの読み込み: Rubyの `require` + `const_get` は、`importlib.import_module("tecsgen.plugin.<Name>")` および同名のクラスを使用する形に置き換えられます。移植されていないプラグインは `PluginNotPorted` を発生させます。
- `plugin/` — 移植されたプラグイン。`plugin/lib/` にはそれらのヘルパーモジュールが格納されています。

生成されるファイル（手動編集せず、ツールで再生成してください）: `messages/*` (`tools/port/gen_messages.py`)、`syntax/*_tables.py` (`tools/port/gen_racc_tables.py`)。これらのツールには Ruby および Ruby のソースコードが必要です。

## Test data

- `tests/golden/cases/<id>/` — ケースごとのRubyの出力（`files/`、標準出力、終了ステータス）。`tools/golden/README.md` に従いWSL環境で取得されたものです。ケース一覧は `tools/golden/cases.toml` に記載されています。`.gitattributes` で `tests/golden/**` が `-text` に設定されており、改行コードの変換が行われないようになっています。

- `tests/golden/kernel/cases/<id>/` — カーネル依存プラグイン（HRP: hrp3+tecs, FMP: fmp3+tecs, HRMP: hrmp3+tecs, HRP2: ev3rt+tecs, ATK1: atk1+tecs; 全11ケース）に関するRubyの出力結果です。これらは `cases_kernel.toml` を用いて `tools/golden/collect_kernel.py` により収集されました。その際、各リポジトリに同梱されているtecsgenの代わりに port-source 版 tecsgen (r3304) が使用され（なお、メインのゴールデン・ベースラインはその後 tecsgen-rb に移行しています。`CHANGELOG.md` を参照してください）、Cプリプロセッサとしては `arm-none-eabi-gcc` が使用されています（ATK1ではホスト環境の `gcc -E -D NC30` が使用されます。`cases_kernel.toml` 内のコメントを参照してください）。`meta.json` には tecsgen の呼び出し内容が `tecsgen_args` として記録され、`environment.json` にはツールチェーンやリビジョン情報が記録されています。既知の制限事項として、hrp2+tecs の sample1 は G1016 構文エラー（古い region 構文）で停止します。また、`ATK1EventPlugin` は、入力データにイベントセルが含まれていないため、空の出力を生成します。`tests/golden/kernel/p3/<id>.jsonl.gz` には、各ケース（ケースID: `kernel/<id>`）の Ruby I/O 記録が格納されています。`tools/port/p4_progress.py` はこれを再生（リプレイ）しますが（`tests/p3_oracle_data.case_ids(include_kernel=True)`）、pytest のテストスイートには、現時点ではカーネル関連のケースは含まれていません。ゴールデンデータの標準出力（stdout）は `make` を介して取得されたため、`tests/p4_gen_check.golden_stdout` では、make による tecsgen 呼び出しコマンドのエコー表示や末尾の `touch` コマンドの出力が除外されており、`touch` によって生成された `tecs.timestamp` も対象外となっています。

`tests/golden/p2/`, `p3/` — Ruby製オラクルによる記録（パーサーのトレース、3つのチェックポイントでのモデルのダンプ、および記録されたホストI/O）。テスト実行時にこれらが再生されます。再記録を行うには `run_p2_oracle.sh` / `run_p3_oracle.sh` を使用してください（WSL + Ruby環境）。

- `*.rbdmp` および `tmp_*.h` は Ruby によって生成されますが、ゴールデンデータには保存されないため、比較対象から除外されます。

- `tests/conftest.py` は、各テストの実行前に `LANG=C` を設定し、コンテキスト、状態、およびホスト環境をリセットします。Ruby Oracle を実際に実行するテストは、`ruby` および `TECSGEN_RUBY_SRC`（`tecslib/` を含む Ruby 版 `tecsgen/` ディレクトリ）が利用可能な場合を除き、スキップされます。
