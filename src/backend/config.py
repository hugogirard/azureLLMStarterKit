from dotenv import load_dotenv
from typing import List
import os

###########################################################
# This is the center class for all environment variable
# needed for the application.  It's easier than having the
# os package everywhere in the program
###########################################################
class Config:
    def __init__(self):
        load_dotenv(override=True)    
    
    def cosmosdb_endpoint(self) -> str:
        return os.getenv('COSMOS_ENDPOINT')
    
    def cosmos_database(self) -> str:
        return os.getenv('COSMOS_DATABASE')
    
    def cosmos_chat_history_container(self) -> str:
        return os.getenv('COSMOS_CHAT_CONTAINER')
    
    def is_development(self) -> bool:
        value = os.getenv('IS_DEVELOPMENT', 'false').lower()
        return value in ['true', '1', 'yes']
    
    def user_principal_name_dev(self) -> str:
        return os.getenv('USER_PRINCIPAL_NAME','')
    
    def search_ai_endpoint(self) -> str:
        return os.getenv('AZURE_AI_SEARCH_ENDPOINT')
    
    def search_ai_index(self) -> str:
        return os.getenv('AZURE_AI_SEARCH_INDEX')
    
    def openai_endpoint(self) -> str:
        return os.getenv('AZURE_OPENAI_ENDPOINT')
    
    def openai_chat_deployment(self) -> str:
        return os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    
    def openai_embedding_deployment(self) -> str:
        return os.getenv('AZURE_OPENAI_EMB_DEPLOYMENT_NAME')
    
    def query_vector_field_name(self) -> str:
        return os.getenv('QUERY_VECTOR_FIELD')