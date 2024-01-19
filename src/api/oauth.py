import os
import base64
from fastapi import HTTPException, Depends
import httpx
from cachetools import TTLCache
from ..dependencies import httpx_client
import logging

#Logging
logging.basicConfig(level=logging.ERROR)

#Final URL for Token URL
KROGER_TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"

# Create an in-memory cache with a time-to-live (TTL) of 1750 seconds (typical kroger token expires in 1800 s)
token_cache = TTLCache(maxsize=5, ttl=1750)  

async def get_access_token(token_cache_key: str, scope: str, client: httpx.AsyncClient = Depends(httpx_client)):
    token = token_cache.get(token_cache_key)
    if not token:
        # Define the OAuth 2.0 authentication parameters
        client_id = os.environ.get("KROGER_OAUTH_CLIENT_ID")
        client_secret = os.environ.get("KROGER_OAUTH_CLIENT_SECRET")
        credentials_string = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials_string.encode("utf-8")).decode("utf-8")
        auth_headers = {
            'Accept': 'application/json; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }
        auth_params = {
            "grant_type": "client_credentials",
            "scope": scope
        }
        try:
            response = await client.post(KROGER_TOKEN_URL, data=auth_params, headers=auth_headers)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logging.exception("Failed to obtain OAuth token %s", e.response.text)
            raise HTTPException(status_code=e.response.status_code, detail="Failed to obtain OAuth token")
        
        if response.status_code == 200:
            token = response.json()['access_token']
            expires_in = response.json()['expires_in']
            token_cache[token_cache_key] = (token_cache_key, token, expires_in)
        else:
            return None
    else:
        token = token[1]
    return token

async def get_oauth_header(token_cache_key: str, scope: str, client: httpx.AsyncClient = Depends(httpx_client)):
    token = await get_access_token(token_cache_key=token_cache_key, scope=scope, client=client)
    return {'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive', 
            'Authorization': f'Bearer {token}',
            'Cache-Control': 'no-chache'}