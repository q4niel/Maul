@echo off
set "containerEngine="
set /p containerEngine=<".\tsk\.container_engine"

set "missingContainerEngineError=Must define 'podman' or 'docker' within tsk/.container_engine!"
set "containerFile=Containerfile"
set "imageName=maul"