import threading
from typing import List
from repository.session_repository import SessionRepository
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
import uuid
from models import Message
from contract import ChatRequest
from config import Config
from semantic_kernel.contents.chat_history import ChatHistory
from factory import AgentFactory
from semantic_kernel import Kernel
from services import SearchService
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings

class ChatService:

    def __init__(self, 
                 session_repository: SessionRepository, 
                 search_service: SearchService,
                 kernel: Kernel,
                 execution_settings: AzureChatPromptExecutionSettings):
        self.config = Config()
        self.session_repository = session_repository
        self.kernel = kernel
        self.execution_settings = execution_settings
        self.search_service = search_service
    
    async def completion(self, chat_request: ChatRequest, username: str) -> Message:

        messages = await self.session_repository.get_session_messages(session_id=chat_request.session_id,username=username)

        history = ChatHistory()

        for message in messages:
            history.add_user_message(message.prompt)
            history.add_assistant_message(message.completion)

        history.add_user_message(chat_request.question)

        chat_client = self.kernel.get_service(type=ChatCompletionClientBase)

        results = await chat_client.get_chat_message_contents(
            chat_history=history,
            settings=self.execution_settings,
            kernel=self.kernel,
            arguments=KernelArguments()
        )
        
        new_message = Message(id=str(uuid.uuid4()),
                              sessionId=chat_request.session_id,
                              username=username,
                              prompt=chat_request.question,
                              completion=str(results[0]))
        
        await self.session_repository.insert_message_session(new_message)

        return new_message            

