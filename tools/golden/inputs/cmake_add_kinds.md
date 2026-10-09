# CMake.add_* を種類ごとのプラグインから呼ぶ合成入力

`cases.toml` の `cmake_add_signature`・`cmake_add_cell`・`cmake_add_composite`・`cmake_add_multi`・`cmake_add_through`・`cmake_add_domain`・`cmake_add_class` が使う入力です（セルタイプは `cmake_add`、`cmake_add/README.md`）。各プラグインは、コンストラクタから `add_source`・`add_define`・`add_include`・`add_line` を種類ごとに別の値で呼びます。出力の `CMakeLists.tecsgen.cmake` に `K_<種類>=1` などが出ます。

| ケース | プラグイン（基底クラス） | 入力 |
|---|---|---|
| `cmake_add_signature` | `MySigPlugin`（`SignaturePlugin`） | 合成 `sig.cdl` |
| `cmake_add_cell` | `MyCellPlugin`（`CellPlugin`） | 合成 `cell.cdl` |
| `cmake_add_composite` | `MyCompositePlugin`（`CompositePlugin`） | 合成 `comp.cdl` |
| `cmake_add_multi` | `MyMultiPlugin`（`MultiPlugin`）と、`get_plugin` が返す `MyMultiCelltypePlugin` | 合成 `multi.cdl` |
| `cmake_add_through` | `Plugin1`（`ThroughPlugin`） | `test/through` の変種 |
| `cmake_add_domain` | `MyDomainPlugin`（`DomainPlugin`） | `test/restrict` の変種 |
| `cmake_add_class` | `MyClassPlugin`（`ClassPlugin`） | `test/class` の変種 |

- **`base`**: through・domain・class は、既存ケースのディレクトリ（`test/<base>`）を `cwd` へ丸ごと写してから、`add_*` を足したプラグイン（`*.rb`）で差し替える。pristine は全ケースで共有するので、`test/<base>` を直接上書きすると元のケースが変わってしまう
- **`cmake_add_multi`**: `MyMultiCelltypePlugin` は `MyMultiPlugin` と同じファイルに書く（ファイル名と違う名前のクラス）。Ruby 版ではこれが動く。Python 版は、`get_plugin` が返したクラスを名前で引けるようにする修正（`plugin_module.py` の `_register_plugin_class`）が入るまで、post_code ファイルが出なかった
- Python 版のプラグインは `tests/user_plugins/<ケース ID>/`
- `cmake_add_signature`・`cell`・`composite`・`multi` の CDL とプラグインは ASCII だけ
