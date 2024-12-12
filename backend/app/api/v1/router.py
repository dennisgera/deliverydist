from fastapi import APIRouter
from app.api.v1.endpoints import query

router = APIRouter()

router.include_router(query.router, prefix="/queries", tags=["queries"])