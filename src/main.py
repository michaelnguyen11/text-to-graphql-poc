import argparse
import logging
import os
import uvicorn

from src.config import settings


def setup_observability():
    """Configure LangSmith observability."""
    if settings.langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2).lower()
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
        logging.info("LangSmith observability enabled for project: %s", settings.langchain_project)


def main():
    """Start the server or run ingestion."""
    parser = argparse.ArgumentParser(description="Text-to-GraphQL Assistant")
    parser.add_argument("--ingest", action="store_true", help="Run metadata ingestion")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    setup_observability()

    if args.ingest:
        from src.context.ingest import ingest_metadata
        logging.info("Starting metadata ingestion...")
        ingest_metadata()
        logging.info("Ingestion complete.")
    else:
        from src.server import create_app
        app = create_app()
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level=settings.log_level,
        )


if __name__ == "__main__":
    main()
