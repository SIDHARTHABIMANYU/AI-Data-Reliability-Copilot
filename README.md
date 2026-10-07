# AI Data Reliability Copilot

> A production-style AI and data engineering system for detecting, investigating, and recovering retail data pipeline failures.

AI Data Reliability Copilot is a retail-focused data reliability platform that helps data engineers detect pipeline failures, investigate data quality issues, understand downstream impact, and propose safe remediation actions.

The project evolved from an AWS Bedrock GenAI chatbot into a data engineering + AI reliability system.

---

## Architecture

```text
Retail Data
    ↓
AWS S3 Bronze
    ↓
Silver
    ↓
Gold
    ↓
Data Quality + Lineage
    ↓
Incident Detection
    ↓
AI Investigation
    ↓
AI Remediation
    ↓
Human Approval
```

---

## Project Evolution

| Version | Focus | Status |
|---|---|---|
| V1 | AWS Bedrock + Claude
| V2 | Production FastAPI Architecture 
| V3 | RAG + Pinecone + LangChain 
| V4 | Retail Data Foundation + S3 + PostgreSQL 
| V5 | Bronze → Silver → Gold Pipeline 
| V6 | Data Quality + Lineage + AI Investigation 
| V7 | ML Anomaly Detection 
| V8 | AI Data Reliability Copilot | 🚧 |
| V9 | LangGraph | 🚧 |
| V10 | MCP + Human-in-the-Loop | 🚧 |
| V11 | Dashboard + Authentication | 🚧 |
| V12 | Evaluation + Observability | 🚧 |
| V13 | Docker + AWS + CI/CD | 🚧 |

---

## Current Capabilities

### Data Engineering

- Synthetic retail sales, inventory, and supplier datasets
- AWS S3 data lake
- Bronze → Silver → Gold architecture
- PostgreSQL + SQLAlchemy
- Data contracts
- Schema validation
- Deduplication and standardization
- Data quality tracking
- Pipeline run tracking

### Reliability

- Incident management
- Failure detection
- Evidence collection
- Data lineage
- Downstream business impact tracking

### ML Anomaly Detection

- Rolling z-score anomaly detection
- Leakage-free historical baselines
- Isolation Forest detection
- Statistical + ML anomaly confirmation
- PostgreSQL anomaly result storage
- Anomaly-to-incident workflow
- Controlled anomaly scenario testing
- Detection agreement evaluation

### AI

- AWS Bedrock + Claude
- LangChain
- AI-powered incident investigation
- Structured root-cause analysis
- AI remediation suggestions
- Human approval workflow

### RAG

- Pinecone
- HuggingFace embeddings
- Semantic retrieval
- Relevance filtering
- Source attribution

---

## Example Failure

A source system changes:

```text
sales_amount → net_amount
```

The system detects the schema mismatch:

```text
Schema Validation
      ↓
Pipeline Failure
      ↓
Incident Created
      ↓
Evidence Collected
      ↓
AI Investigation
      ↓
Remediation Proposal
      ↓
Human Approval
```

The AI does not directly modify production data. Proposed changes require human review.

---

## Technology Stack

**Backend:** Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL

**Data:** Pandas, AWS S3, Bronze/Silver/Gold

**AI:** AWS Bedrock, Claude, LangChain

**RAG:** Pinecone, HuggingFace Embeddings

**Frontend:** Streamlit

**Testing:** Pytest

---

## Project Structure

```text
AI-Data-Reliability-Copilot/
├── backend/
│   ├── config/
│   ├── db/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── data/
├── frontend/
├── knowledge_base/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

---

## Roadmap

The project is being developed incrementally, introducing new technologies only when they solve a real engineering requirement.

```text
V1 → Bedrock
V2 → Production GenAI
V3 → RAG
V4 → Data Foundation
V5 → Medallion Pipeline
V6 → Data Quality + Lineage
V7 → ML Anomaly Detection
V8 → AI Reliability Copilot
V9 → LangGraph
V10 → MCP + Human Approval
V11 → Dashboard + Authentication
V12 → Evaluation + Observability
V13 → Docker + AWS + CI/CD
```

---

## Goal

Build a production-style AI Data Reliability platform that combines:

**Data Engineering + ML + GenAI + Agentic AI**

to help engineering teams detect, investigate, and safely recover data pipeline failures.
