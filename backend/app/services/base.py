from typing import Generic, List, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository

T = TypeVar("T")
ID = TypeVar("ID")

CREATE = TypeVar("CREATE", bound=BaseModel)
UPDATE = TypeVar("UPDATE", bound=BaseModel)
RETURN = TypeVar("RETURN", bound=BaseModel)


def make_repository(repository, db: Session):
    return repository(db)


class BaseService(Generic[CREATE, UPDATE, RETURN]):
    def __init__(self, repository: BaseRepository, db: Session, return_model: BaseModel):
        self.repository = make_repository(repository=repository, db=db)
        self.return_model = return_model

    def get_by_id(self, **kwargs) -> RETURN:
        model = self.repository.get_by_id(**kwargs)
        return self.return_model.model_validate(model)

    def get_all(self) -> List[RETURN]:
        return [self.return_model.model_validate(item) for item in self.repository.get_all()]

    def get_all_for_pagination(self):
        return self.repository.default_query

    def create(self, create: CREATE) -> RETURN:
        return self.return_model.model_validate(self.repository.add(create))

    def update(self, update: UPDATE, **kwargs) -> RETURN:
        return self.return_model.model_validate(self.repository.update(update, **kwargs))

    def delete(self, **kwargs) -> bool:
        return self.repository.delete(**kwargs)
