from fastapi import APIRouter, Depends, HTTPException
from ...schemas import LocationsBase, LocationsResponse
import httpx
from ...dependencies import httpx_client
from ..oauth import get_oauth_header
import logging
import pgeocode
import geopy.distance

router = APIRouter()
BASE_KROGER_URL = "https://api.kroger.com/v1/"
KROGER_LOCATIONS_CACHE_KEY = 'kroger_stores_token'
SCOPE = ''

def get_distances(locations, zipcode):
    nomi = pgeocode.Nominatim('us')
    zipcode_latlong_dataframe = nomi.query_postal_code(zipcode)[['latitude','longitude']]
    starting_coordinates = (zipcode_latlong_dataframe['latitude'], zipcode_latlong_dataframe['longitude'])
    distances = []
    for store in locations:
        store_coordinates = (store["geolocation"]["latitude"], store["geolocation"]["longitude"])
        distances.append(geopy.distance.geodesic(starting_coordinates, store_coordinates).miles)
    return distances

@router.get("/", response_model=LocationsResponse)
async def read_locations(location_params: LocationsBase = Depends(), client: httpx.AsyncClient = httpx_client):
    header = await get_oauth_header(KROGER_LOCATIONS_CACHE_KEY, SCOPE, client=client)
    url = BASE_KROGER_URL + f"locations?filter.zipCode.near={location_params.zipcode}&filter.radiusInMiles={location_params.radiusInMiles}&filter.limit={location_params.limit}"
    try:
        response = await client.get(url, headers=header)
        response.raise_for_status()
        response_json = response.json()
        distances = get_distances(response_json['data'], location_params.zipcode)
        locations_response = LocationsResponse(**location_params.model_dump(),
                                               stores=response_json['data'],
                                               distances=distances)
        return locations_response
    except httpx.HTTPStatusError as e:
        logging.exception("Failed to obtain locations %s", e.response.text)
        raise HTTPException(status_code=e.response.status_code, detail="Failed to obtain locations")
    except httpx.RequestError as e:
        logging.exception("RequestError occurred: %s", e.response.text)
        raise HTTPException(status_code=500, detail="Internal Server Error")