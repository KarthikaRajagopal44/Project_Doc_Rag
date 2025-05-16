from typing import Dict, List, Any

from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq

from app.config import settings
from app.services.pdf_service import PDFService

class ChatService:
    """Service for handling chat with PDF document Q&A"""
    
    def __init__(self, pdf_service: PDFService):
        """
        Initialize chat service
        
        Args:
            pdf_service: PDFService instance for interacting with PDF files
        """
        self.pdf_service = pdf_service
        self.model_name = settings.model_name
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=self.model_name
        )
    
    async def query_pdf(self, file_id: str, query: str) -> Dict[str, Any]:
        """
        Query a PDF document using LangChain and Groq
        
        Args:
            file_id: ID of the PDF file to query
            query: User query string
            
        Returns:
            Dictionary containing the query, answer, and source information
        """
        # Get vector store for the PDF
        vector_store = self.pdf_service.get_vector_store(file_id)
        
        # Create retriever from vector store
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Create QA chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=True
        )
        
        # Execute query
        response = qa_chain({"question": query, "chat_history": []})
        
        # Extract source information
        source_info = []
        for doc in response["source_documents"]:
            source_info.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return {
            "query": query,
            "answer": response["answer"],
            "source_info": source_info
        }
