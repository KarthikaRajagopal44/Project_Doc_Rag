import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    """Application settings"""
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # App settings
    app_name: str = "PDF QA API"
    app_description: str = "API for querying and summarizing PDF documents"
    app_version: str = "0.1.0"
    
    # Paths
    pdf_storage_path: str = os.path.join(os.getcwd(), "storage")
    vector_store_path: str = os.path.join(os.getcwd(), "vector_store")

    # LLM settings
    model_name: str = os.getenv("MODEL_NAME", "llama3-70b-8192")
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Ensure storage directories exist
    def create_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.pdf_storage_path, exist_ok=True)
        os.makedirs(self.vector_store_path, exist_ok=True)

# Create settings instance
settings = Settings()
settings.create_directories()
