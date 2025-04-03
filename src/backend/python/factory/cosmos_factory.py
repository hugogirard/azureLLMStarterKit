from config import Config
import threading
from azure.cosmos.aio import CosmosClient, ContainerProxy

class CosmosFactory:
        
    def _create_client(self):
        
        config = Config()
        
        cosmos_client = CosmosClient(url=config.cosmosdb_endpoint(), 
                                     credential=config.cosmosdb_key())
        
        db = cosmos_client.get_database_client(config.cosmos_database())

        self._container = db.get_container_client(config.cosmos_chat_history_container())        

    @property
    def get_container_client(self) -> ContainerProxy:
        return self._container