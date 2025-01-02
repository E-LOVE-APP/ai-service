# config.py
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(os.getenv("APP_ENV_PATH"))
print(f"Loaded environment variables from {os.getenv('APP_ENV_PATH')}")

# TODO: refactor


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_running_env: str
    greeting_message: str

    class Config:
        env_file = os.getenv("APP_ENV_PATH")
        extra = "ignore"


settings = Settings()
