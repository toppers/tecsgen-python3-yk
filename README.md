# tecsgen-python3

TECS のコンポーネント記述コンパイラ tecsgen（Ruby 実装、v1.9.1）を Python 3 へ移植するプロジェクトです。

- CLI は Ruby 版と完全互換にします。
- CDL と import_C の C ヘッダは、Ruby 版と同じ方法で構文解析します。字句解析器は Ruby 版から移植し、パーサは Ruby 版の racc が生成した LALR 表（`bnf.tab.rb`・`C_parser.tab.rb`）を取り出して、racc の駆動部を移植したもので動かします。構文エラーの位置・件数やエラー回復も Ruby 版と一致します。
- 同じ入力に対して、Ruby 版と同一の生成物を出力することを受入基準にします（正解データは `tests/golden/`、採取手順は `tools/golden/README.md`）。

## セットアップ

```sh
uv sync
uv run pytest
```

### WSL で使う場合

正解データとの比較は WSL（Linux）で行います。Windows 側の `.venv` と混ざらないよう、仮想環境を別の場所に作ります（`/tmp` は WSL の再起動で消えるので使いません）。

Windows から一式（lint・型検査・pytest）を WSL で実行するには:

```powershell
pwsh tools/port/wsl_check.ps1                      # テスト一式
pwsh tools/port/wsl_check.ps1 -Oracle <移植元の作業コピー>   # 先に Ruby 版の記録を採り直す
pwsh tools/port/wsl_check.ps1 -PytestArgs tests/test_p2_parser.py, -x
```

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
| `wsl_check.ps1`・`wsl_check.sh` | WSL で uv sync・ruff・ty・pytest を実行する（仮想環境は `~/.venvs/tecsgen-python3`）。`-Oracle` で記録の採り直しも行う |
| `run_p2_oracle.sh` | 構文解析の差分テスト用に、Ruby 版の経過を記録し直す（WSL で実行。`tests/golden/p2/`） |
