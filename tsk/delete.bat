@echo off
cd /d "%~dp0\.."
call "tsk\.inc.bat"

if "%containerEngine%"=="podman" (
    podman rmi -f "%imageName%:latest"
) else if "%containerEngine%"=="docker" (
    docker rm -f "%imageName%:latest"
) else (
    echo %missingContainerEngineError%
    exit 1
)