from fastapi import APIRouter

from src.api.endpoints import locations, products, health

api_router = APIRouter()
api_router.include_router(locations.router, prefix="/locations")
api_router.include_router(products.router, prefix="/products")
api_router.include_router(health.router, prefix="/health")