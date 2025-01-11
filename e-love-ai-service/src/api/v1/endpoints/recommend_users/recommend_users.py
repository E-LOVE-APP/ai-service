from fastapi import APIRouter

from src.services.reccomend_for_user.reccomend_for_user import \
    ReccomendUsersService

router = APIRouter(
    prefix="/matching-recommendations",
)


@router.post(
    "/",
    tags=["Get users matching recommendations"],
)
async def get_users_matching_recommendations(current_user_data: dict) -> list:
    """
    Get users matching recommendations. Used for and with fe-api gateway microservice, it recommends users based on the current user's data.
    (PREMIUM SUBSCRIPTION REQUIRED!)
    params:
        current_user_data: dict
            The data of the current user
    returns:
        list: The list of users matching recommendations
    """
    service = ReccomendUsersService()
    return service.get_matching_recommendations(current_user_data)
