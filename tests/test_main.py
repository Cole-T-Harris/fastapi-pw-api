import pytest
from httpx import AsyncClient
from fastapi import FastAPI
import json
from jsonschema import validate

from src.main import app

@pytest.mark.asyncio
async def test_valid_read_locations():
    with open("tests/response_jsons/validLocationsResponse.json", "r") as valid_locations_json:
        valid_locations_response = json.load(valid_locations_json)

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/locations/?zipcode=80220&radiusInMiles=50&limit=10")
    assert response.status_code == 200
    assert response.json() == valid_locations_response

@pytest.mark.asyncio
async def test_valid_read_products():
    with open("tests/response_jsons/validProductsResponse.json", "r") as valid_products_json:
        valid_products_response = json.load(valid_products_json)

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/products/?term=crushed tomatoes&locationId=62000005&start=0&limit=10")
    assert response.status_code == 200
    assert response.json() == valid_products_response
    