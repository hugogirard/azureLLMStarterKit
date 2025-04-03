import threading
from semantic_kernel import Kernel
from config import Config
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from openai import AsyncAzureOpenAI
from typing import ClassVar

class AgentFactory:
    
    _instance = None
    _lock = threading.Lock()

    SERVICE_ID:ClassVar[str] = "AZURE-OPENAI-CHAT"

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AgentFactory, cls).__new__(cls)       
                    cls._instance._create_kernel()
                    
        return cls._instance    
    
    def _create_kernel(self):
        
        config = Config()        
        kernel = Kernel()
        
        openai_client = AsyncAzureOpenAI(
            api_key=config.openai_key(),
            api_version="2024-10-21",
            azure_endpoint=config.openai_endpoint()
        )


        kernel.add_service(
            AzureChatCompletion(
                service_id=self.SERVICE_ID,
                deployment_name=config.openai_chat_deployment(),
                endpoint=config.openai_endpoint(),
                api_key=config.openai_key(),
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

        self.kernel = kernel
        self.execution_settings = execution_settings

    @property
    def get_kernel(self) -> Kernel:
        return self.kernel
    
    @property
    def get_execution_settings(self) -> AzureChatPromptExecutionSettings:
        return self.execution_settings
