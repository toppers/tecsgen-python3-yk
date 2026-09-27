#!/bin/sh
# WSL（Linux）上で、正解データを採った環境と同じ条件のテスト一式を実行する。
#
#   sh tools/port/wsl_check.sh [--oracle <移植元 tecsgen ブランチの作業コピー>] [pytest の引数]...
#
# Windows からは tools/port/wsl_check.ps1 で呼ぶ（パスの変換を任せられる）。
#
# - 仮想環境は $HOME/.venvs/tecsgen-python3 に作る（UV_PROJECT_ENVIRONMENT）。
#   指定しないと、リポジトリの .venv（Windows 用）が Linux 用に作り直されてしまう。
#   /tmp は WSL の再起動で消えるので使わない
# - --oracle を付けると、先に run_p2_oracle.sh で Ruby 版の記録（tests/golden/p2/）を採り直す
# - 続けて uv sync・ruff check・ruff format --check・ty check・pytest を順に実行し、
#   最後に各段階の結果をまとめて表示する。どれかが失敗すると終了コード 1
set -u

R=$(cd "$(dirname "$0")/../.." && pwd)
cd "$R" || exit 1

case "$(uname -s)" in
  Linux) ;;
  *) echo "wsl_check.sh: WSL（Linux）で実行してください。Windows からは tools/port/wsl_check.ps1 を使います" >&2
     exit 2 ;;
esac

ORACLE_WC=""
if [ "${1:-}" = "--oracle" ]; then
  ORACLE_WC=${2:?--oracle には移植元の作業コピーを指定します}
  shift 2
fi

export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-$HOME/.venvs/tecsgen-python3}"
# 別のプロジェクトで有効化した仮想環境が残っていると uv が警告するので外す
unset VIRTUAL_ENV

SUMMARY=""
FAILED=0

step() {
  name=$1
  shift
  echo "==> $name"
  if "$@"; then
    SUMMARY="$SUMMARY
  ok    $name"
  else
    SUMMARY="$SUMMARY
  FAIL  $name"
    FAILED=1
  fi
}

if [ -n "$ORACLE_WC" ]; then
  step "run_p2_oracle.sh" sh tools/port/run_p2_oracle.sh "$ORACLE_WC"
fi
step "uv sync" uv sync --quiet
step "ruff check" uv run --quiet ruff check .
step "ruff format --check" uv run --quiet ruff format --check .
step "ty check" uv run --quiet ty check
step "pytest" uv run --quiet pytest -q "$@"

echo
echo "summary (venv: $UV_PROJECT_ENVIRONMENT):$SUMMARY"
exit $FAILED
