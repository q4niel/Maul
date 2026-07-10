#!/bin/bash
cd "$(realpath -m "$0/../..")"
source "tsk/.inc.sh"

podman build -f $containerFile -t $imageName:latest