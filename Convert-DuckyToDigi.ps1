param (
    [string]$InputFile = "payload.txt",
    [string]$OutputFile = "converted.ino"
)

$map = @{
    "enter"     = 'DigiKeyboard.sendKeyStroke(KEY_ENTER);'
    "space"     = 'DigiKeyboard.sendKeyStroke(KEY_SPACE);'
    "win + r"   = 'DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);'
}

$header = @'
#include "DigiKeyboard.h"

void setup() {
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.delay(500);
'@

$footer = @'
}

void loop() {}
'@

$output = @()
$output += $header

Get-Content $InputFile | ForEach-Object {
    $line = $_.Trim()

    if ($line -match '^delay (\d+)$') {
        $output += "  DigiKeyboard.delay($($Matches[1]));"
    }
    elseif ($line -match '^string (.+)$') {
        $text = $Matches[1].Replace('"', '\"')
        $output += $('DigiKeyboard.print("' + $text + '");')
    }
    elseif ($map.ContainsKey($line)) {
        $output += "  " + $map[$line]
    }
    elseif ($line -eq "") {
        $output += ""
    }
    else {
        $output += "  // Somethings wrong: $line"
    }
}

$output += $footer
$output | Set-Content $OutputFile -Encoding UTF8

Write-Host "Your payload is here: $OutputFile"
