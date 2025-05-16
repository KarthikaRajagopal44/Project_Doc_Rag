from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import Annotated

from app.models.schemas import PDFUploadResponse
from app.services.pdf_service import PDFService
from app.dependencies import get_pdf_service

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Operations"]
)

@router.post(
    "/upload", 
    response_model=PDFUploadResponse,
    summary="Upload a PDF document",
    description="Upload a PDF document for processing, querying, and summarization"
)
async def upload_pdf(
    file: Annotated[UploadFile, File(description="PDF file to upload")],
    pdf_service: Annotated[PDFService, Depends(get_pdf_service)]
):
    """
    Upload a PDF file to the system
    
    Args:
        file: The PDF file to upload
        pdf_service: Service for handling PDFs (injected)
        
    Returns:
        Information about the uploaded file
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Process the file
        file_info = await pdf_service.save_uploaded_pdf(file)
        
        # Return response
        return PDFUploadResponse(
            filename=file_info["filename"],
            file_id=file_info["file_id"],
            size=file_info["size"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )
        
        
class A:
        def __init__(self, a: int, b:int, c: int):
            self.a = a
            self.b = b
            self.c = c
   
from dataclasses import  dataclass
@dataclass
class B:
    a:int 
    b:int
    c:int
    
    
