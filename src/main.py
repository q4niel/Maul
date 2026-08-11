from typing import List
import sys, os, argparse
import util
import tasks

def main() -> None:
    # Ensure a project mounting point
    if not os.path.exists("mnt") or not os.path.isdir("mnt"):
        (util.Printer()
            .red("| Error: ")
            .default("No mounting point exists!")
            .newline()

            .red("| ")
            .default("Always mount your project with:")
            .newline()

            .red("| ")
            .cyan("YOUR_CONTAINER_ENGINE ")
            .default("run -v ")
            .cyan("PATH_TO_YOUR_PROJECT")
            .default(":/Maul/mnt maul:latest --")
            .cyan("TASK_TO_RUN")
        .exec())
        return

    util.Config.init()
    util.LocalConfig.init()

    def invalidConfigMsg(string: str) -> None:
        (util.Printer()
            .red("| Error: ")
            .default(f"{string} not valid, exiting process")
        .exec())

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

if __name__ == "__main__": main()