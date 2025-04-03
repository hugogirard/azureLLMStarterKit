from fastapi import FastAPI
from repository.session_repository import SessionRepository
from azure.cosmos.aio import CosmosClient
from services.chat_service import ChatService
from services.search_service import SearchService
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from config import Config
from routes import routes

config = Config()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routes:
    app.include_router(route,prefix="/api")

@app.on_event("startup")
async def startup_event():
        
    cosmos_client = CosmosClient(url=config.cosmosdb_endpoint(), 
                                 credential=config.cosmosdb_key())
    
    db = cosmos_client.get_database_client(config.cosmos_database())

    container = db.get_container_client(config.cosmos_chat_history_container())    

    app.state.session_repository = SessionRepository(container)
    app.state.cosmos_client = cosmos_client
    
    kernel = Kernel()

    kernel.add_service(
        AzureChatCompletion(
            service_id="AZURE-OPENAI-CHAT",
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
    
    search_service = SearchService()
    app.state.chat_service = ChatService(app.state.session_repository, 
                                         search_service,
                                         kernel,
                                         execution_settings)
    
@app.on_event("shutdown")
async def shutdown_event():
    # Perform any cleanup if necessary (e.g., closing connections)
    pass    

@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")