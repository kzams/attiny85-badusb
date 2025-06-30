param (
    [string]$InputFile = "script.ps1",
    [string]$OutputFile = "payload.txt"
)

# load script
$raw = Get-Content $InputFile -Raw

# encode properly
$bytes = [System.Text.Encoding]::Unicode.GetBytes($raw)
$encoded = [Convert]::ToBase64String($bytes)

# ...aaaand save
$encoded | Set-Content $OutputFile -Encoding UTF8

Write-Host "b64 payload generated: $OutputFile"