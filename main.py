from os import environ
from typing import Any, Dict, Optional

from manager import time_it
from service import Interaction
from utils import ImageProcessor


class ChatInterface:
    """
    Client Interface
    """

    def __init__(self) -> None:
        self.__interaction = Interaction()

    def query(self, prompt: str, **kwargs: Dict) -> str:
        """
        Query LLM
        """

        return self.__interaction.call(prompt, **kwargs)

    def locate(self, text: str, path: str) -> Optional[Dict]:
        """
        Locates UI elements in the image based on the text using `ocr`
        """

        return ImageProcessor(path=path).get_location(text)

    def new_action(self, action: str, identifier: str, image_path: str) -> Any:
        """
        Returns new `action` to perform on the media (image) based on user prompt.
        """

        if action.lower() in {"click", "submit"}:
            return self.__submit_action(image_path, identifier)
        else:
            raise NotImplementedError(f"Action {action} is not implemented")

    def __submit_action(self, path: str, identifier: str) -> Dict:
        """ """

        metadata = self.locate(identifier, path)
        return {
            "action": "click",
            "label": identifier,
            "coords": [metadata["x"], metadata["y"]],
        }


if __name__ == "__main__":
    # Env
    environ["TOKENIZERS_PARALLELISM"] = "FALSE"

    interface = ChatInterface()
    file_path = "assets/source.jpg"

    query_1 = "select all apples"

    with time_it("Query 1"):
        response_1 = interface.query(query_1, file_path=file_path)

    print(f"{response_1=}")

    query_1 = "pick apples"

    with time_it("Query 2"):
        response_2 = interface.query(query_1, file_path=file_path)

    print(f"{response_2=}")
