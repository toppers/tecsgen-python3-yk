#!/bin/sh
# P2 のオラクルの記録（tests/golden/p2/）を採り直す。WSL 上で実行する。
#
#   sh tools/port/run_p2_oracle.sh <移植元 tecsgen ブランチの作業コピー>
#
# 作業コピーは CRLF のことがあるので、svn export --native-eol LF で ~/p2work/tecs-src に書き出して使う
# （/tmp は WSL の再起動で消えるため使わない）。
#
# 環境変数（wsl_check.sh の --src-tree・--exclude が設定する）
#   TECS_SRC_TREE   書き出し済みの木（tecsgen/ と test/ を含む）。指定すると svn export の代わりに
#                   これを ~/p2work/tecs-src へ写して使う（作業コピーの引数は無視する）
#   GOLDEN_EXCLUDE  採取しないケースの id（空白区切り）。generate_golden.py の --exclude へ渡す
set -e
WC=${1:?usage: run_p2_oracle.sh <tecsgen branch working copy>}
R=$(cd "$(dirname "$0")/../.." && pwd)
B=$HOME/p2work
mkdir -p "$B"
if [ -n "${TECS_SRC_TREE:-}" ]; then
  rm -rf "$B/tecs-src"
  cp -r "$TECS_SRC_TREE" "$B/tecs-src"
elif [ ! -d "$B/tecs-src" ]; then
  mkdir "$B/tecs-src"
  for d in tecsgen test; do svn export -q -r BASE --native-eol LF "$WC/$d" "$B/tecs-src/$d"; done
fi
EXCL=""
set -f
for g in ${GOLDEN_EXCLUDE:-}; do EXCL="$EXCL --exclude $g"; done
cp "$R/tests/ruby/ruby-p2-oracle" "$R/tests/ruby/p2_oracle.rb" "$B/"
chmod +x "$B/ruby-p2-oracle"
rm -rf "$B/oracle-out"
python3 "$R/tools/golden/generate_golden.py" --source "$B/tecs-src" --out "$B/oracle-out" \
  --work "$B/work" --ruby "$B/ruby-p2-oracle" $EXCL | tail -1
python3 "$R/tools/port/collect_p2_oracle.py" "$B/oracle-out"
