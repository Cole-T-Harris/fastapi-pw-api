from fastapi import Depends
import httpx

async def get_httpx_async_client():
    async with httpx.AsyncClient() as client:
        yield client

httpx_client = Depends(get_httpx_async_client)
