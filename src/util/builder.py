from enum import Enum
from dataclasses import dataclass

class Builder:
    class Platform(Enum):
        Linux = 0,
        Windows = 1

    @dataclass
    class BinData:
        bin: str
        dst: str

    def __init__(self) -> None:
        self.name: str = ""
        self.platform:Builder.Platform = Builder.Platform.Linux
        self.compFlags: list[str] = []
        self.compCFlags: list[str] = []
        self.compCxxFlags: list[str] = []
        self.linkFlags: list[str] = []
        self.linkCFlags: list[str] = []
        self.linkCxxFlags: list[str] = []
        self.mkdirs: list[str] = []
        self.binaries: list[Builder.BinData] = []
    #__init__()
#class Builder