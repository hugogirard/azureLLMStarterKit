from config import Config
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from openai import AsyncAzureOpenAI
from typing import ClassVar, List

class SearchService:

    TOP:ClassVar[int] = 5

    def __init__(self):

        config = Config()

        credential = AzureKeyCredential(config.search_ai_key())

        self.search_client = SearchClient(endpoint=config.search_ai_endpoint(),
                                          index_name=config.search_ai_index(),
                                          credential=credential)
        
        self.openai_client = AsyncAzureOpenAI(
            api_key=config.openai_key(),
            api_version="2024-10-21",
            azure_endpoint=config.openai_endpoint()
        )   

        self.config = config     


    async def search(self,query:str) -> str:
        query_vector_response = await self.openai_client.embeddings.create(input=query,
                                                                           model=self.config.openai_embedding_deployment())    

        vector_query = VectorizedQuery(
            vector=query_vector_response.data[0].embedding,
            k_nearest_neighbors=self.TOP,
            fields=self.config.query_vector_field_name(),
        )            

        search_result = await self.search_client.search(
            search_text=query,
            search_fields=["title, chunk"],
            vector_queries=[vector_query],
            top=self.TOP,
            select=["title", "storageUrl", "chunk"]
        )          

        results = []
        async for result in search_result:
            results.append(result)          
        
        context = self.aggregate_chunks(results)
        
        prompt = self.build_prompt(query, context)

        return prompt

    ###
    # Combine the text chunks from search results into a single context string.
    # This may involve filtering or truncating as needed to fit in the prompt.
    ###
    def aggregate_chunks(self, results: list) -> str:

        if not results:
          return ""
        
        context_parts = []

        # Gather relevant text from each result (e.g., the 'chunk' field)
        context_parts = []
        for i, doc in enumerate(results, start=1):
            # Each doc is a dictionary-like result. Extract the content chunk.
            text = doc.get("chunk", "")
            if not text:
                continue
            # include the title or source info for clarity
            title = doc.get("title") #or doc.get("name") or "Document"
            location = doc.get("storageUrl") or ""
            source_info = f"{title} + {location}" 
            # Format each chunk (numbered list with source info)
            context_parts.append(f"{i}. [{source_info}]\n{text}")
        # Join all chunks with a separator between them
        combined_context = "\n\n".join(context_parts)
        return combined_context
    

    def dispose(self):
        self.search_client.close()
        
