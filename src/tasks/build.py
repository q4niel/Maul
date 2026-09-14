import os
import sys
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

    os.mkdir(buildDir:= f"{outDir}/MAUL_BUILDER")

    if builder not in cfg.builders:
        (util.Printer()
            .red("| Error: ")
            .default("Builder ")
            .cyan(builder)
            .default(" has no definition in config")
        .exec())
    else:
        potentialExec: Any = None

        for binary in cfg.builders[builder].binaries:
            buildBin (
                cfg.builders[builder],
                bin:= cfg.binaries[binary],
                workerDir,
                buildDir
            )

            if bin.type == util.Binary.Type.executable:
                potentialExec = bin

        timestamp: str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        if potentialExec != None:
            with open(f"{outDir}/LATEST_BUILD", "wb") as file:
                content: str = (
                    f"{timestamp}/bin/{potentialExec.filename}"
                )
                file.write(content.encode("utf-8"))

        os.rename(buildDir, f"{outDir}/{timestamp}")

    shutil.rmtree(workerDir)
#task()

def getCompiler(bldr: util.Builder, cxx: bool) -> str:
    r: str = ""
    match bldr.platform:
        case util.Builder.Platform.Linux:
            r = "clang"
        case util.Builder.Platform.Windows:
            r = "/opt/llvm-mingw/bin/x86_64-w64-mingw32-clang"

    return r + "++" if cxx else r

def buildBin(bldr: util.Builder, bin: util.Binary, workerDir: str, buildDir: str) -> None:
    linkAsCxx: bool = False
    os.mkdir(binDir:= f"{buildDir}/bin")

    for src in bin.sources:
        explicitPath: bool = False

        if src.startswith(":"):
            src = src.removeprefix(":")
            explicitPath = True

        srcPath: str = f"mnt/{bin.sourceDirectory}/{src}"

        def compile(cxx: bool, path: str):
            (util.Printer()
                .magenta("| Compiling ")
                .cyan(path)
                .default(" [...]")
            .exec(False))

            procArgs: list[str] = [
                getCompiler(bldr, cxx),
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
            ]

            callback: subprocess.CompletedProcess[str] = subprocess.run (
                procArgs,
                capture_output=True,
                text=True
            )

            sys.stdout.write("\033[4D")
            sys.stdout.flush()

            if callback.returncode != 0:
                (util.Printer()
                    .red(" FAIL")
                    .default(" ]")
                    .newline()
                    .default(callback.stderr)
                    .newline()
                .exec())
            else:
                (util.Printer()
                    .green(" OK")
                    .default(" ]")
                    .newline()
                .exec())
        #compile()

        if explicitPath:
            if os.path.exists(srcPath):
                compile(linkAsCxx:=srcPath.endswith(cfg.cxxExtension), srcPath)
            else:
                (util.Printer()
                    .red("| Error: ")
                    .default("Unresolved Source Path")
                    .newline()

                    .red("| ")
                    .default("Source ")
                    .cyan(srcPath)
                    .default(" does not exist!")
                .exec())
        elif os.path.exists(p:= f"{srcPath}.{cfg.cExtension}"):
            compile(False, p)
        elif os.path.exists(p:= f"{srcPath}.{cfg.cxxExtension}"):
            linkAsCxx = True
            compile(True, p)
        else:
            (util.Printer()
                .red("| Error: ")
                .default("Unresolved Source Path")
                .newline()

                .red("| ")
                .default("Could not find infered ")
                .cyan(f"{srcPath}.{cfg.cExtension} ")
                .default("or ")
                .cyan(f"{srcPath}.{cfg.cxxExtension}")
                .newline()

                .red("| ")
                .default("Use ")
                .cyan(": (:my_source.c) ")
                .default("for exlicit file usage")
            .exec())

    (util.Printer()
        .magenta("| Linking ")
        .cyan(bin.name)
        .default(" [...]")
    .exec(False))

    procArgs: list[str] = [
        getCompiler(bldr, linkAsCxx),
        *(
            cfg.globalLinkFlags +
            bin.linkFlags +
            bldr.linkFlags +
            (
                cfg.globalLinkCxxFlags +
                bin.linkCxxFlags +
                bldr.linkCxxFlags
                if linkAsCxx else
                cfg.globalLinkCFlags +
                bin.linkCFlags +
                bldr.linkCFlags
            )
        ),
        *(f"{workerDir}/{o}" for o in os.listdir(workerDir)),
        "-o",
        f"{binDir}/{bin.filename}"
    ]

    callback: subprocess.CompletedProcess[str] = subprocess.run (
        procArgs,
        capture_output=True,
        text=True
    )

    sys.stdout.write("\033[4D")
    sys.stdout.flush()

    if callback.returncode != 0:
        (util.Printer()
            .red(" FAIL")
            .default(" ]")
            .newline()
            .default(callback.stderr)
            .newline()
        .exec())
    else:
        (util.Printer()
            .green(" OK")
            .default(" ]")
            .newline()
        .exec())
#buildBin()