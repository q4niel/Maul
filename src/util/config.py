import os
import tomllib
from typing import BinaryIO
import util
from enum import Enum
from typing import Any

class Config:
    isValid: bool = True
    hExtension: str = "h"
    cExtension: str = "c"
    hxxExtension: str = "hpp"
    cxxExtension: str = "cpp"
    globalCompFlags: list[str] = []
    globalCompCFlags: list[str] = []
    globalCompCxxFlags: list[str] = []
    globalLinkFlags: list[str] = []
    globalLinkCFlags: list[str] = []
    globalLinkCxxFlags: list[str] = []
    builders: dict[str, util.Builder] = {}
    binaries: dict[str, util.Binary] = {}

    @staticmethod
    def init() -> None:
        for lang in [
            "toml"
        ]:
            if (os.path.exists(p:= f"mnt/maul.{lang}")
            and os.path.isfile(p)
            ):
                with open(p, "rb") as file:
                    match lang:
                        case "toml":
                            Config.evalToml(file)
                        case _:
                            return
            else:
                Config.isValid = False
    #init()

    @staticmethod
    def evalToml(file: BinaryIO) -> None:
        blds: Any = None

        for key, value in tomllib.load(file).items():
            match key:
                case "h_extension":
                    Config.hExtension = value

                case "c_extension":
                    Config.cExtension = value

                case "hxx_extension":
                    Config.hxxExtension = value

                case "cxx_extension":
                    Config.cxxExtension = value

                case "global_comp_flags":
                    Config.globalCompFlags = value
                case "global_comp_c_flags":
                    Config.globalCompCFlags = value
                case "global_comp_cxx_flags":
                    Config.globalCompCxxFlags = value

                case "global_link_flags":
                    Config.globalLinkFlags = value
                case "global_link_c_flags":
                    Config.globalLinkCFlags = value
                case "global_link_cxx_flags":
                    Config.globalLinkCxxFlags = value

                case "builder":
                    blds = value

                case "binary":
                    for name, info in value.items():
                        bin: util.Binary = util.Binary()
                        bin.name = name

                        for k, v in info.items():
                            match k:
                                case "filename":
                                    bin.filename = v

                                case "type":
                                    match v:
                                        case "executable":
                                            bin.type = util.Binary.Type.executable
                                        case "static_lib":
                                            bin.type = util.Binary.Type.staticlib
                                        case "dynamic_lib":
                                            bin.type = util.Binary.Type.dynamiclib

                                case "comp_flags":
                                    bin.compFlags = v
                                case "comp_c_flags":
                                    bin.compCFlags = v
                                case "comp_cxx_flags":
                                    bin.compCxxFlags = v

                                case "link_flags":
                                    bin.linkFlags = v
                                case "link_c_flags":
                                    bin.linkCFlags = v
                                case "link_cxx_flags":
                                    bin.linkCxxFlags = v

                                case "source_directory":
                                    bin.sourceDirectory = v

                                case "sources":
                                    bin.sources = v

                        if bin.name in Config.binaries:
                            Config.isValid = False
                            (util.Printer()
                                .red("| Error: ")
                                .default("Binary ")
                                .cyan(bin.name)
                                .default(" has multiple definitions in config")
                            .exec())
                            break
                        else:
                            Config.binaries[bin.name] = bin

        if blds is None: return

        for name, info in blds.items():
            bld: util.Builder = util.Builder()
            bld.name = name

            for k, v in info.items():
                match k:
                    case "comp_flags":
                        bld.compFlags = v
                    case "comp_c_flags":
                        bld.compCFlags = v
                    case "comp_cxx_flags":
                        bld.compCxxFlags = v

                    case "link_flags":
                        bld.linkFlags = v
                    case "link_c_flags":
                        bld.linkCFlags = v
                    case "link_cxx_flags":
                        bld.linkCxxFlags = v

                    case "mkdirs":
                        bld.mkdirs = v

                    case "binaries":
                        for b in v:
                            if b["bin"] not in Config.binaries:
                                (util.Printer()
                                    .red("| Error: ")
                                    .default("Use of undefined binary ")
                                    .cyan(b["bin"])
                                    .default(" in builder ")
                                    .cyan(bld.name)
                                .exec())
                                Config.isValid = False
                                break
                            else:
                                bld.binaries.append (
                                    util.Builder.BinData (
                                        b["bin"],
                                        b.get("dst", "")
                                    )
                                )
            if bld.name in Config.builders:
                (util.Printer()
                    .red("| Error: ")
                    .default("Builder ")
                    .cyan(bld.name)
                    .default(" has multiple definitions in config")
                .exec())
                Config.isValid = False
                break
            else:
                Config.builders[bld.name] = bld
    #evalToml()
#class Config

class LocalConfig:
    class TaskType(Enum):
        none = 0
        linuxShell = 1
        windowsBatch = 2
    #class TaskType

    isValid: bool = True
    containerEngine: str = "none"
    taskType: TaskType = TaskType.none

    @staticmethod
    def init() -> None:
        for lang in [
            "toml"
        ]:
            if (os.path.exists(p:= f"mnt/maul.local.{lang}")
                and os.path.isfile(p)
                ):
                    with open(p, "rb") as file:
                        match lang:
                            case "toml":
                                LocalConfig.evalToml(file)
                            case _:
                                return
            else:
                LocalConfig.isValid = False

        if LocalConfig.containerEngine == "none":
            LocalConfig.isValid = False
    #init()

    @staticmethod
    def evalToml(file: BinaryIO) -> None:
        for key, value in tomllib.load(file).items():
            match key:
                case "container_engine":
                    match value:
                        case "podman":
                            LocalConfig.containerEngine = "podman"
                        case "docker":
                            LocalConfig.containerEngine = "docker"
                        case _:
                            (util.Printer()
                                .red("| Error: ")
                                .default("Invalid container engine in local config")
                            .exec())
                            LocalConfig.isValid = False
                            break

                case "task_type":
                    match value:
                        case "linux_shell":
                            LocalConfig.taskType = LocalConfig.TaskType.linuxShell
                        case "windows_batch":
                            LocalConfig.taskType = LocalConfig.TaskType.windowsBatch
                        case _:
                            (util.Printer()
                                .red("| Error: ")
                                .default("Invalid task type in local config")
                            .exec())
                            LocalConfig.isValid = False
                            break
    #evalToml()
#class LocalConfig