# 正解データ（golden）の採取

Ruby 版 tecsgen の実行結果を保存し、Python 版の出力と比べるための正解データにします。

## 前提

- WSL（Ubuntu）で実行します。Ruby・gcc・Python 3.11 以上が必要です。
  - テストの多くは `import_C` で C プリプロセッサ（`gcc -E`）を使い、cygwin 相当の POSIX ヘッダ（`pthread.h` など）を読みます。Windows 上の `clang -E` では足りません。
  - Windows 版 Ruby は改行を CRLF で出力するため、正解データの改行は LF に統一しています。
- 移植元のブランチ（`test/` と `tecsgen/` を含むディレクトリ）が必要です。

## 実行

Windows 上の SVN 作業コピーは、ファイルが CRLF になっていることがあります（リポジトリ本体は LF）。tecsgen は生成コードのテンプレートを Ruby ソースに埋め込んでいるため、作業コピーをそのまま使うと出力まで CRLF になります。先に `svn export` でリポジトリ本来の内容を WSL 側へ書き出してから採取します。WSL 側に置くと、`/mnt/e` から読むより大幅に速くなります。

```sh
WC=/mnt/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
SRC=/tmp/tecsgen-src-r3304
for d in tecsgen test; do
  svn export -q -r BASE --native-eol LF "$WC/$d" "$SRC/$d"
done

python3 tools/golden/generate_golden.py \
  --source "$SRC" \
  --source-label "toppers tecsgen branches/ykominami_r3033 r3304 (svn export -r BASE --native-eol LF)" \
  --out /tmp/golden-out
rm -rf tests/golden && cp -r /tmp/golden-out tests/golden
```

`--case <id>` を付けると、そのケースだけを採取し直します（glob 可、複数指定可）。

## ケース一覧

`cases.toml` に、移植元 `test/` の Makefile・シェルスクリプトから抜き出した tecsgen の呼び出しを並べています。make と C コンパイルは行わず、tecsgen の実行だけを再現します。

## カーネル依存プラグインの正解データ

`test/` には HRP・HRP2・FMP・HRMP 系のプラグインを使うケースが無いため、TOPPERS カーネル（hrp3+tecs・fmp3+tecs・hrmp3+tecs・ev3rt+tecs）の sample アプリケーションで別に採取します。`collect_kernel.py` が、リポジトリの `svn export` → 同梱 tecsgen を移植元へ差し替え → `configure.rb` → `make tecs` を再現し、`tests/golden/kernel/` に保存します。ケースは `cases_kernel.toml` です。

| リポジトリ | プラグイン | 実行方法 |
|---|---|---|
| hrp3+tecs | HRP（`HRPObjectPlugin`・`HRPTaskPlugin`・`HRPSVC*` ほか） | `configure.rb` → `make tecs` |
| fmp3+tecs | FMP（`FMPObjectPlugin` ほか） | 同上 |
| hrmp3+tecs | HRMP（`HRMPKernelObjectPlugin`・`HRMPPlugin`） | 同上（`zybo_z7_gcc`。`zybo_gcc` は `Makefile.target` が無く使えない） |
| ev3rt+tecs | HRP2（`HRP2Plugin`・`HRP2TaskPlugin` ほか） | `configure` を使わず、`hr-tecs/workspace/<名前>/` で `make tecs`（ケースの `workdir`） |
| atk1+tecs | ATK1（`ATK1KernelPlugin`・`ATK1TaskPlugin`・`ATK1AlarmPlugin`・`ATK1ISRPlugin`・`ATK1ResourcePlugin`・`ATK1EventPlugin`） | Makefile が無いので、tecsgen の引数をケースの `tecsgen_args` に直接書く（`.tmk` の呼び出しを r3304 向けに置き換えたもの。経緯は `cases_kernel.toml` のコメント）。`-U` の有無で2ケース |

