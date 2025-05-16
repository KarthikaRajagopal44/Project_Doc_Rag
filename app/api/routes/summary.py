from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.models.schemas import SummaryRequest, SummaryResponse
from app.services.summary_service import SummaryService
from app.dependencies import get_summary_service

router = APIRouter(
    prefix="/summary",
    tags=["Summary Operations"]
)

@router.post(
    "/generate",
    response_model=SummaryResponse,
    summary="Generate summary of a PDF",
    description="Generate a summary of a PDF document and optionally extract detailed information"
)
async def generate_summary(
    request: SummaryRequest,
    summary_service: Annotated[SummaryService, Depends(get_summary_service)]
):
    """
    Generate a summary of a PDF document
    
    Args:
        request: Summary request containing file ID and option flags
        summary_service: Service for generating summaries (injected)
        
    Returns:
        Summary of the PDF document and optionally extracted details
    """
    try:
        # Generate summary
        result = await summary_service.generate_summary(
            file_id=request.file_id,
            include_details=request.include_details
        )
        
        # Return response
        response = SummaryResponse(
            file_id=request.file_id,
            summary=result["summary"]
        )
        
        # Include details if available
        if "details" in result:
            response.details = result["details"]
        
        return response
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {str(e)}"
        )
