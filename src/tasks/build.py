import os
import shutil
import util
from util import Config as cfg
import subprocess

def task() -> None:
    if not cfg.isValid:
        print(util.strColour(util.Colour.Red, "| Error: "), end="")
        print("Invalid Config File!")
        return

    if not os.path.exists(maulDir:= "mnt/.maul"):
        print(util.strColour(util.Colour.Red, "| Error: "), end="")
        print("Directory", util.strColour(util.Colour.Cyan, maulDir), "does not exist!")
        print(util.strColour(util.Colour.Red, "| "), end="")
        print("Have the", util.strColour(util.Colour.Cyan, "setup"), "task been ran?")
        return

    if os.path.exists(workerDir:= f"{maulDir}/worker"):
        shutil.rmtree(workerDir)
    os.mkdir(workerDir)

    for bin in cfg.binaries:
        buildBin(bin, workerDir)

    shutil.rmtree(workerDir)
#task()

def buildBin(bin: util.Binary, workerDir: str) -> None:
    for src in bin.sources:
        subprocess.run ([
            "clang++",
            "-std=c++23",
            "-c",
            f"mnt/{bin.sourceDirectory}/{src}.{cfg.cxxExtension}",
            "-o",
            f"{workerDir}/{f"{bin.sourceDirectory}/{src}".replace("/", "__")}.o"
        ])

    subprocess.run ([
        "clang++",
        "-std=c++23",
        *(f"{workerDir}/{o}" for o in os.listdir(workerDir)),
        "-o",
        f"mnt/.maul/out/{bin.filename}"
    ])
#buildBin()