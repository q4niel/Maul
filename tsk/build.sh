#!/bin/bash
cd "$(realpath -m "$0/../..")"
source "tsk/.inc.sh"

# podman build -f $containerFile -t $imageName:latest

if [[ $containerEngine == podman ]]; then
    podman build -f $containerFile -t $imageName:latest .
elif [[ $containerEngine == docker ]]; then
    docker buildx build -f $containerFile -t $imageName:latest .
else
    echo -e $missingContainerEngineError
    exit 1
fi