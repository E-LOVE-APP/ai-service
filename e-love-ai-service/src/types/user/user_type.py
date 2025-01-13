from typing import Any, Dict, List, TypedDict, Union


class UserGender:
    """
    UserGender class that contains the gender information
    params:
        id: str
        gender_name: str
    """

    id: str
    gender_name: str


class UserPost:
    """
    UserPost class that contains the post information
    params:
        id: str
        post_title: str
        post_descr: str
        user_id: str
        created_at: str
        updated_at: str
    """

    id: str
    post_title: str
    post_descr: str
    user_id: str
    created_at: str
    updated_at: str


class UserCategory:
    """
    UserCategory class that contains the category information
    params:
        id: str
        category_name: str
        category_descr: str
        category_icon: str
    """

    id: str
    category_name: str
    category_descr: str
    category_icon: str


class User:
    """
    User class that contains the user information
    params:
        id: str
        first_name: str
        last_name: str
        email: str
        user_descr: str
        categories: List[UserCategory]
        posts: List[UserPost]
        genders: List[UserGender]
    """

    id: str
    first_name: str
    last_name: str
    email: str
    user_descr: str
    categories: List[UserCategory]
    posts: List[UserPost]
    genders: List[UserGender]


class MatchingUsersResponse:
    """
    MatchingUsersResponse class that contains the response of the matching users
    params:
        users: List[User]
        total: int
        next_token: str
    """

    users: List[User]
    total: int
    next_token: str
