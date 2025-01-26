from typing import Any, Dict, List, Optional

import moondream as md
from moondream.types import EncodedImage
from PIL import Image, ImageFile

from models import BaseLLM


class MoonDream(BaseLLM):
    """
    MoonDream Interface
    """

    def __init__(self, path: Optional[str] = None, key: Optional[str] = None) -> None:
        if path:
            self.__model = md.vl(model=path)

        elif key:
            self.__model = md.vl(api_key=key)

        else:
            raise ValueError("One of the `path` or `key` is required")

    def __encoded_image(self, path: str) -> EncodedImage:
        """
        Returns `EncodedImage`
        """

        image: ImageFile = Image.open(path)
        return self.__model.encode_image(image)

    def detect(self, file_path: str, identifier: str) -> List[Dict[str, float]]:
        """
        Returns box coords corresponding to given `identifier`
        """

        encoded = self.__encoded_image(file_path)
        response = self.__model.detect(encoded, identifier)

        return response["objects"]

    def execute(self, prompt: str, **kwargs: Dict[str, Any]) -> str:
        """
        Query on the `image` file
        """

        path = kwargs.get("file_path")

        if not path:
            raise ValueError("Please provide `file_path` of the image")

        image = self.__encoded_image(path)
        response = self.__model.query(image=image, question=prompt)

        return response["answer"]
