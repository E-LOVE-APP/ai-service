from fastapi import Depends, Request

from src.services.reccomend_for_user.reccomend_for_user import \
    ReccomendUsersService


def get_recommend_users_service(request: Request) -> ReccomendUsersService:
    """
    Fabric method that creates recommend_users service instance.
    """
    model = request.app.state.model
    df_all_users = request.app.state.all_users_df
    all_categories = request.app.state.all_categories
    return ReccomendUsersService(model, df_all_users, all_categories)
