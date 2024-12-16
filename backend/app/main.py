from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import request_middleware
import logging
from app.api.v1.router import router

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
     allow_origins=[
        "https://deliverydist-web.fly.dev",  
        "http://localhost:3000",            
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_middleware)

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Distance Calculator API"}