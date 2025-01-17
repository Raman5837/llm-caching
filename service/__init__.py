from typing import Dict, Optional, Tuple

from cache import Cache
from models import BaseLLM


class Interaction:
    """
    Service Layer To Interact With LLM
    """

    def __init__(self, cache: Cache, llm: BaseLLM) -> None:
        self.__llm: BaseLLM = llm
        self.__cache: Cache = cache

    def call(self, query: str, **kwargs: Dict) -> Tuple[str, Optional[str]]:
        """
        Interact With LLM
        """

        cached, media_files = self.__cache.get(query, **kwargs)
        if cached:
            print(f"[CacheHit]: {query}")
            return cached, media_files

        print(f"[CacheMiss]: {query}")
        response = self.__llm.execute(query)
        self.__cache.set(query, response, **kwargs)

        return response, None
