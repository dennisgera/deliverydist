from typing import Generic, TypeVar, Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.repositories.base import BaseRepository
from app.exceptions import RecordNotFoundException

T = TypeVar("T")
CREATE = TypeVar("CREATE", bound=BaseModel)
UPDATE = TypeVar("UPDATE", bound=BaseModel)

class BaseController(Generic[T, CREATE, UPDATE]):
    def __init__(
        self,
        db: Session,
        repository_class: type[BaseRepository],
        *repository_args,
        **repository_kwargs
    ):
        self.db = db
        self.repository = repository_class(
            db=db,
            *repository_args,
            **repository_kwargs
        )

    def get_all(self) -> List[T]:
        """Retrieve all records"""
        try:
            return self.repository.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving records: {str(e)}"
            )

    def get_by_id(self, **kwargs) -> Optional[T]:
        """Retrieve a single record by its primary key(s)"""
        try:
            return self.repository.get_by_id(**kwargs)
        except RecordNotFoundException:
            raise HTTPException(
                status_code=404,
                detail="Record not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving record: {str(e)}"
            )

    def create(self, create_schema: CREATE) -> T:
        """Create a new record"""
        try:
            return self.repository.add(create_schema)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating record: {str(e)}"
            )

    def update(self, update_schema: UPDATE, **kwargs) -> T:
        """Update an existing record"""
        try:
            return self.repository.update(update_schema, **kwargs)
        except RecordNotFoundException:
            raise HTTPException(
                status_code=404,
                detail="Record not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating record: {str(e)}"
            )

    def delete(self, **kwargs) -> bool:
        """Delete a record (soft delete)"""
        try:
            return self.repository.delete(**kwargs)
        except RecordNotFoundException:
            raise HTTPException(
                status_code=404,
                detail="Record not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting record: {str(e)}"
            )

    def _handle_exception(self, e: Exception, operation: str) -> None:
        """Common exception handler for controller operations"""
        if isinstance(e, RecordNotFoundException):
            raise HTTPException(
                status_code=404,
                detail="Record not found"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error during {operation}: {str(e)}"
        )