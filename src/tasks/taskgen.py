import os
import shutil
import util

def genLinuxBash(tsk: str): return (
    "#!/bin/bash\n"
    f"{util.LocalConfig.containerEngine} run -itv $(realpath -m $0/../../..):/Maul/mnt maul:latest --{tsk}"
)

def task() -> None:
    if os.path.exists("mnt/.maul"):
        shutil.rmtree("mnt/.maul")

    os.makedirs("mnt/.maul")
    os.makedirs("mnt/.maul/out")
    os.makedirs("mnt/.maul/tasks")

    tasks: list[str] = os.listdir("tasks")
    tasks.remove("__init__.py")
    if (foo:= "__pycache__") in tasks:
        tasks.remove(foo)

    match util.LocalConfig.taskType:
        case util.LocalConfig.TaskType.linuxShell:
            for task in tasks:
                def gen(t: str) -> None:
                    with open(f"mnt/.maul/tasks/{t.replace(" ", "_")}.sh", "wb") as file:
                        file.write(genLinuxBash(t).encode("utf-8"))

                t: str = task.removesuffix(".py")

                if t == "build":
                    for bldr in util.Config.builders:
                        gen(f"{t} {bldr}")
                    continue

                gen(t)
#task()