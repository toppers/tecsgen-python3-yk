# tecsgen-python3

TECS のコンポーネント記述コンパイラ tecsgen（Ruby 実装、v1.9.1）を Python 3 へ移植するプロジェクトです。

- CLI は Ruby 版と完全互換にします。
- CDL と C ヘッダの構文解析には、tree-sitter 製のパーサ（`tree-sitter-cdl`・`tree-sitter-tecs-cdecl`）を使います。
- 同じ入力に対して、Ruby 版と同一の生成物を出力することを受入基準にします。

## セットアップ

```sh
uv sync
uv run pytest
```

## tree-sitter パーサの動作確認

```sh
uv run example
```

CDL パーサの DLL の場所は、環境変数 `TECSGEN_CDL_DLL` で指定できます。
