"""Central configuration using Pydantic Settings."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    openai_temperature: float = 0.1
    openai_embedding_model: str = "text-embedding-3-small"

    # Ingestion (RAG Pipeline)
    ingest_model: str = "gpt-4.1-mini"
    ingest_temperature: float = 0.0

    # Retrieval (RAG Fusion)
    retrieval_model: str = "gpt-4.1-mini"
    retrieval_temperature: float = 0.0

    # ChromaDB
    chroma_persist_dir: str = "./chroma_data"

    # Data
    data_dir: str = "./data"

    # Server
    host: str = "0.0.0.0"
    port: int = 4444
    log_level: str = "info"

    # Agent
    max_retrieval_results: int = 10
    planner_temperature: float = 0.0
    answer_temperature: float = 0.3

    # Observability
    langsmith_enabled: bool = True

    # LangSmith / LangChain
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "tcb-text-to-graphql"
    langchain_endpoint: str = "https://api.smith.langchain.com"

    # Enterprise / Bedrock
    aws_region: str = "ap-southeast-1"

    model_config = {
        "env_file": ".env", 
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

    @property
    def project_root(self) -> Path:
        """Get the absolute path to the project root."""
        return Path(__file__).parent.parent.absolute()

    @property
    def data_path(self) -> Path:
        path = Path(self.data_dir)
        if not path.is_absolute():
            return (self.project_root / path).absolute()
        return path.absolute()

    @property
    def chroma_path(self) -> Path:
        path = Path(self.chroma_persist_dir)
        if not path.is_absolute():
            return (self.project_root / path).absolute()
        return path.absolute()


settings = Settings()
