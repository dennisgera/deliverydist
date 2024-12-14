from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import request_middleware
import logging
from app.api.v1.router import router

logger = logging.getLogger(__name__)

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
