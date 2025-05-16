from typing import Dict, Any

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pypdf import PdfReader

from app.config import settings
from app.services.pdf_service import PDFService

class SummaryService:
    """Service for generating summaries of PDF documents"""
    
    def __init__(self, pdf_service: PDFService):
        """
        Initialize summary service
        
        Args:
            pdf_service: PDFService instance for interacting with PDF files
        """
        self.pdf_service = pdf_service
        self.model_name = settings.model_name
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=self.model_name
        )
    
    async def generate_summary(self, file_id: str, include_details: bool = False) -> Dict[str, Any]:
        """
        Generate a summary of a PDF document
        
        Args:
            file_id: ID of the PDF file to summarize
            include_details: Whether to include detailed information extraction
            
        Returns:
            Dictionary containing the summary and optionally detailed information
        """
        # Get path to PDF file
        pdf_path = self.pdf_service.get_pdf_path(file_id)
        
        # Extract text from PDF
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Create summary prompt
        summary_template = """
        I need you to provide a concise summary of the following document.
        Focus on the main topics, key points, and conclusions.

        DOCUMENT:
        {text}

        SUMMARY:
        """
        
        summary_prompt = PromptTemplate(
            input_variables=["text"],
            template=summary_template
        )
        
        # Create summary chain
        summary_chain = LLMChain(
            llm=self.llm,
            prompt=summary_prompt
        )
        
        # Generate summary
        summary_result = summary_chain.run(text=text)
        
        result = {
            "summary": summary_result.strip()
        }
        
        # Include detailed information if requested
        if include_details:
            details = await self._extract_details(text)
            result["details"] = details
        
        return result
    
    async def _extract_details(self, text: str) -> Dict[str, Any]:
        """
        Extract detailed information from document text
        
        Args:
            text: Document text
            
        Returns:
            Dictionary containing extracted details
        """
        # Create details extraction prompt
        details_template = """
        Extract the following information from the document if present:
        
        1. Key entities (people, organizations, locations)
        2. Dates and time references
        3. Important numerical data or statistics
        4. Key arguments or positions
        5. Action items or next steps
        
        Format the response as structured information.
        
        DOCUMENT:
        {text}
        
        EXTRACTED DETAILS:
        """
        
        details_prompt = PromptTemplate(
            input_variables=["text"],
            template=details_template
        )
        
        # Create details chain
        details_chain = LLMChain(
            llm=self.llm,
            prompt=details_prompt
        )
        
        # Generate details
        details_result = details_chain.run(text=text)
        
        # Process the details output into a structured format
        # This is a simplified approach - in a real app, you might want more structured parsing
        details_sections = details_result.split("\n\n")
        processed_details = {}
        
        for section in details_sections:
            if ":" in section:
                key, value = section.split(":", 1)
                processed_details[key.strip()] = value.strip()
            else:
                # Handle sections without clear key-value structure
                if "Details" not in processed_details:
                    processed_details["Details"] = []
                processed_details["Details"].append(section)
        
        return processed_details
