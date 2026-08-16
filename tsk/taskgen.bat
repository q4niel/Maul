@echo off
cd /d "%~dp0\.."
call "tsk\.inc.bat"

call :foo "tst/hello_c"
call :foo "tst/hello_cxx"
exit 0

:foo
if "%containerEngine%"=="podman" (
    podman run -itv "%~1:/Maul/mnt" %imageName%:latest --taskgen
) else if "%containerEngine%"=="docker" (
    docker run -itv "%~1:/Maul/mnt" %imageName%:latest --taskgen
) else (
    echo %missingContainerEngineError%
    exit 1
)
exit /b 0