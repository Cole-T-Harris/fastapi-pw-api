from fastapi import APIRouter

from src.api.endpoints import locations, products, health

api_router = APIRouter()
api_router.include_router(locations.router, prefix="/api/locations")
api_router.include_router(products.router, prefix="/api/products")
api_router.include_router(health.router, prefix="/health")