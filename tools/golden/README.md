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

### 移植元が svn でないとき（tecsgen-rb）

正解データの基準は、2026-10-05 から tecsgen-rb（git リポジトリ `asp3_stm32cube_TECS` の `tecsgen-rb`。cmake 対応を含む）です。tecsgen-rb には `test/` が無いので、`test/` は svn の作業コピーから、`tecsgen/` は git から取り出した木を作り、`wsl_check.sh` の共通オプションで指定します（手書きの WSL コマンドは使いません）。

```sh
# 木を作る（出力先は $HOME 配下。/tmp は WSL の再起動で消える）
sh tools/port/wsl_check.sh --build-src-tree "$WC" /mnt/e/Ccur/python3/asp3_stm32cube_TECS tecsgen-rb "$HOME/p2work/tecsgen-rb-src"

T=$HOME/p2work/tecsgen-rb-src
# tests/golden/cases（test/ 配下の全ケース）。--exclude したケースは再採取せず、既存の正解を残す
sh tools/port/wsl_check.sh --src-tree "$T" --exclude transparent_marshaler --cases-golden
# p2・p3 の記録（Ruby 版の外界とのやりとり）
sh tools/port/wsl_check.sh --src-tree "$T" --exclude transparent_marshaler --oracle -
# カーネル依存プラグイン（メモリを抑えるなら --case 'atk1/*' のように系統ごとに分ける。--p3-oracle で記録も採る）
sh tools/port/wsl_check.sh --src-tree "$T" --kernel-golden - [--p3-oracle] [--case '<id>']
# 展開済みパッケージ（既存の出力先は上書きされないので、別ディレクトリへ採って cases/ へ写す。--p3-oracle で記録も採る）
sh tools/port/wsl_check.sh --src-tree "$T" --package-golden - --out "$HOME/p5packageplugins/rb-capture"
sh tools/port/wsl_check.sh --src-tree "$T" --package-golden - --p3-oracle --out tests/golden/packages
```

記録（p2・p3）を `--case` で絞って採るには、先頭の共通オプションに `--case <id>` を置く（`--exclude` と同じ位置。glob 可、繰り返し可）。テスト一式も続けて走る。

```sh
sh tools/port/wsl_check.sh --src-tree "$T" --cases-golden --case cmake_add     # 正解データ（--case は末尾）
sh tools/port/wsl_check.sh --src-tree "$T" --case cmake_add --oracle -         # p2・p3 の記録
```

**`cmake_add`（2026-10-09）**: `TECSGEN::CMake.add_*` を呼ぶプラグインは、標準付属プラグインにも `asp3_stm32cube_TECS` にも無いので、利用者プラグイン（`-L .`）の合成入力（`tools/golden/inputs/cmake_add/`。CDL と Ruby 版プラグイン）で動かす。Python 版プラグインは `tests/user_plugins/cmake_add/MyCMakePlugin.py`。`gen_cmake_tecsgen` は生成の最初に走るので、`gen_factory` から足したものが出力に反映されないこと（Ruby 版と同じ）も正解データに含む。`generate_golden.py` の `place_inputs` は、`inputs` の `*.cdl` に加えて `*.rb` も写し、`cwd` が `test/` に無ければ作る。

**`cmake_add_<種類>`（2026-10-09）**: `cmake_add` はセルタイププラグインだけなので、ほかの種類（`signature`・`cell`・`composite`・`multi`・`through`・`domain`・`class`）のコンストラクタから `CMake.add_*` を呼ぶケースを足した。入力は `tools/golden/inputs/cmake_add_<種類>/`、一覧と作りは `tools/golden/inputs/cmake_add_kinds.md`。`through`・`domain`・`class` は既存ケースのプラグインに `add_*` を足した変種で、ケースの `base`（`test/<base>` を `cwd` へ写してから `inputs` を重ねる）を使う。採取は `--cases-golden --case 'cmake_add_*'`（正解データ）と、先頭の `--case 'cmake_add_*' --oracle -`（p2・p3 の記録）。

`transparent_marshaler` は、tecsgen-rb に `TransparentMarshalerPlugin.rb` が無いため再採取できず、r3304 で採った正解データ・記録を残しています（`tools/port/p4_progress.py` の `BASELINE_EXCEPTIONS`。比較の対象外）。

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

