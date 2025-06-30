param (
    [string]$InputFile = "script.ps1",
    [string]$OutputFile = "payload.txt"
)

# load script
$raw = Get-Content $InputFile -Raw

# encode properly
$bytes = [System.Text.Encoding]::Unicode.GetBytes($raw)
$encoded = [Convert]::ToBase64String($bytes)

# final commad
$command = "powershell -EncodedCommand $encoded"

# whole pseudoducky here
$payload = @(
    "win + r",
    "delay 500",
    "string $command",
    "enter"
)

# ...aaaand save
$payload | Set-Content $OutputFile -Encoding UTF8

Write-Host "ducky-style payload generated: $OutputFile"
