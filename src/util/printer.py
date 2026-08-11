from typing import Self

class Printer:
    def __init__(self) -> None:
        self.string: str = ""
    #__init__()

    def exec(self) -> None:
        if self.string == "": return
        print(self.string)
    #exec()

    def default(self, string: str) -> Self:
        self.string += string
        return self

    def space(self) -> Self:
        self.string += " "
        return self

    def newline(self) -> Self:
        self.string += "\n"
        return self

    def retrieveCoded(self, code: str, string: str) -> str:
        return f"\033[{code}m{string}\033[0m"

    def code(self, code: str, string: str) -> Self:
        self.string += self.retrieveCoded(code, string)
        return self

    def red(self, string: str) -> Self:
        self.string += self.retrieveCoded("31", string)
        return self

    def cyan(self, string: str) -> Self:
        self.string += self.retrieveCoded("36", string)
        return self

    def magenta(self, string: str) -> Self:
        self.string += self.retrieveCoded("35", string)
        return self

#class Printer