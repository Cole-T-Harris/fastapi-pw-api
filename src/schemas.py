from pydantic import BaseModel
from typing import List

#Database pydantic Schemas
class ThumbnailBase(BaseModel):
    branch: str
    url: str

class ThumbnailCreate(ThumbnailBase):
    pass

class Thumbnail(ThumbnailBase):
    id: int
    class Config:
        from_attributes = True

#Location API Endpoint Models
class LocationsBase(BaseModel):
    zipcode: int
    radiusInMiles: int 
    limit: int

class Address(BaseModel):
    addressLine1: str
    city: str
    state: str
    zipCode: str
    county: str

class Geolocation(BaseModel):
    latitude: float
    longitude: float

class DailyHours(BaseModel):
    open: str
    close: str

class Hours(BaseModel):
    monday: DailyHours
    tuesday: DailyHours
    wednesday: DailyHours
    thursday: DailyHours
    friday: DailyHours
    saturday: DailyHours
    sunday: DailyHours

class Store(BaseModel):
    locationId: str
    chain: str
    name: str
    address: Address
    geolocation: Geolocation
    thumbnail: str
    hours: Hours
    distance: float 

class LocationsResponse(BaseModel):
    zipcode: int
    radiusInMiles: int 
    limit: int
    stores: List[Store]

#Products API Endpoint Models
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