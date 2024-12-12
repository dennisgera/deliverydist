# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import query

router = APIRouter()

# Include endpoint routers
router.include_router(query.router, prefix="/queries", tags=["queries"])