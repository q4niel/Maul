from typing import List
import sys, os, argparse
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

    util.Config.init()
    util.LocalConfig.init()

    def invalidConfigMsg(string: str) -> None:
        print (
            util.strColour(util.Colour.Red, "| Error: "),
            end=""
        )
        print(f"{string} not valid, exiting process")

    if not util.Config.isValid and not util.LocalConfig.isValid:
        invalidConfigMsg("maul and maul.local configs are")
        return
    elif not util.Config.isValid:
        invalidConfigMsg("maul config is")
        return
    elif not util.LocalConfig.isValid:
        invalidConfigMsg("maul.local config is")
        return

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
    group.add_argument (
        "-g",
        "--taskgen",
        action="store_true",
        help="Generate tasks for easier execution of Maul, define type in maul.local config"
    )
    group.add_argument (
        "-b",
        "--build",
        type=str,
        help="Run the provided builder, defined in maul.local config"
    )
    args: argparse.Namespace = parser.parse_args()

    if args.taskgen:
        tasks.taskgen()
    elif args.build:
        tasks.build(args.build)
#main()

if __name__ == "__main__": main()#noqa