#!/bin/bash
cd "$(realpath -m "$0/../..")"
source "tsk/.inc.sh"

# podman rmi -f $imageName:latest

if [[ $containerEngine == podman ]]; then
    podman rmi -f $imageName:latest
elif [[ $containerEngine == docker ]]; then
    docker rm -f $imageName:latest
else
    echo -e $missingContainerEngineError
    exit 1
fi