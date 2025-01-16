from typing import Union

from models.abstract import BaseLLM
from models.ollama import Ollama

LLM = Union[BaseLLM, Ollama]
