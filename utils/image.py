import hashlib
import time
from os import makedirs, path
from random import randint
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from cv2 import COLOR_BGR2GRAY, COLOR_RGB2BGR, cvtColor, imread, imwrite, rectangle
from PIL import Image
from pytesseract import Output, image_to_data

CoordsT = Tuple[int, int, int, int]


class ImageProcessor:
    """
    Service layer to work with images
    """

    def __init__(self, path: str = None, image: Image.Image = None) -> None:
        if path:
            self.__image = imread(filename=path)

        elif image:
            self.__image = cvtColor(np.array(image), COLOR_RGB2BGR)

        else:
            raise ValueError("path or image is required")

        self.__grayscale = cvtColor(self.__image, COLOR_BGR2GRAY)

    def ocr(self) -> List[Dict[str, Any]]:
        """
        Performs `OCR`
        """

        elements: List[Dict[str, Any]] = []
        data = image_to_data(self.__grayscale, output_type=Output.DICT)

        for index in range(len(data["text"])):
            if data["text"][index].strip():
                element = {
                    "y": data["top"][index],
                    "x": data["left"][index],
                    "text": data["text"][index],
                    "width": data["width"][index],
                    "height": data["height"][index],
                }
                elements.append(element)

        return elements

    def get_location(self, text: str) -> Optional[Dict]:
        """
        Returns `Location Metadata` for given `text`
        """

        elements = self.ocr()

        return next(
            (
                element
                for element in elements
                if text.lower() in element["text"].lower()
            ),
            None,
        )

    def draw_boundary(self, coords: CoordsT, directory: str) -> None:
        """
        Draws a boundary box using given `coords`
        """

        try:
            x_min, y_min, x_max, y_max = map(int, coords)
            rectangle(self.__image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            output_dir = path.join("./assets", directory)
            makedirs(output_dir, exist_ok=True)

            file_name = f"image__{int(time.time())}__{randint(1, 9999)}.png"
            file_path = path.join(output_dir, file_name)

            imwrite(file_path, self.__image)

        except Exception as exception:
            print(f"[ImageProcessor]: {exception}")

    def hashed(self) -> str:
        """
        Returns a unique hash for the image
        """

        return hashlib.sha256(self.__image.tobytes()).hexdigest()
