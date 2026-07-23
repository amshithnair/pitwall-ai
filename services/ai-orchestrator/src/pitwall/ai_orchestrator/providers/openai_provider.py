import os
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from pitwall.ai_orchestrator.providers.base import LLMProvider

class OpenAIProvider(LLMProvider):
    """OpenAI implementation of the LLMProvider interface."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.0):
        self.api_key = os.getenv("OPENAI_API_KEY", "mock")
        self.model_name = model_name
        self.temperature = temperature
        
    def get_chat_model(self) -> BaseChatModel:
        return ChatOpenAI(
            temperature=self.temperature,
            model=self.model_name,
            api_key=self.api_key
        )
