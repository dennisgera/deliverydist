from sqlalchemy.orm import Session
from app.controllers.base import BaseController
from app.repositories.query_repository import QueryRepository
from app.services.geocoding import GeocodingService
from app.services.distance_calculator import DistanceCalculatorService
from app.schemas.query import QueryCreate, QueryCreateInternal
from app.models.query import Query as QueryModel

class QueryController(BaseController[QueryModel, QueryCreate, None]):
    def __init__(
        self,
        db: Session,
        geocoding_service: GeocodingService = GeocodingService(),
        distance_calculator_service: DistanceCalculatorService = DistanceCalculatorService(),
    ):
        super().__init__(
            db=db,
            repository_class=QueryRepository
        )
        self.geocoding_service = geocoding_service
        self.distance_calculator_service = distance_calculator_service

    async def calculate_distance(self, query_data: QueryCreate) -> QueryModel:
        """Custom controller method for distance calculation"""
        try:
            # Check if we already have this query
            existing_query = self.repository.finder.find_by_addresses(
                query_data.source_address,
                query_data.destination_address
            )
            if existing_query:
                return existing_query
            
            source_coords = await self.geocoding_service.get_coordinates(query_data.source_address)
            destination_coords = await self.geocoding_service.get_coordinates(query_data.destination_address)

            # Calculate new distance
            distance = self.distance_calculator_service.calculate_distance(
                source_coords,
                destination_coords,
            )
            
            create = QueryCreateInternal(
                source_address=query_data.source_address,
                destination_address=query_data.destination_address,
                distance=distance
            )
            
            return self.create(create)
            
        except Exception as e:
            self._handle_exception(e, "calculating distance")