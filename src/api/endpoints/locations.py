from fastapi import APIRouter, Depends, HTTPException
from ...models import LocationsBase, LocationsResponse
import httpx
from ...dependencies import httpx_client
from ..oauth import get_oauth_header
import logging

router = APIRouter()
BASE_KROGER_URL = "https://api.kroger.com/v1/"
KROGER_LOCATIONS_CACHE_KEY = 'kroger_stores_token'
SCOPE = ''

@router.get("/")
async def read_locations(location_params: LocationsBase = Depends(), client: httpx.AsyncClient = httpx_client):
    header = await get_oauth_header(KROGER_LOCATIONS_CACHE_KEY, SCOPE, client=client)
    url = BASE_KROGER_URL + f"locations?filter.zipCode.near={location_params.zipcode}&filter.radiusInMiles={location_params.radiusInMiles}&filter.limit={location_params.limit}"
    try:
        response = await client.get(url, headers=header)
        response.raise_for_status()
        # locations_response = LocationsResponse(**location_params.model_dump())
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.exception("Failed to obtain locations %s", e.response.text)
        raise HTTPException(status_code=e.response.status_code, detail="Failed to obtain locations")
    except httpx.RequestError as e:
        logging.exception("RequestError occurred: %s", e.response.text)
        raise HTTPException(status_code=500, detail="Internal Server Error")