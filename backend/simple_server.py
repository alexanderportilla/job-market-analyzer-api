#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Job Market Analyzer API",
    description="An API to scrape and analyze job market data for software developers in Colombia.",
    version="1.0.0",
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"], summary="Root endpoint of the API")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Job Market Analyzer API!"}

@app.get("/test", tags=["Test"], summary="Test endpoint")
def test_endpoint():
    """
    A test endpoint to verify the API is working.
    """
    return {"status": "ok", "message": "API is working correctly!"}

if __name__ == "__main__":
    import uvicorn
    print("Starting Simple Job Market Analyzer API...")
    print("Server will be available at: http://127.0.0.1:8001")
    print("API Documentation: http://127.0.0.1:8001/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info"
    ) 