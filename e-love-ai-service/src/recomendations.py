import logging
from typing import List

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from embeddings import text_similarity_sbert
from inference import predict_with_model
from src.types.user.user_type import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
This module contains the functions for generating user vectors, extracting keywords from user descriptions, and recommending partners. 
"""


# TODO: refactor:
# 1. User categories - whom categories? categories of the current user or an absolute random user?
# 2. All categories param - isn't it better to extract it as an external state (class/type) and just re-use it here, instead of always re-creating it?
async def generate_user_vector(user_categories: list, all_categories: list) -> pd.DataFrame:
    """
    Generates a user vector based on the categories they like.
    params:
        user_categories: list
            The categories the user likes
        all_categories: list
            A list of all possible categories
    returns:
        pd.DataFrame: A DataFrame with the user vector
    """
    try:
        return await pd.DataFrame(
            [[int(cat in user_categories) for cat in all_categories]],
            columns=all_categories,
        )
    except Exception as e:
        print(f"Error in generation user vector: {e}")
        logger.error(f"Error in generation user vector: {e}")


async def extract_keywords(user_description: str, corpus: list, top_n: int = 5) -> dict:
    """
    Extracts the top keywords from the user description.
    params:
        user_description: str
            The user description to extract keywords from
        corpus: list
            A list of descriptions to compare against
        top_n: int
            The number of top keywords to extract
    returns:
        dict: A dictionary of keywords and their TF-IDF scores
    """
    try:
        vectorizer = await TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = await vectorizer.fit_transform([user_description] + corpus)
        feature_names = await vectorizer.get_feature_names_out()

        # TODO: это просто пиздец а не код!
        user_tfidf = tfidf_matrix[0].toarray()[0]
        top_indices = user_tfidf.argsort()[-top_n:][::-1]
        keywords = {feature_names[i]: user_tfidf[i] for i in top_indices if user_tfidf[i] > 0}
        return keywords
    except Exception as e:
        print(f"Error in extracting keywords: {e}")
        logger.error(f"Error in extracting keywords: {e}")


async def recommend_partners(
    model: RandomForestClassifier,
    other_users_df: pd.DataFrame,
    current_user_vector: pd.DataFrame,
    current_user_description: str,
    other_descriptions: list,
    keywords: str = None,
) -> List[User]:
    """
    Predicts the top 10 partners for the current user.
    params:
        model: RandomForestClassifier
            The trained model to use for prediction
        other_users_df: pd.DataFrame
            The other set of users to predict on (+10 next)
        current_user_vector: pd.DataFrame
            The vector of the current user
        current_user_description: str
            The description of the current user
        other_descriptions: list
            A list of descriptions of the other users
        keywords: dict
            A dictionary of keywords and their weights for weighting the embeddings
    returns:
        list: The top 10 partners for the current user
    """
    try:
        # TODO: refactor - magic numbers (0.5, 10); срез; лямбда
        cat_probabilities = predict_with_model(model, new_users_df)
        text_sims = text_similarity_sbert(current_user_description, new_descriptions, keywords)

        final_scores = 0.5 * cat_probabilities + 0.5 * np.array(text_sims)

        combined = [
            (idx, cp, ts, fs)
            for idx, cp, ts, fs in zip(
                new_users_df.index, cat_probabilities, text_sims, final_scores
            )
        ]
        sorted_combined = sorted(combined, key=lambda x: x[3], reverse=True)

        return sorted_combined[:10]
    except Exception as e:
        print(f"Error in recommending partners: {e}")
        logger.error(f"Error in recommending partners: {e}")