**`ATK1EventPlugin` の限界**: atk1+tecs のアプリケーション CDL は `sample.cdl` だけで、イベントを使うセルが無い（inferred）。プラグインは読み込まれて実行されるが、`tmp_ATK1EventPlugin_0.cdl`・`tmp_ATK1EventPlugin_post_code.cdl`・`EVENT_tecsgen.oil` は 0 バイトで、生成ロジックの本体は記録されていない。記録されているのは「イベントが無いとき何も出さない」経路だけ。`ATK1DelayTaskPlugin` は atk1+tecs の CDL に使用箇所が無く、対象外。

一部のケースだけを採るには、`wsl_check.ps1` の `-PytestArgs` に `collect_kernel.py` の引数を配列で渡す。PowerShell のセッションから直接呼ぶ（例: `& ./tools/port/wsl_check.ps1 -KernelGolden <作業コピー> -PytestArgs '--case','atk1/*'`。atk1 の2ケースだけなら約30秒）。`pwsh ...` を子プロセスとして起動して `--case,'atk1/*'` と書くと、1つの文字列として渡されて `unrecognized arguments` になる。`-KernelGolden` の後ろに直接 `--case` を書いても、スクリプトのパラメータに束縛されず届かない（全ケースが再採取される）。

HRP2 は hrp2+tecs 自体の sample1 では採れません。`region` の古い文法（`[domain(DOMAIN1), out_through(), in_through()]`）が現行の tecsgen で構文エラー（G1016）になり、プラグインまで進まないためです。HRP2 ベースの ev3rt+tecs（`hr-tecs`）を使っています。

```sh
pwsh tools/port/wsl_check.ps1 -KernelGolden E:/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
```

- 前提: WSL に `gcc-arm-none-eabi`（ターゲットの `CC` は `arm-none-eabi-gcc`）と Ruby の `shell` gem（`gem install --user-install shell`。`configure.rb` が使う）。カーネルの SVN 作業コピーは `~/repo/svn-toppers-TECS-2/svn/toppers/<名前>/trunk`（環境変数 `KERNEL_REPOS_ROOT` で変更）。
- 作業ディレクトリは `~/p5kernel`（`/tmp` は WSL の再起動で消える）。採取には10分ほどかかります（`/mnt/e` への書き込みが遅い）。
- `--p3-oracle`（`wsl_check.ps1 -KernelP3`）を付けると、正解データは採り直さず、`tests/ruby/p3_oracle.rb` を差し込んで同じケースを実行し、Ruby 版の外界とのやりとりの記録を `tests/golden/kernel/p3/<ID>.jsonl.gz` に書く。出力がコミット済みの正解データと一致したときだけ記録を置く（フックが出力を変えていない確認）。`tools/port/p4_progress.py` が再生する。全11ケースで30分ほどかかる。
- 各ケースの `meta.json` の `tecsgen_args` に、`make -n tecs` で得た tecsgen の呼び出しを記録します。
- カーネルのリポジトリは r3306 で、移植元 tecsgen（r3304）とは版が違います。同梱の tecsgen（r3306）は Ruby 3.x で `Proc.new` のエラーになるため、r3304 に差し替えて実行しています。カーネル側の CDL 自体は r3306 のままです。

## プラグインの網羅状況の計測

正解データが TECS のどのプラグインを実際に実行したかを、`plugin_trace.rb` で計測します。プラグイン名を出力から検索する方法は、名前が出力に現れない経路（`OpaqueMarshalerPlugin` など）を見落とすので使いません。

```sh
pwsh tools/port/wsl_check.ps1 -PluginCoverage E:/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
```

- `run_plugin_coverage.sh` が、`test/` の155ケース（`generate_golden.py`）とカーネルのケース（`collect_kernel.py`）を、`RUBYOPT=-r plugin_trace.rb` 付きで実行します。採取結果は `~/p5kernel/cov/` に捨て、`tests/golden/` には何も書きません。20〜40分かかります。
- `plugin_trace.rb` は、`Kernel#load`／`require` したファイル（`load`）と、`Plugin` の子クラスのインスタンス生成（`new`）を `TECS_PLUGIN_LOG` に書きます。
- `plugin_coverage.py` がログを集計し、「一度もロードされなかった（正解データが無い）」「ロードされたが生成されなかった（基底・振り分け用・管理用。抜けとは限らない）」「生成回数が少ない」に分けて `~/p5kernel/cov/report.txt` に出します。
- 判定はロードと生成の有無だけです。プラグイン内の全メソッド・全分岐を実行したかは見ません。出力が空になる場合（`ATK1EventPlugin` など）も「生成された」に数えます。

