import time
from typing import Dict, Optional, Tuple

from database import DBManager, MediaStorage
from utils import TextProcessor


class Cache:
    """
    Cache Layer
    """

    def __init__(
        self,
        vector_db: DBManager,
        media_storage: MediaStorage,
        text_processor: TextProcessor,
        ttl_in_seconds: float = 3600,
    ) -> None:
        self.__db: DBManager = vector_db
        self.__media_storage = media_storage

        self.__ttl: float = ttl_in_seconds
        self.__text_processor: TextProcessor = text_processor

    def __generate_key(self, key: str, media_hash: Optional[str] = None) -> str:
        """
        Generates a unique cache key based on the query and media file hash (if available).
        """

        return f"{key}:{media_hash}" if media_hash else key

    def __upload_media(self, **kwargs: Dict) -> Optional[str]:
        """
        Save `media_file`
        """

        if file_path := kwargs.get("file_path"):
            print(f"[Cache]: Saved media file {file_path}")
            return self.__media_storage.insert(file_path)

        return None

    def set(self, key: str, value: str, **kwargs: Dict) -> None:
        """
        Adds a new query-response pair to the cache.
        """

        # Handle media file upload if provided
        saved_path = self.__upload_media(**kwargs)
        # media_hash = self.__media_storage.get_hash(saved_path) if saved_path else None

        timestamp: float = time.time()
        embedding = self.__text_processor.embedding(key)
        # new_key: str = self.__generate_key(key, media_hash)
        # print(f"[VectorDB]: {new_key=}")

        self.__db.insert(
            key=key,
            response=value,
            embedding=embedding,
            metadata={
                "extras": kwargs,
                "timestamp": timestamp,
                "file_path": saved_path,
            },
        )

    def get(self, key: str, **kwargs: Dict) -> Tuple[str, Optional[str]]:
        """
        Retrieves the cached response for a given query.
        """

        embedding = self.__text_processor.embedding(key)

        if cached := self.__db.search(embedding=embedding):
            current_time: float = time.time()
            cached_at: float = cached["metadata"]["timestamp"]

            if kwargs.get("file_path"):
                file_path = kwargs.get("file_path")
            else:
                file_path: Optional[str] = cached["metadata"]["file_path"]

            if current_time - cached_at <= self.__ttl:
                if file_path:
                    media_file = self.__media_storage.search(file_path=file_path)
                else:
                    media_file = None

                return cached["response"], media_file

            self.__db.delete(key)
            if file_path:
                self.__media_storage.delete(file_path)

        return None, None
