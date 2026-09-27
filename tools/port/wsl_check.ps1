<#
.SYNOPSIS
  Windows から WSL を起動し、tools/port/wsl_check.sh を実行する。

.DESCRIPTION
  リポジトリと移植元の作業コピーのパスを WSL のパス（/mnt/e/...）に変換してから渡す。
  Git Bash から wsl.exe に "/" で始まるパスを渡すと MSYS のパス変換で壊れるが、
  PowerShell から呼べばその問題は起きない。

.EXAMPLE
  pwsh tools/port/wsl_check.ps1
  pwsh tools/port/wsl_check.ps1 -Oracle E:/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033
  pwsh tools/port/wsl_check.ps1 -PytestArgs tests/test_p2_parser.py, -x
#>
param(
  # 指定すると、先に Ruby 版の記録（tests/golden/p2/・p3/）を採り直す
  [string]$Oracle = "",
  # pytest にそのまま渡す引数
  [string[]]$PytestArgs = @()
)

$ErrorActionPreference = "Stop"

function ConvertTo-WslPath([string]$Path) {
  $full = [System.IO.Path]::GetFullPath($Path) -replace '\\', '/'
  if ($full -notmatch '^([A-Za-z]):/(.*)$') {
    throw "WSL のパスに変換できません: $Path"
  }
  "/mnt/$($Matches[1].ToLower())/$($Matches[2])"
}

$repo = ConvertTo-WslPath (Join-Path $PSScriptRoot "../..")
$argsList = @()
if ($Oracle) {
  $argsList += @("--oracle", (ConvertTo-WslPath $Oracle))
}
$argsList += $PytestArgs

# 引数は bash の位置パラメータとして渡し、シェルの解釈を受けないようにする
wsl.exe -e bash -lc 'cd "$0" && sh tools/port/wsl_check.sh "$@"' $repo @argsList
exit $LASTEXITCODE
