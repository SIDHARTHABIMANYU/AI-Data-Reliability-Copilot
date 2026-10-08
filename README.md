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

The V8 Reliability Copilot uses:

```text
Incident
   ↓
Evidence Collection
   ↓
Reliability RAG
   ↓
Context Construction
   ↓
AWS Bedrock + Claude
   ↓
Structured Investigation
```

The Copilot returns:

- Root cause
- Supporting evidence
- Business impact
- Recommended action
- Confidence level

The AI is designed not to invent evidence or assume that renamed fields have the same business meaning.

## Example

If an upstream source changes:

```text
sales_amount → net_amount
```

the system detects the schema mismatch, creates an incident, collects evidence, retrieves relevant reliability knowledge, and asks Claude to investigate the issue.

The system recommends validating the business meaning before applying any data mapping.

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

| Version | Milestone                    | Status |
|---------|------------------------------|--------|
| V1      | Bedrock                      | ✅     |
| V2      | Production GenAI             | ✅     |
| V3      | RAG                          | ✅     |
| V4      | Data Foundation              | ✅     |
| V5      | Medallion Pipeline           | ✅     |
| V6      | Data Quality + Lineage       | ✅     |
| V7      | ML Anomaly Detection         | ✅     |
| V8      | AI Reliability Copilot       | ✅     |
| V9      | LangGraph                    | 🚧     |
| V10     | MCP + Human Approval         | 🚧     |
| V11     | Dashboard + Authentication   | 🚧     |
| V12     | Evaluation + Observability   | 🚧     |
| V13     | Docker + AWS + CI/CD         | 🚧     |

## Goal

Build a production-style AI platform that combines Data Engineering + ML + GenAI + Agentic AI to make business data more reliable and help engineering teams safely respond to pipeline failures.
