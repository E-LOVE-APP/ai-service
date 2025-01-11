from fastapi import FastAPI

from config.config import settings

"""
Module that represents an app general instance
"""

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
