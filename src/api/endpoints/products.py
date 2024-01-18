from fastapi import APIRouter, Depends, HTTPException
import httpx
import logging
from ...schemas import ProductsBase, ProductsResponse, ProductImages, ProductPrice
from ...dependencies import httpx_client
from ..oauth import get_oauth_header

router = APIRouter()

BASE_KROGER_URL = "https://api.kroger.com/v1/"
KROGER_PRODUCTS_CACHE_KEY = 'kroger_products_token'
SCOPE = 'product.compact'

def get_image_perspective(image):
    return image["perspective"]

def get_index_of_medium_image(images):
    if len(images) == 5:
        return 2
    else:
        for i in range(len(images)):
            if images[i]["size"] == "medium":
                return i
        return 0
    
def get_index_of_thumbnail_image(images):
    if len(images) == 5:
        return 4
    else:
        for i in range(len(images)):
            if images[i]["size"] == "thumbnail":
                return i
        return -1
    
def get_image_url(image, index):
    return image["sizes"][index]["url"]

def build_product_images(image_array):
    thumbnail = ""
    front_image = ""
    back_image = ""
    left_image = ""
    right_image = ""
    for image in image_array:
        if get_image_perspective(image) == "front":
            front_image = get_image_url(image, get_index_of_medium_image(image["sizes"]))
            thumbnail_index = get_index_of_thumbnail_image(image["sizes"])
            thumbnail = get_image_url(image, thumbnail_index) if thumbnail_index >= 0 else ""
        elif get_image_perspective(image) == "back":
            back_image = get_image_url(image, get_index_of_medium_image(image["sizes"]))
        elif get_image_perspective(image) == "right":
            right_image = get_image_url(image, get_index_of_medium_image(image["sizes"]))
        elif get_image_perspective(image) == "left":
            left_image = get_image_url(image, get_index_of_medium_image(image["sizes"]))
    images = ProductImages(thumbnail=thumbnail, frontImage=front_image, backImage=back_image, rightImage=right_image, leftImage=left_image)
    return images

@router.get("/", response_model=ProductsResponse)
async def read_products(product_params: ProductsBase = Depends(), client: httpx.AsyncClient = httpx_client):
    header = await get_oauth_header(KROGER_PRODUCTS_CACHE_KEY, SCOPE, client=client)
    url = BASE_KROGER_URL + f"products?filter.term={product_params.term}&filter.locationId={product_params.locationId}&filter.start={product_params.start}&filter.limit={product_params.limit}"
    try:
        response = await client.get(url, headers=header)
        response.raise_for_status()
        response_json = response.json()
        for product in response_json["data"]:
            product["images"] = build_product_images(product["images"])
            product["stock"] = product.get("items", [{}])[0].get("inventory", {}).get("stockLevel", "")
            product["size"] = product.get("items", [{}])[0].get("size", "")
            product["priceSize"] = product.get("items", [{}])[0].get("soldBy", "")
            product["prices"] = ProductPrice(price=product.get("items", [{}])[0].get("price", {}).get("regular", 0.00),
                                             promo=product.get("items", [{}])[0].get("price", {}).get("promo", 0.00))
        products_response = ProductsResponse(**product_params.model_dump(),
                                             products=response_json["data"],
                                             meta=response_json["meta"])
        return products_response
    except httpx.HTTPStatusError as e:
        logging.exception("Failed to obtain products %s", e.response.text)
        raise HTTPException(status_code=e.response.status_code, detail="Failed to obtain products")
    except httpx.RequestError as e:
        logging.exception("RequestError occurred: %s", e.response.text)
        raise HTTPException(status_code=500, detail="Internal Server Error")