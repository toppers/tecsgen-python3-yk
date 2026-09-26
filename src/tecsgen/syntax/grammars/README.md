# 同梱している tree-sitter 文法

tree-sitter が生成した C ソースを、移植元からそのまま複製しています。ここのファイルは編集しません。文法を変えるときは移植元で `grammar.ts` を直して `npm run generate` し、もう一度複製します。

| ディレクトリ | 取り込み元 | 移植元の文法 |
|---|---|---|
| `cdl/` | `tools-ts/tree-sitter-cdl/src` | `tecslib/core/bnf.y.rb`（CDL） |
| `tecs_cdecl/` | `tools-ts/tree-sitter-tecs-cdecl/src` | `tecslib/core/C_parser.y.rb`（import_C 用の C ヘッダ） |

- 取り込み元: TOPPERS TECS SVN `tecsgen/branches/ykominami_r3033`、r3305
- 生成ツール: tree-sitter CLI 0.25.10、ABI 15、外部スキャナなし
- ライセンス: MIT（取り込み元の `tree-sitter.json` による）
- 複製したもの: `parser.c`・`tree_sitter/*.h`・`node-types.json`（`grammar.json` は使わないので除いた）

## 複製し直す手順

Windows 上の SVN 作業コピーは CRLF になっていることがあるため、`svn export` で LF のまま書き出します。

```sh
WC=/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
svn export -r BASE --native-eol LF "$WC/tools-ts/tree-sitter-cdl/src" cdl
svn export -r BASE --native-eol LF "$WC/tools-ts/tree-sitter-tecs-cdecl/src" tecs_cdecl
rm -f cdl/grammar.json tecs_cdecl/grammar.json
```
