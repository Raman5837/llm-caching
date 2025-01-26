from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class BaseLLM(metaclass=ABCMeta):
    """
    Base Class For LLM
    """

    @abstractmethod
    def execute(self, prompt: str, **kwargs: Dict[str, Any]) -> Any:
        raise NotImplementedError
