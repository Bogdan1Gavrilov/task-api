from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

mock_chain = MagicMock()
mock_chain.invoke.return_value = "Mock"
mock_retriever = MagicMock()
mock_retriever.invoke.return_value = []

with patch("app.main.build_rag_chain", return_value=(mock_chain, mock_retriever)):
    from app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}