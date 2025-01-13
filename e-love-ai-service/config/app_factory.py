import json
import os
import pickle

from fastapi import FastAPI

from src.api.v1.router.router import api_router

CATEGORIES_PATH = os.getenv("CATEGORIES_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
DATAFRAME_PATH = os.getenv("DATAFRAME_PATH")


# TODO: add docstrings
def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(api_router)

    @app.on_event("startup")
    async def load_data_on_startup():

        # <-- LOAD CATEGORIES -->
        if not os.path.exists(CATEGORIES_PATH):
            print(f"Categories file {CATEGORIES_PATH} not found.")
            app.state.all_categories = []
        else:
            with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            app.state.all_categories = [item["category_name"] for item in data["items"]]
            print("Loaded categories info from", CATEGORIES_PATH)

        # <-- LOAD MODEL -->
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                app.state.model = pickle.load(f)
            print("Loaded model from", MODEL_PATH)
        else:
            app.state.model = None

        # <-- LOAD DATAFRAME -->
        if os.path.exists(DATAFRAME_PATH):
            with open(DATAFRAME_PATH, "rb") as f:
                app.state.all_users_df = pickle.load(f)
            print("Loaded all_users_df from", DATAFRAME_PATH)
        else:
            app.state.all_users_df = None

    @app.get("/hello")
    async def hello_test_route():
        return {"message": "Hello World"}

    return app
