"""Context retrieval tool for LangGraph agents."""

import json
import logging

from langchain_core.tools import tool

from src.context.retriever import LlamaContextRetriever

logger = logging.getLogger(__name__)

# Module-level retriever (initialized in server.py startup)
_retriever: LlamaContextRetriever | None = None


def set_retriever(retriever: LlamaContextRetriever) -> None:
    """Set the retriever instance."""
    global _retriever
    _retriever = retriever


@tool
def retrieve_context(question: str, intent: str = "customer_overview") -> str:
    """Retrieve relevant metadata and field information for answering a customer question.

    Use this tool to get schema field descriptions, Vietnamese/English aliases,
    UI mapping information, and resolution hints.

    Args:
        question: The user's question in Vietnamese or English.
        intent: The detected intent (optional hint).
    """
    if _retriever is None:
        return "Retriever not initialized."

    # Search for context using LlamaIndex
    context_text = _retriever.retrieve(f"Question: {question} (Intent: {intent})")
    return context_text
