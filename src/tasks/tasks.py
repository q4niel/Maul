from typing import Dict, Callable
from . import setup#noqa

dict: Dict[str, Callable[[], None]] = {
    "setup": lambda: setup.task()
}