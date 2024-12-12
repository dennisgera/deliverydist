# app/api/v1/endpoints/query.py
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import get_query_controller
from app.controllers.query_controller import QueryController
from app.schemas.query import QueryCreate, Query

router = APIRouter()

@router.post("/", response_model=Query)
async def calculate_distance(
    query_data: QueryCreate,
    controller: QueryController = Depends(get_query_controller)
):
    return await controller.calculate_distance(query_data)

@router.get("/", response_model=list[Query])
async def get_history(controller: QueryController = Depends(get_query_controller)):
    return controller.get_all()