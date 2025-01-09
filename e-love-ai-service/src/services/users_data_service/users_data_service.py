####################################################################################
# Users Data service that interacts with input data that goes from fe-api gateway. #
# It accepts the data and use embeddings, pre-trained SBERT model                  #
# that reccomends new users list, based on AI.                                     #
####################################################################################

# Сервис читает данные из data/raw и обучает на них модель (по типу что модель (одна) сама знает кто из пользователей друг другу хорошо подходит)
#  РАБОТА - СО ВСЕМИ ЮЗЕРАМИ

import os

import pandas as pd

from src.embeddings import (get_bert_embeddings, text_similarity_sbert,
                            weighted_sbert_embeddings)
from src.inference import predict_with_model
from src.recomendations import (extract_keywords, generate_user_vector,
                                recommend_partners)
from src.training import one_hot_encode, train_model


class UserDataService:

    def __init__(self, usersList: list, currentUser: dict):
        self.usersList = usersList
        self.currentUser = currentUser

    async def accept_users_data(self, usersList: list, currentUserId: int):
        self.usersList = usersList
        self.currentUserId = currentUserId

    # Standart 'path' parameter reads data only from the folder. It has to read data from the last returned file in the folder.
    async def read_raw_users_data(self) -> pd.DataFrame:
        RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")

        # return pd.read_csv(path)

    # Дальше - создавать вектор для каждого юзера для дальнейшей работы?

    # def __init__(self):

    # TODO:
    # 1. Должно сохраняться состояние ответа от фетчинга из fe-api:
    #   1.1: self.currentUser: User
    #   1.2: self.otherUsers: List[User]
    #   1.3 ->

    # async def generateUserVector(self, user_categories: list, all_categories: list) -> pd.DataFrame

    # async def compare_users_text(self, curr_user_description: str, users_descriptions: list)

    # async def make_users_prediction(model: someType, users: df, current_user_vector: vectorType, current_user_description: str, new_descriptions: list, keywords: dict) -> ReturnUsersInterface

    # async def handle_user_recommendations
