$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$resolvedRoot = (Resolve-Path -LiteralPath $root).Path

function Assert-UnderRoot {
    param([string]$Path)
    $resolved = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
    if (-not $resolved.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove outside repository: $resolved"
    }
    return $resolved
}

$dirNames = @(
    "__pycache__", "Work", "Emulation-SW", "Emulation-HW", "package", "sd_card",
    ".Xil", "_x", "xsim.dir", "aiesimulator_output", "hw_emu", "sw_emu"
)

$removedDirs = 0
Get-ChildItem -LiteralPath $resolvedRoot -Force -Recurse -Directory -ErrorAction SilentlyContinue |
    Where-Object { ($dirNames -contains $_.Name) -or ($_.Name -like "tmp_*check") } |
    Sort-Object { $_.FullName.Length } -Descending |
    ForEach-Object {
        $path = Assert-UnderRoot $_.FullName
        Remove-Item -LiteralPath $path -Recurse -Force
        $removedDirs++
    }

$generatedExts = @(".txt", ".tmp", ".csv", ".dat", ".bin", ".npy", ".npz", ".pgm")
$removedFiles = 0

Get-ChildItem -LiteralPath $resolvedRoot -Force -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Extension -in @(".pyc", ".pyo", ".log", ".jou", ".wdb", ".xo", ".xclbin", ".xsa") -or
        (($_.FullName -match "\\(data|board_data)\\") -and ($generatedExts -contains $_.Extension.ToLowerInvariant()))
    } |
    ForEach-Object {
        $path = Assert-UnderRoot $_.FullName
        Remove-Item -LiteralPath $path -Force
        $removedFiles++
    }

Write-Host "Removed directories: $removedDirs"
Write-Host "Removed files: $removedFiles"
