from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base
from app.models.table_model import TableModel

class Query(TableModel, Base):
    __tablename__ = "query"

    id = Column(Integer, primary_key=True, index=True)
    source_address = Column(String, nullable=False)
    destination_address = Column(String, nullable=False)
    distance = Column(Float, nullable=False)