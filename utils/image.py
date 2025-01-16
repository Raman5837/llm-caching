import hashlib
from typing import Any, Dict, List, Optional

from cv2 import COLOR_BGR2GRAY, cvtColor, imread
from pytesseract import Output, image_to_data


class ImageProcessor:
    """
    Service Layer To Work With Images
    """

    def __init__(self, path: str) -> None:
        self.__image = imread(filename=path)
        self.__grayscale = cvtColor(self.__image, COLOR_BGR2GRAY)

    def ocr(self) -> None:
        """ """

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

    def hashed(self) -> str:
        """
        Returns a unique hash for the image
        """

        return hashlib.sha256(self.__image.tobytes()).hexdigest()
