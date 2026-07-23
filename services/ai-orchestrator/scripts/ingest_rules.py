import os
import uuid
import sys
# Allow importing from sibling src dir
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from pitwall.ai_orchestrator.rag import RAGManager
from qdrant_client.models import PointStruct

def ingest_sample_rules():
    manager = RAGManager()
    
    if not manager.embeddings:
        print("Skipping real ingestion because OPENAI_API_KEY is not set or is mock.")
        return
        
    rules = [
        "Safety Car Rule 55.4: During a Safety Car period, no car may be driven unnecessarily slowly, erratically or in a manner which could be deemed potentially dangerous.",
        "Pit Lane Rule 34.8: The speed limit in the pit lane is 80km/h during all sessions, except where modified by the Race Director.",
        "Tyre Rule 30.5: Each driver must use at least two different specifications of dry-weather tyres during the race, unless wet or intermediate tyres have been used."
    ]
    
    vectors = manager.embeddings.embed_documents(rules)
    
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vectors[i], payload={"text": rules[i]})
        for i in range(len(rules))
    ]
    
    manager.client.upsert(
        collection_name=manager.COLLECTION_NAME,
        points=points
    )
    print(f"Successfully ingested {len(rules)} rules into Qdrant.")

if __name__ == "__main__":
    ingest_sample_rules()
