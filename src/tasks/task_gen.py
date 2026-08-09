import os
import shutil
import util
from . import tasks

def genLinuxBash(tsk: str): return (
    "#!/bin/bash\n"
    f"podman run -itv $(realpath -m $0/../../..):/Maul/mnt maul:latest --{tsk}"
)

def task() -> None:
    if os.path.exists("mnt/.maul"):
        shutil.rmtree("mnt/.maul")

    os.makedirs("mnt/.maul")
    os.makedirs("mnt/.maul/out")
    os.makedirs("mnt/.maul/tasks")

    match util.LocalConfig.taskType:
        case util.LocalConfig.TaskType.linuxShell:
            for key in tasks.dict:
                with open(f"mnt/.maul/tasks/{key}.sh", "wb") as file:
                    file.write(genLinuxBash(key).encode("utf-8"))
#task()