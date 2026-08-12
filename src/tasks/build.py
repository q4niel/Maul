import os
import shutil
import util
from util import Config as cfg
import subprocess
from datetime import datetime
from typing import Any

def task(builder: str) -> None:
    if not cfg.isValid:
        (util.Printer()
            .red("| Error: ")
            .default("Invalid Config File!")
        .exec())
        return

    if not os.path.exists(maulDir:= "mnt/.maul"):
        os.mkdir(maulDir)

    if not os.path.exists(outDir:= f"{maulDir}/out"):
        os.mkdir(outDir)

    if os.path.exists(workerDir:= f"{maulDir}/worker"):
        shutil.rmtree(workerDir)
    os.mkdir(workerDir)

    buildDir: str = f"{outDir}/MAUL_BUILDER"

    if builder not in cfg.builders:
        (util.Printer()
            .red("| Error: ")
            .default("Builder ")
            .cyan(builder)
            .default(" has no definition in config")
        .exec())
    else:
        for dir in cfg.builders[builder].mkdirs:
            os.makedirs(f"{buildDir}/{dir}")

        potentialExec: Any = None
        execDst: str = ""

        for binData in cfg.builders[builder].binaries:
            buildBin (
                cfg.builders[builder],
                bin:= cfg.binaries[binData.bin],
                workerDir,
                f"{buildDir}/{binData.dst}"
                    if binData.dst != "" else
                buildDir
            )

            if bin.type == util.Binary.Type.executable:
                potentialExec = bin
                execDst = binData.dst

        timestamp: str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        if potentialExec != None:
            with open(f"{outDir}/LATEST_BUILD", "wb") as file:
                content: str = (
                    f"{timestamp}/{execDst}{
                        "/" if execDst != "" else ""
                    }{potentialExec.filename}"
                )
                file.write(content.encode("utf-8"))

        os.rename(f"{outDir}/MAUL_BUILDER", f"{outDir}/{timestamp}")

    shutil.rmtree(workerDir)
#task()

def buildBin(bldr: util.Builder, bin: util.Binary, workerDir: str, buildDir: str) -> None:
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
                path,
                "-o",
                f"{workerDir}/{f"{bin.sourceDirectory}/{src}".replace("/", "__")}.o"
            ])
        #compile()

        if os.path.exists(p:= f"{srcPath}.{cfg.cExtension}"):
            compile(False, p)
        elif os.path.exists(p:= f"{srcPath}.{cfg.cxxExtension}"):
            containsCxx = True
            compile(True, p)
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

    if not os.path.exists(buildDir):
        os.makedirs(buildDir)

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
        f"{buildDir}/{bin.filename}"
    ])
#buildBin()