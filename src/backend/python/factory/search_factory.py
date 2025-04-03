import threading
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential
from config import Config

class SearchFactory:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SearchFactory, cls).__new__(cls)       
                    cls._instance._create_client()
                    
        return cls._instance    
    
    def _create_client(self):
        
        config = Config()

        credential = AzureKeyCredential(config.search_ai_key())

        self.search_client = SearchClient(endpoint=config.search_ai_endpoint(),
                                          index_name=config.search_ai_index(),
                                          credential=credential)   

    @property
    def get_search_client(self) -> SearchClient:
        return self.search_client