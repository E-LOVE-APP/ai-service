import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def one_hot_encode(df, categories_column, all_categories) -> pd.DataFrame:
    """
    One-hot encodes the categories in the given column of the dataframe.
    params:
        df: pd.DataFrame
            The dataframe to encode
        categories_column: str
            The name of the column containing the categories
        all_categories: list
            A list of all possible categories
    returns:
        pd.DataFrame: The original dataframe with the categories one-hot encoded
    """
    one_hot = pd.DataFrame(
        df[categories_column]
        .apply(lambda x: [int(category in x) for category in all_categories])
        .tolist(),
        columns=all_categories,
        index=df.index,
    )
    return pd.concat([df.drop(columns=[categories_column]), one_hot], axis=1)


# TODO: make this func async or no?
def train_model(df: pd.DataFrame, all_categories: list) -> RandomForestClassifier:
    """
    Trains a random forest classifier on the given dataframe.
    params:
        df: pd.DataFrame
            The dataframe to train the model on
        all_categories: list
            A list of all possible categories
    returns:
        RandomForestClassifier: The trained random forest classifier
    """
    print("I'm in the start of train_model method")
    # TODO: refactor - magic numbers (0.15, 42)
    negatives = df[df["liked"] == 0].sample(frac=0.15, random_state=42)
    training_df = pd.concat([df[df["liked"] == 1], negatives], ignore_index=True)

    # TODO: refactor - magic numbers (42)
    X = training_df[all_categories]
    y = training_df["liked"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    # TODO: refactor - magic numbers (100, 42)
    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return rf, accuracy
