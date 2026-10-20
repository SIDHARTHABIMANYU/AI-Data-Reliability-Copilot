# AI Data Reliability Copilot — Frontend Web Dashboard (V11)

Enterprise-grade observability and AI incident response dashboard for data reliability engineering, replacing the legacy Streamlit interface.

Built with **React 18**, **TypeScript**, **Vite**, **Tailwind CSS**, and **Recharts**.

---

## 1. Prerequisites

- **Node.js**: `v18.0.0` or higher (verified on Node `v24.13.0`)
- **npm**: `v9.0.0` or higher (verified on npm `v11.6.2`)
- **Python**: `3.10+` with the existing project virtual environment (`venv`)
- **PostgreSQL**: Local or remote database running for the FastAPI backend

---

## 2. Quickstart & Installation

Navigate to the `frontend/` directory and install dependencies:

```bash
cd frontend
npm install
```

---

## 3. Environment Variables Configuration

The frontend uses Vite environment variables configured in `.env`:

```bash
# frontend/.env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

An example template is available at `frontend/.env.example`.

> **Security Note:** Never place AWS credentials, database secrets, or API keys in `VITE_` environment variables, as Vite bundles these into client-side code.

---

## 4. Launching the Application

### Option A: Development Server (Hot Reload)

```bash
npm run dev
```

The Vite dev server starts on `http://localhost:5173`.

### Option B: Production Build & Preview

```bash
npm run build
npm run preview
```

The optimized static production bundle will be generated into `dist/` with automated vendor chunk-splitting.

---

## 5. Backend Server Startup

To run the companion FastAPI backend:

```bash
# From repository root
.\venv\Scripts\Activate.ps1
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 6. Backend API Endpoints Integrated

The frontend connects directly to the following FastAPI backend endpoints:

| Endpoint | HTTP Method | Description |
|---|---|---|
| `/health` | `GET` | Backend heartbeat check and connectivity indicator |
| `/dashboard/summary` | `GET` | Overview metrics (`total_incidents`, `open_incidents`, `high_severity_incidents`, `pending_remediations`, `approved_remediations`) |
| `/incidents` | `GET` | Live incident records with dataset, severity, status, and detection timestamp |
| `/incidents/{incident_id}/evidence` | `GET` | Telemetry package including linked pipeline run and data quality check results |
| `/incidents/{incident_id}/investigation` | `GET` | LangGraph multi-step AI investigation synthesizing root causes, verified evidence, impact, and confidence |
| `/incidents/{incident_id}/remediation` | `GET` | AI suggested remediation plan with problem statement, code adjustments, validation steps, and risk level |
| `/remediations/{remediation_id}/approve` | `POST` | Human review approval endpoint with payload `{"approved_by": "Name"}` |
| `/remediations/{remediation_id}/reject` | `POST` | Human review rejection endpoint with payload `{"approved_by": "Name"}` |
| `/anomalies` | `GET` | Machine learning retail anomaly detection results (Isolation Forest & Z-scores) |

---

## 7. Features Awaiting Dedicated Backend Endpoints

In strict compliance with architectural rules, the frontend avoids presenting mock metrics or fabricating unbacked data:

1. **Global Pipeline Batch History (`GET /pipelines/runs`)**:
   - Currently, pipeline run logs are accessible through the MCP Server tool (`get_pipeline_runs`) and for individual incidents via `GET /incidents/{id}/evidence`.
   - The UI includes an incident-linked pipeline run inspector and a documented notice indicating that a dedicated global REST adapter endpoint is planned for V12.

2. **Global Data Quality History Feed (`GET /data-quality`)**:
   - Quality checks for alerted incidents are fully viewable via `GET /incidents/{id}/evidence`.
   - A global table scan history endpoint is planned as a future REST adapter for the MCP `get_data_quality_results` tool.

---

## 8. Key Features Implemented

- **Enterprise Observability Design**: Dark navy/charcoal styling with high data density, subtle status accents, and glassmorphism.
- **Persistent Sidebar & Top Navigation**: Real-time backend connectivity pill, latency monitor, manual sync button, and responsive mobile drawer.
- **Interactive Overview KPI Cards & Charts**: Real incident breakdown using Recharts without fabricated trend numbers.
- **Incident Management**: Search, multi-attribute filtering (severity, status), and one-click routing to investigation.
- **AI Investigation Center**: Full LangGraph result visualization (root causes, factual evidence, impact assessments, confidence ratings, and raw telemetry traces).
- **Human-in-the-Loop Remediation Review**: Pre-flight confirmation dialog, engineer name validation, action disabling during submission, and real-time state feedback.
- **ML Anomaly Detection**: Store-level metrics, revenue impact, and Isolation Forest score breakdown.
- **Reliability & Resilience**: Comprehensive Axios error interceptor handling timeouts (up to 75s for LLM operations), 404, 409, 422, 500, and offline states.
