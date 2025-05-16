"""
Dependency injection module for FastAPI application
"""

from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService
from app.services.summary_service import SummaryService

# Service singletons
_pdf_service = None
_chat_service = None
_summary_service = None

def get_pdf_service() -> PDFService:
    """
    Get PDF service singleton instance
    
    Returns:
        PDFService instance
    """
    global _pdf_service
    
    if _pdf_service is None:
        _pdf_service = PDFService()
        
    return _pdf_service

def get_chat_service() -> ChatService:
    """
    Get chat service singleton instance
    
    Returns:
        ChatService instance
    """
    global _chat_service
    
    if _chat_service is None:
        pdf_service = get_pdf_service()
        _chat_service = ChatService(pdf_service)
        
    return _chat_service

def get_summary_service() -> SummaryService:
    """
    Get summary service singleton instance
    
    Returns:
        SummaryService instance
    """
    global _summary_service
    
    if _summary_service is None:
        pdf_service = get_pdf_service()
        _summary_service = SummaryService(pdf_service)
        
    return _summary_service
