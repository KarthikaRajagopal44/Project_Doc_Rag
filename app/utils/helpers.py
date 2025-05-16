"""
Utility helper functions for the PDF QA application
"""
import os
import logging
from typing import Dict, List, Any, Optional
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_unique_id() -> str:
    """
    Generate a unique ID for files or other resources
    
    Returns:
        Unique string ID
    """
    return str(uuid.uuid4())

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to ensure it's safe for storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove potentially dangerous characters
    sanitized = ''.join(c for c in filename if c.isalnum() or c in '._- ')
    sanitized = sanitized.strip()
    
    # Ensure the filename isn't empty after sanitization
    if not sanitized:
        sanitized = "unnamed_file"
    
    return sanitized

def log_api_request(endpoint: str, request_data: Dict[str, Any]) -> None:
    """
    Log API request information for monitoring
    
    Args:
        endpoint: API endpoint path
        request_data: Request data (filtered for sensitive info)
    """
    logger.info(f"API Request to {endpoint}: {request_data}")

def log_api_response(endpoint: str, status_code: int, response_data: Optional[Dict[str, Any]] = None) -> None:
    """
    Log API response information for monitoring
    
    Args:
        endpoint: API endpoint path
        status_code: HTTP status code
        response_data: Response data (optional)
    """
    logger.info(f"API Response from {endpoint} - Status: {status_code}")
    if response_data:
        logger.debug(f"Response data: {response_data}")

def remove_temporary_files(file_paths: List[str]) -> None:
    """
    Remove temporary files from the system
    
    Args:
        file_paths: List of file paths to remove
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logger.debug(f"Removed temporary file: {path}")
        except Exception as e:
            logger.error(f"Error removing file {path}: {str(e)}")

def format_byte_size(size_bytes: int) -> str:
    """
    Format byte size to human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024 or unit == 'GB':
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

def create_error_response(error_msg: str, error_code: str = "error") -> Dict[str, str]:
    """
    Create standardized error response
    
    Args:
        error_msg: Error message
        error_code: Error code identifier
        
    Returns:
        Standardized error response dictionary
    """
    return {
        "status": "error",
        "error_code": error_code,
        "message": error_msg
    }

def paginate_results(results: List[Any], page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    Paginate a list of results
    
    Args:
        results: List of results to paginate
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Dictionary with paginated results and metadata
    """
    # Ensure valid page and page_size
    page = max(1, page)
    page_size = max(1, min(100, page_size))  # Limit page size between 1 and 100
    
    # Calculate indices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    # Get page items
    page_items = results[start_idx:end_idx] if start_idx < len(results) else []
    
    # Calculate total pages
    total_items = len(results)
    total_pages = (total_items + page_size - 1) // page_size
    
    return {
        "items": page_items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

def validate_file_id(file_id: str) -> bool:
    """
    Validate if a file ID is in the correct format (UUID)
    
    Args:
        file_id: File ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        uuid_obj = uuid.UUID(file_id)
        return str(uuid_obj) == file_id
    except (ValueError, AttributeError):
        return False