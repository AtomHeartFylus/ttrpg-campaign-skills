# Install (copy) the skills into an agent skills directory.
#
#   ./install.ps1 -Target "$HOME/.agents/skills"
#   ./install.ps1 -Target "$HOME/.agents/skills" -DryRun     # say what would happen
#   ./install.ps1 -Target "$HOME/.agents/skills" -Uninstall  # remove what this installed
#
# If the host execution policy is Restricted:
#   powershell -ExecutionPolicy Bypass -File ./install.ps1 -Target "$HOME/.agents/skills"
#
# The repo is the canonical copy: installing REPLACES each target folder wholesale.
[CmdletBinding()]
param(
    [string]$Target = "$HOME/.agents/skills",
    [switch]$DryRun,
    [switch]$Uninstall
)

# Without these two, a half-failed copy exits 0 and leaves a partial install behind.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$src = Join-Path $PSScriptRoot 'skills'
$manifest = Join-Path $Target '.ttrpg-skills-manifest'
$folders = @(Get-ChildItem -Path $src -Directory)

if ($Uninstall) {
    $removed = 0
    foreach ($f in $folders) {
        $dest = Join-Path $Target $f.Name
        if (Test-Path $dest) {
            Remove-Item -Recurse -Force $dest
            Write-Host "removed $dest"
            $removed++
        }
    }
    if (Test-Path $manifest) { Remove-Item -Force $manifest }
    Write-Host "uninstalled $removed skill folder(s) from $Target"
    exit 0
}

if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $Target | Out-Null }

foreach ($f in $folders) {
    $dest = Join-Path $Target $f.Name
    if ($DryRun) {
        if (Test-Path $dest) {
            Write-Host "would REPLACE $dest (existing folder is deleted first)"
        } else {
            Write-Host "would install $($f.Name) -> $dest"
        }
        continue
    }
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse $f.FullName $dest
    Write-Host "installed $($f.Name) -> $dest"
}

if ($DryRun) {
    Write-Host "dry run: $($folders.Count) skill folder(s) would be installed into $Target"
    exit 0
}

$versionFile = Join-Path $PSScriptRoot 'VERSION'
$version = if (Test-Path $versionFile) { (Get-Content $versionFile -Raw).Trim() } else { 'unknown' }
$commit = 'unknown'
try { $commit = (git -C $PSScriptRoot rev-parse --short HEAD 2>$null).Trim() } catch { }
if (-not $commit) { $commit = 'unknown' }

@(
    "package: ttrpg-campaign-skills"
    "version: $version"
    "commit: $commit"
    "source: $PSScriptRoot"
    "installed: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))"
    "skills: $($folders.Count)"
) | Set-Content -Path $manifest -Encoding UTF8

Write-Host "$($folders.Count) skill folder(s) installed into $Target (version $version, commit $commit)"
Write-Host "edit the repo, never the installed copy: the next install replaces these folders whole."
