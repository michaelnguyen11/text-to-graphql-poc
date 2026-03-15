"""Ingest metadata into ChromaDB using the LlamaIndex IngestionPipeline."""

import logging
from pathlib import Path
from typing import Optional, List

import chromadb
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

from src.config import settings
from src.context.llama_pipeline import run_ingestion_pipeline

logger = logging.getLogger(__name__)


def ingest_metadata(data_dir: Path | None = None, chroma_dir: Path | None = None) -> tuple[VectorStoreIndex, List[BaseNode]]:
    """Ingest metadata files from data_dir into ChromaDB or load existing index.

    Returns the initialized VectorStoreIndex and the list of ingested nodes.
    """
    from src.context.retriever import load_nodes_from_index
    
    data_dir = data_dir or settings.data_path
    chroma_dir = chroma_dir or settings.chroma_path

    # Initialize ChromaDB
    db = chromadb.PersistentClient(path=str(chroma_dir))
    
    # Check if we already have data in the collection
    collection_name = "llama_metadata"
    exists = False
    try:
        chroma_collection = db.get_collection(collection_name)
        if chroma_collection.count() > 0:
            exists = True
            logger.info("Found existing metadata in ChromaDB collection '%s'. Skipping ingestion.", collection_name)
    except Exception:
        chroma_collection = db.create_collection(collection_name)
        logger.info("Created new ChromaDB collection '%s'.", collection_name)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    embed_model = OpenAIEmbedding(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )

    if not exists:
        logger.info("Ingesting metadata from %s into ChromaDB with LlamaIndex", data_dir)
        # 1. Load documents
        reader = SimpleDirectoryReader(
            input_dir=str(data_dir),
            recursive=False,
            required_exts=[".md"],
        )
        documents = reader.load_data()
        logger.info(f"Loaded {len(documents)} documents from {data_dir}")

        # 2. Run Ingestion Pipeline (this also adds to vector_store)
        nodes = run_ingestion_pipeline(
            documents=documents,
            embedding_model=embed_model,
            vector_store=vector_store,
            show_progress=True,
            reformat_model=settings.ingest_model,
            reformat_api_key=settings.openai_api_key,
        )
    else:
        # Load index from vector store
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context, embed_model=embed_model
        )
        # Reconstruct nodes from Chroma for BM25 initialization
        nodes = load_nodes_from_index(index)
        return index, nodes

    # 3. Create index for retrieval (if newly ingested)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context, embed_model=embed_model
    )
    
    logger.info("Metadata ingestion complete.")
    return index, nodes