**HRP2 の個別プラグインは合成入力で採る**: `HRP2SemaphorePlugin` など7種（Semaphore・Eventflag・Dataqueue・PriorityDataqueue・FixedSizeMemoryPool・AlarmHandler・CyclicHandler）、`HRP2SVCPlugin`、`HRP2RPCPlugin`、`GenHRP2Marshaler` は、実プロジェクトの CDL が使わない。`tools/golden/inputs/hrp2/` の合成アプリケーション（カーネルの CDL を import し、現行の文法で region を書いたもの）を `obj-golden/` へ置いて実行する。ケースは `hrp2/objects`（5種のオブジェクトと SVC）、`hrp2/rpc`（RPC）、`hrp2/cyclic`・`hrp2/alarm`・`hrp2/rpc_ptr`（Ruby 版が例外で止まる経路。例外・終了コード・それまでに作られたファイルが正解）。経緯と各ケースの配置は `tools/golden/inputs/hrp2/README.md`。採取は `sh tools/port/wsl_check.sh --kernel-golden <作業コピー> --case 'hrp2/*'`（約2分）。`HRP2Cache.rb`（コメントだけ）と `HRP2PostHook.rb`（tecslib のどこからも参照されない）は動かす経路が無く、対象外。`HRPRPCPlugin` は HRP2 ではなく HRP（hr-tecs3）のプラグインで、このケースには含まない。

**残りの未移植プラグインの正解データ（2026-10-03）**:

| プラグイン | 正解データ | 採り方 |
|---|---|---|
| `HRPRPCPlugin` | `kernel/cases/hrp3/blueninja_gcc/sample2`（Ruby 版が `S9999` で途中で止まる実プロジェクトのまま）、`sample2_rpc` | hrp3+tecs の `sample/sample2.cdl` は2つのユーザドメイン間の結合を持つ。`sample2_rpc` は、そのままだと通らない箇所を `patch`（`cases_kernel.toml` に理由を書いた）で直したもの。`PPAllocatorSize` の「必要」「不要」の両方の経路を通す。`tSample2` は単一ドメインで通らない |
| `ATK1DelayTaskPlugin` | `kernel/cases/et_robcon/nxt_sample/{etrobo,et2011,mini,syslog}` | et_robcon の `atk1+tecs/nxt_sample` が `tDelayTask`（`tecs_lib/mindstorms_nxt`）を使う。各 Makefile の `make tecs`。リポジトリは `repo_dir` で `et_robcon/trunk/atk1+tecs` を指す。`ATK1KernelPlugin` が id の重複（S3003・S3001）をエラーにするが、make は成功で終わる（Ruby 版の振る舞い） |
| `MrubyInfoBridgePlugin`・`MrubyInfoBridgeCellPlugin`・`MrubyInfoBridgeSignaturePlugin` | `cases/mruby/MrubyInfoBridge-SimpleSample`、`cases/mruby/MrubyInfoBridge-test` | 移植元の `test/mruby` の2本。tecsgen の実行に要るのは mruby のヘッダだけなので、`--mruby-include`（既定は `mruby/mruby-master/include`）を `{MRUBY_INCLUDE}` として渡す |
| `TransparentMarshalerPlugin` | `cases/transparent_marshaler` | 使用例が無いので合成入力（`inputs/transparent/`） |
| `Mruby2CBridgePlugin`・`TECS2CBridgePlugin` | `packages/cases/MrubyBridgePluginPackage-130616/Mruby2C`（既存）、`Mruby2C-File` | `Mruby2C` は小さなシグニチャだけ。`Mruby2C-File` は C のファイル I/O（ポインタ・`size_is`・string）を渡し、経路が広い。`-D TECS` が要る（`FILEptr` の定義が `#ifdef TECS`） |

**P3 記録（差分テスト用）**: 上の各ケースの記録も採ってあり、`tools/port/p4_progress.py` で Python 版と比べる。`test/` 系（`cases/mruby/*`・`transparent_marshaler`）は `run_p2_oracle.sh`・`run_p3_oracle.sh` に `--case` を付けた形（全件を採り直す必要は無い）、カーネル系は `--kernel-golden … --p3-oracle --case …`、パッケージ系は `--package-golden … --p3-oracle --case '<id>'`（`tests/golden/packages/p3/`。ケース ID は `packages/<id>`）。パッケージ系は `plugin_trace.txt` に P3 フックがロードしたファイルが加わるので、そのファイルだけは正解データと比べない。

`generate_golden.py` の `inputs`（`tools/golden/inputs/<名前>/*.cdl` を `cwd` へ写す）と `{MRUBY_INCLUDE}`、`collect_kernel.py` の `repo_dir`（`<repo>/trunk` 以外）と `patch`（書き出したソースの文字列置換。置換元が1か所でなければ失敗する）が、今回足した仕組み。

**`ATK1EventPlugin` の限界**: atk1+tecs のアプリケーション CDL は `sample.cdl` だけで、イベントを使うセルが無い（inferred）。プラグインは読み込まれて実行されるが、`tmp_ATK1EventPlugin_0.cdl`・`tmp_ATK1EventPlugin_post_code.cdl`・`EVENT_tecsgen.oil` は 0 バイトで、生成ロジックの本体は記録されていない。記録されているのは「イベントが無いとき何も出さない」経路だけ。`ATK1DelayTaskPlugin` は atk1+tecs の CDL に使用箇所が無く、対象外。

