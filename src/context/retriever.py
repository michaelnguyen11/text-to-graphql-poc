"""Context retrieval logic using LlamaIndex with RAG Fusion and Hybrid search."""

import logging
import json
from typing import List, Optional

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever, QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.schema import NodeWithScore, BaseNode, TextNode
from llama_index.llms.openai import OpenAI

from src.config import settings

logger = logging.getLogger(__name__)

# Global retriever instance
_retriever = None


def load_nodes_from_index(index: VectorStoreIndex) -> List[BaseNode]:
    """Helper to reconstruct nodes from the index's vector store (Chroma).
    
    This allows initializing BM25 at runtime without re-reading source files.
    """
    try:
        from llama_index.vector_stores.chroma import ChromaVectorStore
        if not isinstance(index.storage_context.vector_store, ChromaVectorStore):
            return []
            
        vector_store = index.storage_context.vector_store
        # results = collection.get() returns documents, metadatas, etc.
        results = vector_store._collection.get()
        
        nodes = []
        if results and "ids" in results:
            for i in range(len(results["ids"])):
                metadata = results["metadatas"][i]
                # LlamaIndex stores the full node JSON in _node_content
                node_content = metadata.get("_node_content")
                if node_content:
                    try:
                        node_dict = json.loads(node_content)
                        # Reconstruct the correct node type (usually TextNode)
                        node = TextNode.from_dict(node_dict)
                        nodes.append(node)
                    except Exception:
                        # Fallback to simple TextNode if JSON fails
                        nodes.append(TextNode(
                            id_=results["ids"][i],
                            text=results["documents"][i],
                            metadata=metadata
                        ))
                else:
                    nodes.append(TextNode(
                        id_=results["ids"][i],
                        text=results["documents"][i],
                        metadata=metadata
                    ))
        return nodes
    except Exception as e:
        logger.error("Failed to load nodes from vector store: %s", e)
        return []


class LlamaContextRetriever:
    """Advanced Hybrid Fusion Retriever with query enhancement and RRF.
    
    This implementation combines:
    1. Pre-retrieval: Query enhancement (generating multiple query variations)
    2. Retrieval: Hybrid Search (Vector + BM25 Keyword)
    3. Post-retrieval: Reciprocal Rank Fusion (RRF) to merge results
    """

    def __init__(self, index: VectorStoreIndex, nodes: List[BaseNode] = None):
        self.index = index
        self.nodes = nodes
        
        # If nodes aren't provided (e.g., at runtime), try to load them from Chroma
        if not self.nodes:
            logger.info("Nodes not provided. Attempting to load from vector store for BM25...")
            self.nodes = load_nodes_from_index(index)

        # 1. Base Vector Retriever
        self.vector_retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=5,
        )
        
        # 2. Base Keyword Retriever (BM25)
        self.bm25_retriever = None
        if self.nodes:
            try:
                self.bm25_retriever = BM25Retriever.from_defaults(
                    nodes=self.nodes,
                    similarity_top_k=5
                )
                logger.info("BM25 retriever initialized with %d nodes", len(self.nodes))
            except Exception as e:
                logger.warning("Failed to initialize BM25 retriever: %s", e)
        else:
            logger.warning("No nodes available for BM25 retriever. Using vector-only fusion.")

        # 3. Hybrid Fusion Retriever
        # This handles:
        # - Query enhancement (via LLM generating num_queries)
        # - Hybrid search (via multiple retrievers: vector and keyword)
        # - RRF (Reciprocal Rank Fusion) for merging ranks
        retrievers = [self.vector_retriever]
        if self.bm25_retriever:
            retrievers.append(self.bm25_retriever)
            
        self.fusion_retriever = QueryFusionRetriever(
            retrievers,
            llm=OpenAI(model=settings.openai_model, api_key=settings.openai_api_key),
            query_gen_prompt=(
                "Bạn là một chuyên gia truy vấn dữ liệu ngân hàng. "
                "Hãy tạo ra {num_queries} biến thể truy vấn tìm kiếm khác nhau cho câu hỏi dưới đây. "
                "Mỗi biến thể nên khai thác một góc nhìn khác nhau: sử dụng từ đồng nghĩa, "
                "thay đổi độ chi tiết (rộng hơn/hẹp hơn), và xem xét các khía cạnh kỹ thuật như "
                "tên trường dữ liệu (field names) hoặc ý nghĩa nghiệp vụ ngân hàng. "
                "Tránh tạo ra các câu hỏi chỉ là thay đổi từ ngữ đơn giản.\n"
                "Câu hỏi gốc: {query}\n"
                "Danh sách {num_queries} truy vấn:"
            ),
            num_queries=4,
            mode="reciprocal_rerank",
            similarity_top_k=settings.max_retrieval_results // 2 if settings.max_retrieval_results else 5,
            verbose=True,
        )

    def retrieve(self, query: str, filters: dict = None) -> str:
        """Retrieve relevant context using Hybrid Fusion approach."""
        try:
            # QueryFusionRetriever handles the multi-query enhancement internally
            nodes = self.fusion_retriever.retrieve(query)
        except Exception as e:
            logger.error(f"Fusion retrieval failed: {e}. Falling back to basic vector search.")
            nodes = self.vector_retriever.retrieve(query)
        
        if not nodes:
            return "No relevant metadata found."

        context_parts = []
        for i, node in enumerate(nodes):
            text = node.get_content().strip()
            score = node.score if hasattr(node, "score") else "N/A"
            source = node.metadata.get("file_name", "Unknown")
            context_parts.append(f"--- Context Chunk {i+1} (Source: {source}, Score: {score}) ---\n{text}")

        return "\n\n".join(context_parts)


def set_retriever(retriever: LlamaContextRetriever):
    """Set the global retriever instance."""
    global _retriever
    _retriever = retriever


def get_retriever() -> Optional[LlamaContextRetriever]:
    """Get the global retriever instance."""
    return _retriever
