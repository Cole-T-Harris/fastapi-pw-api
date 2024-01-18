from fastapi import Depends
import httpx
from .database import SessionLocal

async def get_httpx_async_client():
    async with httpx.AsyncClient() as client:
        yield client

httpx_client = Depends(get_httpx_async_client)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
