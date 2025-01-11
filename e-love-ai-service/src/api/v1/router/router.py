from fastapi import APIRouter
from src.api.v1.endpoints.upload_users_data.upload_users_data import router as get_users_data_router
from src.api.v1.endpoints.recommend_users.recommend_users import router as recommend_users_router

api_router = APIRouter()

api_router.include_router(get_users_data_router, prefix="/api/v1/", tags=["Get users data"])
api_router.include_router(
    recommend_users_router,
    prefix="/api/v1/",
    tags=["Get users matching recommendations", "Premium subscription"],
)
