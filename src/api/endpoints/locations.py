from fastapi import APIRouter, Depends
from ...models import LocationsBase, LocationsResponse

router = APIRouter()

@router.get("/", response_model=LocationsResponse)
async def read_locations(location_params: LocationsBase = Depends()):
    locations_response = LocationsResponse(**location_params.model_dump())
    return locations_response