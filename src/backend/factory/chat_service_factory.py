from infrastructure.enum import ChatServiceType
from config import Config
from services import BaseChatService, SearchService, KernelChatService
from repository.session_repository import SessionRepository
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider

class ChatFactoryService:
    
    def __init__(self,
                 config:Config,
                 search_service: SearchService, 
                 session_repository:SessionRepository):
        
        self.search_service = search_service
        self.session_repository = session_repository
        self.config = config

    def create_chat_service(self,chat_service_type:ChatServiceType) -> BaseChatService:
        
        if chat_service_type == ChatServiceType.SEMANTIC_KERNEL:
            return self._create_kernel();

    def _create_kernel(self) -> BaseChatService:

        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

        kernel = Kernel()
        
        kernel.add_service(
            AzureChatCompletion(
                service_id="AZURE-OPENAI-CHAT",
                deployment_name=self.config.openai_chat_deployment(),
                endpoint=self.config.openai_endpoint(),
                ad_token_provider=token_provider,
                api_version="2024-02-01"
            )
        )
        
        execution_settings = AzureChatPromptExecutionSettings(
            service_id="azure-openai-chat",
            ai_model_id="gpt-4o",
            temperature=0.0,
            max_tokens=2048,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )   

        return KernelChatService(self.session_repository, 
                                 self.search_service,
                                 kernel,
                                 execution_settings)                             