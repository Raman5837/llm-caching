import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
from torch import Tensor


class TextProcessor:
    """
    Contains utility methods related to Text Embedding and Keywords Extraction
    """

    def __init__(self) -> None:
        self.__model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2")

        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("averaged_perceptron_tagger", quiet=True)

        self.__stop_words = set(stopwords.words("english"))

    def embedding(self, text: str) -> Tensor:
        """
        Returns Embeddings
        """

        return self.__model.encode(text)

    def extract(self, prompt: str) -> str:
        """
        Extracts the most contextually relevant keyword(s) or phrase(s) from the prompt.
        """

        words = word_tokenize(prompt.lower())
        filtered_words = [
            word for word in words if word.isalnum() and word not in self.__stop_words
        ]

        # Part-of-speech tagging to identify nouns and adjectives
        pos_tags = nltk.pos_tag(filtered_words)

        # Combining adjectives and nouns to form meaningful phrases
        phrases = []
        current_phrase = []

        for word, pos in pos_tags:
            if pos in {"JJ", "JJR", "JJS"}:  # Adjective
                current_phrase.append(word)

            elif pos in {"NN", "NNS", "NNP", "NNPS"}:  # Noun
                current_phrase.append(word)
                phrases.append(" ".join(current_phrase))
                current_phrase = []  # Reset after a noun

            else:
                current_phrase = []  # Reset if not adjective/noun

        if not phrases:
            return prompt  # Fallback to original prompt if no phrases are found

        # Computing embeddings for the full prompt and extracted phrases
        prompt_embedding = self.__model.encode(prompt, convert_to_tensor=True)
        phrase_embeddings = self.__model.encode(phrases, convert_to_tensor=True)

        # Computing cosine similarity between the prompt and each phrase
        similarities = util.cos_sim(prompt_embedding, phrase_embeddings)[0]

        # Ranking nouns by similarity score
        ranked_phrases = sorted(
            zip(phrases, similarities), key=lambda x: x[1], reverse=True
        )

        return ranked_phrases[0][0] if ranked_phrases else prompt
