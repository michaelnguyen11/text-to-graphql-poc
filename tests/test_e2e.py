import pytest
import os
from src.agents.supervisor import chat
from src.graphql_facade import data_loader
from src.context.ingest import ingest_metadata
from src.context.retriever import LlamaContextRetriever
from src.tools.context_retrieval import set_retriever

@pytest.fixture(scope="module")
def setup_context():
    # Only run if API key is present
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("Skipping E2E test: OPENAI_API_KEY not set")

    data_loader.load_data()
    index = ingest_metadata()
    retriever = LlamaContextRetriever(index)
    set_retriever(retriever)

def test_e2e_customer_overview(setup_context):
    # Vietnamese question for customer overview
    question = "Cho tôi thông tin tổng quan về khách hàng Nguyen van A"
    response = chat(question)
    
    assert response is not None
    assert len(response) > 50
    # Check for keywords usually present in answer
    assert "Nguyen van A" in response or "Cus1" in response
    assert "Gold" in response or "hạng" in response

def test_e2e_casa_lookup(setup_context):
    # Vietnamese question for specific field
    question = "CASA hiện tại của Cus1 là bao nhiêu?"
    response = chat(question)
    
    assert response is not None
    assert "CASA" in response
    assert "Cus1" in response

def test_e2e_nbo_lookup(setup_context):
    # Vietnamese question for NBO
    question = "Khách hàng Pham Quang Minh có những gợi ý sản phẩm nào?"
    response = chat(question)
    
    assert response is not None
    assert "Pham Quang Minh" in response
    assert any(term in response for term in ["NBO", "gợi ý", "đề xuất", "sản phẩm"])
