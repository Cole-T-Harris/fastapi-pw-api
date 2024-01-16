from fastapi import FastAPI
from fastapi.routing import APIRoute

from src.api.api import api_router

app = FastAPI()

app.include_router(api_router)
