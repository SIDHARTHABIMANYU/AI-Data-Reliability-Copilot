from fastapi import FastAPI

from backend.routers import incidents
from backend.routers import incident_evidence
from backend.routers import investigation
from backend.routers import remediation
from backend.routers import remediation_approval
from backend.routers import dashboard
from backend.routers import anomalies


app = FastAPI(
    title="AI Data Reliability Copilot API",
    description="Backend API for detecting, investigating, and managing retail data reliability incidents.",
    version="1.0.0"
)


# Incident API
app.include_router(incidents.router)

app.include_router(incident_evidence.router)

app.include_router(investigation.router)

app.include_router(remediation.router)

app.include_router(remediation_approval.router)

app.include_router(dashboard.router)

app.include_router(anomalies.router)


@app.get("/")
def root():
    return {
        "message": "AI Data Reliability Copilot API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }