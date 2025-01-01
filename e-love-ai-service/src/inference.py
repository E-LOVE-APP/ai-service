import numpy as np


def predict_with_model(model, data):
    """
    Predicts the target variable using the given model and data.
    params:
        model: RandomForestClassifier
            The trained model to use for prediction
        data: pd.DataFrame
            The data to predict on
    returns:
        np.ndarray: The predicted probabilities
    """
    # TODO: refactor - magic numbers (1), срез
    return model.predict_proba(data)[:, 1]
