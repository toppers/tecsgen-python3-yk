#!/bin/sh
# WSL（Linux）上で、正解データを採った環境と同じ条件のテスト一式を実行する。
#
#   sh tools/port/wsl_check.sh [--oracle <移植元 tecsgen ブランチの作業コピー>] [pytest の引数]...
#   --package-inventory [refs|targets|layout|file|locate] と --package-golden も PowerShell から使用する。
#
# Windows からは tools/port/wsl_check.ps1 で呼ぶ（パスの変換を任せられる）。
#
# - 仮想環境は $HOME/.venvs/tecsgen-python3 に作る（UV_PROJECT_ENVIRONMENT）。
#   指定しないと、リポジトリの .venv（Windows 用）が Linux 用に作り直されてしまう。
#   /tmp は WSL の再起動で消えるので使わない
# - --oracle を付けると、先に run_p2_oracle.sh・run_p3_oracle.sh で Ruby 版の記録（tests/golden/p2/・p3/）を採り直す
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

if [ "${1:-}" = "--package-inventory" ]; then
  root="$HOME/Ccur/TECS-WG-DL"
  context="$R/tools/golden/packages_context.txt"
  [ -d "$root" ] || { echo "package directory not found: $root" >&2; exit 2; }
  [ -f "$context" ] || { echo "package list not found: $context" >&2; exit 2; }
  if [ "${2:-}" = "refs" ]; then
    while IFS= read -r package; do
      [ -d "$root/$package" ] || continue
      find "$root/$package" -type f -iname '*.cdl' -exec grep -HnE 'generate[[:space:]]*\(' {} +
    done < "$context"
    exit 0
  fi
  if [ "${2:-}" = "layout" ]; then
    while IFS= read -r package; do
      dir="$root/$package"
      [ -d "$dir" ] || continue
      [ -z "${3:-}" ] || [ "$package" = "$3" ] || continue
      printf 'PACKAGE\t%s\n' "$package"
      find "$dir" -maxdepth 9 -type f \( -name configure.rb -o -name Makefile -o -name tecsgen -o -name tecsgen.rb \) -print
    done < "$context"
    exit 0
  fi
  if [ "${2:-}" = "targets" ]; then
    while IFS= read -r package; do
      case "$package" in asp3_*) ;; *) continue ;; esac
      dir="$root/$package"
      [ -d "$dir" ] || continue
      printf 'PACKAGE\t%s\n' "$package"
      find "$dir" -type f -path '*/target/*/Makefile.target' -print
    done < "$context"
    exit 0
  fi
  if [ "${2:-}" = "file" ]; then
    package=${3:?package name required}
    relative=${4:?relative file path required}
    grep -Fxq -- "$package" "$context" || { echo "package not in Context: $package" >&2; exit 2; }
    case "$package/$relative" in
      *..*|/*) echo "invalid package file path" >&2; exit 2 ;;
    esac
    file="$root/$package/$relative"
    [ -f "$file" ] || { echo "package file not found: $file" >&2; exit 2; }
    cat "$file"
    exit 0
  fi
  if [ "${2:-}" = "locate" ]; then
    package=${3:?package name required}
    filename=${4:?file name required}
    grep -Fxq -- "$package" "$context" || { echo "package not in Context: $package" >&2; exit 2; }
    case "$package/$filename" in *..*|*/*/*) echo "invalid package or filename" >&2; exit 2 ;; esac
    find "$root/$package" -type f -name "$filename" -print
    exit 0
  fi
  while IFS= read -r package; do
    dir="$root/$package"
    if [ ! -d "$dir" ]; then
      printf '%s\tMISSING\n' "$package"
      continue
    fi
    count=$(find "$dir" -type f -iname '*.cdl' | wc -l)
    printf '%s\t%s\n' "$package" "$count"
  done < "$context"
  exit 0
fi

if [ "${1:-}" = "--package-golden" ]; then
  TECSGEN_WC=${2:?--package-golden requires the Ruby tecsgen working copy}
  shift 2
  exec python3 tools/golden/collect_packages.py \
    --packages-root "$HOME/Ccur/TECS-WG-DL" \
    --tecsgen-wc "$TECSGEN_WC" \
    --out tests/golden/packages "$@"
fi

ORACLE_WC=""
if [ "${1:-}" = "--oracle" ]; then
  ORACLE_WC=${2:?--oracle には移植元の作業コピーを指定します}
  shift 2
fi

# --kernel-golden <移植元 tecsgen ブランチの作業コピー> [collect_kernel.py の引数]...
#   カーネル依存プラグイン用の正解データ（tests/golden/kernel/）を採取して終わる。テストは走らせない。
#   作業ディレクトリは $HOME/p5kernel、SVN 作業コピー群は $HOME/repo/svn-toppers-TECS-2/svn/toppers
if [ "${1:-}" = "--kernel-golden" ]; then
  TECSGEN_WC=${2:?--kernel-golden には移植元 tecsgen ブランチの作業コピーを指定します}
  shift 2
  exec python3 tools/golden/collect_kernel.py \
    --repos-root "${KERNEL_REPOS_ROOT:-$HOME/repo/svn-toppers-TECS-2/svn/toppers}" \
    --tecsgen-wc "$TECSGEN_WC" \
    --out tests/golden/kernel "$@"
fi

# --plugin-coverage <移植元 tecsgen ブランチの作業コピー>
#   正解データを採る Ruby 版の実行を計測フック付きで走らせ、どのプラグインが実行されたかを集計して終わる。
#   テストは走らせない。詳細は tools/golden/README.md
if [ "${1:-}" = "--plugin-coverage" ]; then
  TECSGEN_WC=${2:?--plugin-coverage には移植元 tecsgen ブランチの作業コピーを指定します}
  exec sh tools/golden/run_plugin_coverage.sh "$TECSGEN_WC"
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
  step "run_p3_oracle.sh" sh tools/port/run_p3_oracle.sh "$ORACLE_WC"
fi
step "uv sync" uv sync --quiet
step "ruff check" uv run --quiet ruff check .
step "ruff format --check" uv run --quiet ruff format --check .
step "ty check" uv run --quiet ty check
step "pytest" uv run --quiet pytest -q "$@"

echo
echo "summary (venv: $UV_PROJECT_ENVIRONMENT):$SUMMARY"
exit $FAILED
