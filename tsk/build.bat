@echo off
cd /d "%~dp0\.."
call "tsk\.inc.bat"

if "%containerEngine%"=="podman" (
    podman build -f %containerFile% -t "%imageName%:latest" .
) else if "%containerEngine%"=="docker" (
    docker buildx build -f %containerFile% -t "%imageName%:latest" .
) else (
    echo %missingContainerEngineError%
    exit 1
)