import os
import shutil
from pathlib import Path
import util

def genLinuxBash(tsk: str): return (
    "#!/bin/bash\n"
    f"{util.LocalConfig.containerEngine} run -itv $(realpath -m $0/../../..):/Maul/mnt maul:latest --{tsk}"
)

def genWindowsBatch(tsk: str): return (
    "@echo off\n"
    f"{util.LocalConfig.containerEngine} run -itv \"%~dp0..\\..:/Maul/mnt\" maul:latest --{tsk}"
)

def task() -> None:
    if not os.path.exists(maulDir:= "mnt/.maul"):
        os.mkdir(maulDir)

    if os.path.exists(tasksDir:= f"{maulDir}/tasks"):
        shutil.rmtree(tasksDir)
    os.mkdir(tasksDir)

    pyTasks: list[str] = []

    for path in Path("tasks").iterdir():
        if (path.name in ("__init__.py", "__pycache__")
        or  path.is_dir()
        ): continue

        pyTasks.append(path.stem)

    match util.LocalConfig.taskType:
        case util.LocalConfig.TaskType.linuxShell:
            for py in pyTasks:
                def gen(t: str) -> None:
                    with open(f"{tasksDir}/{t.replace(" ", "_")}.sh", "wb") as file:
                        file.write(genLinuxBash(t).encode("utf-8"))

                if py == "build":
                    for bldr in util.Config.builders:
                        gen(f"{py} {bldr}")
                    continue

                gen(py)

            for sh in os.listdir(prefix:= "tasks/linux_shell"):
                shutil.copy(f"{prefix}/{sh}", tasksDir)

        case util.LocalConfig.TaskType.windowsBatch:
            for py in pyTasks:
                def gen(t: str) -> None:
                    with open(f"{tasksDir}/{t.replace(" ", "_")}.bat", "wb") as file:
                        file.write(genWindowsBatch(t).encode("utf-8"))

                if py == "build":
                    for bldr in util.Config.builders:
                        gen(f"{py} {bldr}")
                    continue

                gen(py)

                for bat in os.listdir(prefix:= "tasks/windows_batch"):
                    shutil.copy(f"{prefix}/{bat}", tasksDir)
#task()