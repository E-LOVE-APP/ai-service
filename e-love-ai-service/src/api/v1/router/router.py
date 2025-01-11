from fastapi import APIRouter
from src.api.v1.endpoints.upload_users_data.upload_users_data import router as get_users_data_router

api_router = APIRouter()

api_router.include_router(get_users_data_router, tags=["Get users data"])
