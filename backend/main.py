from fastapi import FastAPI

from backend.routers import chat


app = FastAPI(
    title="Business Idea Assistant API",
    description="Backend API for the Business Idea Suggestion Chatbot",
    version="1.0.0"
)


app.include_router(chat.router)


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