import time
from os import environ
from typing import Any, Dict, Optional

from cache import Cache
from database import MediaStorage, VectorDB
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
        self.__media_storage = MediaStorage(storage_dir="./assets")
        self.__cache = Cache(
            vector_db=self.__db,
            transformer=self.__transformer,
            media_storage=self.__media_storage,
        )
        self.__interaction = Interaction(cache=self.__cache, llm=Ollama())

    def query(self, prompt: str, **kwargs: Dict) -> str:
        """
        Perform plain text based queries
        """

        return self.__interaction.call(prompt, **kwargs)

    def locate(self, text: str, path: str) -> Optional[Dict]:
        """
        Locates UI elements in the image based on the text.
        """

        return self.__processor(path).get_location(text)

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

    app = ChatInterface()

    s1 = time.time()
    q1 = "What is 2 plus 2"
    r1 = app.query(q1)
    print(f"Response for query `{q1}` is `{r1}` took {time.time() - s1}")

    s2 = time.time()
    q2 = "what is 2 + 2"
    r2 = app.query(q2)
    print(f"Response for query `{q2}` is `{r2}` took {time.time() - s2}")

    file_path = "assets/image.png"
    action = app.new_action("click", "Search", file_path)

    s3 = time.time()
    q3 = f"Given action {action} and image path {file_path}. Write integration test code for this"
    r3 = app.query(q3, file_path=file_path, action=action)
    print(f"Response for query `{q3}` is `{r3}` took {time.time() - s3}")

    s4 = time.time()
    q4 = f"Given intent {action} and image {file_path}. write integration test for this"
    r4 = app.query(q4, file_path=None, action=action)
    print(f"Response for query `{q4}` is `{r4}` took {time.time() - s4}")
