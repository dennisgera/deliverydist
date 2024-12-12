from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.query_controller import QueryController

def get_query_controller(db: Session = Depends(get_db)) -> QueryController:
    return QueryController(db)
