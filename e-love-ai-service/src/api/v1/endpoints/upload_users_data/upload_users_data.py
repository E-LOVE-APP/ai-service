import ast
import io
import os
import pickle

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

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
async def upload_users_dataset(request: Request, file: UploadFile = File(...)):
    """
    Uploads the dataset of users and trains the model. Used for and with Prefect flows. (each day data extraction)
    params:
        file: UploadFile
            The file containing the dataset
    returns:
        GetUsersDataResponse: The response containing the accuracy of the model
    """
    # TODO: For @Neeplc -> PLEASE MOVE THE CODE BELOW TO A SEPARATE SERVICE!
    print("MODEL_PATH:", MODEL_PATH)
    print("DATAFRAME_PATH:", DATAFRAME_PATH)
    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
        df = pd.read_csv(io.StringIO(csv_text))

        if "categories" in df.columns:
            df["categories"] = df["categories"].apply(lambda x: ast.literal_eval(x))
        else:
            raise HTTPException(
                status_code=400, detail="'categories' column not found in the dataset"
            )

        all_categories = request.app.state.all_categories

        df = one_hot_encode(df, "categories", all_categories)

        # <-- TRAIN MODEL -->
        rf_model, accuracy = train_model(df, all_categories=all_categories)

        with open(MODEL_PATH, "wb") as file:
            pickle.dump(rf_model, file)

        with open(DATAFRAME_PATH, "wb") as file:
            pickle.dump(df, file)

        request.app.state.model = rf_model
        request.app.state.all_users_df = df

        return {"detail": f"Dataset uploaded, model retrained with accuracy={accuracy}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
