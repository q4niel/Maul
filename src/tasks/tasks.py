from typing import Dict, Callable
from .test import test

dict: Dict[str, Callable[[], None]] = {
    "test": lambda: test()
}