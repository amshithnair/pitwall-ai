from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

class LLMProvider(ABC):
    """Abstract interface for LLM Providers."""
    
    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        """Returns a configured LangChain ChatModel instance."""
        pass
