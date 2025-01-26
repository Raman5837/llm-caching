from typing import Union

from models.abstract import BaseLLM
from models.clip import Clip
from models.moon_dream import MoonDream
from models.ollama import Ollama

Models = Union[Ollama, Clip, MoonDream, BaseLLM]
