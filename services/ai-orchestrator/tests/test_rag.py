import pytest
import os
from pitwall.ai_orchestrator.rag import RAGManager

def test_rag_mock_fallback(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "mock")
    manager = RAGManager()
    
    assert manager.embeddings is None
    
    # Should fallback gracefully
    res = manager.search_rules("What is the safety car rule?")
    assert "Mock Rule" in res
