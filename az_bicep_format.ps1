#!/usr/bin/env pwsh
#$in = Get-ChildItem -Recurse -Filter "*.bicep"
param([switch] $noupgrade )
$in = $args

$error_azbuild = $false;
az bicep version

if (! $noupgrade) {
    az bicep upgrade
}
foreach ($b in $in) {
    $a = az bicep format --stdout --file $b
    if ( $LASTEXITCODE -eq 0 ) {
    }
    else {
        $error_azbuild = $true
    }
}
if ( $error_azbuild -eq $true ) {
    Exit 25
}