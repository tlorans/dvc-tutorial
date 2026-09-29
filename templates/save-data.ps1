<#
Save a new version of a data file with DVC, in one command.

    .\save-data.ps1 inputs\client-portfolio.xlsx "Client portfolio, September 2026"

It runs, in order: dvc add, git add, git commit, dvc push, git push.
It stops at the first command that fails, so nothing is half-saved silently.
#>
param(
    [Parameter(Mandatory = $true)] [string] $File,
    [Parameter(Mandatory = $true)] [string] $Message
)

function Run {
    Write-Host "> $args" -ForegroundColor Cyan
    & $args[0] $args[1..($args.Count - 1)]
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Stopped: the command above failed. Nothing after it was run." -ForegroundColor Red
        exit 1
    }
}

if (-not (Test-Path $File)) {
    Write-Host "File not found: $File" -ForegroundColor Red
    exit 1
}

$folder = Split-Path $File -Parent
if (-not $folder) { $folder = "." }

Run uv run dvc add $File
Run git add "$File.dvc" (Join-Path $folder ".gitignore")
Run git commit -m $Message
Run uv run dvc push
Run git push

Write-Host "Saved. Colleagues get this version with: git pull, then uv run dvc pull" -ForegroundColor Green
