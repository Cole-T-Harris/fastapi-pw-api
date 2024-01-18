from fastapi import APIRouter, Depends, HTTPException
from ...schemas import LocationsBase, LocationsResponse
import httpx
from ...dependencies import httpx_client, get_db
from ..oauth import get_oauth_header
import logging
import pgeocode
import geopy.distance
from sqlalchemy.orm import Session
from ...crud import get_thumbnails_by_branch

router = APIRouter()
BASE_KROGER_URL = "https://api.kroger.com/v1/"
KROGER_LOCATIONS_CACHE_KEY = 'kroger_stores_token'
SCOPE = ''

def get_distance(store, zipcode):
    nomi = pgeocode.Nominatim('us')
    zipcode_latlong_dataframe = nomi.query_postal_code(zipcode)[['latitude','longitude']]
    starting_coordinates = (zipcode_latlong_dataframe['latitude'], zipcode_latlong_dataframe['longitude'])
    store_coordinates = (store["geolocation"]["latitude"], store["geolocation"]["longitude"])
    distance = geopy.distance.geodesic(starting_coordinates, store_coordinates).miles
    return distance

def get_thumbnail(branch, db: Session = Depends(get_db)):
    query_response = get_thumbnails_by_branch(db, branch=branch)
    if query_response is None:
        query_response = get_thumbnails_by_branch(db, branch="KROGER")
    return query_response.url

@router.get("/", response_model=LocationsResponse)
async def read_locations(location_params: LocationsBase = Depends(), client: httpx.AsyncClient = httpx_client, db: Session = Depends(get_db)):
    header = await get_oauth_header(KROGER_LOCATIONS_CACHE_KEY, SCOPE, client=client)
    url = BASE_KROGER_URL + f"locations?filter.zipCode.near={location_params.zipcode}&filter.radiusInMiles={location_params.radiusInMiles}&filter.limit={location_params.limit}"
    try:
        response = await client.get(url, headers=header)
        response.raise_for_status()
        response_json = response.json()
        # Add thumbnail and get distances for response
        for store in response_json['data']:
            store["distance"] = get_distance(store=store, zipcode=location_params.zipcode)
            store["thumbnail"] = get_thumbnail(store["chain"], db)

        locations_response = LocationsResponse(**location_params.model_dump(),
                                               stores=response_json['data'])
        return locations_response
    except httpx.HTTPStatusError as e:
        logging.exception("Failed to obtain locations %s", e.response.text)
        raise HTTPException(status_code=e.response.status_code, detail="Failed to obtain locations")
    except httpx.RequestError as e:
        logging.exception("RequestError occurred: %s", e.response.text)
        raise HTTPException(status_code=500, detail="Internal Server Error")