import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from langchain_openai import OpenAIEmbeddings

class RAGManager:
    """Manages Vector DB interactions for rulebooks and context."""
    
    COLLECTION_NAME = "f1_rules"
    
    def __init__(self):
        self.qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        # Fallback for dev without OpenAI key
        api_key = os.getenv("OPENAI_API_KEY", "mock")
        if api_key == "mock":
            # Using mock embedding dimension of 1536 (OpenAI ada-002 size) for testing
            self.embeddings = None
        else:
            self.embeddings = OpenAIEmbeddings(api_key=api_key)
            
        self.client = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)
        self._ensure_collection()
        
    def _ensure_collection(self):
        if not self.client.collection_exists(self.COLLECTION_NAME):
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            
    def search_rules(self, query: str, limit: int = 3) -> str:
        """Searches Qdrant for relevant rules."""
        if not self.embeddings:
            return "Mock Rule: Safety Car requires maintaining delta time."
            
        query_vector = self.embeddings.embed_query(query)
        search_result = self.client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit
        )
        
        contexts = [hit.payload.get("text", "") for hit in search_result]
        return "\n---\n".join(contexts)
