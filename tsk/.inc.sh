#!/bin/bash

containerFile=Containerfile
imageName=maul

deleteImage() {
    podman rmi -f $imageName:latest
}

buildImage() {
    podman build -f $containerFile -t $imageName:latest
}

runImage() {
    podman run -v $(pwd)/mnt:/Maul/mnt $imageName:latest "$@"
}