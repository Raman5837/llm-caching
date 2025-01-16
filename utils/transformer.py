from sentence_transformers import SentenceTransformer
from torch import Tensor


class TextTransformer:
    """
    Text To Embedding Transformer
    """

    def __init__(self) -> None:
        self.__model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2")

    def embedding(self, text: str) -> Tensor:
        """
        Returns Embeddings
        """

        return self.__model.encode(text)