一部のケースだけを採るには、`--kernel-golden <作業コピー>` の後ろに `collect_kernel.py` の引数をそのまま付ける（例: `sh tools/port/wsl_check.sh --kernel-golden <作業コピー> --case 'atk1/*'`。atk1 の2ケースだけなら約30秒）。

HRP2 は hrp2+tecs 自体の sample1 では採れません。`region` の古い文法（`[domain(DOMAIN1), out_through(), in_through()]`）が現行の tecsgen で構文エラー（G1016）になり、プラグインまで進まないためです。HRP2 ベースの ev3rt+tecs（`hr-tecs`）を使っています。

```sh
sh tools/port/wsl_check.sh --kernel-golden /mnt/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
```

- 前提: WSL に `gcc-arm-none-eabi`（ターゲットの `CC` は `arm-none-eabi-gcc`）と Ruby の `shell` gem（`gem install --user-install shell`。`configure.rb` が使う）。カーネルの SVN 作業コピーは `~/repo/svn-toppers-TECS-2/svn/toppers/<名前>/trunk`（環境変数 `KERNEL_REPOS_ROOT` で変更）。
- 作業ディレクトリは `~/p5kernel`（`/tmp` は WSL の再起動で消える）。採取には10分ほどかかります（`/mnt/e` への書き込みが遅い）。
- `--p3-oracle`（`wsl_check.sh --kernel-golden <作業コピー> --p3-oracle`）を付けると、正解データは採り直さず、`tests/ruby/p3_oracle.rb` を差し込んで同じケースを実行し、Ruby 版の外界とのやりとりの記録を `tests/golden/kernel/p3/<ID>.jsonl.gz` に書く。出力がコミット済みの正解データと一致したときだけ記録を置く（フックが出力を変えていない確認）。`tools/port/p4_progress.py` が再生する。全11ケースで30分ほどかかる。
- 各ケースの `meta.json` の `tecsgen_args` に、`make -n tecs` で得た tecsgen の呼び出しを記録します。
- カーネルのリポジトリは r3306 で、移植元 tecsgen（r3304）とは版が違います。同梱の tecsgen（r3306）は Ruby 3.x で `Proc.new` のエラーになるため、r3304 に差し替えて実行しています。カーネル側の CDL 自体は r3306 のままです。

## プラグインの網羅状況の計測

正解データが TECS のどのプラグインを実際に実行したかを、`plugin_trace.rb` で計測します。プラグイン名を出力から検索する方法は、名前が出力に現れない経路（`OpaqueMarshalerPlugin` など）を見落とすので使いません。

```sh
sh tools/port/wsl_check.sh --plugin-coverage /mnt/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
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

```sh
sh tools/port/wsl_check.sh --package-inventory
sh tools/port/wsl_check.sh --package-golden /mnt/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033 --out /home/ykomi/p5packageplugins/new-capture
```

`tools/golden/cases_packages.toml` が採集ケースです。`--package-golden` は `collect_packages.py` を呼び、成功したケースだけを `cases/<id>/` に保存します。既存の出力先は上書きせず、追加入力時は `--append --case <id>` を指定します。終了コード0、エラー0、タイムアウトなし、Plugin のインスタンス生成と生成ファイルあり、を正解ケースの条件とします。失敗した試行は `diagnostics/<id>/` に分離します。各 `meta.json` には元パッケージの CDL の SHA-256、実行引数、Plugin のロード・生成記録があり、`plugin_trace.txt` に生ログを保存します。

`--package-inventory refs` は CDL 内の `generate()` 指定、`targets` は ASP3 ターゲット一覧を表示します。`layout <package>`、`file <package> <relative-path>`、`locate <package> <filename>` はパッケージの調査に使います。既知の失敗2ケースは manifest で `enabled = false` とし、診断の再実行時だけ `--include-disabled --case <id>` を渡します。

採集済みは16ケースです。ASP3 系13パッケージの `NotifierPlugin`、`atk1+tecs` の ATK1 系、`MrubyBridgePluginPackage` の `Mruby2C`／C ブリッジ系、`mruby-on-ev3rt+tecs` の HRP2・mruby 系を含みます。RX 用の `ccrx.exe` は WSL に無く、旧 `MrubyBridge-test` は `cygwin_kernel.cdl` が r3304 で T1007 となるため、両試行は診断記録に留めています。`mruby-on-asp+tecs` と GR-PEACH の Plugin 使用は採集済み系統と重複し、`stm32primer2_tecs_edu` と `tecscde-MinGW` の製品 CDL には `generate()` の指定がありません。
