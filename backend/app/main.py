from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import request_middleware
import logging
from sqlalchemy import inspect
from app.db.database import engine, Base, DATABASE_URL
from app.api.v1.router import router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db_path = Path(DATABASE_URL.replace('sqlite:///', ''))
    logger.info(f"Looking for database at: {db_path}")
    logger.info(f"Database exists: {db_path.exists()}")
    
    # Check tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables in database: {tables}")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    yield
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_middleware)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Distance Calculator API"}
