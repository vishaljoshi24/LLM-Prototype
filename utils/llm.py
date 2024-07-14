from enum import Enum
from langchain.callbacks.manager import CallbackManager
from langchain_community.llms.llamafile import Llamafile
from langchain_community.llms.ollama import Ollama

class LLMClass(Enum):
    """ LLM formats"""

    LLAMAFILE = "llamafile"
    OLLAMA = "ollama"


class LlamafileModel(Enum):
    """
    Llamafile model names.
    """

    LLAMA13B = "llama-2-13b-chat.Q8_0"
    LLAMA7B = "llama-2-7b-chat.Q8_0"


def create_llm(llm: LLMClass, model: str, callback_manager: CallbackManager):
    """Create a language model."""

    if llm == LLMClass.LLAMAFILE:
        return  Llamafile(
            name=f"server/llamafile/{model}.llamafile",
            streaming=True,
            callback_manager=callback_manager,
            verbose=True,
        )
    
    if llm == LLMClass.OLLAMA:
        return Ollama(
            model=model,
            callback_manager=callback_manager,
            verbose=True,
        )
    
    raise ValueError(f"Invalid format: {llm}")