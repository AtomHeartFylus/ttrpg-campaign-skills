# Install (copy) the skills into an agent skills directory.
#
#   ./install.ps1 -Target "$HOME/.agents/skills"
#   ./install.ps1 -Target "$HOME/.agents/skills" -DryRun     # say what would happen
#   ./install.ps1 -Target "$HOME/.agents/skills" -Uninstall  # remove what this installed
#   ./install.ps1 -Target "$HOME/.agents/skills" -Force      # also replace folders it doesn't own
#
# If the host execution policy is Restricted:
#   powershell -ExecutionPolicy Bypass -File ./install.ps1 -Target "$HOME/.agents/skills"
#
# The repo is the canonical copy: installing REPLACES each target folder wholesale.
#
# Ownership is tracked by the manifest (`skill: <name>` lines). A folder this installer did not
# create - an unmanaged name collision - is left untouched and the run exits non-zero, unless
# -Force is given. -Uninstall refuses to run against a missing or legacy (no `skill:` lines)
# manifest rather than guess which folders are ours, and only ever removes manifest-listed ones.
[CmdletBinding()]
param(
    [string]$Target = "$HOME/.agents/skills",
    [switch]$DryRun,
    [switch]$Uninstall,
    [switch]$Force
)

# Without these two, a half-failed copy exits 0 and leaves a partial install behind.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$src = Join-Path $PSScriptRoot 'skills'
$manifest = Join-Path $Target '.ttrpg-skills-manifest'
$folders = @(Get-ChildItem -Path $src -Directory)

function Get-ManagedSkills {
    param([string]$ManifestPath)
    if (-not (Test-Path $ManifestPath)) { return @() }
    $names = @(Get-Content $ManifestPath | Where-Object { $_ -match '^skill: ' } |
        ForEach-Object { $_.Substring(7).Trim() })
    return $names
}

# A manifest `skill:` value is trusted enough to be Remove-Item -Recurse'd, so it must be a
# bare basename naming an actual skill folder in THIS package's skills/ - never a path (no
# `/`, no `\`, no `.`/`..`) and never an unknown name. Checked by exact match against the real
# directory listing, not by testing path existence (which a `..`-laden name could satisfy).
function Test-ValidSkillName {
    param([string]$Name)
    if ([string]::IsNullOrEmpty($Name)) { return $false }
    if ($Name -eq '.' -or $Name -eq '..') { return $false }
    if ($Name -match '[\\/]') { return $false }
    return @($folders | Where-Object { $_.Name -eq $Name }).Count -gt 0
}

if ($Uninstall) {
    if (-not (Test-Path $manifest)) {
        Write-Error "refusing to uninstall: no manifest at $manifest - cannot tell which folders in $Target are ours"
        exit 1
    }
    $managed = @(Get-ManagedSkills -ManifestPath $manifest)
    if ($managed.Count -eq 0) {
        Write-Error "refusing to uninstall: $manifest has no 'skill:' entries (legacy manifest, or one hand-edited) - cannot tell which folders in $Target are ours"
        exit 1
    }
    $invalid = @($managed | Where-Object { -not (Test-ValidSkillName $_) })
    if ($invalid.Count -gt 0) {
        Write-Error "refusing to uninstall: $manifest lists invalid or unknown skill: entries (($($invalid -join ', '))) - it may be hand-edited or corrupted; touching nothing"
        exit 1
    }
    $removed = 0
    foreach ($name in $managed) {
        $dest = Join-Path $Target $name
        if (Test-Path $dest) {
            Remove-Item -Recurse -Force $dest
            Write-Host "removed $dest"
            $removed++
        }
    }
    Remove-Item -Force $manifest
    Write-Host "uninstalled $removed skill folder(s) from $Target"
    exit 0
}

# Ownership established by a prior install of THIS package: only these names may be replaced
# wholesale without -Force.
$existingManaged = @(Get-ManagedSkills -ManifestPath $manifest | Where-Object { Test-ValidSkillName $_ })

if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $Target | Out-Null }

$installedNames = @()
$skipped = 0
$considered = 0
foreach ($f in $folders) {
    $dest = Join-Path $Target $f.Name
    $collision = Test-Path $dest
    $owned = $collision -and ($existingManaged -contains $f.Name)
    $considered++

    if ($DryRun) {
        if (-not $collision) {
            Write-Host "would install $($f.Name) -> $dest"
        } elseif ($Force -or $owned) {
            Write-Host "would REPLACE $dest (existing folder is deleted first)"
        } else {
            Write-Host "would REFUSE $dest (unmanaged folder in the way; rerun with -Force to replace it)"
        }
        continue
    }

    if ($collision -and -not $Force -and -not $owned) {
        Write-Warning "refusing to replace unmanaged folder: $dest (not owned by a prior install of this package; use -Force to override)"
        $skipped++
        continue
    }

    if ($collision) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse $f.FullName $dest
    Write-Host "installed $($f.Name) -> $dest"
    $installedNames += $f.Name
}

if ($DryRun) {
    Write-Host "dry run: $considered skill folder(s) considered for $Target"
    exit 0
}

$versionFile = Join-Path $PSScriptRoot 'VERSION'
$version = if (Test-Path $versionFile) { (Get-Content $versionFile -Raw).Trim() } else { 'unknown' }
$commit = 'unknown'
try { $commit = (git -C $PSScriptRoot rev-parse --short HEAD 2>$null).Trim() } catch { }
if (-not $commit) { $commit = 'unknown' }

$manifestLines = @(
    "package: ttrpg-campaign-skills"
    "version: $version"
    "commit: $commit"
    "source: $PSScriptRoot"
    "installed: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))"
    "skills: $($installedNames.Count)"
) + ($installedNames | ForEach-Object { "skill: $_" })
$manifestLines | Set-Content -Path $manifest -Encoding UTF8

Write-Host "$($installedNames.Count) skill folder(s) installed into $Target (version $version, commit $commit)"
Write-Host "edit the repo, never the installed copy: the next install replaces these folders whole."
if ($skipped -gt 0) {
    Write-Warning "$skipped folder(s) refused (unmanaged collision) - use -Force to replace them"
    exit 1
}
