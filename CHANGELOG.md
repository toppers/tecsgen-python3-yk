# Changelog

## Unreleased

- `tecsgen-path` コマンドを追加: 標準 CDL ライブラリ（`tecs/`）を含むディレクトリを標準出力へ書く（CMake などの呼び出し側が `tecs/` の場所を知るため。`tecsgen` コマンドには新しいオプションを足さない）。
- Ruby 版（tecsgen-rb）の cmake 対応を移植: `gen/CMakeLists.tecsgen.cmake`（ソース一覧のマニフェスト。`Makefile.tecsgen` の代わりに CMake から `include()` する）を生成し、プラグイン向けの `CMake` API（`add_source`・`add_include`・`add_define`・`add_link_option`・`add_custom_command`・`add_line`）を追加。CLI オプションの追加は無い。
- `TransparentRPCSignaturePlugin` を移植（tecsgen-rb で追加されたプラグイン）。これにより `RPCPlugin`・`DataPumpHolderPlugin` を使う CDL が、Ruby 版と同じく成功する（`DataPumpHolderPlugin` の `gen_ep_func_body` も移植）。
- 正解データの基準を、SVN r3304 から tecsgen-rb（`asp3_stm32cube_TECS` の `tecsgen-rb`）へ切り替えた。`transparent_marshaler` だけは tecsgen-rb に `TransparentMarshalerPlugin.rb` が無いため、r3304 の正解データを残している。
- 標準 CDL ライブラリ（`tecs/`）をパッケージに同梱（`uv tool install` で import できるように）。
- `tecsmerge` を移植（Ruby 版 `tecsmerge.rb` と、標準出力・標準エラー出力・終了コード・生成ファイルが一致）。
- `--help`・`--version` の出力が Ruby 版と一致することをテストに追加。
