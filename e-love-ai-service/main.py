"""
This is the main file for the e-love-ai-service
"""

import logging
import os

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from config.config import settings
from easter_eggs.greeting import ascii_hello, ascii_hello_devs
from src.api.v1.router.router import api_router

logging.basicConfig(level=logging.INFO)
logging.info("Starting e-love-ai-service")
print(ascii_hello_devs)
print(ascii_hello)

MODEL_PATH = os.getenv("MODEL_PATH")
DATAFRAME_PATH = os.getenv("DATAFRAME_PATH")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(api_router)


@app.on_event("startup")
async def load_data_on_startup():
    """
    1) При старте: загружаем categories.json => сохраняем в app.state.all_categories
    2) Пытаемся загрузить (model, df) с диска => app.state.model, app.state.all_users_df
    """
    if not Path(CATEGORIES_JSON_PATH).exists():
        print(f"Categories file {CATEGORIES_JSON_PATH} not found.")
        app.state.all_categories = []  # или raise Exception
    else:
        with open(CATEGORIES_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_cat_names = [item["category_name"] for item in data["items"]]
        app.state.all_categories = all_cat_names  # ["Science", "Education", ...]

    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            app.state.model = pickle.load(f)
        print("Loaded model from", MODEL_PATH)
    else:
        app.state.model = None

    if os.path.exists(DATAFRAME_PATH):
        with open(DATAFRAME_PATH, "rb") as f:
            app.state.all_users_df = pickle.load(f)
        print("Loaded all_users_df from", DATAFRAME_PATH)
    else:
        app.state.all_users_df = None


# A couple of routes to test the service
@app.get("/hello")
async def hello_test_route():
    return {"message": "Hello World"}


@app.get("/app/config")
async def get_app_config():
    return settings.dict()
