import os
import uuid
from typing import Dict, List, Any
import shutil

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import settings

class PDFService:
    """Service for handling PDF operations"""

    def __init__(self):
        """Initialize the PDF service"""
        self.storage_path = settings.pdf_storage_path
        self.vector_store_path = settings.vector_store_path
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    async def save_uploaded_pdf(self, file) -> Dict[str, Any]:
        """
        Save an uploaded PDF file and return its metadata
        
        Args:
            file: The uploaded file object
            
        Returns:
            Dictionary containing file metadata
        """
        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())
        
        # Create unique filename
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(self.storage_path, filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Process PDF for vector store
        await self.process_pdf_for_vector_store(file_id, file_path)
        
        return {
            "filename": file.filename,
            "file_id": file_id,
            "path": file_path,
            "size": file_size
        }
    
    async def process_pdf_for_vector_store(self, file_id: str, file_path: str) -> None:
        """
        Process a PDF file and store its vector embeddings
        
        Args:
            file_id: Unique identifier for the file
            file_path: Path to the PDF file
        """
        # Extract text from PDF
        text = self._extract_text_from_pdf(file_path)
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        chunks = text_splitter.split_text(text)
        
        # Create vector store
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        
        # Save vector store
        vector_store_path = os.path.join(self.vector_store_path, file_id)
        vector_store.save_local(vector_store_path)
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text content from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        reader = PdfReader(file_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        return text
    
    def get_pdf_path(self, file_id: str) -> str:
        """
        Get the path to a PDF file by its ID
        
        Args:
            file_id: Unique identifier for the file
            
        Returns:
            Path to the PDF file
        """
        for filename in os.listdir(self.storage_path):
            if filename.startswith(file_id):
                return os.path.join(self.storage_path, filename)
        
        raise FileNotFoundError(f"PDF with ID {file_id} not found")
    
    def get_vector_store(self, file_id: str):
        """
        Load vector store for a specific PDF
        
        Args:
            file_id: Unique identifier for the file
            
        Returns:
            FAISS vector store
        """
        vector_store_path = os.path.join(self.vector_store_path, file_id)
        
        if not os.path.exists(vector_store_path):
            raise FileNotFoundError(f"Vector store for PDF with ID {file_id} not found")
        
        return FAISS.load_local(vector_store_path, self.embeddings)
