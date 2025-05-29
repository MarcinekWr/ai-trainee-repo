import json
import os
import sys
from unittest.mock import Mock, patch

import azure.functions as func
import pytest


sys.path.append(os.path.dirname(__file__))

from ask_rag import main as ask_rag_http_handler
from ask_rag_plugin import ask_rag


class TestAskRagFunction:
    """Test cases for the RAG functionality"""

    @patch("ask_rag_plugin.embeddings")
    @patch("ask_rag_plugin.search_client")
    @patch("ask_rag_plugin.llm")
    def test_ask_rag_success(self, mock_llm, mock_search_client, mock_embeddings):
        """Test successful RAG query processing"""
        mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]

        mock_search_client.search.return_value = [
            {"id": "1", "content": "Test content 1"},
            {"id": "2", "content": "Test content 2"},
        ]

        mock_llm.invoke.return_value = Mock(content="Test answer")

        query = "Test question"
        result = ask_rag(query)

        assert result["question"] == query
        assert result["answer"] == "Test answer"
        assert "Test content 1" in result["context"]

    @patch("ask_rag.ask_rag")
    def test_http_trigger_success(self, mock_ask_rag):
        """Test HTTP trigger with successful response"""
        mock_ask_rag.return_value = {
            "question": "Test query",
            "answer": "Test answer",
            "context": "Test context",
        }

        req = func.HttpRequest(
            method="POST",
            body=json.dumps({"query": "Test query"}).encode("utf-8"),
            url="http://localhost:7071/api/ask_rag",
            headers={"content-type": "application/json"},
        )

        response = ask_rag_http_handler(req)

        assert response.status_code == 200
        data = json.loads(response.get_body().decode())
        assert data["status"] == "success"
        assert data["data"]["question"] == "Test query"
        assert data["data"]["answer"] == "Test answer"

    def test_http_trigger_missing_query(self):
        """Test HTTP trigger with missing query parameter"""
        req = func.HttpRequest(
            method="POST",
            body=b"{}",
            url="http://localhost:7071/api/ask_rag",
            headers={"content-type": "application/json"},
        )

        response = ask_rag_http_handler(req)

        assert response.status_code == 400
        assert b"Brak pytania" in response.get_body()
