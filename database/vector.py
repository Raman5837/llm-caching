import hashlib
from typing import Dict, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from torch import Tensor, tensor

from constants import INDEX_DIMENSION

from .abstract import DBManager


class VectorDB(DBManager):
    """
    Vector DB Layer
    """

    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__client = QdrantClient(":memory:")

    def create(self) -> None:
        """
        Creates A New Collection
        """

        if not self.__client.collection_exists(self.__name):
            self.__client.create_collection(
                collection_name=self.__name,
                vectors_config=VectorParams(
                    size=INDEX_DIMENSION, distance=Distance.COSINE
                ),
            )

    def __get_id(self, query: str) -> int:
        """
        Returns Hashed `id`
        """

        return int(hashlib.md5(query.encode()).hexdigest(), 16) % (10**8)

    def insert(
        self, query: str, embedding: Tensor, response: str, metadata: Dict
    ) -> None:
        """
        Insert data into the collections
        """

        point = PointStruct(
            id=self.__get_id(query),
            vector=tensor(embedding).cpu().numpy().tolist(),
            payload={"query": query, "response": response, "metadata": metadata},
        )

        self.__client.upsert(collection_name=self.__name, points=[point])

    def search(self, embedding: Tensor, threshold: float = 0.8) -> Optional[str]:
        """
        Search response for given `query`
        """

        if search_result := self.__client.search(
            collection_name=self.__name,
            query_vector=tensor(embedding).tolist(),
            limit=5,
        ):
            closest = search_result[0]
            results = [(item.id, item.version, item.score) for item in search_result]

            print(f"[VectorDB]: {results=}")
            print(f"[VectorDB]: Closest {(closest.id, closest.version, closest.score)}")

            if closest.score >= threshold:
                return closest.payload

        return None

    def delete(self, query: str) -> None:
        """
        Deletes an entry from the database.
        """

        _id = self.__get_id(query)
        self.__client.delete(collection_name=self.__name, points_selector=[_id])
