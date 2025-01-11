import io
import os
import pickle

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile

from config.app_instance import app
from src.training import one_hot_encode, train_model

router = APIRouter(
    prefix="/upload-dataset",
)

MODEL_PATH = os.getenv("MODEL_PATH")
DATAFRAME_PATH = os.getenv("DATAFRAME_PATH")


@router.post(
    "/",
    tags=["Get users data"],
)
async def upload_users_dataset(file: UploadFile = File(...)):
    """
    Uploads the dataset of users and trains the model. Used for and with Prefect flows. (each day data extraction)
    params:
        file: UploadFile
            The file containing the dataset
    returns:
        GetUsersDataResponse: The response containing the accuracy of the model
    """
    # TODO: For @Neeplc -> PLEASE MOVE THE CODE BELOW TO A SEPARATE SERVICE!
    try:
        content = await file.read()
        df = pd.read_csv(content.decode("utf-8"))

        all_categories = app.state.all_categories

        df = one_hot_encode(df, "categories", all_categories)

        # Train model
        rf_model, accuracy = train_model(df, all_categories=all_categories)

        with open(MODEL_PATH, "wb") as file:
            pickle.dump(rf_model, file)

        app.state.model = rf_model

        with open(DATAFRAME_PATH, "wb") as file:
            pickle.dump(df, file)
        app.state.all_users_df = df

        return {"detail": f"Dataset uploaded, model retrained with accuracy={accuracy}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
