# AI Data Reliability Copilot

> AI-powered data reliability platform for detecting, investigating, and safely recovering retail data pipeline failures.

AI Data Reliability Copilot combines **Data Engineering, Machine Learning, RAG, and GenAI** to help data engineers identify broken pipelines, understand root causes, assess business impact, and receive safe remediation recommendations.

## Architecture

```text
Retail Data
    ↓
AWS S3 Bronze
    ↓
Silver → Gold
    ↓
Data Quality + Lineage
    ↓
Anomaly Detection
    ↓
Incident Detection
    ↓
Evidence + RAG Context
    ↓
AI Reliability Copilot
    ↓
AWS Bedrock + Claude
    ↓
Root Cause + Impact + Recommendation
    ↓
Human Approval
```

## Key Capabilities

- **Data Engineering:** Bronze → Silver → Gold retail data pipeline
- **Data Quality:** Schema validation, duplicate detection, standardization, and quarantine
- **Data Reliability:** Incident detection, evidence collection, lineage, and impact analysis
- **ML Detection:** Rolling Z-score and Isolation Forest anomaly detection
- **RAG:** Pinecone + HuggingFace embeddings for reliability knowledge retrieval
- **GenAI:** AWS Bedrock + Claude for incident investigation
- **Remediation:** AI-generated recommendations with human review
- **API:** FastAPI backend with PostgreSQL
- **Testing:** Pytest automated test suite

## AI Investigation Flow

The V9 LangGraph Reliability Copilot orchestrates the investigation through a structured workflow:

```text
Incident
   ↓
Evidence Collection
   ↓
Reliability RAG Retrieval
   ↓
AWS Bedrock + Claude Analysis
   ↓
Evidence Validation
   ↓
   ├── Insufficient Evidence → Stop
   │
   └── Sufficient Evidence
            ↓
      Business Impact
            ↓
      Remediation Recommendation
            ↓
      Human Review
```

The LangGraph workflow coordinates the existing evidence collection, RAG retrieval, and Claude investigation services.

The Copilot returns:

- Incident summary
- Root-cause analysis
- Supporting evidence
- Business impact assessment
- Recommended action
- Confidence level
- Evidence sufficiency status

**Reliability principle:** The system distinguishes between detecting an incident and confirming its underlying root cause. When evidence is insufficient, the workflow stops before building its impact and recommendation outputs. Remediation recommendations require human review.

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL
- **Data:** Pandas, AWS S3, Bronze/Silver/Gold
- **ML:** Scikit-learn, Isolation Forest
- **AI:** AWS Bedrock, Claude, LangChain
- **RAG:** Pinecone, HuggingFace Embeddings
- **Frontend:** Streamlit
- **Testing:** Pytest

## Project Structure

```text
backend/
├── config/
├── db/
├── routers/
├── schemas/
├── services/
├── tests/
└── main.py

data/
frontend/
knowledge_base/
scripts/
requirements.txt
README.md
```

## Development Roadmap

| Version | Milestone | Status |
|---|---|---|
| V1 | Bedrock | ✅ Completed |
| V2 | Production GenAI | ✅ Completed |
| V3 | RAG + Pinecone + LangChain | ✅ Completed |
| V4 | Data Foundation | ✅ Completed |
| V5 | Medallion Pipeline | ✅ Completed |
| V6 | Data Quality + Lineage | ✅ Completed |
| V7 | ML Anomaly Detection | ✅ Completed |
| V8 | AI Reliability Copilot | ✅ Completed |
| V9 | LangGraph Investigation Workflow | ✅ Completed |
| V10 | MCP + Human Approval | 🚧 In Progress |
| V11 | Dashboard + Authentication | 🚧 Planned |
| V12 | Evaluation + Observability | 🚧 Planned |
| V13 | Docker + AWS + CI/CD | 🚧 Planned |

## Goal

Build a production-style AI platform that combines Data Engineering + ML + GenAI + Agentic AI to make business data more reliable and help engineering teams safely respond to pipeline failures.
