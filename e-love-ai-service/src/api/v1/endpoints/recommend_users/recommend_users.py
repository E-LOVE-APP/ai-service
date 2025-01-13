from fastapi import APIRouter, Depends, Body
import logging

logger = logging.getLogger(__name__)

from dependencies.recommend_users_service.create_recommend_users_service import (
    get_recommend_users_service,
)
from src.services.reccomend_for_user.reccomend_for_user import ReccomendUsersService

router = APIRouter(
    prefix="/matching-recommendations",
)


@router.post(
    "",
    tags=["Get users matching recommendations"],
)
async def get_users_matching_recommendations(
    current_user_data: dict = Body(...),
    service: ReccomendUsersService = Depends(get_recommend_users_service),
) -> list:
    """
    Get users matching recommendations. Used for and with fe-api gateway microservice, it recommends users based on the current user's data.
    (PREMIUM SUBSCRIPTION REQUIRED!)
    params:
        current_user_data: dict
            The data of the current user
    returns:
        list: The list of users matching recommendations
    """
    logger.info(f"Received data: {current_user_data}")
    try:
        result = await service.reccomend_users(current_user_data)
        return result
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise
