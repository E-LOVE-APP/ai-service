"""
This is the main file for the e-love-ai-service
"""

import logging

from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse

from config.config import settings
from easter_eggs.greeting import ascii_hello, ascii_hello_devs

logging.basicConfig(level=logging.INFO)
logging.info("Starting e-love-ai-service")
print(ascii_hello_devs)
print(ascii_hello)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


# A couple of routes to test the service
@app.get("/hello")
async def hello_test_route():
    return {"message": "Hello World"}


@app.get("/app/config")
async def get_app_config():
    return settings.dict()
