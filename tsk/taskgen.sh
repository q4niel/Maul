#!/bin/bash
cd "$(realpath -m "$0/../..")"
source "tsk/.inc.sh"

foo() {
    if [[ $containerEngine == podman ]]; then
        podman run -itv $(pwd)/$1:/Maul/mnt $imageName:latest --taskgen
    elif [[ $containerEngine == docker ]]; then
        docker run -itv $(pwd)/$1:/Maul/mnt $imageName:latest --taskgen
    else
        echo -e $missingContainerEngineError
        exit 1
    fi
}

foo tst/hello_c
foo tst/hello_cxx