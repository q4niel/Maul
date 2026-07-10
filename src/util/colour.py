from enum import Enum

class Colour(Enum):
    Red = 31
    Cyan = 36
    Magenta = 35
    Maul = Magenta
#class Colour(Enum)

def strColour(clr: Colour, str: str) -> str:
    return f"\033[{clr.value}m{str}\033[0m"
#strColour()