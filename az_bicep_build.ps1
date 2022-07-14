#!/usr/bin/env pwsh
#$in = Get-ChildItem -Recurse -Filter "*.bicep"
$in = $args

$error_azbuild = $false;
az bicep version
foreach ($b in $in) {
    $a = az bicep build --stdout --file $b
    if ( $LASTEXITCODE -eq 0 ) {
    }
    else {
        $error_azbuild = $true
    }
}
if ( $error_azbuild -eq $true ) {
    Exit 25
}
