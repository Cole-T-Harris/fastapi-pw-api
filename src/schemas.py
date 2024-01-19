from pydantic import BaseModel
from typing import List, Optional

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

class AisleLocation(BaseModel):
    bayNumber: Optional[str] = ""
    description: Optional[str] = ""
    number: Optional[str] = ""
    numberOfFacings: Optional[str] = ""
    side: Optional[str] = ""
    shelfNumber: Optional[str] = ""
    shelfPositionInBay: Optional[str] = ""

class ProductImages(BaseModel):
    thumbnail: Optional[str] = None
    frontImage: Optional[str] = None
    backImage: Optional[str] = None
    rightImage: Optional[str] = None
    leftImage: Optional[str] = None

class ProductPrice(BaseModel):
    price: Optional[float] = None
    promo: Optional[float] = None

class ProductPagination(BaseModel):
    start: Optional[int] = 0
    limit: Optional[int] = 0
    total: Optional[int] = 0

class ProductMetaData(BaseModel):
    pagination: ProductPagination

class Product(BaseModel):
    productId: str
    aisleLocations: Optional[List[AisleLocation]] = []
    brand: Optional[str] = ""
    countryOfOrigin: Optional[str] = ""
    description: Optional[str] = ""
    stock: Optional[str] = None
    prices: Optional[ProductPrice] = None
    size: Optional[str] = None
    priceSize: Optional[str] = None
    images: Optional[ProductImages] = None


class ProductsResponse(BaseModel):
    term: str
    locationId: int
    start: int
    limit: int
    products: Optional[List[Product]] = []
    meta: ProductMetaData
    