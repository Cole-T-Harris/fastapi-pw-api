from pydantic import BaseModel

class LocationsBase(BaseModel):
    zipcode: int
    radiusInMiles: int 
    limit: int 

class LocationsResponse(BaseModel):
    zipcode: int
    radiusInMiles: int 
    limit: int 

class ProductsBase(BaseModel):
    term: str
    locationId: int
    start: int
    limit: int

class ProductsResponse(BaseModel):
    term: str
    locationId: int
    start: int
    limit: int