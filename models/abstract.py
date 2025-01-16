from abc import ABCMeta, abstractmethod
from typing import Any


class BaseLLM(metaclass=ABCMeta):
    """
    Base Class For LLM
    """

    @abstractmethod
    def execute(self, prompt: str) -> Any:
        raise NotImplementedError
