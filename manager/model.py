from typing import Dict

from env import MOON_DREAM_API_KEY
from models import Clip, Models, MoonDream, Ollama


class ModelManager:
    """
    Centralized manager for handling models. Dynamically loads and initializes models.
    """

    def __init__(self) -> None:
        self.__models: Dict[str, Models] = {
            "clip": Clip(),
            "ollama": Ollama(),
            "moon_dream": MoonDream(key=MOON_DREAM_API_KEY),
        }

    def model(self, name: str) -> Models:
        """
        Get the requested model by name.
        """

        if name not in self.__models:
            raise KeyError(f"Model '{name}' does not exist.")

        return self.__models[name]
