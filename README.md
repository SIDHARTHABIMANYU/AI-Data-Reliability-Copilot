# AI Data Reliability Copilot

> A production-style AI and data engineering system for detecting, investigating, and recovering retail data pipeline failures.

AI Data Reliability Copilot is a business-focused data reliability platform designed for a retail environment where daily sales, inventory, and supplier data feed business dashboards.

The project combines modern data engineering with Generative AI to help data engineers understand broken pipelines, investigate data quality issues, identify business impact, and safely propose recovery actions.

The project started as a basic AWS Bedrock business assistant and evolved through multiple engineering stages into a data reliability system combining data pipelines, RAG, vector search, LLMs, and eventually agentic workflows with human approval.

---

## Project Evolution

### V1 — Basic GenAI Chatbot
- AWS Bedrock
- Claude
- Streamlit
- FastAPI

### V2 — Production-style GenAI Application
- Structured FastAPI architecture
- Pydantic schemas
- Configuration management
- Error handling
- Logging
- Health endpoints
- Conversation handling

### V3 — RAG Pipeline
- LangChain
- Pinecone
- HuggingFace embeddings
- Semantic retrieval
- Relevance filtering
- Source attribution
- Automated RAG tests

### V4 — Data Foundation
- Synthetic retail datasets
- PostgreSQL
- SQLAlchemy
- Data contracts
- Retail ingestion pipeline
- S3 integration
- Bronze data layer
- Pipeline execution metadata

### V5 — Medallion Data Pipeline
- Bronze → Silver → Gold
- Data validation
- Deduplication
- Standardization
- Data transformation
- Business-ready datasets

### Future Stages
- Data quality framework
- Data lineage
- Statistical anomaly detection
- AI incident investigation
- Repair proposals
- LangGraph orchestration
- MCP tools
- Human approval workflows
- Dashboard
- Evaluation and observability
- Docker and AWS deployment

---

# Business Problem

Retail businesses receive data from multiple sources every day:

- Sales systems
- Inventory systems
- Suppliers

A small data problem can affect business reporting.

For example:

```text
Supplier changes a column
        ↓
Pipeline validation fails
        ↓
Silver data is affected
        ↓
Gold revenue metric becomes incomplete
        ↓
Dashboard shows incorrect information
