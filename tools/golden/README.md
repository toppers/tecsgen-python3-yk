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

`--case <id>` を付けると、そのケースだけを採取し直します（glob 可、複数指定可）。

## ケース一覧

`cases.toml` に、移植元 `test/` の Makefile・シェルスクリプトから抜き出した tecsgen の呼び出しを並べています。make と C コンパイルは行わず、tecsgen の実行だけを再現します。

## 出力

`tests/golden/cases/<id>/` に次のファイルを保存します。

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
