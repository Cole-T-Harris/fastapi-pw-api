from fastapi import APIRouter, Depends
from ...schemas import ProductsBase, ProductsResponse

router = APIRouter()

@router.get("/", response_model=ProductsResponse)
async def read_products(product_params: ProductsBase = Depends()):
    products_response = ProductsResponse(**product_params.model_dump())
    return products_response