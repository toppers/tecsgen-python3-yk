# HRP2 プラグイン用の合成入力 CDL

`tools/golden/cases_kernel.toml` の `hrp2/*` ケースが使う入力です。`collect_kernel.py` がカーネルのリポジトリの `obj-golden/` へ置き、現行の tecsgen（r3304）で実行します。

実プロジェクトの CDL は、次のプラグインを一度も使いません。

- hrp2+tecs の sample1 は、region の古い文法（`domain(DOMAIN1)` など）が現行の tecsgen で構文エラー（G1016）になり、プラグインまで進みません。
- ev3rt+tecs の `kernel.cdl` は `HRP2ObjectPlugin`・`HRP2HandlerPlugin` を使い、個別プラグインを使いません。

そこでカーネルの CDL を import し、現行の文法（`domain(HRP2, "trusted")`）で region を書いた最小のアプリケーションを置きます。

CDL のコメントは ASCII だけにしています。tecsgen を `-k euc`（カーネルの CDL が EUC-JP のため）で呼ぶので、UTF-8 の日本語を入れると EUC として不正なバイトになるためです。説明はこのファイルに書きます。

| ケース | 入力 | カーネルの CDL | 動くプラグイン | 結果 |
|---|---|---|---|---|
| `hrp2/objects` | `hrp2_objects.cdl` | hrp2+tecs `include/kernel.cdl` | `HRP2Plugin`、`HRP2SemaphorePlugin`・`HRP2EventflagPlugin`・`HRP2DataqueuePlugin`・`HRP2PriorityDataqueuePlugin`・`HRP2FixedSizeMemoryPoolPlugin`、`HRP2SVCPlugin` | 正常終了 |
| `hrp2/cyclic` | `hrp2_cyclic.cdl` | 同上 | `HRP2CyclicHandlerPlugin` | 例外（終了コード 1） |
| `hrp2/alarm` | `hrp2_alarm.cdl` | 同上 | `HRP2AlarmHandlerPlugin` | 例外（終了コード 1） |
| `hrp2/rpc` | `hrp2_rpc.cdl`（＋`hrp2_rpc_common.cdl`） | ev3rt+tecs `hr-tecs/include/kernel.cdl` | `HRP2RPCPlugin`、`GenHRP2Marshaler`、`GenTransparentMarshaler` | 正常終了 |
| `hrp2/rpc_ptr` | `hrp2_rpc_ptr.cdl`（＋`hrp2_rpc_common.cdl`） | 同上 | 同上 | 例外（終了コード 1） |

## 配置で網羅している分岐（`hrp2/objects`）

- カーネルドメイン（trusted）・ユーザドメイン（nontrusted）・無所属（OutOfDomain）の3種。ドメインによって `KERNEL_DOMAIN{}`／`DOMAIN(...){}` の出力先と、`accessPattern` の省略時の既定値（`TACP_KERNEL`／`TACP(<ドメイン>)`／`TACP_SHARED`）が変わる。
- `accessPattern` を省略したセルと、明示したセル。
- ユーザドメインからカーネルオブジェクトセルへの結合（仲介プラグインなし）と、カーネルドメインの通常セルへの結合（`HRP2SVCPlugin`）。

## 例外になるケース

- **周期・アラームハンドラ**: `HRP2CyclicHandlerPlugin`・`HRP2AlarmHandlerPlugin` は region の古い API（`get_region_type == :DOMAIN`、`get_param == :KERNEL_DOMAIN`）でカーネルドメインを判定する。`HRP2Plugin` の `domain(HRP2, "trusted")` で宣言した region ではこの判定が成り立たず、どこに置いても `must belong to kernel domain.` の例外になる。例外で処理が止まるので、1ケースに1種類しか置けない。
- **RPC のポインタ引数**: `GenHRP2Marshaler` は整数のビット幅（8・16・32・64・128）が決まる値渡しだけを扱う。ポインタ・配列の引数は `HRP2 RPC supports only specified bit_size` の例外になる。

どちらも Ruby 版の振る舞いなので、Python 版も同じ例外・終了コードと、例外までに作られたファイルを再現する対象になる。

## RPC のための補い（`hrp2_rpc_common.cdl`）

`HRP2RPCPlugin` が前提にする `tMessagebufferChannel`・`tRPCDedicatedTaskMain` は、手元のどのカーネル定義にもそのままでは合わないので、ここで定義する。

- ev3rt+tecs 同梱の `tMessageBufferChannel.cdl` は、`tMessageBuffer` に無い属性 `maxMessageSize` と、`tSemaphore` に無い属性 `initialCount` を使う。
- `tecs/rpc/RPCTask.cdl` の `tRPCDedicatedTaskMain` は `sUnmarshalerMain` を受けるが、`HRP2RPCPlugin` が生成するアンマーシャラの受け口は `sTaskBody`。
