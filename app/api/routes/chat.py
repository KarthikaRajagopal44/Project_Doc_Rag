from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.dependencies import get_chat_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat Operations"]
)

@router.post(
    "/query",
    response_model=ChatResponse,
    summary="Query a PDF document",
    description="Query a PDF document using natural language processing"
)
async def query_pdf(
    request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(get_chat_service)]
):
    """
    Query a PDF document using natural language
    
    Args:
        request: Chat request containing file ID and query
        chat_service: Service for handling chat (injected)
        
    Returns:
        Answer to the query based on the PDF content
    """
    try:
        # Query the PDF
        response = await chat_service.query_pdf(
            file_id=request.file_id,
            query=request.query
        )
        
        # Return response
        return ChatResponse(
            file_id=request.file_id,
            query=response["query"],
            answer=response["answer"],
            source_info=response["source_info"]
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying PDF: {str(e)}"
        )
