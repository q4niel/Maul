import os
import shutil
import util
from util import Config as cfg
import subprocess

def task(builder: str) -> None:
    if not cfg.isValid:
        (util.Printer()
            .red("| Error: ")
            .default("Invalid Config File!")
        .exec())
        return

    if not os.path.exists(maulDir:= "mnt/.maul"):
        (util.Printer()
            .red("| Error: ")
            .default("Directory ")
            .cyan(maulDir)
            .default(" does not exist!")
            .newline()

            .red("| ")
            .default("Have the ")
            .cyan("taskgen ")
            .default("task been ran?")
        .exec())
        return

    if os.path.exists(workerDir:= f"{maulDir}/worker"):
        shutil.rmtree(workerDir)
    os.mkdir(workerDir)

    if builder not in cfg.builders:
        (util.Printer()
            .red("| Error: ")
            .default("Builder ")
            .cyan(builder)
            .default(" has no definition in config")
        .exec())
    else:
        for bin in cfg.builders[builder].binaries:
            buildBin(cfg.builders[builder], cfg.binaries[bin], workerDir)

    shutil.rmtree(workerDir)
#task()

def buildBin(bldr: util.Builder, bin: util.Binary, workerDir: str) -> None:
    containsCxx: bool = False

    for src in bin.sources:
        srcPath: str = f"mnt/{bin.sourceDirectory}/{src}"

        def compile(cxx: bool, path: str):
            subprocess.run ([
                f"clang{"++" if cxx else ""}",
                *(
                    cfg.globalCompFlags +
                    bin.compFlags +
                    bldr.compFlags +
                    (
                        cfg.globalCompCxxFlags +
                        bin.compCxxFlags +
                        bldr.compCxxFlags
                        if cxx else
                        cfg.globalCompCFlags +
                        bin.compCFlags +
                        bldr.compCFlags
                    )
                ),
                "-c",
                f"{srcPath}.{cfg.cxxExtension if cxx else cfg.cExtension}",
                "-o",
                f"{workerDir}/{f"{bin.sourceDirectory}/{src}".replace("/", "__")}.o"
            ])

        if os.path.exists(nPath:= f"{srcPath}.{cfg.cExtension}"):
            compile(False, nPath)
        elif os.path.exists(nPath:= f"{srcPath}.{cfg.cxxExtension}"):
            containsCxx = True
            compile(True, nPath)
        else:
            (util.Printer()
                .red("| Error: ")
                .default("Unresolved Source Path")
                .newline()

                .red("| ")
                .default("Neither ")
                .cyan(f"{srcPath}.{cfg.cExtension} ")
                .default("or ")
                .cyan(f"{srcPath}.{cfg.cxxExtension} ")
                .default("exists!")
            .exec())

    subprocess.run ([
        f"clang{"++" if containsCxx else ""}",
        *(
            cfg.globalLinkFlags +
            bin.linkFlags +
            bldr.linkFlags +
            (
                cfg.globalLinkCxxFlags +
                bin.linkCxxFlags +
                bldr.linkCxxFlags
                if containsCxx else
                cfg.globalLinkCFlags +
                bin.linkCFlags +
                bldr.linkCFlags
            )
        ),
        *(f"{workerDir}/{o}" for o in os.listdir(workerDir)),
        "-o",
        f"mnt/.maul/out/{bin.filename}"
    ])
#buildBin()