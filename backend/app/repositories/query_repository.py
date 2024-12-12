# app/repositories/query_repository.py
from sqlalchemy.orm import Session
from app.models.query import Query
from app.repositories.base import BaseFinder, BaseRepository

class QueryFinder(BaseFinder[Query]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(db.query(Query).filter(Query.deleted_at.is_(None)))
    
    def find_by_addresses(self, source: str, destination: str):
        return self.base_query.filter(
            Query.source_address == source,
            Query.destination_address == destination
        ).first()

class QueryRepository(BaseRepository[Query, int]):
    def __init__(self, db):
        super().__init__(
            model_class=Query,
            db=db,
            finder=QueryFinder
        )
    