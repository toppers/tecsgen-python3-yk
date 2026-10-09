# CMake.add_* を呼ぶプラグイン用の合成入力

`tools/golden/cases.toml` の `cmake_add` ケースが使う入力です。`generate_golden.py` が `test/cmake_add/` へ置き、`-L .` で `MyCMakePlugin.rb` を読ませて tecsgen-rb で実行します。

標準付属プラグインにも `asp3_stm32cube_TECS` にも `TECSGEN::CMake.add_*` を呼ぶ箇所が無いので、利用者プラグインで合成します（`gen_cmake_tecsgen` が `get_*` で読むだけ）。Python 版のプラグインは `tests/user_plugins/cmake_add/MyCMakePlugin.py` です。

`MyCMakePlugin` はセルタイププラグインで、次を確かめます。

- コンストラクタから `add_source`（重複・Symbol）、`add_include`（`$(BASE_DIR)` 付き・`\` を含む絶対パス）、`add_define`（文字列・整数）、`add_link_option`、`add_custom_command`、`add_line`（重複）を呼ぶ。出力で、重複が除かれ、Symbol・整数が文字列になり、`\` が `/` になること
- `new_cell` から `add_source` を呼ぶ。コンストラクタの後に追加されること
- `gen_factory` から `add_source` を呼ぶ。`gen_cmake_tecsgen` は生成の最初に走るので、**出力に反映されない**こと（`too_late.c` が出ない）

ソースの文字は ASCII だけにしています。
