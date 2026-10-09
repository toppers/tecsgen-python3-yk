#!/bin/sh
# P3 のオラクルの記録（tests/golden/p3/）を採り直す。WSL 上で実行する。
#
#   sh tools/port/run_p3_oracle.sh <移植元 tecsgen ブランチの作業コピー>
#
# ソースの書き出しは run_p2_oracle.sh と共用する（~/p2work/tecs-src）。
# 環境変数 TECS_SRC_TREE・GOLDEN_EXCLUDE の意味も run_p2_oracle.sh と同じ。
set -e
WC=${1:?usage: run_p3_oracle.sh <tecsgen branch working copy>}
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
for g in ${GOLDEN_CASE:-}; do EXCL="$EXCL --case $g"; done
cp "$R/tests/ruby/ruby-p3-oracle" "$R/tests/ruby/p3_oracle.rb" "$B/"
chmod +x "$B/ruby-p3-oracle"
rm -rf "$B/oracle-out-p3"
python3 "$R/tools/golden/generate_golden.py" --source "$B/tecs-src" --out "$B/oracle-out-p3"   --work "$B/work" --ruby "$B/ruby-p3-oracle" $EXCL | tail -1
python3 "$R/tools/port/collect_p2_oracle.py" "$B/oracle-out-p3" p3
