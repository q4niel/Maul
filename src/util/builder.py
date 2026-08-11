class Builder:
    def __init__(self) -> None:
        self.name: str = ""
        self.compFlags: list[str] = []
        self.compCFlags: list[str] = []
        self.compCxxFlags: list[str] = []
        self.linkFlags: list[str] = []
        self.linkCFlags: list[str] = []
        self.linkCxxFlags: list[str] = []
        self.binaries: list[str] = []
    #__init__()
#class Builder