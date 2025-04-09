from repository.session_repository import SessionRepository
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
import uuid
from models import Message
from contract import ChatRequest
from config import Config
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel import Kernel
from services.search_service import SearchService
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

class ChatService:

    SYSTEM_PROMPT = (
        "You are an AI assistant with access to the following context from documents.\n"
        "Use the information to answer the question accurately. If the context is insufficient, say you don't know.\n\n"
        "Please provide a concise and informative answer based on the context provided.\n\n"
        "always provide citation for the answer and generate response in Markdown format.\n"
    )

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

        context = await self.search_service.search(chat_request.question)

        system_prompt = self._build_system_prompt(context)

        messages = await self.session_repository.get_session_messages(session_id=chat_request.session_id,username=username)

        history = ChatHistory()

        history.add_system_message(system_prompt)

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

    def _build_system_prompt(self, context: str) -> str:
        return f"{self.SYSTEM_PROMPT} Context: {context}"        
