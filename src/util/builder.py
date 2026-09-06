from enum import Enum
from dataclasses import dataclass

class Builder:
    class Platform(Enum):
        Linux = 0,
        Windows = 1

    def __init__(self) -> None:
        self.name: str = ""
        self.platform:Builder.Platform = Builder.Platform.Linux
        self.compFlags: list[str] = []
        self.compCFlags: list[str] = []
        self.compCxxFlags: list[str] = []
        self.linkFlags: list[str] = []
        self.linkCFlags: list[str] = []
        self.linkCxxFlags: list[str] = []
        self.binaries: list[str] = []
    #__init__()
#class Builder