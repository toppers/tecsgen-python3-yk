#!/bin/sh
# 既存の正解データ採取（tecsgen の test/ 155ケース＋カーネルのケース）を、計測フック付きで実行し、
# どのプラグインが実行されたかを集計する。WSL（Linux）で実行する。
#
#   sh tools/golden/run_plugin_coverage.sh <移植元 tecsgen ブランチの作業コピー>
#
# Windows からは tools/port/wsl_check.ps1 -PluginCoverage <作業コピー> で呼ぶ。
#
# - 採取結果は $HOME/p5kernel/cov/ に捨てる（tests/golden には何も書かない）。目的はプラグインの記録だけ
# - 記録は plugin_trace.rb（RUBYOPT=-r で差し込む）が TECS_PLUGIN_LOG に書く
# - 集計は plugin_coverage.py。結果は標準出力と $HOME/p5kernel/cov/report.txt
# - 20〜40分ほどかかる（/mnt/e への書き込みが遅い）
set -u

WC=${1:?移植元 tecsgen ブランチの作業コピーを指定します}
HERE=$(cd "$(dirname "$0")" && pwd)
W=${COV_WORK:-$HOME/p5kernel/cov}
REPOS=${KERNEL_REPOS_ROOT:-$HOME/repo/svn-toppers-TECS-2/svn/toppers}
mkdir -p "$W"
: > "$W/trace_main.log"
: > "$W/trace_kernel.log"

echo "==> export test/ and tecsgen/ (svn export -r BASE --native-eol LF)"
rm -rf "$W/src" && mkdir -p "$W/src"
for d in tecsgen test; do
  svn export -q -r BASE --native-eol LF "$WC/$d" "$W/src/$d" || exit 1
done

export RUBYOPT="-r$HERE/plugin_trace.rb"

echo "==> tecsgen test/ cases"
TECS_PLUGIN_LOG="$W/trace_main.log" python3 "$HERE/generate_golden.py" \
  --source "$W/src" --out "$W/out-main" --work "$W/work-main" > "$W/main.out" 2>&1
echo "    exit=$?  ($(tail -1 "$W/main.out"))"

echo "==> kernel cases"
TECS_PLUGIN_LOG="$W/trace_kernel.log" python3 "$HERE/collect_kernel.py" \
  --repos-root "$REPOS" --tecsgen-wc "$WC" \
  --out "$W/out-kernel" --work "$W/work-kernel" > "$W/kernel.out" 2>&1
echo "    exit=$?  ($(tail -1 "$W/kernel.out"))"

unset RUBYOPT
python3 "$HERE/plugin_coverage.py" --plugin-dir "$W/src/tecsgen/tecslib/plugin" \
  --trace "main=$W/trace_main.log" --trace "kernel=$W/trace_kernel.log" | tee "$W/report.txt"
echo "report: $W/report.txt"