## 出力

`tests/golden/cases/<id>/` に次のファイルを保存します（カーネル用の `tests/golden/kernel/cases/<id>/` も同じ構成です）。

| ファイル | 内容 |
|---|---|
| `stdout.txt` / `stderr.txt` | 標準出力・標準エラー出力 |
| `files/` | 実行によって作られた、または変更されたファイル（`test/` からの相対パス） |
| `meta.json` | 引数・終了コード・エラー/警告件数・ErrorCase の期待件数との一致・保存しなかったファイルのハッシュ |

- 各ケースは、テストツリーの作業コピーを毎回作り直してから実行します。
- 作業ディレクトリとソースの絶対パスは `@WORK@`・`@SOURCE@` に置き換えます。
- `*.rbdmp`（Ruby の Marshal 形式。Python 版では再現しない）と `tmp_*.h`（C プリプロセッサの出力）は保存せず、ハッシュとサイズだけを `meta.json` に記録します。
- 実行環境（Ruby・gcc・tecsgen のバージョン、ソースの出所）は `tests/golden/environment.json` に記録します。
- `.gitattributes` で `tests/golden/**` を改行変換の対象外にしています。

## 展開済みパッケージの Plugin 正解データ

Vault の `work/active/tecsgen-python3/tecsgen-python3.md` の Context にある `~/Ccur/TECS-WG-DL/` の21パッケージは、すべて `.cdl` を含みます。採集対象と除外理由は `tests/golden/packages/package_inventory.json` に記録します。パッケージに同梱された古い tecsgen は実行せず、移植元の Ruby 版（r3304）を作業コピーに差し替えます。元の展開済みパッケージは変更しません。

```powershell
& ./tools/port/wsl_check.ps1 -PackageInventory
& ./tools/port/wsl_check.ps1 -PackageGolden E:/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033 -PytestArgs @('--out','/home/ykomi/p5packageplugins/new-capture')
```

`tools/golden/cases_packages.toml` が採集ケースです。`-PackageGolden` は `collect_packages.py` を呼び、成功したケースだけを `cases/<id>/` に保存します。既存の出力先は上書きせず、追加入力時は `--append --case <id>` を指定します。終了コード0、エラー0、タイムアウトなし、Plugin のインスタンス生成と生成ファイルあり、を正解ケースの条件とします。失敗した試行は `diagnostics/<id>/` に分離します。各 `meta.json` には元パッケージの CDL の SHA-256、実行引数、Plugin のロード・生成記録があり、`plugin_trace.txt` に生ログを保存します。

`-PackageInventory -PytestArgs @('refs')` は CDL 内の `generate()` 指定、`@('targets')` は ASP3 ターゲット一覧を表示します。`@('layout','<package>')`、`@('file','<package>','<relative-path>')`、`@('locate','<package>','<filename>')` はパッケージの調査に使います。既知の失敗2ケースは manifest で `enabled = false` とし、診断の再実行時だけ `--include-disabled --case <id>` を渡します。

採集済みは16ケースです。ASP3 系13パッケージの `NotifierPlugin`、`atk1+tecs` の ATK1 系、`MrubyBridgePluginPackage` の `Mruby2C`／C ブリッジ系、`mruby-on-ev3rt+tecs` の HRP2・mruby 系を含みます。RX 用の `ccrx.exe` は WSL に無く、旧 `MrubyBridge-test` は `cygwin_kernel.cdl` が r3304 で T1007 となるため、両試行は診断記録に留めています。`mruby-on-asp+tecs` と GR-PEACH の Plugin 使用は採集済み系統と重複し、`stm32primer2_tecs_edu` と `tecscde-MinGW` の製品 CDL には `generate()` の指定がありません。
