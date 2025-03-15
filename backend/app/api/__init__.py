
# Initialize API package
from fastapi import APIRouter
from app.api import topics

api_router = APIRouter()
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])

