param(
    [int]$RetentionDays = 3,
    [string]$Root = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
if ($RetentionDays -lt 1) { throw 'RetentionDays must be at least 1.' }

$ResolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$VarRoot = Join-Path $ResolvedRoot 'var'
$Cutoff = (Get-Date).AddDays(-$RetentionDays)
$Removed = 0

foreach ($Directory in @('evidence', 'logs', 'reports')) {
    $Target = Join-Path $VarRoot $Directory
    if (-not (Test-Path -LiteralPath $Target -PathType Container)) { continue }
    $TargetRoot = (Resolve-Path -LiteralPath $Target).Path
    Get-ChildItem -LiteralPath $TargetRoot -File -Recurse | Where-Object {
        $_.LastWriteTime -lt $Cutoff
    } | ForEach-Object {
        $File = $_.FullName
        if (-not $File.StartsWith($TargetRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to delete a path outside the target directory: $File"
        }
        Remove-Item -LiteralPath $File -Force
        $Removed++
    }
}

Write-Output "Removed $Removed file(s) older than $RetentionDays day(s)."
