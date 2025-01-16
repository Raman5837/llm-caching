from typing import List

from ollama import ChatResponse, chat

from .abstract import BaseLLM


class Ollama(BaseLLM):
    """
    Ollama Interface
    """

    def __init__(self, model_name: str = "mistral") -> None:
        self.__messages: List[str] = []
        self.__model_name: str = model_name

    def execute(self, prompt: str) -> str:
        """
        Execute The Prompt
        """

        content = prompt.strip().replace("\n\n", "\n")

        self.__messages.append({"role": "user", "content": content})
        response: ChatResponse = chat(model=self.__model_name, messages=self.__messages)

        response: str = response.message.content.strip()
        self.__messages.append({"role": "assistant", "content": response})
        return response
