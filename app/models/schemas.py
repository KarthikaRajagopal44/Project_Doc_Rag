from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PDFUploadResponse(BaseModel):
    """Response model for PDF upload endpoint"""
    filename: str
    file_id: str
    message: str = "PDF uploaded successfully"
    size: int

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    file_id: str
    query: str
    
class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    file_id: str
    query: str
    answer: str
    source_info: Optional[List[Dict[str, Any]]] = None

class SummaryRequest(BaseModel):
    """Request model for summary endpoint"""
    file_id: str
    include_details: bool = False
    
class SummaryResponse(BaseModel):
    """Response model for summary endpoint"""
    file_id: str
    summary: str
    details: Optional[Dict[str, Any]] = None
