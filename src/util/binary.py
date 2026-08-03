from enum import Enum

class Binary:
    class Type(Enum):
        none = 0,
        executable = 1,
        staticlib = 2,
        dynamiclib = 3
    #class Type(Enum)

    def __init__(self) -> None:
        self.name: str = ""
        self.filename = "mauled_binary"
        self.type: Binary.Type = Binary.Type.none
        self.compFlags: list[str] = []
        self.compCFlags: list[str] = []
        self.compCxxFlags: list[str] = []
        self.linkFlags: list[str] = []
        self.linkCFlags: list[str] = []
        self.linkCxxFlags: list[str] = []
        self.sourceDirectory: str = "src"
        self.sources: list[str] = []
    #__init__()

#class Binary