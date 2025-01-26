from typing import Any, Dict, Optional, Tuple

from cache import Cache
from database import MediaStorage, VectorDB
from manager import ModelManager
from utils import BoxUtility, ImageProcessor, TextProcessor


class Interaction:
    """
    Service layer to interact with LLMs
    """

    def __init__(self) -> None:
        self.__manager = ModelManager()
        self.__db = VectorDB(name="cache")

        self.__box_utils = BoxUtility()
        self.__image_processor = ImageProcessor
        self.__text_processor = TextProcessor()
        self.__media_storage = MediaStorage(storage_dir="./assets")

        self.__cache = Cache(
            vector_db=self.__db,
            media_storage=self.__media_storage,
            text_processor=self.__text_processor,
        )

    def call(self, query: str, **kwargs: Dict) -> Tuple[str, Optional[str]]:
        """
        Interact with LLM
        """

        cached, media_files = self.__cache.get(query, **kwargs)
        if cached:
            print(f"[CacheHit]: {query}")
            return cached, media_files

        print(f"[CacheMiss]: {query}")

        if file_path := kwargs.get("file_path"):
            response = self.__handle_request(query, file_path)
        else:
            model = self.__manager.model("clip")
            response = model.execute(query)

        self.__cache.set(query, response, **kwargs)

        return response, None

    def __handle_request(self, prompt: str, file_path: str) -> Any:
        """
        Calls LLM, Get the response and generates images to cross check the coordinates
        """

        model = self.__manager.model("moon_dream")
        identifier = self.__text_processor.extract(prompt)

        print(f"[Interaction]: {prompt=} and {identifier=}")

        response = model.detect(file_path, identifier)

        # for box in response:
        #     coords = self.__box_utils.absolute_pixels(file_path, box)
        #     self.__image_processor(file_path).draw_boundary(coords, directory="intermediate")

        merged_coords = self.__box_utils.merge_boxes(file_path, response)

        for coords in merged_coords:
            self.__image_processor(file_path).draw_boundary(
                coords, directory="generated"
            )

        return merged_coords
