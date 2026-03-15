"""Main LlamaIndex ingestion pipeline logic for context preparation."""

import logging
import hashlib
import concurrent.futures
from datetime import datetime
from functools import partial
from typing import Any, List, Sequence, Optional

from llama_index.core import Document
from llama_index.core.schema import BaseNode
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.vector_stores.types import VectorStore
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import (
    MarkdownNodeParser,
    SentenceSplitter,
)
from pydantic import BaseModel, Field

from src.context.transforms import (
    SourceHTMLCleaner, 
    LLMTableReformatter,
    SmallChunkMerger,
    generate_deterministic_chunk_id
)

logger = logging.getLogger(__name__)


class BatchResult(BaseModel):
    """Result of a batch operation."""
    succeeded: int = 0
    failed: int = 0
    failed_ids: List[str] = Field(default_factory=list)


def build_pipeline(
    embedding_model: BaseEmbedding,
    chunk_size: int = 1024,
    chunk_overlap: int = 200,
    *,
    enable_cache: bool = True,
    reformat_model: str = "gpt-4.1-nano",
    reformat_api_key: str | None = None,
) -> IngestionPipeline:
    """Create a high-quality ingestion pipeline for markdown documents.

    Pipeline:
        SourceHTMLCleaner → LLMTableReformatter → MarkdownNodeParser 
        → RecursiveCharacterTextSplitter → SmallChunkMerger → EmbeddingModel
    """
    
    transformations: List[Any] = []

    # Step 1: Clean HTML artifacts
    transformations.append(SourceHTMLCleaner())

    # Step 2: Reformat tables using LLM
    transformations.append(
        LLMTableReformatter(
            model=reformat_model,
            api_key=reformat_api_key
        )
    )

    # Step 3: Split by markdown headers
    markdown_parser = MarkdownNodeParser.from_defaults(
        include_metadata=True,
        include_prev_next_rel=True,
    )

    # Step 4: Token-aware recursive text splitting (Native LlamaIndex)
    text_splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        include_metadata=True,
        include_prev_next_rel=True,
    )

    # Step 5: Merge tiny chunks
    transformations.extend([markdown_parser, text_splitter, SmallChunkMerger()])

    # Final step: embedding
    transformations.append(embedding_model)

    # Cache is optional (in-memory if no Redis specified)
    cache = IngestionCache() if enable_cache else None

    logger.info(f"Built ingestion pipeline: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

    return IngestionPipeline(
        transformations=transformations,
        cache=cache,
    )


def _batch_add_nodes(vector_store: VectorStore, nodes: List[BaseNode]) -> BatchResult:
    """Add nodes to vector store in a batch."""
    try:
        vector_store.add(nodes)
        return BatchResult(succeeded=len(nodes))
    except Exception as e:
        logger.error(f"Error adding nodes to vector store: {e}")
        return BatchResult(failed=len(nodes), failed_ids=[n.id_ for n in nodes])


def run_ingestion_pipeline(
    documents: Sequence[Document],
    embedding_model: BaseEmbedding,
    vector_store: VectorStore,
    show_progress: bool = False,
    chunk_size: int = 1024,
    chunk_overlap: int = 200,
    max_workers: int = 4,
    batch_size: int = 50,
    delete_existing_chunks: bool = True,
    *,
    enable_cache: bool = True,
    num_pipeline_workers: int | None = 4,
    reformat_model: str = "gpt-4.1-nano",
    reformat_api_key: str | None = None,
) -> List[BaseNode]:
    """Run the ingestion pipeline with multi-threaded vector store operations."""
    
    pipeline = build_pipeline(
        embedding_model=embedding_model,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        enable_cache=enable_cache,
        reformat_model=reformat_model,
        reformat_api_key=reformat_api_key,
    )

    doc_id_to_original_title: dict[str, str] = {}
    for doc in documents:
        doc_id = doc.metadata.get("documentId") or doc.metadata.get("docId") or doc.id_
        original_title = doc.metadata.get("title")
        if doc_id and original_title:
            doc_id_to_original_title[doc_id] = original_title

    run_kwargs: dict[str, Any] = {
        "documents": documents,
        "show_progress": show_progress,
    }
    if num_pipeline_workers is not None and num_pipeline_workers > 1:
        run_kwargs["num_workers"] = num_pipeline_workers

    nodes = pipeline.run(**run_kwargs)

    timestamp = datetime.utcnow().isoformat() + "Z"
    for idx, node in enumerate(nodes):
        node.metadata["chunkId"] = idx
        node.metadata["ingestedAt"] = timestamp
        
        # Determine parent doc ID reliably
        parent_doc_id = node.metadata.get("documentId") or node.metadata.get("docId") or (node.parent_node.node_id if node.parent_node else "")

        if parent_doc_id and parent_doc_id in doc_id_to_original_title:
            node.metadata["title"] = doc_id_to_original_title[parent_doc_id]

        if parent_doc_id:
            content_sample = getattr(node, "text", "")[:100]
            content_hash = hashlib.md5(content_sample.encode()).hexdigest()
            chunk_id = generate_deterministic_chunk_id(parent_doc_id, idx, content_hash)
            node.id_ = chunk_id
            node.metadata["docId"] = parent_doc_id
            node.metadata["documentId"] = chunk_id
        else:
            fallback_id = f"chunk-{idx}-{timestamp.replace(':','-')}"
            node.id_ = fallback_id

    if nodes:
        overall_result = BatchResult()
        node_batches = [nodes[i : i + batch_size] for i in range(0, len(nodes), batch_size)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            batch_add_func = partial(_batch_add_nodes, vector_store)
            futures = [executor.submit(batch_add_func, batch) for batch in node_batches]
            for future in concurrent.futures.as_completed(futures):
                br = future.result()
                overall_result.succeeded += br.succeeded
                overall_result.failed += br.failed
                overall_result.failed_ids.extend(br.failed_ids)

        logger.info(f"Successfully added {overall_result.succeeded}/{len(nodes)} nodes to vector store.")

    return list(nodes)
