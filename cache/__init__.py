import time
from typing import Dict, Optional

from database import DBManager
from utils import TextTransformer


class Cache:
    """
    Cache Layer
    """

    def __init__(
        self, db: DBManager, transformer: TextTransformer, ttl: float = 3600
    ) -> None:
        self.__ttl: float = ttl
        self.__db: DBManager = db
        self.__transformer: TextTransformer = transformer

    def set(self, key: str, value: str, extras: Optional[Dict] = None) -> None:
        """
        Adds a new query-response pair to the cache.
        """

        timestamp: float = time.time()
        embedding = self.__transformer.embedding(key)

        self.__db.insert(
            query=key,
            response=value,
            embedding=embedding,
            metadata={"timestamp": timestamp, "extras": extras},
        )

    def get(self, key: str) -> Optional[str]:
        """
        Retrieves the cached response for a given query.
        """

        embedding = self.__transformer.embedding(key)

        if cached := self.__db.search(embedding=embedding):
            current_time: float = time.time()
            cached_at: float = cached["metadata"]["timestamp"]

            if current_time - cached_at <= self.__ttl:
                return cached["response"]

            self.__db.delete(key)

        return None
