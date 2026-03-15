# Text-to-GraphQL Architecture

This document describes the technical architecture of the Text-to-GraphQL PoC, which enables querying banking customer data using natural Vietnamese language.

## 🏗 System Overview

The system follows a **Supervisor Agent** pattern implemented with **LangGraph**. It bridges the gap between unstructured Vietnamese queries and a structured GraphQL API by using a specialized Planner agent and a robust Context Retrieval (RAG) system.

### High-Level Component Diagram

```mermaid
graph TD
    User((User)) -->|Vietnamese Query| Supervisor[Supervisor Agent]

    subgraph Agentic_Orchestration [LangGraph Orchestration]
        Supervisor -->|Delegate| Planner[Planner Agent]
        Planner -->|Resolve Identity| CR[Customer Resolver Tool]
        Planner -->|Retrieve Context| RAG[RAG Retrieval Tool]
        Planner -.->|JSON Query Plan| Supervisor

        Supervisor -->|Validate| PT[Plan Validator Tool]
        Supervisor -->|Execute| GE[GraphQL Executor Tool]
    end

    subgraph RAG_System [Advanced RAG Fusion]
        RAG -->|Hybrid Search| ChromaDB[(Vector Store)]
        RAG -->|Keyword Search| BM25[BM25 Retriever]
        RAG -->|Merge & Rerank| RRF[Reciprocal Rank Fusion]
    end

    subgraph Data_Layer [GraphQL Facade]
        GE -->|Query| Schema[Strawberry GraphQL Schema]
        Schema -->|Resolve| Data[(Sample JSON Data)]
    end

    GE -->|Structured Result| Supervisor
    Supervisor -->|Natural Language Response| User
```

---

## 🤖 Agent Architecture (`src/agents/`)

The agent layer is built on **LangGraph Supervisor**, which provides a stateful, multi-agent workflow.

### Architecture Diagram

```mermaid
graph TD
    User([User]) <--> Supervisor[Supervisor Agent Node]

    subgraph "LangGraph Core"
        Supervisor <--> State[(Conversation State)]
        Supervisor -->|Delegates Task| Planner[Planner Agent Node]
        Supervisor -->|Calls Tool| Validator[Validator Tool]
        Supervisor -->|Calls Tool| Executor[GraphQL Executor]
    end

    subgraph "Planner Capability"
        Planner --> CustomerResolver[Customer Resolver]
        Planner --> ContextRetriever[Context Retrieval]
    end
```

### Execution Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as Supervisor
    participant P as Planner
    participant T as Tools (Resolver/RAG)
    participant E as Executor (GraphQL)

    U->>S: "Số dư của khách hàng Minh?"
    S->>P: Need a Query Plan
    P->>T: resolve_customer("Minh")
    T-->>P: CustomerID: 123
    P->>T: retrieve_context("số dư")
    T-->>P: Field mapping: casaAccount.balance
    P-->>S: JSON Plan { query: "customer_overview", args: { id: 123 } }
    S->>S: validate_plan()
    S->>E: execute_graphql_query(plan)
    E-->>S: Raw Data: { balance: 100M }
    S->>S: Reformat to natural Vietnamese
    S-->>U: "Khách hàng Minh hiện có số dư là 100.000.000 VND"
```

---

## 🔍 Data Ingestion Pipeline (`src/context/`)

Knowledge and metadata are ingested into a Vector Store to enable the agent to "understand" the data lake schema and Vietnamese business terms.

### Ingestion Flow Diagram

```mermaid
graph LR
    Docs[MD Metadata & UI Mapping] --> Reader[SimpleDirectoryReader]

    subgraph "LlamaIndex Ingestion Pipeline"
        Reader --> Cleaner[SourceHTMLCleaner]
        Cleaner --> Reformatter[LLM Reformatter]
        Reformatter --> Parser[MarkdownNodeParser]
        Parser --> Splitter[SentenceSplitter]
        Splitter --> ChunkMerger[SmallChunkMerger]
        ChunkMerger --> Embed[OpenAI Embedding]
    end

    Embed --> IDGen[Deterministic ID Gen]
    IDGen --> Chroma[(ChromaDB)]
```

### Retrieval Flow (RAG Fusion)

The retrieval process uses a multi-stage **RAG Fusion** approach to ensure high accuracy when mapping Vietnamese business terms to technical GraphQL fields.

```mermaid
graph TD
    Query([User Query]) --> Rewriter[Query Enhancer / Rewriter]
    Rewriter -->|Query V1| H1[Hybrid Retriever]
    Rewriter -->|Query V2| H2[Hybrid Retriever]
    Rewriter -->|Query VN| HN[Hybrid Retriever]

    subgraph "Hybrid Bridge"
        H1 --> Dense1[Chroma Vector Search]
        H1 --> Sparse1[BM25 Keyword Search]
    end

    Dense1 & Sparse1 & H2 & HN --> RRF[Reciprocal Rank Fusion]
    RRF --> Reranked[Top K Context Nodes]
    Reranked --> Output([Final Context for Agent])
```

#### Detailed Retrieval Logic:

- **Query Enhancement**: Generates multiple variations of the user's Vietnamese query to capture different semantic angles.
- **Hybrid Retrieval**: Executes both semantic (Dense) and keyword (Sparse) searches for every query variation.
- **Reciprocal Rank Fusion (RRF)**: Merges all search results into a single list, ensuring that tokens found across multiple versions or retrievers are boosted to the top.

### Key Components:

- **LLM Reformatter**: Uses GPT-4o-mini to clean and re-index raw metadata into a more "retrievable" format for the agent.
- **Deterministic IDs**: Uses SHA-256 hashes of content to ensure that re-running the pipeline updates existing documents instead of creating duplicates.
- **Advanced Retrieval**:
  - **Hybrid Fusion**: Combines Vector Search (Dense) + BM25 (Sparse).
  - **RRF (Reciprocal Rank Fusion)**: Reranks the merged results to ensure the most relevant schema mappings appear first.

---

## 🧩 Other Core Components

### 1. GraphQL Facade (`src/graphql_facade/`)

- **Schema (`schema.py`)**: Defines domain types (Customer, Account, AUM, NBO).
- **Resolvers (`resolvers.py`)**: Connects GraphQL queries to physical JSON data files.

### 2. Implementation Tools (`src/tools/`)

- **Customer Resolver**: Identity resolution tool.
- **Context Retrieval**: RAG-powered schema mapping tool.
- **Validator**: Logic to prevent halluncinated or unsafe queries.
- **Executor**: Bridge between the Agent's plan and the GraphQL endpoint.

---

## 🛠 Tech Stack

- **Orchestration**: LangGraph (Supervisor Pattern)
- **RAG Framework**: LlamaIndex
- **Embedding**: OpenAI `text-embedding-3-small`
- **Vector DB**: ChromaDB
- **GraphQL**: Strawberry (Python-native)
- **API**: FastAPI
