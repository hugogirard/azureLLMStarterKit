import threading
from config import Config
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential

class SearchService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls,*args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SearchService, cls).__new__(cls)                                
        return cls._instance

    def _create_search_instance(self):

        config = Config()

        credential = AzureKeyCredential(config.search_ai_key())

        self.search_client = SearchClient(endpoint=config.search_ai_endpoint(),
                                          index_name=config.search_ai_index(),
                                          credential=credential)
    
    @property
    def get_search_client(self) -> SearchClient:
        return self.search_client
        