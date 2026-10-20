# AI Data Reliability Copilot

An AI-powered data reliability platform for detecting, investigating, and managing data pipeline incidents using machine learning, retrieval-augmented generation (RAG), and human-reviewed remediation workflows.

## Overview

AI Data Reliability Copilot combines data engineering, machine learning, and generative AI to help engineers understand data quality failures and investigate their potential causes.

The platform includes a React dashboard, a FastAPI backend, evidence-based incident investigation, AI-generated remediation proposals, and an approval workflow that records reviewer decisions.

## Key Features

- **Incident monitoring:** View detected incidents, severity, status, and associated pipeline information.
- **Data quality evidence:** Inspect incident-linked pipeline runs and quality-check results.
- **ML anomaly detection:** Use Isolation Forest and Z-score-based techniques to identify unusual retail data patterns.
- **AI incident investigation:** Use LangGraph to organize investigation steps and generate structured findings from incident evidence.
- **Retrieval-augmented generation:** Use Pinecone retrieval with local Hugging Face embeddings to provide relevant context for AI workflows.
- **AI remediation proposals:** Generate suggested corrective actions, validation steps, and risk assessments.
- **Human-in-the-loop review:** Approve or reject proposed remediation actions and record reviewer decisions.
- **Auditability:** Store remediation review information in PostgreSQL.
- **Web dashboard:** Use a React and TypeScript interface with Recharts visualizations.
- **Configurable LLM provider:** Support Google Gemini for development and testing while retaining AWS Bedrock integration.

> AI-generated findings and remediation plans are recommendations for engineering review. They should not be treated as independently verified root causes or automatically executed database changes.

## Architecture

```text
Retail Data and Pipeline Telemetry
                |
                v
       Data Quality Checks
                |
                v
       Incident and Evidence APIs
                |
                v
       LangGraph Investigation
                |
                v
    Pinecone Retrieval + Embeddings
                |
                v
    Configured LLM Provider
       Gemini / AWS Bedrock
                |
                v
 Root-Cause Analysis and Remediation
                |
                v
       Engineer Review Decision
          Approve / Reject
                |
                v
 PostgreSQL Remediation Audit Records
                |
                v
       React Web Dashboard
```

The exact processing path depends on the incident and the backend services involved. The diagram is a high-level view of the platform rather than a claim that every request traverses every component.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, Recharts |
| Backend API | Python, FastAPI, Pydantic |
| AI workflows | LangGraph, LangChain |
| LLM providers | Google Gemini, AWS Bedrock |
| RAG | Pinecone, Hugging Face sentence embeddings |
| Machine learning | scikit-learn, Isolation Forest, Z-score analysis |
| Data and persistence | PostgreSQL, SQLAlchemy, AWS S3 |
| Testing | Pytest and application-level endpoint checks |

## Project Structure

```text
BEDROCK/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ routers/
â”‚   â”œâ”€â”€ schemas/
â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â””â”€â”€ reliability/
â”‚   â”œâ”€â”€ tests/
â”‚   â””â”€â”€ main.py
â”œâ”€â”€ data/
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ public/
â”‚   â”œâ”€â”€ package.json
â”‚   â”œâ”€â”€ vite.config.ts
â”‚   â””â”€â”€ README.md
â”œâ”€â”€ knowledge_base/
â”œâ”€â”€ scripts/
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

Some directories may contain additional project-specific modules. Refer to the repository for the current implementation.

## Prerequisites

- Python 3.10 or later, compatible with the installed backend dependencies
- Node.js 18 or later and npm
- PostgreSQL
- Valid credentials and configuration for the services you use, such as Pinecone, Google Gemini, AWS S3, or AWS Bedrock

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd BEDROCK
```

### 2. Set up the Python environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If the virtual environment already exists, activate it rather than recreating it.

### 3. Configure backend environment variables

Create or update the backend `.env` file using the environment variable names defined in `backend/config/settings.py`.

Common provider settings include:

```dotenv
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL_ID=gemini-2.5-flash

AWS_REGION=us-east-1
BEDROCK_MODEL_ID=your_bedrock_model_id
AWS_BEARER_TOKEN_BEDROCK=your_bedrock_token

PINECONE_API_KEY=your_pinecone_api_key
S3_BUCKET_NAME=your_s3_bucket_name
```

Use the settings required by your selected provider and the existing backend services. Do not commit `.env` files, API keys, AWS credentials, database credentials, or other secrets.

For AWS Bedrock, ensure your account, model access, and authentication method permit the requested operation.

### 4. Start the backend

From the repository root:

```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend will be available at `http://127.0.0.1:8000`.

Where enabled, interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 5. Configure and start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
```

Create `frontend/.env` if needed:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Then start the development server:

```powershell
npm run dev
```

Open `http://localhost:5173` in your browser.

For frontend build instructions and dashboard-specific details, see [`frontend/README.md`](frontend/README.md).

## Incident Investigation and Remediation Workflow

1. An incident is detected and exposed through the backend API.
2. The dashboard displays incident details and associated evidence.
3. The investigation workflow gathers relevant evidence and retrieval context.
4. The configured LLM generates structured investigation findings.
5. An engineer reviews the proposed remediation plan and its risk.
6. The engineer approves or rejects the proposal.
7. The backend records the review decision and associated audit information.

Approval records a review decision; it does not mean that an unverified remediation has automatically changed production data.

## Frontend API Integration

The dashboard integrates with backend routes for functionality such as:

- Health and dashboard summary
- Incident listing and evidence
- AI investigation results
- Remediation proposal retrieval
- Remediation approval and rejection
- Anomaly detection results

The frontend documentation describes the specific routes and payloads used by the current dashboard. Global pipeline-run and data-quality history views may require additional backend endpoints.

## Development and Validation

Validate changes locally before committing:

```powershell
git diff --check
git status --short
```

Start the backend and frontend separately and exercise the relevant workflows. Confirm that incident investigation, remediation generation, and reviewer decisions work with the currently configured services.

Run the available automated tests using the project's configured test setup. Do not treat a successful manual workflow as proof that the complete test suite or every deployment scenario has passed.

## Security and Operational Notes

- Keep credentials in environment variables or an appropriate secret manager.
- Never expose backend secrets through `VITE_` frontend environment variables.
- Restrict CORS origins appropriately outside local development.
- Review AI-generated changes before applying them to real data systems.
- Keep reviewer decisions auditable.
- Configure service permissions and provider access before deploying to another environment.

## Project Goal

The goal is to build a production-oriented AI data reliability platform that combines observability, evidence-based investigation, machine learning, retrieval, and human oversight to help engineers diagnose and manage data incidents more effectively.
