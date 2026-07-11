from typing import Dict, Callable
from . import setup, build#noqa

dict: Dict[str, Callable[[], None]] = {
    "build": lambda: build.task(),
    "setup": lambda: setup.task()
}