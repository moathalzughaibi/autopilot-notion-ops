
# verify_checksums.ps1
Param(
  [string]$IndexJson = "IFNS_Indicators_Packs_Index_v0_18.json"
)
$index = Get-Content $IndexJson | ConvertFrom-Json
$all_ok = $true
foreach ($item in $index.items) {
  $path = Join-Path (Split-Path $IndexJson) $item.filename
  if (-Not (Test-Path $path)) {
    Write-Host "MISSING: $($item.filename)"
    $all_ok = $false
    continue
  }
  $hash = Get-FileHash -Algorithm SHA256 $path
  if ($hash.Hash.ToLower() -ne $item.sha256.ToLower()) {
    Write-Host "MISMATCH: $($item.filename)"
    Write-Host " expected: $($item.sha256)"
    Write-Host " actual  : $($hash.Hash.ToLower())"
    $all_ok = $false
  } else {
    Write-Host "OK: $($item.filename)"
  }
}
if ($all_ok) { Write-Host "ALL OK" } else { exit 2 }
