from typing import Union

from manager.context import time_it
from manager.model import ModelManager

Manager = Union[time_it, ModelManager]
