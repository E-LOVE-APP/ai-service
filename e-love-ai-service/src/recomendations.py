import numpy as np
import pandas as pd
from inference import predict_with_model
from embeddings import text_similarity_sbert
from sklearn.feature_extraction.text import TfidfVectorizer


def generate_user_vector(user_categories, all_categories):
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
    return pd.DataFrame(
        [[int(cat in user_categories) for cat in all_categories]],
        columns=all_categories,
    )


def extract_keywords(user_description, corpus, top_n=5):
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
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform([user_description] + corpus)
    feature_names = vectorizer.get_feature_names_out()

    user_tfidf = tfidf_matrix[0].toarray()[0]
    top_indices = user_tfidf.argsort()[-top_n:][::-1]
    keywords = {feature_names[i]: user_tfidf[i] for i in top_indices if user_tfidf[i] > 0}
    return keywords


def recommend_partners(
    model,
    new_users_df,
    current_user_vector,
    current_user_description,
    new_descriptions,
    keywords=None,
):
    """
    Predicts the top 10 partners for the current user.
    params:
        model: RandomForestClassifier
            The trained model to use for prediction
        new_users_df: pd.DataFrame
            The new users to predict on
        current_user_vector: pd.DataFrame
            The vector of the current user
        current_user_description: str
            The description of the current user
        new_descriptions: list
            A list of descriptions of the new users
        keywords: dict
            A dictionary of keywords and their weights for weighting the embeddings
    returns:
        list: The top 10 partners for the current user
    """
    # TODO: refactor - magic numbers (0.5, 10); срез; лямбда
    cat_probabilities = predict_with_model(model, new_users_df)
    text_sims = text_similarity_sbert(current_user_description, new_descriptions, keywords)

    final_scores = 0.5 * cat_probabilities + 0.5 * np.array(text_sims)

    combined = [
        (idx, cp, ts, fs)
        for idx, cp, ts, fs in zip(new_users_df.index, cat_probabilities, text_sims, final_scores)
    ]
    sorted_combined = sorted(combined, key=lambda x: x[3], reverse=True)

    return sorted_combined[:10]
