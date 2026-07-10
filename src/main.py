from typing import List
import sys
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

    tasks.dict[selectedTask]()
    return
#main()

if __name__ == "__main__": main()#noqa