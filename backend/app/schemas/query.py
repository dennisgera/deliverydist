from pydantic import BaseModel, ConfigDict

class QueryBase(BaseModel):
    source_address: str
    destination_address: str

class QueryCreate(QueryBase):
    pass

class QueryCreateInternal(QueryCreate):
    distance: float

class Query(QueryBase):
    id: int
    distance: float

    model_config = ConfigDict(from_attributes=True)


