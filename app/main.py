import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import settings
from app.api.routes import pdf, chat, summary

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(pdf.router)
app.include_router(chat.router)
app.include_router(summary.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check if API key is set
    if not settings.groq_api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY environment variable not set"
        )
    
    # Check if storage directories exist
    if not os.path.exists(settings.pdf_storage_path):
        raise HTTPException(
            status_code=500,
            detail="PDF storage directory not found"
        )
    
    if not os.path.exists(settings.vector_store_path):
        raise HTTPException(
            status_code=500,
            detail="Vector store directory not found"
        )
    
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True
    )
