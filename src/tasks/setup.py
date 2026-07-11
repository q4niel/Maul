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

    print(util.strColour(util.Colour.Cyan, "0"), " : None")
    print(util.strColour(util.Colour.Cyan, "1"), " : Linux Bash")

    match input("Tasks to generate: "):
        case "1":
            for key in tasks.dict:
                with open(f"mnt/.maul/tasks/{key}.sh", "wb") as file:
                    file.write(genLinuxBash(key).encode("utf-8"))
#task()