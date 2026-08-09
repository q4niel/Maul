from typing import Dict, Callable
from . import task_gen, build#noqa

dict: Dict[str, Callable[[], None]] = {
    "build": lambda: build.task(),
    "task-gen": lambda: task_gen.task()
}