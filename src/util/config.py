import os
import tomllib
from typing import BinaryIO
import util

class Config:
    isValid: bool = False
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
    binaries: list[util.Binary] = []

    @staticmethod
    def init() -> None:
        for lang in [
            "toml"
        ]:
            if Config.isValid:
                print (
                    util.strColour(util.Colour.Red, "| Error: "),
                    end=""
                )
                print("Multiple config files is not allowed")
                break

            if (os.path.exists(p:= f"mnt/maul.{lang}")
            and os.path.isfile(p)
            ):
                with open(p, "rb") as file:
                    match lang:
                        case "toml":
                            Config.evalToml(file)
                        case _:
                            return

                    Config.isValid = True
    #__init__()

    @staticmethod
    def evalToml(file: BinaryIO) -> None:
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

                        Config.binaries.append(bin)
    #evalToml()
#class Config