# Changelog

## Unreleased

- `tecsgen-path` コマンドを追加: 標準 CDL ライブラリ（`tecs/`）を含むディレクトリを標準出力へ書く（CMake などの呼び出し側が `tecs/` の場所を知るため。`tecsgen` コマンドには新しいオプションを足さない）。
- Ruby 版（tecsgen-rb）の cmake 対応を移植: `gen/CMakeLists.tecsgen.cmake`（ソース一覧のマニフェスト。`Makefile.tecsgen` の代わりに CMake から `include()` する）を生成し、プラグイン向けの `CMake` API（`add_source`・`add_include`・`add_define`・`add_link_option`・`add_custom_command`・`add_line`）を追加。CLI オプションの追加は無い。
- `TransparentRPCSignaturePlugin` を移植（tecsgen-rb で追加されたプラグイン）。これにより `RPCPlugin`・`DataPumpHolderPlugin` を使う CDL が、Ruby 版と同じく成功する（`DataPumpHolderPlugin` の `gen_ep_func_body` も移植）。
- `MultiPlugin#get_plugin` が返したクラスを、実行ごとの名前表に登録して名前で引けるようにした（`plugin_module.py` の `_register_plugin_class`）。ファイル名と違う名前のクラス（利用者の `MultiPlugin` と同じファイルに書いたクラス）は、これまで post_code の生成などで見つからず黙って飛ばされ、`tmp_<クラス名>_post_code.cdl` と `TECS_IMPORT_CDLS` の行が Ruby 版と違っていた。
- `CMake.add_*` を signature・cell・composite・multi・through・domain・class の各プラグインから呼ぶ正解データ `cmake_add_<種類>` を追加（Ruby 版と一致）。`generate_golden.py` のケースに `base`（既存ケースのディレクトリを写してから `inputs` を重ねる）を追加。
- `CMake.add_*` を呼ぶプラグインの正解データ `cmake_add` を追加（合成した利用者プラグイン。`gen/` の 13 ファイルが tecsgen-rb と一致）。`wsl_check.sh` に、`--oracle` で記録を採るケースを絞る先頭オプション `--case` を追加。`generate_golden.py` の合成入力は `*.rb` も写し、`cwd` が無ければ作る。
- 正解データの基準を、SVN r3304 から tecsgen-rb（`asp3_stm32cube_TECS` の `tecsgen-rb`）へ切り替えた。`transparent_marshaler` だけは tecsgen-rb に `TransparentMarshalerPlugin.rb` が無いため、r3304 の正解データを残している。
- 標準 CDL ライブラリ（`tecs/`）をパッケージに同梱（`uv tool install` で import できるように）。
- `tecsmerge` を移植（Ruby 版 `tecsmerge.rb` と、標準出力・標準エラー出力・終了コード・生成ファイルが一致）。
- `--help`・`--version` の出力が Ruby 版と一致することをテストに追加。
