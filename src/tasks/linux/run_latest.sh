#!/bin/bash

red='\033[0;31m'
cyan='\033[0;36m'
default='\033[0m'
outDir="$(realpath -m "$0/../../out")"

if [[ -f "$outDir/LATEST_BUILD" ]]; then
    "$outDir/$(<"$outDir/LATEST_BUILD")"
else
    echo -e "${red}| Error:${default} Could not find the latest build"
    echo -e "${red}|${default} Have the project been successfully built?"
    echo -e "${red}|${default} Have the ${cyan}LATEST_BUILD${default} file been manually altered?"
fi