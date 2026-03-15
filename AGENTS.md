# 🤖 AGENTS.md — Development Guidelines

This document provides context for AI agents (and human developers) working on the Text-to-GraphQL PoC.

## 🏗 System Design Patterns

### 1. Agent Orchestration (LangGraph)

We use a **Supervisor** pattern (`src/agents/supervisor.py`) based on `langgraph-supervisor`.

- **Supervisor**: The central coordinator. It manages the conversation history, validates candidate plans, and executes the final GraphQL query.
- **Planner Agent**: A specialized react agent (`src/agents/planner.py`) responsible for high-level reasoning. It resolves customer identities and uses RAG to map Vietnamese terms to GraphQL fields.
- **State Management**: LangGraph ensures the conversation thread is persistent. Key tools are split between the Supervisor (execution/validation) and the Planner (retrieval/resolution).

### 2. Context Layer (LlamaIndex Advanced RAG)

Metadata is ingested and retrieved using a sophisticated pipeline (`src/context/`).

- **Ingestion (`llama_pipeline.py`)**: Uses a `MarkdownNodeParser` and `SentenceSplitter`. Includes an `LLMReformatter` step to optimize metadata for vector search.
- **Idempotency**: Deterministic UUIDs (SHA-256) ensure that re-ingesting the same documentation doesn't pollute the vector store.
- **Retrieval (`retriever.py`)**: Implements **RAG Fusion**. It uses Hybrid Search (Chroma semantic + BM25 keyword) and Reciprocal Rank Fusion (RRF) to merge results from multiple query rewrites.

### 3. GraphQL Facade

We use **Strawberry** for a clean, Python-native GraphQL implementation (`src/graphql_facade/schema.py`).

- **Resolvers**: Logic is isolated in `resolvers.py`, reading from simulated data in `data/*.json`.
- **Dynamic Context**: The `retrieve_context` tool provides the LLM with the exact schema snippets needed for the current query.

## 🛠 Adding New Capabilities

### To add a new data field:

1. Add the field to the sample JSON data in `data/`.
2. Update the Strawberry type class in `src/graphql_facade/schema.py`.
3. Add a resolver for the field in `src/graphql_facade/resolvers.py` (if complex).
4. Update the metadata in `data-lake-metadata-enriched-compact.md` with descriptions and Vietnamese aliases.
5. Re-run ingestion: `python -m src.main --ingest`.

### To add a new query intent:

1. Update `src/agents/prompts.py` (PLANNER_SYSTEM_PROMPT) with descriptions and instructions for the new intent.
2. Update `src/tools/validator.py` (`SUPPORTED_INTENTS` list).
3. Update `src/tools/graphql_executor.py` to handle the new operation mapping.
4. Add the corresponding GraphQL query/field to the schema if it's a new root operation.

## 🧪 Testing

### Unit & Integration Tests

```bash
pytest tests/test_customer_resolver.py
pytest tests/test_graphql_facade.py
```

### End-to-End Pipeline

Use the `notebooks/End_to_End_Testing.ipynb` for interactive verification of the full flow (User -> Agent -> RAG -> GQL -> Answer).

## 📜 Coding Conventions

- **Pydantic V2**: Use `src/config.py` for all environment-based configuration.
- **LangSmith Tracing**: Ensure `LANGCHAIN_API_KEY` is set. Traces are sent to the `tcb-text-to-graphql` project.
- **Vietnamese Support**: All prompts and tools must prioritize preserving Vietnamese nuance and returning natural business prose.
- **Tooling**: Prefer atomic tool definitions in `src/tools/`. Never allow the LLM to call GraphQL directly; it must always go through the `QueryPlan` validation step.
