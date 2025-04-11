from abc import ABC, abstractmethod
from contract import ChatRequest
from models import Message

class BaseChatService(ABC):
    
    @abstractmethod
    async def summarize(self, prompt:str) -> str:
        pass

    @abstractmethod
    async def completion(self, chat_request: ChatRequest, username: str) -> Message:
        pass