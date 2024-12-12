from typing import Generic, List, Optional, TypeVar

import pydantic
from sqlalchemy import Column
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import update

from app.exceptions import RecordNotFoundException
from app.utils.date import now

T = TypeVar("T")
ID = TypeVar("ID")

CREATE = TypeVar("CREATE")
UPDATE = TypeVar("UPDATE")
RETURN = TypeVar("RETURN")


class BaseFinder(Generic[T]):
    def __init__(self, base_query):
        self.base_query: Query = base_query

    @property
    def query(self):
        return self.base_query

    def all(self) -> List[T]:
        return self.base_query.all()

    def count(self) -> int:
        return self.base_query.count()

    def first(self) -> T:
        return self.base_query.first()


class BaseRepository(Generic[T, ID]):
    def __init__(
        self,
        *model_pk: Column,
        model_class: T,
        db: Session,
        finder: Optional[BaseFinder] = None,
    ):
        self.model_class = model_class
        self.model_pk = model_pk
        self.pk_labels = {column.key: column for column in model_pk}
        self.db = db
        if finder:
            self._finder = finder(self.default_query)

    @property
    def default_query(self) -> Optional[BaseFinder]:
        return self.db.query(self.model_class).filter(self.model_class.deleted_at.is_(None))

    @property
    def finder(self):
        return self._finder

    def get_all(self) -> Query:
        return self.default_query.all()

    def _make_filters(self, **kwargs):
        filters = []
        for label in self.pk_labels:
            if not kwargs.get(label):
                required = self.pk_labels.keys()
                raise KeyError(f"Missing primary key: {list(required)} are required")
            else:
                filters.append(self.pk_labels[label] == kwargs.get(label))
        return filters

    def get_by_id(self, **kwargs) -> T:
        model = self.default_query.filter(*self._make_filters(**kwargs)).first()
        if not model:
            raise RecordNotFoundException()
        return model

    def add(self, create_schema: pydantic.BaseModel) -> T:
        created_model = self.model_class(**create_schema.model_dump())
        self.db.add(created_model)
        self.db.flush()
        self.db.refresh(created_model)
        return created_model

    def delete(self, **kwargs) -> bool:
        update_status = self.db.execute(
            update(self.model_class)
            .where(*self._make_filters(**kwargs))
            .where(self.model_class.deleted_at.is_(None))
            .values({"deleted_at": now()})
        )
        if update_status.rowcount:
            return True
        else:
            raise RecordNotFoundException()

    def update(
        self,
        update_schema: pydantic.BaseModel,
        **kwargs,
    ) -> T:
        update_status = self.db.execute(
            update(self.model_class)
            .where(*self._make_filters(**kwargs))
            .values(**update_schema.model_dump(exclude_unset=True, exclude_none=True))
        )
        if update_status.rowcount:
            return self.get_by_id(**kwargs)
        else:
            raise RecordNotFoundException()
