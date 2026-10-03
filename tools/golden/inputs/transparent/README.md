# TransparentMarshalerPlugin 用の合成入力 CDL

`tools/golden/cases.toml` の `transparent_marshaler` ケースが使う入力です。`generate_golden.py` が `test/rpc/` へ置き、現行の tecsgen（r3304）で実行します。

`TransparentMarshalerPlugin` は tecsgen の r3301 で加わった `SignaturePlugin` で、tecslib のどこからも `generate` されず、実プロジェクトの CDL にも使用例がありません（`SelectiveJoinSignaturePlugin` を持つ別ブランチだけが名前を挙げる）。`GenTransparentMarshaler` で marshaler・unmarshaler のセルタイプの CDL（`gen/tMarshaler_<シグニチャ>.cdl`）を作るだけのプラグインなので、`test/rpc/rpc_test.cdl` と同じ前提（`cygwin_kernel.cdl`・`rpc.cdl`）に、`generate(TransparentMarshalerPlugin, ...)` を置きます。

- `sSample`: ポインタ・文字列・構造体・oneway を含み、`PPAllocator` が必要になるシグニチャ
- `sPlain`: 値渡しだけで、`PPAllocator` が要らないシグニチャ

CDL のコメントは ASCII だけにしています。
