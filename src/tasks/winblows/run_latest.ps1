function red {
    process { Write-Host -NoNewline $_ -ForegroundColor Red }
}

function cyan {
    process { Write-Host -NoNewline $_ -ForegroundColor Cyan }
}

$outDir = "$PSScriptRoot/../out"

if (Test-Path "$outDir/LATEST_BUILD") {
    & "$outDir/$(Get-Content -Path "$outDir/LATEST_BUILD")"
}
else {
    Write-Output "$("| Error:" | red) Could not find the latest build"
    Write-Output "$("|" | red) Have the project been successfully built?"
    Write-Output "$("|" | red)$(Write-Host -NoNewline " Have the ")$("LATEST_BUILD" | cyan) file been manually altered?"
}