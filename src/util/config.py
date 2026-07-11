import os
import tomllib
from typing import BinaryIO
import util

class Config:
    isValid: bool = False
    hxxExtension: str = "hpp"
    cxxExtension: str = "cpp"
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
                case "hxx_extension":
                    Config.hxxExtension = value

                case "cxx_extension":
                    Config.cxxExtension = value

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

                                case "source_directory":
                                    bin.sourceDirectory = v

                                case "sources":
                                    bin.sources = v

                        Config.binaries.append(bin)
    #evalToml()
#class Config