from typing import Union

from utils.box import BoxUtility
from utils.image import ImageProcessor
from utils.text import TextProcessor

Utility = Union[BoxUtility, TextProcessor, ImageProcessor]
