from typing import List
import sys
import os
import util
import tasks

def main() -> None:
    msg: str = "Welcome to Maul"
    prints: List[str] = [
        "\n" * 10,
        "-" * len(msg),
        f"\n{msg}\n",
        "-" * len(msg),
        "\n" * 5
    ]
    for p in prints:
        print(util.strColour(util.Colour.Maul, p))

    # Ensure a project mounting point
    if not os.path.exists("mnt") or not os.path.isdir("mnt"):
        print (
            util.strColour(util.Colour.Red, "| Error:"),
            "No mounting point exists!"
        )
        print (
            util.strColour(util.Colour.Red, "|"),
            "Always mount your project with:"
        )
        print (
            util.strColour(util.Colour.Red, "|"),
            util.strColour(util.Colour.Cyan, "YOUR_CONTAINER_ENGINE"),
            "run -v",
            util.strColour(util.Colour.Cyan, "PATH_TO_YOUR_PROJECT") + ":/Maul/mnt maul:latest",
            "--" + util.strColour(util.Colour.Cyan, "TASK_TO_RUN")
        )
        return

    # Validate Flags
    flags: List[str] = []
    for i, a in enumerate(sys.argv):
        if i == 0 or not a.startswith("--"): continue#noqa
        flags.append(a.removeprefix("--"))

    # Ensure one task flag
    selectedTask: str = "NONE"
    for f in flags:
        if not "NONE" == selectedTask:
            print(util.strColour(util.Colour.Red, "| Error: "), end="")
            print("Task flag", util.strColour(util.Colour.Cyan, selectedTask), "already provided")
            print(util.strColour(util.Colour.Red, "|"), "Multiple tasks is not allowed")
            return

        selectedTask = f

    # Ensure selected task exists
    if selectedTask not in tasks.dict:
        print(util.strColour(util.Colour.Red, "| Error: "), end="")
        print("Task", util.strColour(util.Colour.Cyan, selectedTask), "doesn't exist")
        return

    util.Config.init()
    tasks.dict[selectedTask]()
    return
#main()

if __name__ == "__main__": main()#noqa