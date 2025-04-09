from config import Config
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
#from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from typing import ClassVar, List

class SearchService:

    TOP:ClassVar[int] = 5

    def __init__(self):

        config = Config()

        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

        self.search_client = SearchClient(endpoint=config.search_ai_endpoint(),
                                          index_name=config.search_ai_index(),
                                          credential=credential)
        
        self.openai_client = AsyncAzureOpenAI(
            api_version="2024-10-21",
            azure_endpoint=config.openai_endpoint(),
            azure_ad_token_provider=token_provider
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
            search_fields=["recipe_name, description, ingredients, instructions"],
            vector_queries=[vector_query],        
            top=self.TOP,
            select=["country","city","recipe_name", "description", "ingredients", "instructions"]
        )          

        results = []
        async for result in search_result:
            results.append(result)          
        
        context = self._aggregate_chunks(results)
        
        prompt = self._build_prompt(query, context)

        return prompt

    def _build_prompt(self, question: str, context: str) -> str:
        """
        Construct the final prompt for the LLM, including the retrieved context and the user question.
        """
        # Instruction for the assistant on how to use the context
        instruction = (
            "You are an AI assistant with access to the following context from documents.\n"
            "Use the information to answer the question accurately. If the context is insufficient, say you don't know.\n\n"
            "Please provide a concise and informative answer based on the context provided.\n\n"
            "always provide citation for the answer and generate response in Markdown format.\n"
        )
        # Include the context and then ask the question
        prompt = f"{instruction}Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        return prompt     

    ###
    # Combine the text chunks from search results into a single context string.
    # This may involve filtering or truncating as needed to fit in the prompt.
    ###
    def _aggregate_chunks(self, results: list) -> str:

        if not results:
          return ""
        
        context_parts = []

        # Gather relevant text from each result (e.g., the 'chunk' field)
        context_parts = []
        for i, doc in enumerate(results, start=1):
            # Each doc is a dictionary-like result. Extract the content chunk.
            text = f"{doc.get("description", "")}\ningredients: {doc.get("ingredients")}\ninstructions:{doc.get("instructions")}"
            if not text:
                continue            
            # include the title or source info for clarity
            recipe_name = doc.get("recipe_name") #or doc.get("name") or "Document"
            location = f"country: {doc.get("storageUrl")} city: {doc.get("contry")}"
            source_info = f"{recipe_name} + {location}" 
            # Format each chunk (numbered list with source info)
            context_parts.append(f"{i}. [{source_info}]\n{text}")
        # Join all chunks with a separator between them
        combined_context = "\n\n".join(context_parts)
        return combined_context
    

    def dispose(self):
        self.search_client.close()
        
