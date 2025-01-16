import time
from typing import Any, Dict, Optional

from cache import Cache
from database import VectorDB
from models import Ollama
from service import Interaction
from utils import ImageProcessor, TextTransformer


class ChatInterface:
    """ """

    def __init__(self) -> None:
        self.__db = VectorDB(name="cache")
        self.__db.create()
        self.__processor = ImageProcessor

        self.__transformer = TextTransformer()
        self.__cache = Cache(db=self.__db, transformer=self.__transformer)
        self.__interaction = Interaction(cache=self.__cache, llm=Ollama())

    def query(self, prompt: str) -> str:
        """
        Perform plain text based queries
        """

        return self.__interaction.call(prompt)

    def locate(self, text: str, path: str) -> Optional[Dict]:
        """
        Locates UI elements in the image based on the text.
        """

        return self.__processor(path).get_location(text)

    def perform_action(self, action: str, identifier: str, image_path: str) -> Any:
        """
        Perform action on image based on user prompt.
        """

        if action.lower() in {"click", "submit"}:
            return self.__perform_submit(image_path, identifier)
        else:
            raise NotImplementedError(f"Action {action} is not implemented")

    def __perform_submit(self, path: str, identifier: str) -> Dict:
        """ """

        x, y, _, _, _ = self.locate(identifier, path)

        return {"action": "intent", "coords": [x, y], "label": identifier}


if __name__ == "__main__":
    app = ChatInterface()

    s1 = time.time()
    q1 = "What is 2 plus 2"
    r1 = app.query(q1)
    print(f"Response for query `{q1}` is `{r1}` took {time.time() - s1}")

    s2 = time.time()
    q2 = "what is 2 + 2"
    r2 = app.query(q2)
    print(f"Response for query `{q2}` is `{r2}` took {time.time() - s2}")

    response = app.perform_action("click", "Search", "assets/image.png")
    print(response)

    # element = app.locate("Search", "image.png")
    # print(element)
