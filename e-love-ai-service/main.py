import logging
import os
import uvicorn
import json
import pickle
import aiofiles
import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.api.v1.router.router import api_router

from config.app_factory import create_app
from easter_eggs.greeting import ascii_hello, ascii_hello_devs

logging.basicConfig(level=logging.INFO)
logging.info("Starting e-love-ai-service")
print(ascii_hello_devs)

CATEGORIES_PATH = os.getenv("CATEGORIES_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
DATAFRAME_PATH = os.getenv("DATAFRAME_PATH")


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Асинхронная загрузка категорий с использованием aiofiles
#     if os.path.exists(CATEGORIES_PATH):
#         async with aiofiles.open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
#             data_text = await f.read()
#         data = json.loads(data_text)
#         app.state.all_categories = [item["category_name"] for item in data["items"]]
#         print("Loaded categories info from", CATEGORIES_PATH)
#     else:
#         print(f"Categories file {CATEGORIES_PATH} not found.")
#         app.state.all_categories = []

#     # Получаем текущий событийный цикл
#     loop = asyncio.get_running_loop()

#     # Асинхронная загрузка модели с использованием run_in_executor
#     if os.path.exists(MODEL_PATH):

#         def load_pickle_model():
#             with open(MODEL_PATH, "rb") as f:
#                 return pickle.load(f)

#         app.state.model = await loop.run_in_executor(None, load_pickle_model)
#         print("Loaded model from", MODEL_PATH)
#     else:
#         print(f"Model file {MODEL_PATH} not found.")
#         app.state.model = None

#     # Асинхронная загрузка датафрейма с использованием run_in_executor
#     if os.path.exists(DATAFRAME_PATH):

#         def load_pickle_dataframe():
#             with open(DATAFRAME_PATH, "rb") as f:
#                 return pickle.load(f)

#         app.state.all_users_df = await loop.run_in_executor(None, load_pickle_dataframe)
#         print("Loaded all_users_df from", DATAFRAME_PATH)
#     else:
#         print(f"Dataframe file {DATAFRAME_PATH} not found.")
#         app.state.all_users_df = None

#     yield
#     # Здесь можно добавить код для обработки shutdown, если нужно.


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(CATEGORIES_PATH):
        print(f"Categories file {CATEGORIES_PATH} not found.")
        app.state.all_categories = []
    else:
        with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        app.state.all_categories = [item["category_name"] for item in data["items"]]
        print("Loaded categories info from", CATEGORIES_PATH)

    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            app.state.model = pickle.load(f)
        print("Loaded model from", MODEL_PATH)
    else:
        app.state.model = None
        print(f"Categories file {MODEL_PATH} not found.")

    if os.path.exists(DATAFRAME_PATH):
        with open(DATAFRAME_PATH, "rb") as f:
            app.state.all_users_df = pickle.load(f)
        print("Loaded all_users_df from", DATAFRAME_PATH)
    else:
        app.state.all_users_df = None
        print(f"Categories file {DATAFRAME_PATH} not found.")

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

# @app.on_event("startup")
# async def load_data_on_startup():

#     # <-- LOAD CATEGORIES -->
#     if not os.path.exists(CATEGORIES_PATH):
#         print(f"Categories file {CATEGORIES_PATH} not found.")
#         app.state.all_categories = []
#     else:
#         with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
#             data = json.load(f)
#         app.state.all_categories = [item["category_name"] for item in data["items"]]
#         print("Loaded categories info from", CATEGORIES_PATH)

#     # <-- LOAD MODEL -->
#     if os.path.exists(MODEL_PATH):
#         with open(MODEL_PATH, "rb") as f:
#             app.state.model = pickle.load(f)
#         print("Loaded model from", MODEL_PATH)
#     else:
#         app.state.model = None

#     # <-- LOAD DATAFRAME -->
#     if os.path.exists(DATAFRAME_PATH):
#         with open(DATAFRAME_PATH, "rb") as f:
#             app.state.all_users_df = pickle.load(f)
#         print("Loaded all_users_df from", DATAFRAME_PATH)
#     else:
#         app.state.all_users_df = None


# @app.get("/hello")
# async def hello_test_route():
#     return {"message": "Hello World"}


# app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
