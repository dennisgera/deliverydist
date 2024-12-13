from fastapi import HTTPException
from typing import Optional
from loguru import logger

class ErrorHandlerService:
    """Service responsible for converting exceptions into user-friendly HTTP responses"""
    
    @staticmethod
    def handle_application_error(exc: Exception, operation: Optional[str] = None) -> None:
        """
        Convert various exceptions into user-friendly HTTPException objects
        Args:
            exc: The caught exception
            operation: Optional string describing the operation being performed
        Raises:
            HTTPException: A FastAPI HTTP exception with a user-friendly message
        """
        if isinstance(exc, HTTPException):
            error_message = str(exc.detail).lower()
            logger.error(f"HTTPException: {exc.status_code} - {error_message}")
            
            if exc.status_code == 404:
                if "address not found" in error_message:
                    address = str(exc.detail).split(": ")[-1]
                    raise HTTPException(
                        status_code=404,
                        detail=f"We couldn't find '{address}'. Please check the spelling and try again, or provide more details like city and country."
                    )
                if "invalid coordinates" in error_message:
                    raise HTTPException(
                        status_code=404,
                        detail="We couldn't determine the exact location. Please make the address more specific by adding city, state, or country."
                    )
            elif exc.status_code == 503:
                raise HTTPException(
                    status_code=503,
                    detail="We're having trouble connecting to our location service. Please try again in a few moments."
                )
            raise exc
        
        error_message = str(exc).lower()
        
        if isinstance(exc, (TimeoutError, ConnectionError)) or "timeout" in error_message:
            raise HTTPException(
                status_code=504,
                detail="The request took too long to process. Please try again or check if the addresses are correct."
            )
        
        if "validation" in error_message or isinstance(exc, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Please ensure both addresses are properly formatted and include enough details."
            )
        
        if "database" in error_message or isinstance(exc, (Exception,)) and "db" in str(type(exc).__name__).lower():
            raise HTTPException(
                status_code=500,
                detail="We're having trouble saving your request. Please try again in a few moments."
            )

        operation_context = f" while {operation}" if operation else ""
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong{operation_context}. Please try again or contact support if the problem persists."
        )