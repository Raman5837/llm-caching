from cache import Cache
from models import BaseLLM


class Interaction:
    """
    Service Layer To Interact With LLM
    """

    def __init__(self, cache: Cache, llm: BaseLLM) -> None:
        self.__llm: BaseLLM = llm
        self.__cache: Cache = cache

    def call(self, query: str) -> str:
        """
        Interact With LLM
        """

        if cached := self.__cache.get(query):
            print(f"[CacheHit]: {query}")
            return cached

        print(f"[CacheMiss]: {query}")
        response = self.__llm.execute(query)
        self.__cache.set(query, response)

        return response
