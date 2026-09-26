# First build of the packwiz modpack from mods.txt on Windows. Requires: packwiz and python in PATH.
$PackName    = "suze modpack"
$PackAuthor  = "gwendalos"
$PackVersion = "1.0.0"

if (-not (Test-Path pack.toml)) {
  packwiz init --name "$PackName" --author "$PackAuthor" --version "$PackVersion" `
    --mc-version 26.2 --modloader fabric --fabric-latest
}
"" | Set-Content failed.txt
Get-Content mods.txt | ForEach-Object {
  $line = ($_ -replace '#.*', '').Trim()
  if ($line -eq '') { return }
  $parts = $line -split '\s+'
  $slug = $parts[0]
  if ($parts.Count -ge 3) {
    $ver = $parts[2]
    Write-Host "==> $slug (pinned $ver)"
    packwiz -y modrinth add "https://modrinth.com/mod/$slug/version/$ver"
    if ($LASTEXITCODE -eq 0) { packwiz pin $slug } else { Add-Content failed.txt "$slug $ver (version not found)" }
  } else {
    Write-Host "==> $slug"
    packwiz -y modrinth add $slug
    if ($LASTEXITCODE -ne 0) { Add-Content failed.txt $slug }
  }
}
python apply_sides.py
packwiz refresh
Write-Host "Check failed.txt for anything that needs attention."
