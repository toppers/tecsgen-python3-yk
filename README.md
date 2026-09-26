# tecsgen-python3

TECS のコンポーネント記述コンパイラ tecsgen（Ruby 実装、v1.9.1）を Python 3 へ移植するプロジェクトです。

- CLI は Ruby 版と完全互換にします。
- CDL と C ヘッダの構文解析には、tree-sitter 製のパーサ（`tree-sitter-cdl`・`tree-sitter-tecs-cdecl`）を使います。文法の C ソースは `src/tecsgen/syntax/grammars/` に同梱し、C 拡張としてビルドします。
- 同じ入力に対して、Ruby 版と同一の生成物を出力することを受入基準にします（正解データは `tests/golden/`、採取手順は `tools/golden/README.md`）。

## セットアップ

C コンパイラが必要です（Windows は Visual Studio の MSVC、Linux は gcc）。

```sh
uv sync
uv run pytest
```

### Windows で `uv sync` のビルドが失敗する場合

シェルに Visual Studio の開発者コマンドプロンプトの環境（`VSCMD_ARG_TGT_ARCH` など）が読み込まれていると、ビルドに失敗することがあります。

- x86 用の環境が読み込まれていると、64 ビット版 Python 向けなのに 32 ビット用のリンカが選ばれ、`LNK2001`（`__imp__PyModule_Create2` が未解決）で失敗します。
- PATH が長すぎると、setuptools が呼ぶ `vcvarsall.bat` が「入力行が長すぎます」で失敗します。

その場合は、開発者コマンドプロンプトの環境変数を外し、PATH を短くしてからビルドします（PowerShell）。

```powershell
foreach ($v in 'VSCMD_ARG_HOST_ARCH','VSCMD_ARG_TGT_ARCH','VSCMD_ARG_app_plat','VSCMD_VER','VSINSTALLDIR','INCLUDE','LIB','LIBPATH','__VSCMD_PREINIT_PATH') {
    Remove-Item "env:$v" -ErrorAction SilentlyContinue
}
$uv = (Get-Command uv).Source
$env:PATH = "$(Split-Path $uv);C:\Windows\System32;C:\Windows;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Program Files (x86)\Microsoft Visual Studio\Installer"
uv sync
```

### WSL で使う場合

正解データとの比較は WSL（Linux）で行います。Windows 側の `.venv` と混ざらないよう、仮想環境を別の場所に作ります。

```sh
export UV_PROJECT_ENVIRONMENT=/tmp/tecsgen-venv
uv sync
uv run pytest
```

## tree-sitter パーサの動作確認

```sh
uv run example
```
