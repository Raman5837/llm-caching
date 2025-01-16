from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional


class DBManager(metaclass=ABCMeta):
    """
    Base DB Layer
    """

    @abstractmethod
    def create(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert(self, query: str, **kwargs: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, **kwargs: Dict[str, Any]) -> Optional[str]:
        raise NotImplementedError
