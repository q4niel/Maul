#!/bin/bash
cd "$(realpath -m "$0/../..")"
source "tsk/.inc.sh"

foo() {
    podman run -itv $(pwd)/$1:/Maul/mnt $imageName:latest --task-gen
}

foo tst/hello_c
foo tst/hello_cxx