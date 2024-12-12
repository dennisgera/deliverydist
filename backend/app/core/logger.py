import logging
import time
from fastapi import Request
from typing import Callable
import uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def request_middleware(request: Request, call_next: Callable):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Get request body
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
            body = body.decode()
        except Exception:
            body = "Could not read body"

    logger.info(
        f"Request started | ID: {request_id} | "
        f"Method: {request.method} | "
        f"Path: {request.url.path} | "
        f"Query params: {dict(request.query_params)} | "
        f"Body: {body} | "
        f"Client: {request.client.host if request.client else 'Unknown'}"
    )

    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"Request completed | ID: {request_id} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.3f}s"
        )
        
        return response
    except Exception as e:
        logger.error(
            f"Request failed | ID: {request_id} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise