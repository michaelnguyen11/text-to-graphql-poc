"""Custom LlamaIndex transformations for the ingestion pipeline.

This module provides transformations for cleaning HTML, reformatting tables using LLM,
and merging small chunks for better RAG quality.
"""

from __future__ import annotations

import logging
import re
import hashlib
from typing import Any, List, Optional

from llama_index.core.schema import BaseNode, TransformComponent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Global cache for document reformatting results
# ---------------------------------------------------------------------------
_DOC_REFORMAT_CACHE: dict[str, str] = {}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def clean_html_in_markdown(text: str) -> str:
    """Strip HTML tags and normalize whitespace in markdown."""
    if not text:
        return ""
    # Convert <br/> to newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    # Remove all other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ---------------------------------------------------------------------------
# LLMTableReformatter: Whole Document Version
# ---------------------------------------------------------------------------

DOCUMENT_REFORMAT_PROMPT = """\
You are a senior technical writer and data engineer. I will provide a markdown document \
that may contain several tables. 

Your task is to REWRITE the entire document into a clean, semantically dense markdown \
format that is optimized for LLM retrieval and embedding.

CRITICAL INSTRUCTION FOR TABLES:
- Identify every markdown table in the document.
- Convert each table into well-structured prose or a "Key: Value" list format.
- Preserve ALL information from the tables. Do NOT omit any rows or columns.
- Use bold (**Field Name**) for keys and normal text for values.
- Group related information under appropriate sub-headings (###).

GENERAL FORMATTING:
- Preserve the existing heading structure (#, ##).
- Keep all non-table text as is, but clean up any formatting artifacts.
- The output must be valid markdown.
- Do NOT add any introduction, conclusion, or commentary. Output ONLY the rewritten markdown.
- Ensure the output is complete and not truncated.

DOCUMENT CONTENT:
{content}
"""

def _get_reformat_llm(model: str | None = None, api_key: str | None = None):
    from openai import OpenAI
    from src.config import settings
    key = api_key or settings.openai_api_key
    return OpenAI(api_key=key), (model or "gpt-4.1-nano")

class LLMTableReformatter(TransformComponent):
    """
    Transformer that reformats a whole markdown document at once using an LLM.
    It identifies tables and rewrites them into semantic prose to improve RAG quality.
    """
    
    model: str = "gpt-4.1-nano"
    api_key: str | None = None
    max_chars: int = 100000  # OpenAI limit for some models/requests

    def __init__(self, model: str = "gpt-4.1-nano", api_key: str | None = None, max_chars: int = 100000, **kwargs):
        super().__init__()
        self.model = model
        self.api_key = api_key
        self.max_chars = max_chars

    def _should_reformat(self, text: str) -> bool:
        """Check if the document contains a markdown table."""
        return "|" in text and "-|-" in text

    def _reformat_document(self, text: str) -> str:
        """Process the whole document via LLM."""
        # Clean HTML first
        cleaned = clean_html_in_markdown(text)
        
        # Check cache
        content_hash = hashlib.md5(cleaned.encode()).hexdigest()
        if content_hash in _DOC_REFORMAT_CACHE:
            return _DOC_REFORMAT_CACHE[content_hash]

        if len(cleaned) > self.max_chars:
            logger.warning(f"Document too large for LLM reformat ({len(cleaned)} chars). Skipping.")
            return cleaned

        logger.info(f"Reformatting whole document via LLM ({len(cleaned)} chars)")
        
        # Use simple string concatenation to avoid f-string/format issues with curly braces in content
        prompt = DOCUMENT_REFORMAT_PROMPT.replace("{content}", cleaned)
        
        try:
            client, model_name = _get_reformat_llm(self.model, self.api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.ingest_temperature,
                max_tokens=4096, # Reduce max_tokens to a safer value for markdown output
            )

            if response.choices[0].finish_reason == "length":
                logger.warning("LLM document reformat hit max_tokens limit. Content might be truncated!")
            
            result = (response.choices[0].message.content or "").strip()
            if not result:
                return cleaned

            # Cache result
            _DOC_REFORMAT_CACHE[content_hash] = result
            return result
            
        except Exception as e:
            logger.error(f"Whole document reformat failed: {e}")
            return cleaned

    def __call__(self, nodes: list[BaseNode], **kwargs: Any) -> list[BaseNode]:
        for node in nodes:
            original = node.get_content()
            if not original or not self._should_reformat(original):
                continue
            
            reformatted = self._reformat_document(original)
            if reformatted != original:
                node.set_content(reformatted)
        return nodes

# ---------------------------------------------------------------------------
# Reusable TransformComponents (kept for pipeline compatibility)
# ---------------------------------------------------------------------------

class SourceHTMLCleaner(TransformComponent):
    """Strip HTML artifacts from markdown text."""
    def __call__(self, nodes: list[BaseNode], **kwargs: Any) -> list[BaseNode]:
        for node in nodes:
            node.set_content(clean_html_in_markdown(node.get_content()))
        return nodes

class SmallChunkMerger(TransformComponent):
    """Merge tiny chunks into their next sibling to eliminate noise."""
    min_chunk_chars: int = 80

    def __call__(self, nodes: list[BaseNode], **kwargs: Any) -> list[BaseNode]:
        if len(nodes) <= 1: return nodes
        merged, carry = [], ""
        for node in nodes:
            content = node.get_content()
            if len(content) < self.min_chunk_chars:
                carry = (carry + "\n\n" + content).strip() if carry else content
            else:
                if carry:
                    node.set_content(carry + "\n\n" + content)
                    carry = ""
                merged.append(node)
        if carry and merged:
            merged[-1].set_content(merged[-1].get_content() + "\n\n" + carry)
        elif carry:
            nodes[0].set_content(carry)
            merged.append(nodes[0])
        return merged

def generate_deterministic_chunk_id(doc_id: str, chunk_index: int, content_hash: str) -> str:
    """Generate a deterministic ID for a chunk to allow idempotent upserts."""
    raw_id = f"{doc_id}_{chunk_index}_{content_hash}"
    return hashlib.md5(raw_id.encode()).hexdigest()
