from fastapi import FastAPI

from backend.routers import chat
from backend.routers import incidents
from backend.routers import incident_evidence
from backend.routers import investigation
from backend.routers import remediation
from backend.routers import remediation_approval
from backend.routers import dashboard
from backend.routers import anomalies

app = FastAPI(
    title="Business Idea Assistant API",
    description="Backend API for the Business Idea Suggestion Chatbot",
    version="1.0.0"
)


# Chat API
app.include_router(chat.router)

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
        "message": "Business Idea Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }