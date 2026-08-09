#!/bin/bash
containerEngine=$(head -n 1 ./tsk/.container_engine)
missingContainerEngineError="Must define 'podman' or 'docker' within tsk/.container_engine!"
containerFile=Containerfile
imageName=maul