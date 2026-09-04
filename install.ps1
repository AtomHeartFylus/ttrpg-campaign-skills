# Install (copy) the skills into an agent skills directory.
#   ./install.ps1 -Target "$HOME/.agents/skills"
param([string]$Target = "$HOME/.agents/skills")
$src = Join-Path $PSScriptRoot 'skills'
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Get-ChildItem -Path $src -Directory | ForEach-Object {
    $dest = Join-Path $Target $_.Name
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse $_.FullName $dest
    $refs = Join-Path $dest 'references'
    New-Item -ItemType Directory -Force -Path $refs | Out-Null
    Copy-Item (Join-Path $PSScriptRoot 'docs/PRINCIPLES.md') (Join-Path $refs 'PRINCIPLES.md')
    Write-Host "installed $($_.Name) -> $dest"
}
