"""FastAPI server with GraphQL playground and Gradio chat UI."""

import logging

import gradio as gr
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.graphql_facade.schema import schema as graphql_schema
from src.graphql_facade import data_loader
from src.context.ingest import ingest_metadata
from src.context.retriever import LlamaContextRetriever
from src.tools.context_retrieval import set_retriever
from src.config import settings

logger = logging.getLogger(__name__)


def create_gradio_ui():
    """Create the Gradio ChatInterface UI."""

    def chat_fn(message, history):
        try:
            from src.agents.supervisor import chat

            # Simple session ID based on constant for PoC
            response = chat(message, session_id="gradio-session")
            return response
        except Exception as e:
            logger.error("Chat error: %s", e, exc_info=True)
            return f"Xin lỗi, đã xảy ra lỗi: {str(e)}"

    with gr.Blocks(theme=gr.themes.Soft(), title="🏦AI Banking Assistant") as demo:
        gr.ChatInterface(
            fn=chat_fn,
            title="🏦 Banking Assistant (Text-to-GraphQL)",
            description="Relationship Manager Tool for querying Customer Data Lake in Vietnamese.",
            examples=[
                "Cho tôi tổng quan khách hàng Nguyen van A",
                "CASA hiện tại của khách hàng có mã Cus1 là bao nhiêu?",
                "Top 3 NBO và AUM 3 tháng của khách hàng Pham Quang Minh là gì?",
                "Thông tin thu nhập và chi phí hàng tháng của khách hàng Minh?",
                "AUM 3 tháng gần đây của khách hàng Cus2?",
                "Khách hàng Chan Thi B đang dùng những sản phẩm gì?",
            ],
            textbox=gr.Textbox(
                placeholder="Nhập câu hỏi của bạn tại đây...", container=False, scale=7
            ),
        )
    return demo


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="Text-to-GraphQL Assistant",
        description="AI Banking Assistant PoC - Vietnamese Text to GraphQL",
        version="0.1.0",
    )

    # Mount GraphQL endpoint
    graphql_app = GraphQLRouter(graphql_schema)
    app.include_router(graphql_app, prefix="/graphql")

    @app.on_event("startup")
    async def startup():
        """Initialize data and metadata on startup."""
        # Load sample data
        data_loader.load_data()
        logger.info("Sample data loaded")

        # Load/Ingest metadata using LlamaIndex
        try:
            # Note: ingest_metadata handles skipping if already ingested
            index, nodes = ingest_metadata()
            retriever = LlamaContextRetriever(index, nodes=nodes)
            set_retriever(retriever)
            logger.info("RAG Index loaded/initialized")
        except Exception as e:
            logger.error("Failed to initialize RAG context: %s", e, exc_info=True)

    @app.get("/health")
    async def health():
        return {"status": "ok", "model": settings.openai_model}

    # Mount Gradio UI
    app = gr.mount_gradio_app(app, create_gradio_ui(), path="/")

    return app
