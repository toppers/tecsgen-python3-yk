#!/bin/sh
# P2 のオラクルの記録（tests/golden/p2/）を採り直す。WSL 上で実行する。
#
#   sh tools/port/run_p2_oracle.sh <移植元 tecsgen ブランチの作業コピー>
#
# 作業コピーは CRLF のことがあるので、svn export --native-eol LF で ~/p2work/tecs-src に書き出して使う
# （/tmp は WSL の再起動で消えるため使わない）。
set -e
WC=${1:?usage: run_p2_oracle.sh <tecsgen branch working copy>}
R=$(cd "$(dirname "$0")/../.." && pwd)
B=$HOME/p2work
mkdir -p "$B"
if [ ! -d "$B/tecs-src" ]; then
  mkdir "$B/tecs-src"
  for d in tecsgen test; do svn export -q -r BASE --native-eol LF "$WC/$d" "$B/tecs-src/$d"; done
fi
cp "$R/tests/ruby/ruby-p2-oracle" "$R/tests/ruby/p2_oracle.rb" "$B/"
chmod +x "$B/ruby-p2-oracle"
rm -rf "$B/oracle-out"
python3 "$R/tools/golden/generate_golden.py" --source "$B/tecs-src" --out "$B/oracle-out" \
  --work "$B/work" --ruby "$B/ruby-p2-oracle" | tail -1
python3 "$R/tools/port/collect_p2_oracle.py" "$B/oracle-out"
