#!/bin/bash
cd "$(realpath -m "$0/../..")"
source "tsk/.inc.sh"

foo() {
    podman run -v $(pwd)/$1:/Maul/mnt $imageName:latest --setup
}

foo tst/hello_world