from config import Config
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential

class SearchService:

    def __init__(self):

        config = Config()

        credential = AzureKeyCredential(config.search_ai_key())

        self.search_client = SearchClient(endpoint=config.search_ai_endpoint(),
                                          index_name=config.search_ai_index(),
                                          credential=credential)
        